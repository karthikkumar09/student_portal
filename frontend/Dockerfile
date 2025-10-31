# Build stage
FROM node:18-alpine as build

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY . .

# Build the application
RUN 
# --- Added for correct backend URLs during build ---
ARG VITE_COURSE_SERVICE_URL
ARG VITE_STUDENT_SERVICE_URL
ARG VITE_ENROLLMENT_SERVICE_URL
ENV VITE_COURSE_SERVICE_URL=$VITE_COURSE_SERVICE_URL
ENV VITE_STUDENT_SERVICE_URL=$VITE_STUDENT_SERVICE_URL
ENV VITE_ENROLLMENT_SERVICE_URL=$VITE_ENROLLMENT_SERVICE_URL
# ---------------------------------------------------

RUN npm run build

# Production stage
FROM nginx:alpine

# Copy built assets from build stage
COPY --from=build /app/dist /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost/ || exit 1

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
