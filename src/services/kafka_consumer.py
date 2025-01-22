from kafka import KafkaConsumer
import json
from src.services.stripe_service import create_customer
from src.config.settings import KAFKA_BROKER, KAFKA_TOPIC

consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

def consume_events():
    print("Listening for customer events...")
    for message in consumer:
        event_data = message.value
        if event_data['event'] == 'customer_created':
            create_customer(event_data['data']['name'], event_data['data']['email'])
        print(f"Processed event: {event_data}")
