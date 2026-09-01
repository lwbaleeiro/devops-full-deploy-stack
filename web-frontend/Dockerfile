FROM nginx:alpine

# Copies static files to the default Nginx folder
COPY index.html /usr/share/nginx/html/
COPY src/ /usr/share/nginx/html/src/

# Configura o proxy_pass para o backend
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
