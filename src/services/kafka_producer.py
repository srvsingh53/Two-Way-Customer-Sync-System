from kafka import KafkaProducer
import json
from src.config.settings import KAFKA_BROKER, KAFKA_TOPIC

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def send_to_kafka(event_type, customer_data):
    event = {"event": event_type, "data": customer_data}
    producer.send(KAFKA_TOPIC, event)
    producer.flush()
    print(f"Sent event to Kafka: {event}")
