# EKS GitOps with ArgoCD

## Overview

This project implements GitOps deployment to Amazon EKS using ArgoCD.

The Git repository acts as the source of truth for Kubernetes application configuration.

ArgoCD continuously monitors the repository and reconciles the desired state defined in Git with the actual state running in the EKS cluster.

The project also demonstrates the App of Apps pattern for managing multiple ArgoCD Applications from a single root Application.

---

## Architecture

```text
Developer
    |
    | git push
    v
GitHub Repository
    |
    | desired state
    v
ArgoCD
    |
    | App of Apps
    |
    +------------+
    |            |
    v            v
eks-demo      Future Apps
    |
    v
Helm Chart
    |
    v
Amazon EKS
    |
    +-- Deployment
    +-- Service
    +-- Ingress
    +-- HPA
    |
    v
AWS Application Load Balancer