# syntax=docker/dockerfile:1
FROM node:22.20.0-alpine AS builder

WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm ci

COPY . .
RUN npm run build

# nginx-unprivileged: listens on 8080 and runs as uid 101 by default, so no
# extra USER/chown work is needed here to satisfy G1's non-root requirement.
FROM nginxinc/nginx-unprivileged:1.27-alpine

COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx/default.conf.template /etc/nginx/templates/default.conf.template

ENV BACKEND_HOST=backend \
    BACKEND_PORT=8000

EXPOSE 8080
