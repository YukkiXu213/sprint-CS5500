
# Use the Node.js base image
FROM node:20

# Set the working directory in the container
WORKDIR /app

# Copy the package files and install dependencies
COPY package*.json ./
RUN npm install

# Copy the application code
COPY . .

# Expose the application port (change as needed)
EXPOSE 3000

# Command to run the application
CMD ["npm", "start"]

