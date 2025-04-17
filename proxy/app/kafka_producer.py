import json
import os
from datetime import datetime
from typing import Dict, Any, Optional
from confluent_kafka import Producer

# Kafka configuration
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")


class KafkaProducer:
    def __init__(self):
        self.producer = Producer({
            'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
            'client.id': 'api_service_producer'
        })
        
        # Define topics
        self.USER_REGISTRATION_TOPIC = "user_registration"
        self.POST_LIKE_TOPIC = "post_like"
        self.POST_VIEW_TOPIC = "post_view"
        self.POST_COMMENT_TOPIC = "post_comment"
    
    def _delivery_report(self, err, msg):
        """Called once for each message produced to indicate delivery result."""
        if err is not None:
            print(f'Message delivery failed: {err}')
        else:
            print(f'Message delivered to {msg.topic()} [{msg.partition()}]')
    
    def _serialize_datetime(self, obj):
        """JSON serializer for datetime objects."""
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError(f"Type {type(obj)} not serializable")
    
    def send_event(self, topic: str, data: Dict[str, Any], key: Optional[str] = None):
        """Send an event to the specified Kafka topic."""
        payload = json.dumps(data, default=self._serialize_datetime).encode('utf-8')
        self.producer.produce(
            topic=topic,
            key=key.encode('utf-8') if key else None,
            value=payload,
            callback=self._delivery_report
        )
        # Flush to ensure message is sent immediately
        self.producer.flush()
    
    def send_user_registration_event(self, user_data: Dict[str, Any]):
        self.send_event(
            topic=self.USER_REGISTRATION_TOPIC,
            data={
                "event_type": "user_registration",
                "timestamp": datetime.now(),
                "user": user_data
            },
            key=str(user_data["id"])
        )
    
    def send_post_like_event(self, user_id: str, post_id: int):
        self.send_event(
            self.POST_LIKE_TOPIC,
            data={
                "event_type": "post_like",
                "timestamp": datetime.now(),
                "user_id": user_id,
                "post_id": post_id
            },
            key=str(post_id)
        )
    
    def send_post_view_event(self, user_id: str, post_id: int, post_name: str):
        self.send_event(
            topic=self.POST_VIEW_TOPIC,
            data={
                "event_type": "post_view",
                "timestamp": datetime.now(),
                "user_id": user_id,
                "post_id": post_id,
                "post_name": post_name
            },
            key=str(post_id)
        ) 
    
    def send_post_comment_event(self, user_id: str, post_id: int):
        self.send_event(
            topic=self.POST_COMMENT_TOPIC,
            data={
                "event_type": "comment_create",
                "timestamp": datetime.now(),
                "user_id": user_id,
                "post_id": post_id
            },
            key=str(post_id)
        ) 