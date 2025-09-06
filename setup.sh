#!/bin/bash

# Alayatales Setup Script
# This script sets up the development environment using uv

echo "🛕 Setting up Alayatales Temple Management System..."
echo "================================================"

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ uv is not installed. Please install it first:"
    echo "   curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Create virtual environment with uv
echo "📦 Creating virtual environment..."
uv venv --python 3.9

# Sync dependencies from pyproject.toml
echo "📚 Installing dependencies..."
uv sync

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cat > .env << EOL
# MongoDB Configuration
MONGODB_URI=mongodb://localhost:27017/
DB_NAME=alayatales

# Application Configuration
SECRET_KEY=your-secret-key-change-this-in-production
DEBUG=True

# Server Configuration
HOST=localhost
PORT=8501

# Admin User Configuration (for initial setup)
ADMIN_EMAIL=admin@alayatales.com
ADMIN_PASSWORD=admin123

# File Upload Settings
MAX_UPLOAD_SIZE=10485760  # 10MB in bytes
ALLOWED_EXTENSIONS=jpg,jpeg,png,gif,webp

# Session Configuration
SESSION_EXPIRE_MINUTES=60
EOL
    echo "✅ .env file created. Please update it with your settings."
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "⚠️  IMPORTANT: MongoDB must be installed and running"
echo ""
echo "To install MongoDB on macOS:"
echo "1. Download MongoDB Community Edition from:"
echo "   https://www.mongodb.com/try/download/community"
echo ""
echo "2. Or install using Homebrew (if you have permissions):"
echo "   brew tap mongodb/brew"
echo "   brew install mongodb-community"
echo "   brew services start mongodb-community"
echo ""
echo "To run the application:"
echo "   ./run.sh"
echo ""
