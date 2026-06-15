"""
Notification Service

Business layer for notifications.
Called ONLY after ticket + QR are fully created.
"""

from services.queue_service import QueueService
from services.email_service import EmailService
from config import settings

class NotificationService:

    @staticmethod
    def ticket_ready(ticket, event) -> bool:

        payload = {
            "attendee_email": ticket.attendee_email,
            "attendee_name": ticket.attendee_name,
            "ticket_number": ticket.ticket_number,
            "event_title": event.title,
            "event_date": str(event.event_date),
            "ticket_url": (
                f"{settings.base_url}/ticket/{ticket.ticket_number}"
            ),

            
        }

        return QueueService.publish(
            event_type="ticket_ready",
            payload=payload,
            handler=NotificationService._send_ticket_email
        )

    @staticmethod
    def _send_ticket_email(payload: dict) -> bool:

        return EmailService.send_ticket_email(
            attendee_email=payload["attendee_email"],
            attendee_name=payload["attendee_name"],
            ticket_number=payload["ticket_number"],
            event_title=payload["event_title"],
            event_date=payload["event_date"],
            ticket_url=payload["ticket_url"],
            
        )