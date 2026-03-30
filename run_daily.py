import os
import requests

print("Housing split agent started")

try:
    api_key = os.environ.get("SENDGRID_API_KEY")
    email_to = os.environ.get("EMAIL_TO")
    email_from = os.environ.get("EMAIL_FROM")

    if not api_key:
        print("No API key found - skipping email")
    else:
        url = "https://api.sendgrid.com/v3/mail/send"

        data = {
            "personalizations": [
                {"to": [{"email": email_to}]}
            ],
            "from": {"email": email_from},
            "subject": "Housing split agent test",
            "content": [
                {
                    "type": "text/plain",
                    "value": "Agent draait"
                }
            ]
        }

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        response = requests.post(url, headers=headers, json=data)

        print("Mail status:", response.status_code)
        print(response.text)

except Exception as e:
    print("ERROR:", str(e))

print("Script finished WITHOUT crashing")

