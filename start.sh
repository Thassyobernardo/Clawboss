#!/bin/bash

# Ensure config directory exists
mkdir -p /root/.openclaw/

# Force copy local project config to the location OpenClaw expects
cp openclaw.json /root/.openclaw/openclaw.json
echo "Project openclaw.json copied to /root/.openclaw/openclaw.json"

# Initialize Database
python3 db.py

# Stop any existing OpenClaw processes by port
fuser -k 18789/tcp 2>/dev/null || true

# Start OpenClaw Gateway in background
echo "Starting OpenClaw Gateway..."
# Relying on /root/.openclaw/openclaw.json already placed
npx openclaw gateway --allow-unconfigured &

# Start Streamlit Dashboard in foreground
echo "Starting Streamlit Dashboard on port ${PORT:-8501}..."
streamlit run app.py --server.port ${PORT:-8501} --server.address 0.0.0.0
