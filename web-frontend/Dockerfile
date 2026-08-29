FROM nginx:alpine

# Copies static files to the default Nginx folder
COPY index.html /usr/share/nginx/html/
COPY src/ /usr/share/nginx/html/src/

# In a DevOps practice, we would use an nginx.conf template
# to proxy_pass /api calls to the Kubernetes backend service.

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
