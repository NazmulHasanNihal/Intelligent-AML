# Multi-stage production container for Intelligent-AML Frontend
FROM node:20-alpine AS build

WORKDIR /app

# Install dependencies with clean cache
COPY package.json package-lock.json* ./
RUN npm install

# Build production assets
COPY . .
RUN npm run build

# Stage 2: Serve optimized assets via high-performance Nginx
FROM nginx:alpine

COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
