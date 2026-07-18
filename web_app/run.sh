#!/bin/bash
# Run the Word Search multiplayer web app
# Usage: bash run.sh

cd "$(dirname "$0")"

echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "Starting Word Search server at http://localhost:5001"
echo "Open that URL in multiple browser tabs to play!"
echo ""
python app.py
