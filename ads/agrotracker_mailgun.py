import requests
from flask import current_app

def send_notification_email(to_email, subject, message):
    # Параметри Mailgun
    mailgun_api_key = current_app.config['MAILGUN_API_KEY']
    mailgun_domain = current_app.config['MAILGUN_DOMAIN']

    # HTTP-запит до Mailgun API
    response = requests.post(
        f"https://api.mailgun.net/v3/{mailgun_domain}/messages",
        auth=("api", mailgun_api_key),
        data={
            "from": f"AgroTracker <mailgun@{mailgun_domain}>",
            "to": [to_email],
            "subject": subject,
            #"text": message,  # Простий текст
            "html": message   # Якщо ви хочете відправити HTML-лист
        }
    )
    return response