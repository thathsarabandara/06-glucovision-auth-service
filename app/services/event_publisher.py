import logging

logger = logging.getLogger(__name__)

class EventPublisher:
    @staticmethod
    async def publish(event_name: str, payload: dict):
        """
        Mock implementation of event publisher.
        In production, this would integrate with RabbitMQ, Kafka, or Redis Pub/Sub.
        """
        logger.info(f"Published event: {event_name} | Payload: {payload}")
