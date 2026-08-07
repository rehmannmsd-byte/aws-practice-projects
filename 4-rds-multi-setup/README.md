# AWS RDS PostgreSQL with Secure VPC Architecture

This project demonstrates how to deploy a highly secure, production-style Amazon RDS PostgreSQL database inside a custom Amazon VPC. The database is hosted in private subnets and accessed securely through a Bastion Host, following AWS security best practices.

The project focuses on networking, database administration, high availability concepts, automated backups, and secure access to managed database services.

---

# Architecture

```text
                    Internet
                        │
                 Internet Gateway
                        │
        ┌───────────────┴───────────────┐
        │                               │
 Public Subnet A                 Public Subnet B
        │
  Bastion Host (EC2)
        │
    SSH (Port 22)
        │
        ▼
──────────────────────────────────────────────────
        │
 Private Subnet A             Private Subnet B
        │                           │
        └──────── Amazon RDS PostgreSQL ────────┘
```

---

# AWS Services Used

* Amazon VPC
* Amazon EC2
* Amazon RDS (PostgreSQL)
* Internet Gateway
* Public Subnets
* Private Subnets
* Route Tables
* Security Groups
* DB Subnet Groups
* Amazon CloudWatch
* AWS IAM

---

# Features

* Custom Amazon VPC
* Public and Private Subnet Architecture
* Secure Bastion Host for Database Administration
* Amazon RDS PostgreSQL Deployment
* Private Database (No Public Access)
* DB Subnet Group Configuration
* Security Group-Based Access Control
* Automated Backups
* Manual Snapshots
* CloudWatch Monitoring
* PostgreSQL Database Administration
* Production-Oriented Network Design

---

# Project Files

```text
.
├── README.md
```

---

# Infrastructure Overview

The infrastructure consists of:

* One custom Amazon VPC
* Two Public Subnets
* Two Private Subnets
* Internet Gateway
* Public Route Table
* Private Route Table
* Bastion EC2 Instance
* Amazon RDS PostgreSQL Instance
* DB Subnet Group
* Security Groups

The database remains private and can only be accessed through the Bastion Host.

---

# Deployment Workflow

1. Create a custom Amazon VPC.
2. Create two public subnets and two private subnets.
3. Attach an Internet Gateway to the VPC.
4. Configure public and private route tables.
5. Create Security Groups for the Bastion Host and RDS instance.
6. Launch an EC2 Bastion Host in the public subnet.
7. Install the PostgreSQL client (`psql`) on the Bastion Host.
8. Create a DB Subnet Group using the private subnets.
9. Deploy Amazon RDS PostgreSQL.
10. Connect to the database securely using the Bastion Host.
11. Create a database, tables, and sample records.
12. Explore monitoring, backups, and snapshots.

---

# Security Configuration

## Bastion Host Security Group

| Protocol | Port | Source       |
| -------- | ---- | ------------ |
| SSH      | 22   | My Public IP |

## RDS Security Group

| Protocol   | Port | Source                      |
| ---------- | ---- | --------------------------- |
| PostgreSQL | 5432 | Bastion Host Security Group |

This configuration ensures that the PostgreSQL database is never directly accessible from the internet.

---

# PostgreSQL Operations

After connecting to the RDS instance, the following operations were performed:

* Created a new database
* Created tables
* Inserted sample data
* Queried records
* Verified connectivity
* Tested SQL commands using `psql`

---

# Monitoring and Backup

The following Amazon RDS operational features were explored:

* Automated Backups
* Manual Snapshots
* Backup Retention
* Maintenance Windows
* CloudWatch Metrics
* Database Monitoring
* High Availability Concepts
* Multi-AZ Deployment Concepts

---

# Technologies Used

* Amazon VPC
* Amazon EC2
* Amazon RDS PostgreSQL
* PostgreSQL
* Linux (Ubuntu)
* SSH
* SQL
* Amazon CloudWatch
* AWS IAM

---

# Learning Outcomes

This project provided hands-on experience with:

* Designing secure AWS networking architectures
* Creating custom VPCs
* Configuring public and private subnets
* Managing route tables and Internet Gateways
* Implementing Security Groups
* Deploying Amazon RDS PostgreSQL
* Configuring DB Subnet Groups
* Connecting securely through a Bastion Host
* Executing SQL commands using PostgreSQL
* Monitoring databases using CloudWatch
* Understanding automated backups and snapshots
* Learning Multi-AZ high availability concepts

---

# Future Improvements

* Enable Multi-AZ deployment for high availability
* Configure Read Replicas for read scaling
* Integrate an application server with Amazon RDS
* Implement IAM Database Authentication
* Configure CloudWatch Alarms and SNS notifications
* Deploy using Infrastructure as Code (AWS CloudFormation or Terraform)
* Add AWS Systems Manager Session Manager for bastion access

---

# License

This project is created for educational purposes and serves as part of an AWS Cloud Engineering portfolio.
