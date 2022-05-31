FROM timbru31/node-alpine-git as builder

RUN git clone https://github.com/kkvotinova/mentiRu
WORKDIR mentiRu
RUN npm i && \
    npm i typescript@4.6.2

RUN npm run build:prod --output-path=/dist

FROM nginx:alpine

COPY ./ /etc/nginx
COPY --from=builder mentiRu/dist /usr/share/nginx/html

EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]