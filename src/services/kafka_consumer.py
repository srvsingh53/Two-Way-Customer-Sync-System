from kafka import KafkaConsumer
import json
from src.services.stripe_service import create_customer
from src.config.settings import KAFKA_BROKER, KAFKA_TOPIC

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=True
)

def consume_events():
    #logger.info("Consumer started, listening for events...")
    for message in consumer:
        event_data = message.value
        #logger.info(f"Received event: {event_data}")
        
        if event_data['event'] == 'customer_created':
            stripe_customer_id = create_customer(event_data['data']['name'], event_data['data']['email'])
            # if stripe_customer_id:
            #     logger.info(f"Customer created in Stripe with ID: {stripe_customer_id}")
            # else:
            #     logger.error("Failed to create customer in Stripe.")