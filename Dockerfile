# Use the official Nginx image as the base
FROM nginx:alpine

# Copy the index.html file to the Nginx default directory
COPY index.html /usr/share/nginx/html/index.html

# Copy the Nginx configuration file
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 8080 (Fly.io's default port)
EXPOSE 8080

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]