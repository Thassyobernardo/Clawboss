FROM node:22-slim

WORKDIR /app

ENV OPENCLAW_GATEWAY_MODE=local
ENV OPENCLAW_GATEWAY_FOREGROUND=true

# Install Python and dependencies for skills
RUN apt-get update && apt-get install -y python3 python3-pip python3-venv curl libpq-dev build-essential && rm -rf /var/lib/apt/lists/*

# Copy package files
COPY package.json ./

# Install dependencies
RUN npm install

# Copy application code
COPY . .

# Install Python requirements
RUN pip3 install --no-cache-dir --break-system-packages -r requirements.txt

# Make start script executable
RUN chmod +x start.sh

# Expose OpenClaw (18789) and Streamlit (8501)
EXPOSE 18789 8501

# Railway will use the port defined in $PORT, but we'll try to run both
CMD ["./start.sh"]
