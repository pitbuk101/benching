# Step 1: Use a specific version of Node.js as the base image
FROM node:18.18.0

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Copy the package.json and package-lock.json (if available) to the container
COPY package*.json ./

# Step 4: Install dependencies
RUN npm install

# Step 5: Copy the rest of your application code into the container
COPY . /app

# Step 6: Expose the new port (3003)
EXPOSE 3003

# Step 7: Command to run your app
CMD ["node", "app.js"]
