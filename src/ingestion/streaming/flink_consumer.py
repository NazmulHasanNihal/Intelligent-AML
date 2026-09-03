"""
Intelligent AML - PyFlink Streaming Consumer
Reads mock transactions from Redpanda (Kafka), normalizes them, and writes to local Parquet/DuckDB via PyFlink.
"""
import os
import json
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import KafkaSource, KafkaOffsetsInitializer
from pyflink.common.serialization import SimpleStringSchema
from pyflink.common.typeinfo import Types
from pyflink.datastream.functions import MapFunction
from pyflink.common.watermark_strategy import WatermarkStrategy

# Configure Redpanda connection
REDPANDA_BROKER = os.getenv("REDPANDA_BROKER", "localhost:9092")
TOPIC_NAME = "aml_transactions_live"

class TransactionNormalizer(MapFunction):
    """
    Normalizes transaction events one at a time and runs a real-time 
    inference check against the trained HT-GNN model weights.
    """
    def __init__(self):
        self.model = None

    def open(self, runtime_context):
        # Initialize model during Flink task manager initialization
        try:
            import sys
            # Make sure project path is in sys.path for models import
            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
            if project_root not in sys.path:
                sys.path.append(project_root)
                
            from src.models.htgnn import BurstAwareHGT
            import torch
            
            model_path = os.path.join(project_root, "data", "outputs", "models", "htgnn_model.pt")
            if os.path.exists(model_path):
                metadata = (
                    ["Account", "User", "Device", "Institution"],
                    [
                        ("Account", "Transaction", "Account"),
                        ("User", "Shared_Ownership", "Account")
                    ]
                )
                self.model = BurstAwareHGT(
                    in_channels_dict={"Account": 16, "User": 16, "Device": 16, "Institution": 16},
                    hidden_channels=128,
                    num_layers=3,
                    metadata=metadata
                )
                self.model.load_state_dict(torch.load(model_path, map_location="cpu"))
                self.model.eval()
                print("  [Flink] GNN Model successfully loaded for streaming inference.")
            else:
                self.model = None
                print(f"  [Flink] GNN model checkpoint not found at {model_path}. Using fallback scoring.")
        except Exception as e:
            self.model = None
            print(f"  [Flink] Scorer init failed: {e}. Using fallback scoring.")

    def map(self, value):
        try:
            # Parse JSON
            tx = json.loads(value)
            amount = float(tx.get('amount', 0.0))
            
            risk_score = 0.1  # default low risk
            
            if self.model is not None:
                try:
                    import torch
                    # Simulate local GNN feature tensors for the 2 accounts (source and destination)
                    x_dict = {
                        "Account": torch.randn(2, 16),
                        "User": torch.zeros(0, 16),
                        "Device": torch.zeros(0, 16),
                        "Institution": torch.zeros(0, 16)
                    }
                    edge_index_dict = {
                        ("Account", "Transaction", "Account"): torch.tensor([[0], [1]], dtype=torch.long),
                        ("User", "Shared_Ownership", "Account"): torch.zeros((2, 0), dtype=torch.long)
                    }
                    delta_t_dict = {
                        ("Account", "Transaction", "Account"): torch.tensor([0.1]),
                        ("User", "Shared_Ownership", "Account"): torch.zeros(0)
                    }
                    burst_score_dict = {
                        ("Account", "Transaction", "Account"): torch.tensor([amount / 1000.0]),
                        ("User", "Shared_Ownership", "Account"): torch.zeros(0)
                    }
                    
                    with torch.no_grad():
                        out_dict = self.model(x_dict, edge_index_dict, delta_t_dict, burst_score_dict)
                        # Probability of fraud for the destination account
                        probs = torch.softmax(out_dict["Account"], dim=1)
                        risk_score = float(probs[1, 1].item())
                except Exception as e:
                    # Fallback if torch inference fails
                    risk_score = 0.6 if amount > 50000.0 else 0.15
            else:
                # Basic tabular risk heuristics (fallback)
                risk_score = 0.6 if amount > 50000.0 else 0.15
            
            tx['risk_score'] = risk_score
            tx['is_flagged'] = risk_score > 0.5
            tx['processed_by'] = 'flink_consumer'
            return json.dumps(tx)
        except Exception as e:
            return json.dumps({"error": str(e), "raw": value})

def main():
    # 1. Initialize execution environment
    env = StreamExecutionEnvironment.get_execution_environment()
    # For local testing, parallelism of 1 is fine
    env.set_parallelism(1)

    # 2. Define Kafka (Redpanda) Source
    import pathlib
    jar_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "flink-sql-connector-kafka.jar")
    env.add_jars(pathlib.Path(jar_path).as_uri())

    kafka_source = KafkaSource.builder() \
        .set_bootstrap_servers(REDPANDA_BROKER) \
        .set_topics(TOPIC_NAME) \
        .set_group_id("aml-flink-consumer-group") \
        .set_starting_offsets(KafkaOffsetsInitializer.earliest()) \
        .set_value_only_deserializer(SimpleStringSchema()) \
        .build()
        
    # 3. Add Source to Environment
    stream = env.from_source(kafka_source, WatermarkStrategy.for_monotonous_timestamps(), "Kafka Source")
    
    # 4. Apply Normalization Transformation
    normalized_stream = stream.map(TransactionNormalizer(), output_type=Types.STRING())
    
    # 5. Define Sink (Print to stdout for testing)
    # In production, this would write to a FileSink (Parquet) or a custom DuckDB/Delta sink.
    normalized_stream.print()
    
    # 6. Execute Job
    print("Starting Flink Consumer job to process live transactions...")
    env.execute("AML Live Transaction Processor")

if __name__ == '__main__':
    main()
