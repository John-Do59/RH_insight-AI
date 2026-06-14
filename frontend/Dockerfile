# Stage 1: Build Vue application
FROM node:22-alpine as builder

WORKDIR /app

# Install dependencies first for better caching
COPY frontend/vue-app/package*.json ./
RUN npm ci

# Copy the rest of the application
COPY frontend/vue-app/ .

# Build the application
RUN npm run build

# Stage 2: Serve with Nginx
FROM nginx:alpine

# Copy built assets from builder
COPY --from=builder /app/dist /usr/share/nginx/html

# Add custom Nginx configuration
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Nginx runs automatically
CMD ["nginx", "-g", "daemon off;"]
