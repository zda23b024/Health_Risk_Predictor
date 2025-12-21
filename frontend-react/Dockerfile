# Build stage
FROM node:18-alpine as build

WORKDIR /app

ARG REACT_APP_API_URL="http://localhost:5001"
ENV REACT_APP_API_URL=${REACT_APP_API_URL}

COPY package.json package-lock.json* ./
RUN npm install --legacy-peer-deps --no-audit --no-fund

COPY . .

RUN npm run build

# Production stage - serve static files with nginx
FROM nginx:stable-alpine

COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
