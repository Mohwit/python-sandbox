# Docker Setup for Python Sandbox

This document explains how to run the Python Sandbox in a Docker container for isolation and portability.

## Prerequisites

1. **Install Docker Desktop**: Download from [docker.com](https://www.docker.com/products/docker-desktop/)
2. **Start Docker**: Make sure Docker Desktop is running (you should see the Docker icon in your system tray)

## Quick Start

### Option 1: Using the Helper Script (Recommended)

```bash
# Make the script executable (if not already done)
chmod +x docker-run.sh

# Build and run with default code
./docker-run.sh run

# Run with custom Python code
./docker-run.sh custom "import math; print(f'Pi = {math.pi}')"

# Start an interactive bash session
./docker-run.sh interactive

# Get help
./docker-run.sh help
```

### Option 2: Direct Docker Commands

```bash
# Build the image
docker build -t python-sandbox .

# Run with default code
docker run --rm python-sandbox

# Run with custom Python code
docker run --rm python-sandbox deno task run "print('Hello from Docker!')"

# Run interactively
docker run -it --rm python-sandbox /bin/bash
```

### Option 3: Using Docker Compose

```bash
# Build and run
docker-compose up --build

# Run in background
docker-compose up -d --build

# Stop
docker-compose down
```

## Docker Image Details

- **Base Image**: `denoland/deno:2.0.6`
- **Additional Software**: Node.js 18.x, npm
- **Working Directory**: `/app`
- **User**: `sandbox` (non-root for security)
- **Exposed Port**: 8000 (for future web interface)

## Security Features

- **Non-root user**: Container runs as `sandbox` user
- **Resource limits**: Memory and CPU limits in docker-compose
- **Read-only filesystem**: Can be enabled for extra security
- **No new privileges**: Security option enabled

## Development Mode

To develop with live code changes, uncomment the volume mount in `docker-compose.yml`:

```yaml
volumes:
  - ./python-sandbox:/app/python-sandbox:ro
```

This mounts your local source code as read-only in the container.

## Troubleshooting

### Docker Daemon Not Running

```
ERROR: Cannot connect to the Docker daemon
```

**Solution**: Start Docker Desktop application

### Permission Denied

```
docker: permission denied
```

**Solution**:

- On macOS/Windows: Make sure Docker Desktop is running
- On Linux: Add your user to the docker group: `sudo usermod -aG docker $USER`

### Build Fails

```
Error during build
```

**Solution**:

1. Check internet connection (needed to download base images)
2. Make sure Docker has enough disk space
3. Try `docker system prune` to clean up old images

## File Structure

```
.
├── Dockerfile              # Main Docker configuration
├── docker-compose.yml      # Docker Compose configuration
├── docker-run.sh          # Helper script for common operations
├── .dockerignore          # Files to exclude from Docker context
└── DOCKER.md              # This documentation
```

## Examples

### Running Different Python Code

```bash
# Math calculations
./docker-run.sh custom "import math; print(f'Square root of 16: {math.sqrt(16)}')"

# Data processing
./docker-run.sh custom "data = [1,2,3,4,5]; print(f'Sum: {sum(data)}, Avg: {sum(data)/len(data)}')"

# File operations (within container)
./docker-run.sh custom "import os; print(f'Current directory: {os.getcwd()}')"
```

### Interactive Development

```bash
# Start interactive session
./docker-run.sh interactive

# Inside the container:
deno task run "print('Testing inside container')"
python3 python-sandbox/sandbox.py
```

## Next Steps

- Add web interface (port 8000 is already exposed)
- Implement API endpoints for remote code execution
- Add more security restrictions
- Set up container orchestration for scaling
