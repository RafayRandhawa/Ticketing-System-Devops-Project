"""
Email Service

Responsible only for sending emails.
Can later be replaced by AWS SES.
"""

import smtplib
import logging
import time

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from config import settings

logger = logging.getLogger(__name__)


class EmailService:

    MAX_RETRIES = 3

    @staticmethod
    def send_ticket_email(
        attendee_email: str,
        attendee_name: str,
        ticket_number: str,
        event_title: str,
        event_date: str,
        ticket_url: str,
        
    ) -> bool:

        subject = f"Your Ticket - {event_title}"

        body = f"""
Hello {attendee_name},

Your ticket has been successfully created.

-----------------------------------
Event: {event_title}
Date: {event_date}
Ticket Number: {ticket_number}
-----------------------------------

View your ticket here:

{ticket_url}

Please present this ticket at the event entrance.

Thank you.
"""

        return EmailService._send_email(
            recipient=attendee_email,
            subject=subject,
            body=body
        )

    @staticmethod
    def _send_email(
        recipient: str,
        subject: str,
        body: str
    ) -> bool:

        for attempt in range(EmailService.MAX_RETRIES):

            try:

                msg = MIMEMultipart()

                msg["From"] = settings.email_address
                msg["To"] = recipient
                msg["Subject"] = subject

                msg.attach(
                    MIMEText(body, "plain")
                )

                server = smtplib.SMTP(
                    settings.smtp_server,
                    settings.smtp_port
                )

                server.starttls()

                server.login(
                    settings.email_address,
                    settings.email_password
                )

                server.send_message(msg)

                server.quit()

                logger.info(
                    f"Email sent successfully to {recipient}"
                )

                return True

            except Exception as e:

                logger.error(
                    f"Email send failed "
                    f"(attempt {attempt + 1}) : {e}"
                )

                if attempt < EmailService.MAX_RETRIES - 1:
                    time.sleep(2 ** attempt)

        return False