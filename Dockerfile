FROM node:22-slim

WORKDIR /app

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

EXPOSE 18789

CMD ["npm", "start"]
