# Use the official Deno image as base (latest version that supports nodeModulesDir: "auto")
FROM denoland/deno:2.0.6

# Set working directory
WORKDIR /app

# Install Node.js and npm for package management
RUN apt-get update && apt-get install -y \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy package files first for better caching
COPY package*.json ./

# Install npm dependencies
RUN npm install

# Copy Deno configuration files
COPY deno.json ./

# Copy source code
COPY python-sandbox/ ./python-sandbox/
COPY README.md ./

# Cache Deno dependencies (this will regenerate the lockfile if needed)
RUN deno cache python-sandbox/core.ts

# Create a non-root user for security
RUN useradd -m -s /bin/bash sandbox
USER sandbox

# Expose port (if needed for future web interface)
EXPOSE 8000

# Default command - run the sandbox with a simple test
CMD ["deno", "task", "run", "print('Hello from Docker!')"]
