# Build stage
FROM node:20-alpine as build-stage

WORKDIR /app

COPY frontend/vue-app/package*.json ./
RUN npm install

COPY frontend/vue-app/ ./
RUN npm run build

# Production stage
FROM nginx:stable-alpine as production-stage

COPY --from=build-stage /app/dist /usr/share/nginx/html

# Add custom nginx config if needed (for SPA routing)
RUN echo 'server { \
    listen 80; \
    location / { \
        root /usr/share/nginx/html; \
        index index.html; \
        try_files $uri $uri/ /index.html; \
    } \
}' > /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
