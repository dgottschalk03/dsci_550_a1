# Use a lightweight Node.js image
FROM node:20-slim

# Set working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json first (better caching for Docker builds)
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install

# Copy all remaining project files into the container
COPY . .

# Expose the Vite dev server port
EXPOSE 5173

# Start the development server
CMD ["npm", "run", "dev", "--", "--host"]