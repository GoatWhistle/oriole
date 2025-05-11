FROM node:22.1.0-alpine AS frontend

WORKDIR /frontend

COPY src/frontend .

RUN npm install
RUN ls -la
RUN npm run build


FROM nginx:stable-alpine

COPY --from=frontend /frontend/dist /usr/share/nginx/html

COPY ./default.conf /etc/nginx/conf.d/default.conf

CMD ["nginx", "-g", "daemon off;"]