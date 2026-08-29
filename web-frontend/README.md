# Web Frontend

Aplicação SPA (Single Page Application) simples utilizando Vanilla JS, HTML e CSS focado em performance e simplicidade de implantação.

Serve como interface para os usuários interagirem com os Eventos.

## Deploy
Esta aplicação é containerizada utilizando `nginx:alpine` e distribuída pelo cluster.

Em um ambiente Kubernetes com ArgoCD, o Ingress Controller (ou o próprio nginx.conf) ficaria responsável por rotear chamadas de `/api` para o pod do `web-backend`, evitando problemas de CORS e mantendo a arquitetura limpa.

## Docker
```bash
docker build -t web-frontend .
docker run -p 8080:80 web-frontend
```
