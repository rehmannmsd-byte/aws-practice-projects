import json
import boto3
import os
import re
import traceback

# Initialize SES client
ses = boto3.client(
    "ses",
    region_name=os.environ["AWS_REGION"]
)

SENDER_EMAIL = os.environ["SENDER_EMAIL"]
RECIPIENT_EMAIL = os.environ["RECIPIENT_EMAIL"]


def validate_email(email):
    pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
    return re.match(pattern, email)


def response(status_code, message):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "POST,OPTIONS"
        },
        "body": json.dumps({
            "message": message
        })
    }


def lambda_handler(event, context):

    print("========== NEW REQUEST ==========")
    print("Received Event:")
    print(json.dumps(event, indent=2))

    try:

        body = json.loads(event.get("body", "{}"))

        print("\nParsed Request Body:")
        print(json.dumps(body, indent=2))

        name = body.get("name", "").strip()
        email = body.get("email", "").strip()
        subject = body.get("subject", "").strip()
        message = body.get("message", "").strip()

        print("\nParsed Values")
        print("----------------------------")
        print(f"Name    : {name}")
        print(f"Email   : {email}")
        print(f"Subject : {subject}")
        print(f"Message : {message}")

        # ----------------------------
        # Validation
        # ----------------------------

        if not name:
            return response(400, "Name is required.")

        if not validate_email(email):
            return response(400, "Please enter a valid email address.")

        if not subject:
            return response(400, "Subject is required.")

        if not message:
            return response(400, "Message cannot be empty.")

        email_subject = f"Website Contact Form | {subject}"

        email_body = f"""
New Website Contact Form Submission

----------------------------------------

Name:
{name}

Email:
{email}

Subject:
{subject}

Message:
{message}

----------------------------------------

This email was generated automatically by the AWS Serverless Contact Form.
"""

        print("\nSending email through Amazon SES...")

        ses_response = ses.send_email(

            Source=SENDER_EMAIL,

            Destination={
                "ToAddresses": [
                    RECIPIENT_EMAIL
                ]
            },

            Message={
                "Subject": {
                    "Data": email_subject
                },
                "Body": {
                    "Text": {
                        "Data": email_body
                    }
                }
            }

        )

        print("\nSES Response:")
        print(json.dumps(ses_response, indent=2, default=str))

        print("\nEmail sent successfully!")

        return response(
            200,
            "Thank you! Your message has been sent successfully."
        )

    except Exception as e:

        print("\n========== ERROR ==========")
        print(str(e))
        traceback.print_exc()

        return response(
            500,
            "Internal Server Error"
        )