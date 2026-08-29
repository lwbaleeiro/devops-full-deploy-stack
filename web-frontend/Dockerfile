FROM nginx:alpine

# Copia os arquivos estáticos para a pasta padrão do Nginx
COPY index.html /usr/share/nginx/html/
COPY src/ /usr/share/nginx/html/src/

# Na prática de DevOps, usaríamos um template de nginx.conf
# para fazer o proxy_pass para o /api bater no serviço do backend Kubernetes.

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
