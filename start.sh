#!/bin/bash

# Initialize Database
python3 db.py

# Start OpenClaw Gateway in background
echo "Starting OpenClaw Gateway..."
npx openclaw gateway --allow-unconfigured &

# Start Streamlit Dashboard in foreground
echo "Starting Streamlit Dashboard..."
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
