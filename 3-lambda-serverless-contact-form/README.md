# AWS Serverless Contact Form

A serverless contact form built using AWS managed services. This project demonstrates how to build a scalable web application without provisioning or managing servers.

The frontend is hosted on Amazon S3 and delivered through Amazon CloudFront. Form submissions are processed by Amazon API Gateway, which invokes an AWS Lambda function to validate the request and send an email using Amazon Simple Email Service (SES).

---

## Architecture

```text
                User
                  │
                  ▼
        Amazon CloudFront
                  │
                  ▼
        Amazon S3 Static Website
        (index.html + script.js)
                  │
          HTTPS POST Request
                  │
                  ▼
         Amazon API Gateway
                  │
                  ▼
        AWS Lambda (Python)
                  │
                  ▼
        Amazon Simple Email Service
                  │
                  ▼
          Recipient Email Inbox
```

---

## AWS Services Used

* Amazon S3
* Amazon CloudFront
* Amazon API Gateway
* AWS Lambda
* Amazon SES
* AWS IAM
* Amazon CloudWatch

---

## Features

* Serverless architecture
* Static website hosting with Amazon S3
* Secure content delivery using CloudFront
* REST API using API Gateway
* Python-based Lambda backend
* Email sending with Amazon SES
* Input validation
* CORS enabled
* IAM role-based security
* CloudWatch logging for monitoring and debugging

---

## Project Files

```text
.
├── index.html
├── script.js
├── lambda_function.py
└── README.md
```

---

## Application Workflow

1. User opens the website through Amazon CloudFront.
2. CloudFront serves the static website from Amazon S3.
3. User fills out the contact form.
4. JavaScript sends a POST request to Amazon API Gateway.
5. API Gateway invokes the AWS Lambda function.
6. Lambda validates the request.
7. Lambda sends an email using Amazon SES.
8. A success response is returned to the user.

---

## Environment Variables

Configure the following Lambda environment variables:

| Variable          | Description                                          |
| ----------------- | ---------------------------------------------------- |
| `AWS_REGION`      | AWS Region where SES is configured                   |
| `SENDER_EMAIL`    | Verified SES sender email                            |
| `RECIPIENT_EMAIL` | Email address that receives contact form submissions |

---

## IAM Permissions

The Lambda execution role requires the following permissions:

* AWSLambdaBasicExecutionRole
* `ses:SendEmail`
* `ses:SendRawEmail`

---

## Technologies Used

* HTML5
* CSS3
* JavaScript (Fetch API)
* Python 3
* AWS Lambda
* Amazon API Gateway
* Amazon SES
* Amazon S3
* Amazon CloudFront
* Amazon CloudWatch
* AWS IAM

---

## Challenges Solved

During development, the following issues were identified and resolved:

* Configured CloudFront Origin Access Control (OAC)
* Fixed S3 bucket access permissions
* Configured API Gateway CORS
* Resolved CloudFront cache invalidation issues
* Fixed frontend payload validation
* Debugged Lambda using CloudWatch Logs
* Added SES permissions to the Lambda IAM role
* Successfully integrated Amazon SES for email delivery

---

## Future Improvements

* Store contact form submissions in DynamoDB
* Send HTML-formatted emails
* Add Google reCAPTCHA
* Configure a custom domain with Route 53 and ACM
* Implement CI/CD using GitHub Actions
* Add rate limiting and AWS WAF protection

---

## Learning Outcomes

This project provided hands-on experience with:

* Serverless application development
* Static website hosting
* API development
* AWS Lambda functions
* Amazon SES integration
* IAM roles and permissions
* CloudWatch logging
* CORS configuration
* Debugging distributed AWS applications

---

## License

This project is created for learning and portfolio purposes.
