"""
Queue Service

Acts as an abstraction layer.

Today:
    Direct execution

Future:
    AWS SQS
"""

import logging

logger = logging.getLogger(__name__)


class QueueService:

    @staticmethod
    def publish(
        event_type: str,
        payload: dict,
        handler
    ) -> bool:

        try:

            logger.info(
                f"Publishing event: {event_type}"
            )

            return handler(payload)

        except Exception as e:

            logger.error(
                f"Queue publish failed: {e}"
            )

            return False