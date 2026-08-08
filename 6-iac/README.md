# 🚀 AWS Terraform Project – VPC, Bastion Host & RDS (PostgreSQL)

## 📌 Overview

This project provisions a secure AWS infrastructure using Terraform.

It includes:

* Custom VPC
* Bastion Host (EC2) in Public Subnet
* Amazon RDS PostgreSQL in Private Subnets
* Secure Security Groups
* Infrastructure as Code (IaC)

---

## 🏗️ Architecture

```
Internet
   │
   ▼
[Bastion Host - EC2 (Public Subnet)]
   │
   ▼
[RDS PostgreSQL (Private Subnets - Multi AZ)]
```

---

## ✨ Features

* Fully automated infrastructure using Terraform
* Multi-AZ ready database setup
* Secure access via Bastion Host
* No public DB exposure
* Clean and production-ready structure

---

## 🛠️ Prerequisites

* AWS Account
* Terraform (v1.13+)
* AWS CLI configured (`aws configure`)
* SSH Key Pair created in AWS

---

## 📂 Project Structure

```
.
├── main.tf
├── README.md
```

---

## ⚙️ Configuration

Before running, update the following values in `main.tf`:

### 1. Your Public IP

```
cidr_blocks = ["YOUR_PUBLIC_IP/32"]
```

Find your IP: [https://whatismyipaddress.com/](https://whatismyipaddress.com/)

---

### 2. Key Pair

```
key_name = "your-key-name"
```

---

### 3. Database Credentials

```
username = "dbadmin"
password = "StrongPassword123!"
```

---

## ▶️ Deployment Steps

### Initialize Terraform

```
terraform init
```

### Preview Changes

```
terraform plan
```

### Apply Infrastructure

```
terraform apply
```

Type `yes` when prompted.

---

## 📤 Outputs

After deployment, Terraform will display:

* EC2 Public IP
* RDS Endpoint

---

## 🔐 Connect to Bastion Host

```
ssh -i your-key.pem ubuntu@<EC2_PUBLIC_IP>
```

---

## 🧰 Install PostgreSQL Client

```
sudo apt update -y
sudo apt install -y postgresql-client
```

---

## 🔗 Connect to RDS

```
psql -h <RDS_ENDPOINT> -U dbadmin -d company
```

---

## 🧪 Sample SQL

```
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    name TEXT,
    department TEXT,
    salary INT
);

INSERT INTO employees (name, department, salary)
VALUES
('Rehman', 'Cloud', 75000),
('Alice', 'DevOps', 82000),
('Bob', 'Security', 90000);

SELECT * FROM employees;
```

---

## 🔒 Security Best Practices

* SSH access restricted to your IP
* RDS is not publicly accessible
* Only Bastion Host can access the database
* Database is deployed in private subnets

---

## 🧹 Cleanup

To delete all resources:

```
terraform destroy
```

---

## ⚠️ Common Issues

### Reserved Username Error

Do not use:

```
admin, root, postgres
```

Use:

```
dbadmin
```

---

### DB Subnet Group Error

Ensure:

* At least 2 subnets
* Different Availability Zones

---

### SSH Not Working

* Verify your public IP
* Check security group rules
* Ensure correct key pair

---

## 🚀 Future Improvements

* Use Terraform variables
* Create reusable modules
* Add S3 backend for remote state
* Integrate CI/CD pipeline
* Use AWS Secrets Manager

---

## 👨‍💻 Author

rehman

---

## ⭐ Support

If you found this useful, give it a ⭐ on GitHub!

---

If you want next:

👉 Terraform modules
👉 CI/CD pipeline
👉 App deployment on this infra

Just tell me 👍
