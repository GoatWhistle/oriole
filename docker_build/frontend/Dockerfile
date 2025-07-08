FROM node:22.1.0-alpine AS frontend

WORKDIR /frontend

COPY src/frontend/package*.json .

RUN npm install

COPY src/frontend .

RUN npm run build

FROM nginx:stable-alpine

COPY --from=frontend /frontend/dist /usr/share/nginx/html

COPY ./nginx/nginx.dev.conf /etc/nginx/nginx.dev.conf

COPY ./nginx/nginx.prod.conf /etc/nginx/nginx.prod.conf

COPY ./src/backend/nginx_conf.sh /nginx_conf.sh

RUN chmod +x /nginx_conf.sh

ENTRYPOINT ["sh", "./nginx_conf.sh"]

CMD ["nginx", "-g", "daemon off;"]
