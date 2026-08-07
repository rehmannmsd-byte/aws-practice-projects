# 🚀 AWS Project 1 - EC2 Linux Server Bootstrap with Nginx, Flask & CloudWatch

## 📖 Overview

This project demonstrates how to provision an **Amazon EC2 Ubuntu instance** using **EC2 User Data** to automatically configure a production-style Linux server.

The instance boots with:

* Python virtual environment
* Flask web application
* Nginx reverse proxy
* CloudWatch Agent
* AWS Systems Manager Parameter Store integration
* UFW firewall configuration
* Automatic security updates

The goal of this project is to understand **EC2 bootstrapping**, **Linux service management**, **reverse proxy architecture**, and **AWS monitoring**.

---

# 🏗️ Architecture

```text
                Internet
                    │
                    ▼
              EC2 Public IP
                    │
                    ▼
            Nginx (Port 80)
                    │
                    ▼
        Flask Application (Port 8080)
                    │
                    ▼
             Python Virtual Environment

                    │
                    ▼
      CloudWatch Agent → CloudWatch Logs & Metrics

                    │
                    ▼
     Systems Manager Parameter Store
        (CloudWatch Configuration)
```

---

# 📌 Objectives

* Learn EC2 User Data automation
* Configure Linux services automatically
* Deploy a Flask application
* Understand Nginx as a reverse proxy
* Configure CloudWatch Agent
* Store CloudWatch configuration in Systems Manager Parameter Store
* Understand IAM Roles for EC2

---

# 🛠️ Services Used

* Amazon EC2
* Amazon CloudWatch
* AWS Systems Manager Parameter Store
* IAM
* Security Groups

---

# 📂 Project Structure

```text
EC2 Instance
│
├── Flask Application
│   └── /opt/webapp/app.py
│
├── Python Virtual Environment
│   └── /opt/webapp/venv
│
├── Nginx
│   └── Reverse Proxy
│
├── CloudWatch Agent
│
└── User Data Bootstrap Script
```

---

# ⚙️ Technologies

* Ubuntu Server
* Python 3
* Flask
* Nginx
* systemd
* CloudWatch Agent
* AWS CLI
* UFW

---

# 🚀 Deployment Steps

## 1. Launch an EC2 Instance

* Ubuntu Server
* t2.micro (Free Tier eligible)
* Assign a public IP
* Attach an IAM Role with:

  * `CloudWatchAgentServerPolicy`
  * `AmazonSSMManagedInstanceCore`
  * `ssm:GetParameter` permission for the CloudWatch configuration parameter

---

## 2. Create a Parameter Store Entry

Create the following parameter:

```text
/cloudwatch/linux/config
```

Store the CloudWatch Agent JSON configuration as the parameter value.

---

## 3. Add the User Data Script

Paste the bootstrap script into the **User Data** section while launching the instance.

The script automatically:

* Updates the OS
* Installs dependencies
* Creates a Python virtual environment
* Deploys the Flask application
* Configures Nginx
* Creates and starts the `webapp` systemd service
* Installs the CloudWatch Agent
* Fetches the CloudWatch configuration from Parameter Store
* Starts CloudWatch Agent
* Enables the firewall
* Enables automatic security updates

---

## 4. Access the Application

Open:

```text
http://<EC2_PUBLIC_IP>
```

Expected output:

```text
🚀 EC2 Linux Server Running
```

---

# 📊 CloudWatch Integration

The CloudWatch Agent configuration is **not stored on the EC2 instance**.

Instead, it is retrieved from **AWS Systems Manager Parameter Store** during instance initialization.

Metrics collected:

* CPU
* Memory
* Disk Usage

Log files collected:

* `/var/log/syslog`
* `/var/log/nginx/access.log`
* `/var/log/nginx/error.log`
* `/var/log/user-data.log`

---

# 🔐 IAM Permissions

Required managed policies:

```text
CloudWatchAgentServerPolicy
AmazonSSMManagedInstanceCore
```

Additional permission:

```text
ssm:GetParameter
```

to allow the EC2 instance to retrieve the CloudWatch configuration.

---

# 🔄 Request Flow

```text
Browser
    │
    ▼
Nginx (Port 80)
    │
    ▼
Flask (Port 8080)
    │
    ▼
HTML Response
```

---

# 📚 Key Concepts Learned

* EC2 User Data bootstrapping
* Linux service management with systemd
* Python virtual environments
* Reverse proxy using Nginx
* Flask deployment
* CloudWatch Agent configuration
* Parameter Store integration
* IAM Roles for EC2
* Security Groups
* Linux firewall configuration
* CloudWatch metrics and logs

---

# 🧩 Challenges Faced

### CloudFront-style configuration mindset

Initially, the focus was simply on getting services running. Through debugging, it became clear that production deployments require correct configuration ordering and service reloads.

### Nginx Configuration

Nginx initially served the default welcome page because the new configuration was created after Nginx had already started.

**Resolution:**

* Validate configuration with `nginx -t`
* Reload or restart Nginx after configuration changes

### CloudWatch Agent

The CloudWatch Agent was installed but remained in a **Stopped / Not Configured** state.

**Resolution:**

* Store the agent configuration in Systems Manager Parameter Store
* Fetch the configuration during boot
* Start the agent using `amazon-cloudwatch-agent-ctl`

---

# 🚀 Future Improvements

* Deploy using Terraform
* Build a custom AMI
* Store the Flask application in Amazon S3
* Add HTTPS with ACM and an Application Load Balancer
* Deploy behind CloudFront
* Implement CI/CD with GitHub Actions
* Use Auto Scaling Groups
* Store application secrets in AWS Secrets Manager

---

# 🎯 Outcome

By completing this project, I learned how to automate the provisioning of an EC2 instance using User Data, deploy a Python Flask application behind an Nginx reverse proxy, integrate CloudWatch monitoring, and centralize configuration using AWS Systems Manager Parameter Store.

This project also reinforced production-oriented concepts such as infrastructure bootstrapping, service management, monitoring, IAM-based access control, and configuration management.
