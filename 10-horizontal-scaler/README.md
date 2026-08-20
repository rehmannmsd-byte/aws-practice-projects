# Horizontal Auto Scaling with Application Load Balancer and Auto Scaling Group

## Overview

This project demonstrates horizontal auto scaling of a web application on AWS using:

- Amazon VPC
- Application Load Balancer (ALB)
- EC2
- EC2 Launch Template
- Auto Scaling Group (ASG)
- Target Group
- Nginx
- CloudWatch
- Target Tracking Scaling Policy

The application runs on multiple EC2 instances distributed across Availability Zones.

The Application Load Balancer distributes incoming HTTP traffic across healthy EC2 instances, while the Auto Scaling Group automatically adjusts the number of EC2 instances based on demand.

---

## Architecture

```text
                         Internet
                            |
                            v
              +--------------------------+
              | Application Load Balancer|
              |      autoscaling-alb     |
              +------------+-------------+
                           |
                           v
                 +-------------------+
                 |    Target Group   |
                 | autoscaling-web-tg|
                 +---------+---------+
                           |
                 +---------+---------+
                 |                   |
                 v                   v
          +-------------+     +-------------+
          |   EC2 #1    |     |   EC2 #2    |
          | Private AZ1 |     | Private AZ2 |
          +-------------+     +-------------+
                 \                   /
                  \                 /
                   +---------------+
                   | Auto Scaling  |
                   |     Group     |
                   +---------------+
                           |
                  Scale Out / Scale In