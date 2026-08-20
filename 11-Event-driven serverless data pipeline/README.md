# Event-Driven Data Pipeline with SQS, Lambda and S3

## Overview

This project implements a serverless, event-driven data pipeline using Amazon SQS, AWS Lambda, and Amazon S3.

The pipeline accepts application events through Amazon SQS, automatically triggers a Lambda function to process the events, and stores the processed results in Amazon S3 using date-based and event-type-based partitioning.

A Dead Letter Queue (DLQ) is configured to handle events that repeatedly fail processing.

CloudWatch and SNS are used for monitoring and alerting when messages accumulate in the SQS queue.

---

## Architecture

```text
                         Event Producer
                              |
                              v
                    +-------------------+
                    |    Amazon SQS     |
                    |   Main Queue      |
                    +---------+---------+
                              |
                              |
                     SQS → Lambda Trigger
                              |
                              v
                    +-------------------+
                    |    AWS Lambda     |
                    | EventPipeline     |
                    |    Processor      |
                    +---------+---------+
                              |
                              |
                         PutObject
                              |
                              v
                    +-------------------+
                    |    Amazon S3      |
                    |   Data Lake       |
                    +-------------------+
                              |
                              v
                     Downstream Analytics
                     Athena / Glue / BI


                Failed Event Processing
                         |
                         v
                    +---------+
                    |   DLQ   |
                    +---------+


             CloudWatch
                  |
                  v
             SQS Backlog
               Alarm
                  |
                  v
                SNS
                  |
                  v
               Email