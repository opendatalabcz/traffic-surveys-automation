FROM node:alpine as build

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm clean-install --silent

COPY . ./

RUN npm run build

FROM nginx:stable-alpine as release

WORKDIR /usr/share/nginx/html

RUN apk add --update nodejs &&\
    apk add --update npm &&\
    npm install -g runtime-env-cra@0.2.4

COPY --from=build /app/build .
COPY --from=build /app/.env.example ./.env

ENTRYPOINT ["/bin/sh", "-c", "runtime-env-cra && nginx -g \"daemon off;\""]

EXPOSE 80
