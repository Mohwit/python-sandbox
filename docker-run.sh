#!/bin/bash

# Docker run script for Python Sandbox
# This script provides various ways to run the Docker container

set -e

IMAGE_NAME="python-sandbox"
CONTAINER_NAME="python-sandbox-container"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Python Sandbox Docker Runner${NC}"
echo "=================================="

# Function to build the image
build_image() {
    echo -e "${YELLOW}Building Docker image...${NC}"
    docker build -t $IMAGE_NAME .
    echo -e "${GREEN}✅ Image built successfully!${NC}"
}

# Function to run with default command
run_default() {
    echo -e "${YELLOW}Running with default command...${NC}"
    docker run --rm --name $CONTAINER_NAME $IMAGE_NAME
}

# Function to run with custom Python code
run_custom() {
    if [ -z "$1" ]; then
        echo -e "${RED}❌ Please provide Python code as argument${NC}"
        echo "Example: $0 custom 'print(\"Hello World\")'"
        exit 1
    fi
    echo -e "${YELLOW}Running custom Python code...${NC}"
    docker run --rm --name $CONTAINER_NAME $IMAGE_NAME deno task run "$1"
}

# Function to run interactively
run_interactive() {
    echo -e "${YELLOW}Starting interactive container...${NC}"
    docker run -it --rm --name $CONTAINER_NAME $IMAGE_NAME /bin/bash
}

# Function to run with docker-compose
run_compose() {
    echo -e "${YELLOW}Running with docker-compose...${NC}"
    docker-compose up --build
}

# Main script logic
case "$1" in
    "build")
        build_image
        ;;
    "run"|"")
        build_image
        run_default
        ;;
    "custom")
        build_image
        run_custom "$2"
        ;;
    "interactive"|"bash")
        build_image
        run_interactive
        ;;
    "compose")
        run_compose
        ;;
    "help"|"-h"|"--help")
        echo "Usage: $0 [COMMAND] [ARGS]"
        echo ""
        echo "Commands:"
        echo "  build          Build the Docker image"
        echo "  run (default)  Build and run with default Python code"
        echo "  custom <code>  Build and run with custom Python code"
        echo "  interactive    Build and run interactive bash session"
        echo "  compose        Run using docker-compose"
        echo "  help           Show this help message"
        echo ""
        echo "Examples:"
        echo "  $0 run"
        echo "  $0 custom 'import math; print(math.pi)'"
        echo "  $0 interactive"
        echo "  $0 compose"
        ;;
    *)
        echo -e "${RED}❌ Unknown command: $1${NC}"
        echo "Use '$0 help' for usage information"
        exit 1
        ;;
esac
