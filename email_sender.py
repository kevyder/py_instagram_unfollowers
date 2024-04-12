import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from constants import SENDER_EMAIL, RECEIVER_EMAILS, SENDGRID_API_KEY


class EmailSender:
    def __init__(self) -> None:
        self.sender_email = SENDER_EMAIL
        self.receiver_email = RECEIVER_EMAILS

    def send_email(self, unfollowers: list) -> None:
        content = ""
        for unfollower in unfollowers:
            content += f"<strong>{unfollower}</strong><br>"

        try:
            message = Mail(
                from_email=self.sender_email,
                to_emails=self.receiver_email,
                subject="These IG accounts unfollowed you recently",
                html_content=content,
            )
            sg = SendGridAPIClient(SENDGRID_API_KEY)
            response = sg.send(message)
        except Exception as e:
            print(e.message)
