#!/bin/bash

# Alayatales Run Script
# This script runs the Streamlit application using uv

echo "🛕 Starting Alayatales Temple Management System..."
echo "================================================"
echo "☁️  Using MongoDB Atlas (Cloud Database)"
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found. Running setup first..."
    ./setup.sh
fi

# Run the application with uv
echo "🚀 Starting Streamlit application..."
uv run streamlit run app.py
