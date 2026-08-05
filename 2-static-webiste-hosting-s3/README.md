# 🌐 AWS Project 1 - Static Website Hosting with Amazon S3 & CloudFront

## 📖 Overview

This project demonstrates how to host a static website on **Amazon S3** and distribute it globally using **Amazon CloudFront**.

The objective was to understand the fundamentals of static website hosting, content delivery networks (CDNs), caching, origin configuration, and AWS access management.

The website consists of a simple HTML page served from an S3 bucket and delivered through a CloudFront distribution.

---

# 🏗️ Architecture

```text
                User Browser
                     │
                     ▼
          Amazon CloudFront (CDN)
                     │
                     ▼
          Amazon S3 Bucket (Origin)
                     │
                     ▼
               Static Website
```

---

# 🎯 Objectives

* Host a static website using Amazon S3
* Configure an S3 bucket for website hosting
* Create a CloudFront distribution
* Understand CloudFront caching and invalidations
* Learn the difference between S3 Website Endpoints and REST API Endpoints
* Explore Origin Access Control (OAC)
* Troubleshoot common CloudFront and S3 permission issues

---

# 🛠️ AWS Services Used

* Amazon S3
* Amazon CloudFront
* IAM

---

# 📂 Project Structure

```text
project-1/
│
├── index.html
└── README.md
```

---

# 🚀 Deployment Steps

## 1. Create an S3 Bucket

* Create a unique S3 bucket.
* Disable **Block Public Access** (for this learning project).
* Enable **Static Website Hosting**.
* Set:

```text
Index document:
index.html
```

---

## 2. Upload Website Files

Upload:

```text
index.html
```

to the root of the bucket.

---

## 3. Configure Bucket Policy

Allow public read access:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicRead",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::YOUR_BUCKET_NAME/*"
    }
  ]
}
```

---

## 4. Create a CloudFront Distribution

Configure:

* Origin → S3 Bucket
* Viewer Protocol Policy → Redirect HTTP to HTTPS
* Default Root Object:

```text
index.html
```

Wait for the distribution to deploy.

---

## 5. Access the Website

Using S3 Website Endpoint:

```text
http://<bucket-name>.s3-website-<region>.amazonaws.com
```

Using CloudFront:

```text
https://<distribution-id>.cloudfront.net
```

---

# 🌍 Request Flow

```text
Browser
    │
    ▼
CloudFront Edge Location
    │
(Cache Miss)
    │
    ▼
Amazon S3
    │
    ▼
index.html
```

Subsequent requests are served directly from CloudFront's edge cache until the cached object expires or is invalidated.

---

# 📚 Key Concepts Learned

### Amazon S3 Static Website Hosting

* Bucket creation
* Static website hosting
* Bucket policies
* Public object access
* Website endpoints

---

### Amazon CloudFront

* Content Delivery Network (CDN)
* Edge caching
* Cache hits and cache misses
* Distribution deployment
* Default Root Object
* Cache invalidation

---

### Origin Access Control (OAC)

Explored the purpose of OAC and how it enables CloudFront to securely access private S3 buckets.

Key takeaway:

* Public S3 buckets are suitable for learning.
* Private S3 buckets with OAC are the recommended production approach.

---

# 🔍 Challenges Faced

## S3 Access Denied

### Problem

The S3 bucket returned:

```text
403 Access Denied
```

### Root Cause

The bucket policy did not allow public object access.

### Resolution

Configured a bucket policy allowing `s3:GetObject` for the learning environment.

---

## CloudFront 403 Access Denied

### Problem

CloudFront returned:

```text
403 Access Denied
```

while the S3 endpoint worked.

### Root Cause

CloudFront was configured correctly, but the **Default Root Object** had not been set.

CloudFront requested:

```text
/
```

instead of:

```text
/index.html
```

### Resolution

Configured:

```text
Default Root Object = index.html
```

---

## Cached Content

After updating the website, CloudFront continued serving the previous version.

### Resolution

Created a CloudFront invalidation:

```text
/index.html
```

or

```text
/*
```

to remove cached content and force CloudFront to retrieve the latest version from S3.

---

# 💡 Lessons Learned

This project introduced several important AWS concepts:

* Static website hosting with Amazon S3
* CloudFront distributions
* CDN caching behavior
* Cache invalidation
* S3 bucket policies
* Website endpoints vs REST API endpoints
* Origin Access Control (OAC)
* Default Root Objects
* Troubleshooting HTTP 403 errors

---

# 🚀 Future Improvements

* Use a custom domain with Amazon Route 53
* Secure the site using AWS Certificate Manager (ACM)
* Make the S3 bucket private
* Configure CloudFront Origin Access Control (OAC)
* Enable CloudFront access logging
* Deploy automatically using GitHub Actions
* Provision infrastructure using Terraform or AWS CDK

---

# 📸 Suggested Screenshots

Consider adding screenshots of:

* S3 bucket configuration
* Static Website Hosting settings
* Bucket policy
* CloudFront distribution
* CloudFront origin settings
* CloudFront invalidation
* Hosted website
* Browser Developer Tools (showing CloudFront response headers)

---

# 🎯 Outcome

By completing this project, I gained hands-on experience with Amazon S3 and CloudFront, learned how static websites are delivered through a global CDN, understood the importance of proper access policies and cache management, and developed practical troubleshooting skills for common S3 and CloudFront configuration issues.

This project provides a strong foundation for more advanced AWS topics such as Application Load Balancers, Route 53, SSL/TLS with ACM, and Infrastructure as Code.
