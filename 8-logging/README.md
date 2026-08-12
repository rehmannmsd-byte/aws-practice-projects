# Centralized Logging with CloudWatch and OpenSearch

## Overview

This project implements a centralized logging and monitoring solution using Amazon CloudWatch.

An Ubuntu EC2 instance acts as the log source. A sample application continuously generates application logs containing INFO, WARNING, and ERROR events.

The Amazon CloudWatch Agent collects these logs and sends them to CloudWatch Logs.

CloudWatch Metric Filters detect ERROR events and publish them as custom CloudWatch metrics. A CloudWatch Alarm monitors the metric and sends an email notification through Amazon SNS whenever an application error is detected.

The OpenSearch integration is planned as a future extension of the project.

---

## Architecture

```text
                    Ubuntu EC2
                        |
                        |
                application.log
                        |
                        v
              CloudWatch Agent
                        |
                        v
               CloudWatch Logs
                        |
              +---------+---------+
              |                   |
              v                   v
        Metric Filter        OpenSearch
        (ERROR events)       (Planned)
              |
              v
      ApplicationErrors
              |
              v
       CloudWatch Alarm
              |
              v
              SNS
              |
              v
         Email Alert
```

---

## Project Objectives

The main objectives of this project are:

- Collect application logs from an EC2 instance.
- Centralize logs using Amazon CloudWatch Logs.
- Detect application errors automatically.
- Create custom CloudWatch metrics from log events.
- Configure CloudWatch alarms.
- Send error notifications through Amazon SNS.
- Prepare the architecture for advanced log analysis using OpenSearch.

---

# AWS Services Used

## Amazon EC2

Ubuntu EC2 is used as the source of application logs.

The sample application runs on the EC2 instance and writes logs to:

```text
/home/ubuntu/logging-app/application.log
```

---

## CloudWatch Agent

The Amazon CloudWatch Agent runs on the EC2 instance.

It monitors:

```text
/home/ubuntu/logging-app/application.log
```

and sends the contents to CloudWatch Logs.

---

## CloudWatch Logs

The application logs are stored in the following log group:

```text
centralized-app-logs
```

The log stream follows this pattern:

```text
{instance_id}/application
```

---

## CloudWatch Metric Filter

A metric filter detects log entries containing:

```text
ERROR
```

The metric filter is configured with:

```text
Filter Name:
ApplicationErrorFilter

Metric Namespace:
CentralizedLogging

Metric Name:
ApplicationErrors

Metric Value:
1
```

Every matching ERROR log increments the `ApplicationErrors` metric.

---

## CloudWatch Alarm

The CloudWatch alarm monitors:

```text
ApplicationErrors
```

Configuration:

```text
Statistic: Sum
Period: 1 minute
Threshold: Greater than or equal to 1
```

Therefore, when at least one ERROR event is detected during the evaluation period, the alarm changes to:

```text
ALARM
```

---

## Amazon SNS

Amazon SNS is used to send email notifications when the CloudWatch alarm enters the ALARM state.

The SNS topic used for the project is:

```text
centralized-logging-alerts
```

The email subscription must be confirmed before notifications can be received.

---

# Application

The application is intentionally simple.

It continuously generates five types of log messages:

```text
INFO
INFO
WARNING
ERROR
INFO
```

Example:

```text
2026-08-12 13:40:01 INFO Application started successfully
2026-08-12 13:40:06 INFO User request processed successfully
2026-08-12 13:40:11 WARNING High response time detected
2026-08-12 13:40:16 ERROR Database connection failed
2026-08-12 13:40:21 INFO Database connection restored
```

This makes it possible to demonstrate centralized logging and automated error detection without requiring a complex production application.

---

# Files

```text
6-Centralized-Logging/
│
├── README.md
├── app.sh
├── cloudwatch-agent-config.json
└── .gitignore
```

### README.md

Project documentation and architecture.

### app.sh

