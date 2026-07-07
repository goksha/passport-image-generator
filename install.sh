#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "====== Upgrading pip ======"
pip install --upgrade pip

echo "====== Installing dependencies from requirements.txt ======"
pip install -r requirements.txt

echo "====== Installation Complete! ======"
echo "To run your app, use the following command:"
echo "streamlit run app.py"
