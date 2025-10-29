#!/bin/bash
# Quick Reference: Flight Agent Deployment Commands
# Complete step-by-step commands from ADK create to deployment

set -e

echo "🚀 Flight Agent Deployment - Quick Reference"
echo "=============================================="
echo ""

# Step 1: Create ADK Project
echo "Step 1: Create ADK Project"
echo "---------------------------"
echo "adk create flight-agent"
echo "cd flight-agent"
echo ""

# Step 2: Clone MCP Server
echo "Step 2: Clone MCP Server"
echo "-------------------------"
echo "git clone https://github.com/opspawn/Google-Flights-MCP-Server.git"
echo ""

# Step 3: Install MCP Dependencies
echo "Step 3: Install MCP Dependencies"
echo "----------------------------------"
echo "cd Google-Flights-MCP-Server"
echo "pip install -r requirements.txt"
echo "playwright install"
echo "cd .."
echo ""

# Step 4: Update Configuration Files
echo "Step 4: Update Configuration Files"
echo "-----------------------------------"
echo "# Edit pyproject.toml - Add MCP dependencies"
echo "# Edit Dockerfile - Add MCP server copy and Playwright install"
echo "# Create config.py - Add configuration class"
echo "# Edit flight_agent/agent.py - Add MCP integration"
echo "# Edit Makefile - Add environment variables"
echo ""

# Step 5: Set Up GCP
echo "Step 5: Set Up Google Cloud"
echo "----------------------------"
echo "gcloud config set project YOUR_PROJECT_ID"
echo "gcloud services enable run.googleapis.com"
echo "gcloud services enable cloudbuild.googleapis.com"
echo ""

# Step 6: Deploy
echo "Step 6: Deploy to Cloud Run"
echo "----------------------------"
echo "make deploy"
echo ""

# Step 7: Verify
echo "Step 7: Verify Deployment"
echo "--------------------------"
echo "# Get service URL"
echo "gcloud run services describe flight-agent --region us-central1 --format 'value(status.url)'"
echo ""
echo "# Check logs"
echo "gcloud run services logs read flight-agent --region us-central1 --limit 50"
echo ""
echo "# Access Dev UI"
echo "open https://YOUR_SERVICE_URL/dev-ui/"
echo ""

echo "✅ Complete! See COMPLETE_DEPLOYMENT_GUIDE.md for detailed instructions"
