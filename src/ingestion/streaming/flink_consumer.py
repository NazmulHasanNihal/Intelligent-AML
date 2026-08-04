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
    Simulates the normalization step performed by the batch pipeline,
    but processes events one at a time.
    """
    def map(self, value):
        try:
            # Parse JSON
            tx = json.loads(value)
            
            # Here we would do:
            # 1. Type casting
            # 2. Add 'timestamp_normalized' based on burst-aware window rules
            # 3. Create explicit Node and Edge structures
            
            # For now, we just tag it and return a string representation
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
