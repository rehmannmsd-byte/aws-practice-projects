# Amazon EKS Kubernetes Autoscaling Project

## Overview

This project demonstrates deploying and operating a containerized application on Amazon EKS with:

- Amazon EKS managed node groups
- Docker and Amazon ECR
- Kubernetes Deployments and Services
- Helm
- AWS Load Balancer Controller
- Application Load Balancer
- Horizontal Pod Autoscaler (HPA)
- Kubernetes Metrics Server
- Cluster Autoscaler
- Automatic pod scaling
- Automatic EC2 node scaling
- Kubernetes self-healing

The project demonstrates both application-level and infrastructure-level
horizontal scaling.

---

## Architecture

```text
                         Internet
                            |
                            v
                    AWS Application
                    Load Balancer
                            |
                            v
                    Kubernetes Ingress
                            |
                            v
                    Kubernetes Service
                            |
                 +----------+----------+
                 |                     |
                 v                     v
              Pod 1                  Pod 2
                 |                     |
                 +----------+----------+
                            |
                            v
                           HPA
                            |
                    More Pods required
                            |
                            v
                  Kubernetes Scheduler
                            |
                   Insufficient capacity
                            |
                            v
                  Cluster Autoscaler
                            |
                            v
                    EKS Node Group
                            |
                       EC2 Nodes