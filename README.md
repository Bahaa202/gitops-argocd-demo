# GitOps Demo — ArgoCD + Kubernetes

A hands-on demonstration of the **GitOps** deployment pattern using **ArgoCD** on a local Kubernetes cluster (Kind).

## What this project shows

Instead of manually running `kubectl apply`, this project uses **Git as the single source of truth** for the cluster's desired state. ArgoCD continuously watches this repository and automatically applies any change to the Kubernetes cluster — including self-healing if someone manually changes something on the cluster directly.

## Architecture
Git Push -> ArgoCD detects change -> ArgoCD applies to cluster -> Cluster matches Git


## Project structure
gitops-argocd-demo/
├── app/ # Simple Flask app (source code)
│ ├── app.py
│ ├── Containerfile
│ └── requirements.txt
└── k8s-manifests/ # Desired state — what ArgoCD watches and applies
├── deployment.yaml
└── service.yaml


## Stack

- **Podman** — building the container image
- **Kind** — local Kubernetes cluster for testing
- **ArgoCD** — GitOps continuous delivery controller
- **Kubernetes** — Deployment + Service manifests

## How it works

1. The Flask app is built into a container image and loaded into the Kind cluster.
2. `k8s-manifests/` contains the Kubernetes Deployment and Service definitions.
3. An ArgoCD Application resource points at this repo's `k8s-manifests/` path, with **automatic sync** and **self-heal** enabled.
4. Any change pushed to `k8s-manifests/` (e.g. scaling replicas, updating the image tag) is automatically detected and applied to the cluster — no manual `kubectl apply` required.

## Demonstrated in practice

Scaling the app from 1 to 3 replicas by changing a single line in `deployment.yaml` and pushing to `main` — ArgoCD picked up the change and scaled the deployment automatically within its sync interval.

## Local setup (for reference)

\`\`\`bash
# Create the cluster
kind create cluster --name gitops-demo

# Build and load the app image
cd app
podman build -t gitops-demo-app:v1 -f Containerfile .
podman save -o ../gitops-app.tar localhost/gitops-demo-app:v1
kind load image-archive ../gitops-app.tar --name gitops-demo

# Install ArgoCD
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml --server-side --force-conflicts

# Access the ArgoCD UI
kubectl port-forward svc/argocd-server -n argocd 8080:443
# then open https://localhost:8080
\`\`\`

Then create an ArgoCD Application pointing at this repo's `k8s-manifests/` folder with automatic sync enabled.
