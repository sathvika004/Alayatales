#!/bin/bash

# MongoDB Installation Helper Script for macOS
# This script helps install MongoDB Community Edition

echo "🔧 MongoDB Installation Helper"
echo "=============================="
echo ""

# Detect system architecture
ARCH=$(uname -m)
echo "System Architecture: $ARCH"

if [[ "$ARCH" == "arm64" ]]; then
    echo "📱 Detected Apple Silicon (M1/M2/M3) Mac"
    MONGODB_URL="https://fastdl.mongodb.org/osx/mongodb-macos-arm64-7.0.5.tgz"
else
    echo "💻 Detected Intel Mac"
    MONGODB_URL="https://fastdl.mongodb.org/osx/mongodb-macos-x86_64-7.0.5.tgz"
fi

echo ""
echo "Options for installing MongoDB:"
echo ""
echo "1. RECOMMENDED: Install via Homebrew (requires admin permissions)"
echo "   Run these commands:"
echo "   brew tap mongodb/brew"
echo "   brew install mongodb-community"
echo "   brew services start mongodb-community"
echo ""
echo "2. Manual Installation (no admin required)"
echo "   a) Download MongoDB from: $MONGODB_URL"
echo "   b) Extract the archive"
echo "   c) Create data directory: mkdir -p ~/mongodb/data"
echo "   d) Run MongoDB: /path/to/mongodb/bin/mongod --dbpath ~/mongodb/data"
echo ""
echo "3. Download MongoDB Compass (GUI) from:"
echo "   https://www.mongodb.com/products/compass"
echo ""

# Ask if user wants to create local MongoDB directories
read -p "Would you like to create local MongoDB directories? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    mkdir -p ~/mongodb/data
    mkdir -p ~/mongodb/logs
    echo "✅ Created directories:"
    echo "   Data: ~/mongodb/data"
    echo "   Logs: ~/mongodb/logs"
    echo ""
    echo "To run MongoDB manually (after downloading):"
    echo "   mongod --dbpath ~/mongodb/data --logpath ~/mongodb/logs/mongod.log"
fi

echo ""
echo "📝 Quick Start Guide:"
echo "1. Install MongoDB using one of the methods above"
echo "2. Start MongoDB service"
echo "3. Run ./setup.sh to set up the project"
echo "4. Run ./run.sh to start the application"
