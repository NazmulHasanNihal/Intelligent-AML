"""
Intelligent AML - Streaming API
Receives live mock transactions and publishes them to Redpanda (Kafka) for Flink to process.
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from confluent_kafka import Producer
import json
import os

app = FastAPI(title="Intelligent AML - Streaming API")

# Configure Redpanda connection (default local docker mapping)
REDPANDA_BROKER = os.getenv("REDPANDA_BROKER", "localhost:9092")
TOPIC_NAME = "aml_transactions_live"

producer = Producer({
    'bootstrap.servers': REDPANDA_BROKER,
    'client.id': 'aml-fastapi-producer'
})

class TransactionEvent(BaseModel):
    transaction_id: str
    source_account: str
    target_account: str
    amount: float
    timestamp: float
    currency: str = "USD"
    is_flagged: bool = False

def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

@app.post("/transaction")
async def ingest_transaction(tx: TransactionEvent):
    """
    Ingest a single transaction event into the streaming pipeline.
    """
    try:
        # Convert Pydantic model to dict, then to JSON string
        tx_data = tx.model_dump()
        tx_json = json.dumps(tx_data)
        
        # Publish to Redpanda
        producer.produce(
            topic=TOPIC_NAME,
            key=tx.source_account, # Partition by source account
            value=tx_json,
            callback=delivery_report
        )
        producer.poll(0) # trigger delivery reports
        
        return {"status": "success", "message": "Transaction queued for processing."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.on_event("shutdown")
def shutdown_event():
    # Flush remaining messages before shutting down
    producer.flush(10)
