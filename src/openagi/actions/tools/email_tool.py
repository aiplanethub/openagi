# email_tool.py

from openagi.actions.base import Tool
from openagi.config import get_config
import smtplib
import imaplib
import email

class EmailTool(Tool):
    """
    A tool for sending and receiving emails.
    """

    def __init__(self, name="Email", description="A tool for sending and receiving emails."):
        super().__init__(name, description)

    def _execute(self, query: str):
        # Get email configuration from user input
        config = get_config()
        email_address = config.get("email", "address")
        email_password = config.get("email", "password")
        smtp_server = config.get("email", "smtp_server")
        imap_server = config.get("email", "imap_server")

        # Example: Sending an email
        if query.startswith("Send email to"):
            try:
                # Extract recipient, subject, and body from the query
                recipient = query.split("to ")[1].split(",")[0].strip()
                subject = query.split("subject ")[1].split(",")[0].strip()
                body = query.split("body ")[1].strip()

                # Use smtplib to send the email
                server = smtplib.SMTP(smtp_server, 587)
                server.starttls()
                server.login(email_address, email_password)
                message = f"Subject: {subject}\n\n{body}"
                server.sendmail(email_address, recipient, message)
                server.quit()
                return "Email sent successfully."
            except Exception as e:
                return f"Error sending email: {e}"

        # Example: Receiving emails
        elif query.startswith("Check emails"):
            try:
                # Use imaplib to connect to the email server
                mail = imaplib.IMAP4_SSL(imap_server)
                mail.login(email_address, email_password)
                mail.select('inbox')

                # Fetch and return the latest emails
                _, data = mail.search(None, 'ALL')
                latest_email_id = data[0].split()[-1]
                _, data = mail.fetch(latest_email_id, '(RFC822)')
                raw_email = data[0][1]
                email_message = email.message_from_bytes(raw_email)

                # Extract subject and body
                subject = email_message['Subject']
                body = ""
                if email_message.is_multipart():
                    for part in email_message.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True).decode()
                            break
                else:
                    body = email_message.get_payload(decode=True).decode()

                return f"Subject: {subject}\n\n{body}"
            except Exception as e:
                return f"Error checking emails: {e}"

        else:
            return "Invalid query."