Sample application that generates application logs.

### cloudwatch-agent-config.json

CloudWatch Agent configuration used to collect the application log.

### .gitignore

Prevents logs, AWS credentials, private keys, installers, and other sensitive or unnecessary files from being committed.

---

# EC2 Setup

## 1. Create the application directory

```bash
mkdir -p ~/logging-app
cd ~/logging-app
```

Copy `app.sh` into this directory.

Make it executable:

```bash
chmod +x app.sh
```

---

## 2. Start the application

Run:

```bash
./app.sh
```

The application continuously writes logs to:

```text
/home/ubuntu/logging-app/application.log
```

To monitor the logs locally:

```bash
tail -f application.log
```

---

# CloudWatch Agent Installation

The CloudWatch Agent was installed using the official AWS package.

Example:

```bash
wget https://amazoncloudwatch-agent.s3.amazonaws.com/ubuntu/amd64/latest/amazon-cloudwatch-agent.deb
```

Install the package:

```bash
sudo dpkg -i -E ./amazon-cloudwatch-agent.deb
```

Verify the installation:

```bash
/opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent --version
```

---

# IAM Configuration

The EC2 instance uses an IAM role to allow the CloudWatch Agent to publish logs.

The role used for the EC2 instance is:

```text
EC2-CloudWatch-Logs-Role
```

The role should have:

```text
CloudWatchAgentServerPolicy
```

attached.

No AWS access keys are stored on the EC2 instance.

---

# CloudWatch Agent Configuration

The CloudWatch Agent configuration is:

```json
{
  "logs": {
    "logs_collected": {
      "files": {
        "collect_list": [
          {
            "file_path": "/home/ubuntu/logging-app/application.log",
            "log_group_name": "centralized-app-logs",
            "log_stream_name": "{instance_id}/application",
            "timezone": "UTC"
          }
        ]
      }
    }
  }
}
```

The configuration file is placed at:

```text
/opt/aws/amazon-cloudwatch-agent/bin/config.json
```

---

# Start CloudWatch Agent

Run:

```bash
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl \
-a fetch-config \
-m ec2 \
-c file:/opt/aws/amazon-cloudwatch-agent/bin/config.json \
-s
```

Check the status:

```bash
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a status
```

Expected result:

```json
{
  "status": "running",
  "configstatus": "configured"
}
```

---

# Verify CloudWatch Logs

Go to:

```text
AWS Console
→ CloudWatch
→ Logs
→ Log groups
→ centralized-app-logs
```

Open the application log stream.

Application messages should appear there.

---

# Testing the Metric Filter

To manually generate an ERROR event:

```bash
echo "$(date '+%Y-%m-%d %H:%M:%S') ERROR CLOUDWATCH_TEST_ERROR" >> ~/logging-app/application.log
```

Verify locally:

```bash
tail -5 ~/logging-app/application.log
```

The ERROR should then appear in the CloudWatch log stream.

The metric filter should detect the `ERROR` event and increment:

```text
CentralizedLogging
└── ApplicationErrors
```

---

# Testing the CloudWatch Alarm

Generate an error:

```bash
echo "$(date '+%Y-%m-%d %H:%M:%S') ERROR ALARM_TEST" >> ~/logging-app/application.log
```

The expected flow is:

```text
ERROR log
    ↓
CloudWatch Logs
    ↓
Metric Filter
    ↓
ApplicationErrors
    ↓
CloudWatch Alarm
    ↓
SNS
    ↓
Email
```

The alarm should transition to:

```text
ALARM
```

and an SNS notification should be delivered to the confirmed email subscription.

---

# Troubleshooting

## CloudWatch Agent is not running

Check:

```bash
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a status
```

Check the agent logs:

```bash
sudo tail -50 /opt/aws/amazon-cloudwatch-agent/logs/amazon-cloudwatch-agent.log
```

---

## Application logs are not appearing in CloudWatch

