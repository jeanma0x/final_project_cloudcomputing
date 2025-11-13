# NGINX ligero para servir un HTML estático de prueba
FROM nginx:alpine

# Elimina la configuración por defecto para usar la versión personalizada
RUN rm /etc/nginx/conf.d/default.conf

# Copiamos el index estático, la configuración SSL y los certificados
COPY ./index.html /usr/share/nginx/html/index.html
COPY ./nginx.conf /etc/nginx/nginx.conf
COPY ./certs /etc/nginx/certs

# Restringe permisos de la llave privada
RUN chmod 600 /etc/nginx/certs/selfsigned.key
