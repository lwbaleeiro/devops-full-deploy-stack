# Web Frontend

Simple SPA (Single Page Application) using Vanilla JS, HTML, and CSS focused on performance and deployment simplicity.

It serves as the interface for users to interact with Events.

## Deploy
This application is containerized using `nginx:alpine` and distributed across the cluster.

In a Kubernetes environment with ArgoCD, the Ingress Controller (or `nginx.conf` itself) would be responsible for routing calls from `/api` to the `web-backend` pod, avoiding CORS issues and keeping the architecture clean.

## Docker
```bash
docker build -t web-frontend .
docker run -p 8080:80 web-frontend
```