Check the local log:

```bash
tail -f ~/logging-app/application.log
```

Check the CloudWatch Agent status:

```bash
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a status
```

Check the agent log:

```bash
sudo tail -50 /opt/aws/amazon-cloudwatch-agent/logs/amazon-cloudwatch-agent.log
```

Also verify that the EC2 IAM role has:

```text
CloudWatchAgentServerPolicy
```

---

## Metric is not increasing

First confirm the ERROR exists in the CloudWatch log stream.

Generate a test event:

```bash
echo "$(date '+%Y-%m-%d %H:%M:%S') ERROR METRIC_FILTER_TEST" >> ~/logging-app/application.log
```

Then check the metric:

```text
CloudWatch
→ Metrics
→ Custom namespaces
→ CentralizedLogging
→ ApplicationErrors
```

---

## SNS email is not received

Verify that the SNS subscription has been confirmed.

The subscription status should be:

```text
Confirmed
```

If it is:

```text
PendingConfirmation
```

check the email inbox and confirm the SNS subscription.

---

# Security Considerations

The project follows several basic security practices:

- AWS credentials are not stored on the EC2 instance.
- IAM roles are used instead of access keys.
- Application logs are centralized in CloudWatch.
- Sensitive files are excluded using `.gitignore`.
- Private keys are not stored in the repository.
- The OpenSearch integration should use appropriate access controls when implemented.

For production environments, additional controls should be implemented including:

- Least-privilege IAM policies.
- Private VPC networking.
- Restricted security groups.
- Encryption.
- Log retention policies.
- Centralized identity and access management.
- Monitoring and auditing.

---

# OpenSearch Integration

The OpenSearch portion of the project is planned but not yet completed.

The intended architecture is:

```text
CloudWatch Logs
      ↓
Subscription Filter
      ↓
Amazon Data Firehose
      ↓
Amazon OpenSearch Service
      ↓
Search and Log Analysis
```

An OpenSearch domain named:

```text
centralized-logging
```

has been provisioned.

The CloudWatch Logs → Firehose → OpenSearch integration remains to be completed.

---

# Current Project Status

| Component | Status |
|---|---|
| EC2 log source | Completed |
| Application log generation | Completed |
| CloudWatch Agent | Completed |
| CloudWatch Log Group | Completed |
| Metric Filter | Completed |
| Custom CloudWatch Metric | Completed |
| CloudWatch Alarm | Completed |
| SNS notification | Completed |
| Email alert testing | Completed |
| OpenSearch domain | Completed |
| CloudWatch → Firehose | Pending |
| Firehose → OpenSearch | Pending |
| OpenSearch log search | Pending |

---

# Technologies

- Amazon EC2
- Ubuntu Linux
- Amazon CloudWatch
- CloudWatch Agent
- CloudWatch Logs
- CloudWatch Metric Filters
- CloudWatch Alarms
- Amazon SNS
- Amazon OpenSearch Service
- Amazon Data Firehose
- Bash
- AWS IAM

---

# Learning Outcomes

After completing this project, the following concepts are demonstrated:

1. Collecting application logs from an EC2 instance.
2. Installing and configuring the CloudWatch Agent.
3. Centralizing logs using CloudWatch Logs.
4. Creating metric filters from log events.
5. Creating custom CloudWatch metrics.
6. Configuring CloudWatch alarms.
7. Sending automated alerts using SNS.
8. Designing a centralized logging architecture.
9. Preparing application logs for advanced analysis with OpenSearch.

---

# Future Improvements

The following improvements can be added later:

- Complete CloudWatch Logs → Firehose → OpenSearch integration.
- Create OpenSearch dashboards.
- Add additional metric filters for WARNING and other application events.
- Configure log retention policies.
- Add structured JSON application logs.
- Add multiple EC2 instances as log sources.
- Add application-specific dashboards.
- Add automated infrastructure deployment using Terraform.