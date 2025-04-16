#!/bin/bash

set -e
set -o pipefail

# 🌐 Set them locally for testing
REMOTE_USER="${USERNAME:-ec2-user}"
REMOTE_HOST="${REMOTE_HOST:-ec2-54-202-247-139.us-west-2.compute.amazonaws.com}"
SSH_KEY_PATH="/tmp/deploy_key"
REMOTE_APP_DIR="/home/$REMOTE_USER/app"

# 🔐 Load SSH private key from GitHub Secret or local file
if [[ -z "$SSH_PRIVATE_KEY" ]]; then
  echo "ℹ️ SSH_PRIVATE_KEY not found in env, falling back to local file ~/.ssh/aws-deploy-key.pem"
  cp ~/.ssh/aws-deploy-key.pem $SSH_KEY_PATH
else
  echo "$SSH_PRIVATE_KEY" > $SSH_KEY_PATH
fi

chmod 600 $SSH_KEY_PATH

echo "➡️ Connecting to $REMOTE_USER@$REMOTE_HOST..."

# 📦 Copy project directory to remote server
ssh -i $SSH_KEY_PATH -o StrictHostKeyChecking=no $REMOTE_USER@$REMOTE_HOST "mkdir -p $REMOTE_APP_DIR"
rsync -avz --exclude='__pycache__/' --exclude='*.pyc' -e "ssh -i $SSH_KEY_PATH -o StrictHostKeyChecking=no" ./ $REMOTE_USER@$REMOTE_HOST:$REMOTE_APP_DIR

# 🚀 Restart Docker services on remote
ssh -i $SSH_KEY_PATH -o StrictHostKeyChecking=no $REMOTE_USER@$REMOTE_HOST << EOF
  cd $REMOTE_APP_DIR/CommonAssessmentTool
  echo "🛑 Stopping previous container..."
  docker compose down || true
  echo "🚀 Starting new container..."
  docker compose up -d --build
EOF

echo "✅ Deployment complete!"
