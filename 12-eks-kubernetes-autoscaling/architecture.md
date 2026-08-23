# Architecture

## Overview

This project demonstrates a containerized web application running on Amazon EKS with:

- Amazon ECR for container image storage
- Amazon EKS managed node groups
- Kubernetes Deployment and Service
- Helm for application packaging
- AWS Load Balancer Controller
- AWS Application Load Balancer (ALB)
- Kubernetes Ingress
- Metrics Server
- Horizontal Pod Autoscaler (HPA)
- Cluster Autoscaler
- Kubernetes self-healing

The architecture supports both application-level and infrastructure-level horizontal scaling.

---

## High-Level Architecture

```text
                              Internet
                                 |
                                 v
                    +--------------------------+
                    |    AWS Application       |
                    |       Load Balancer      |
                    |          (ALB)            |
                    +------------+-------------+
                                 |
                                 v
                    +--------------------------+
                    | Kubernetes Ingress       |
                    |      eks-demo            |
                    +------------+-------------+
                                 |
                                 v
                    +--------------------------+
                    | Kubernetes Service       |
                    |        ClusterIP         |
                    +------------+-------------+
                                 |
                    +------------+-------------+
                    |                          |
                    v                          v
             +------------+             +------------+
             |   Pod 1    |             |   Pod 2    |
             | eks-demo   |             | eks-demo   |
             +------------+             +------------+
                    |                          |
                    +------------+-------------+
                                 |
                                 v
                         Metrics Server
                                 |
                                 v
                   +--------------------------+
                   | Horizontal Pod Autoscaler|
                   |          (HPA)            |
                   +------------+-------------+
                                |
                                v
                         More / fewer Pods
                                |
                                v
                    Kubernetes Scheduler
                                |
                    Insufficient capacity?
                                |
                                v
                   +--------------------------+
                   |   Cluster Autoscaler     |
                   +------------+-------------+
                                |
                                v
                   +--------------------------+
                   | EKS Managed Node Group   |
                   +------------+-------------+
                                |
                     +----------+----------+
                     |                     |
                     v                     v
                  EC2 Node              EC2 Node