
---

# 2. `lambda/lambda_function.py`

```python
import json
import boto3
import os
from datetime import datetime, timezone


s3 = boto3.client("s3")

BUCKET_NAME = os.environ["DESTINATION_BUCKET"]


def lambda_handler(event, context):

    processed = 0

    for record in event["Records"]:

        body = json.loads(record["body"])

        event_type = body.get("event_type")
        event_id = body.get("event_id")

        if not event_type:
            raise ValueError("Missing event_type")

        if not event_id:
            raise ValueError("Missing event_id")

        processed_at = datetime.now(timezone.utc)

        year = processed_at.strftime("%Y")
        month = processed_at.strftime("%m")
        day = processed_at.strftime("%d")

        result = {
            "event_id": event_id,
            "event_type": event_type,
            "original_event": body,
            "processed_at": processed_at.isoformat(),
            "processor": "EventPipelineProcessor"
        }

        key = (
            f"event_type={event_type}/"
            f"year={year}/"
            f"month={month}/"
            f"day={day}/"
            f"{event_id}.json"
        )

        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=key,
            Body=json.dumps(result, indent=2),
            ContentType="application/json"
        )

        processed += 1

    return {
        "statusCode": 200,
        "processed": processed
    }