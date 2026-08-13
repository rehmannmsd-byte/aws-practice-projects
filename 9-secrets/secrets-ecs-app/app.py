import os
import json
import boto3

secrets_client = boto3.client("secretsmanager")

SECRET_NAME = os.environ.get(
    "SECRET_NAME",
    "prod/rds/postgres"
)


def get_secret():
    response = secrets_client.get_secret_value(
        SecretId=SECRET_NAME
    )

    return json.loads(response["SecretString"])


if __name__ == "__main__":
    secret = get_secret()

    print("Secrets Manager integration successful")
    print(f"Database host: {secret.get('host')}")
    print(f"Database name: {secret.get('dbname')}")
    print(f"Database user: {secret.get('username')}")

    # Intentionally do NOT print the password.