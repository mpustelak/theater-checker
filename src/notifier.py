import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailNotifier:
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.sender_email = os.getenv("SENDER_EMAIL")
        self.sender_password = os.getenv("SENDER_PASSWORD")
        raw_recipients = os.getenv("RECIPIENT_EMAIL", "pustleak.mateusz@gmail.com")
        # Support both ; and , as delimiters, but standardize to ", " for the header
        self.recipient_email = raw_recipients.replace(";", ", ")
        self.use_mock = os.getenv("MOCK_EMAIL", "false").lower() == "true"

    def send_notification(self, new_plays):
        """Sends an email notification in Polish with details of new plays."""
        if not new_plays:
            return

        subject = f"Nowe spektakle w Teatrze im. Siemaszkowej: znaleziono {len(new_plays)}"
        
        body = "Cześć,\n\nznalazłem dla Ciebie nowe spektakle:\n\n"
        for play in new_plays:
            body += f"Tytuł: {play['title']}\n"
            body += f"Data: {play['date']}\n"
            body += f"Link: {play['url']}\n"
            body += f"Opis: {play.get('description', 'Brak opisu.')}\n"
            body += "-" * 20 + "\n\n"
        
        body += "Miłego oglądania!\nTwój Bot Teatralny"

        if self.use_mock:
            print("--- MOCK EMAIL START ---")
            print(f"To: {self.recipient_email}")
            print(f"Subject: {subject}")
            print(f"Body:\n{body}")
            print("--- MOCK EMAIL END ---")
            return True

        return self._send_email(subject, body)

    def _send_email(self, subject, body):
        if not all([self.sender_email, self.sender_password]):
            print("Email credentials not provided. Skipping email notification.")
            return False

        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = self.recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain', 'utf-8'))

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            return True
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False
