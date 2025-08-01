# My Node.js Application

This is a simple Node.js application running inside a Docker container.

## Prerequisites

Before running the application, make sure you have the following installed:

- **Docker**: [Docker Installation Guide](https://docs.docker.com/get-docker/)
- **Node.js** (for local development): [Node.js Download](https://nodejs.org/)

## Setup Instructions

### 1. Clone the repository (if you haven't already)

```bash
git clone repo
cd market-radar

docker build -t market-radar-app .
docker run -p 3003:3003 market-radar-app



