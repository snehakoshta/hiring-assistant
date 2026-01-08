#!/bin/bash

# Force redeploy script for AWS App Runner
echo "🔄 Force redeploying TalentScout Hiring Assistant..."

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: app.py not found. Run this script from the project root directory."
    exit 1
fi

# Add a timestamp to force rebuild
echo "# Last updated: $(date)" >> app.py

# Commit and push changes
git add .
git commit -m "Force redeploy: $(date)"
git push origin main

echo "✅ Force redeploy initiated!"
echo "📱 Check your deployment in 2-3 minutes"
echo "🌐 Your app should reflect the latest changes"