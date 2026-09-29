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

# The base image's own pinned Alpine packages lag behind their upstream
# security fixes (CI-03's Trivy scan caught two fixed CRITICAL libcrypto3/
# libssl3 CVEs here) -- apk upgrade needs root, so switch back to 101
# immediately after, restoring the base image's own non-root default.
USER root
RUN apk update && apk upgrade --no-cache
USER 101

COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx/default.conf.template /etc/nginx/templates/default.conf.template

ENV BACKEND_HOST=backend \
    BACKEND_PORT=8000

EXPOSE 8080
