# Complete Flight Agent Deployment Guide
## From ADK Project Creation to Successful Cloud Run Deployment

This guide documents the complete process from creating a Flight Agent project using ADK to successfully deploying it to Google Cloud Run with MCP server integration.

---

## Prerequisites

```bash
# Ensure you have the following installed:
# - Python 3.10-3.13
# - Google Cloud SDK (gcloud)
# - Docker (for local testing)
# - uv package manager (installed automatically by ADK)
```

---

## Step 1: Create ADK Project

```bash
# Install ADK CLI if not already installed
pip install google-adk[cli]

# Create new agent project
adk create flight-agent

# Navigate to project directory
cd flight-agent
```

**Result**: Creates a new agent-starter-pack project structure with:
- `flight_agent/` directory
- `Dockerfile`
- `Makefile`
- `pyproject.toml`
- `.cloudbuild/` directory

---

## Step 2: Clone Google Flights MCP Server

```bash
# Clone the MCP server repository
git clone https://github.com/opspawn/Google-Flights-MCP-Server.git

# Verify MCP server files
ls -la Google-Flights-MCP-Server/
```

**Expected**: Should see `server.py` and `fast_flights/` directory

---

## Step 3: Install MCP Server Dependencies

```bash
# Navigate to MCP server directory
cd Google-Flights-MCP-Server

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install

# Return to project root
cd ..
```

**Dependencies installed**:
- `mcp>=1.2.0`
- `primp`
- `protobuf`
- `selectolax`
- `playwright`
- `nest-asyncio`

---

## Step 4: Update pyproject.toml with MCP Dependencies

Edit `pyproject.toml` and add MCP dependencies to the `dependencies` list:

```toml
dependencies = [
    "google-adk>=1.15.0,<2.0.0",
    "opentelemetry-exporter-gcp-trace>=1.9.0,<2.0.0",
    "google-cloud-logging>=3.12.0,<4.0.0",
    "google-cloud-aiplatform[evaluation]>=1.118.0,<2.0.0",
    "fastapi~=0.115.8",
    "uvicorn~=0.34.0",
    "psycopg2-binary>=2.9.10,<3.0.0",
    # MCP Server Dependencies
    "mcp>=1.2.0",
    "primp",
    "protobuf",
    "selectolax",
    "playwright",
    "nest-asyncio>=1.6.0,<2.0.0",
]
```

**Command**:
```bash
# Verify dependencies are added
grep -A 15 "dependencies = \[" pyproject.toml
```

---

## Step 5: Update Dockerfile

Edit `Dockerfile` to include MCP server files and Playwright browsers:

```dockerfile
FROM python:3.11-slim

RUN pip install --no-cache-dir uv==0.8.13

WORKDIR /code

COPY ./pyproject.toml ./README.md ./uv.lock* ./

COPY ./flight_agent ./flight_agent

# Copy MCP Server files
COPY ./Google-Flights-MCP-Server ./Google-Flights-MCP-Server

RUN uv sync --frozen

# Install Playwright browsers
RUN uv run playwright install

ARG COMMIT_SHA=""
ENV COMMIT_SHA=${COMMIT_SHA}

EXPOSE 8080

CMD ["uv", "run", "uvicorn", "flight_agent.server:app", "--host", "0.0.0.0", "--port", "8080"]
```

**Key additions**:
- `COPY ./Google-Flights-MCP-Server ./Google-Flights-MCP-Server`
- `RUN uv run playwright install`

---

## Step 6: Create/Update config.py

Create `config.py` in the project root:

```python
"""Configuration file for Flight Agent"""
import os

class config:
    """Configuration settings for Flight Agent"""
    # Google Cloud settings
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
    GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT", "")
    GOOGLE_CLOUD_LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    
    # Model settings
    MODEL_NAME = "gemini/gemini-2.5-flash"
    TEMPERATURE = 0.1
    
    # MCP settings
    MCP_TIMEOUT = 360  # 6 minutes timeout for MCP calls
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # App settings
    APP_NAME = "flight_agent_app"
```

**Command**:
```bash
# Create config file
cat > config.py << 'EOF'
[content from above]
EOF
```

---

## Step 7: Configure Agent for MCP Integration

Edit `flight_agent/agent.py`:

### 7.1 Add Imports

```python
import asyncio
import os
import logging
from pathlib import Path
from google.adk import Agent, Runner
from google.adk.models import Gemini
from google.adk.sessions import InMemorySessionService
from google.genai import types
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters
from vertexai.preview.reasoning_engines import AdkApp
from google.adk.artifacts import GcsArtifactService

# Import configuration
try:
    from config import config
except ImportError:
    # Fallback to default values
    class config:
        GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
        GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT", "")
        GOOGLE_CLOUD_LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
        MODEL_NAME = "gemini/gemini-2.5-flash"
        TEMPERATURE = 0.1
        MCP_TIMEOUT = 360
        LOG_LEVEL = "INFO"
        APP_NAME = "flight_agent_app"
```

### 7.2 Configure MCP Server Path

```python
# Get the absolute path to the Google Flights MCP Server
BASE_DIR = Path(__file__).parent.parent
MCP_SERVER_PATH = BASE_DIR / "Google-Flights-MCP-Server" / "server.py"

# Use container's Python (for Cloud Run)
import sys
PYTHON_EXECUTABLE = sys.executable
```

### 7.3 Initialize LLM with Vertex AI

```python
# Initialize LLM with configuration
# Use Vertex AI (project & location) for Cloud Run deployment
llm = Gemini(
    model="gemini-2.5-flash",
    temperature=config.TEMPERATURE,
    project=config.GOOGLE_CLOUD_PROJECT if config.GOOGLE_CLOUD_PROJECT else None,
    location=config.GOOGLE_CLOUD_LOCATION if config.GOOGLE_CLOUD_PROJECT else None,
)
```

### 7.4 Configure MCPToolset

```python
root_agent = Agent(
    model=llm,
    name='Flight_Agent',
    description="Expert flight search assistant...",
    instruction="""[Your agent instructions...]""",
    tools=[
        greeting, 
        MCPToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command=PYTHON_EXECUTABLE,
                    args=[str(MCP_SERVER_PATH)],
                ),
                timeout=config.MCP_TIMEOUT
            ),
        )
    ],
)
```

---

## Step 8: Update Makefile for Deployment

Edit `Makefile` to set environment variables:

```makefile
deploy:
	PROJECT_ID=$$(gcloud config get-value project) && \
	gcloud beta run deploy flight-agent \
		--source . \
		--memory "4Gi" \
		--project $$PROJECT_ID \
		--region "us-central1" \
		--allow-unauthenticated \
		--no-cpu-throttling \
		--labels "created-by=adk" \
		--set-env-vars \
		"COMMIT_SHA=$(shell git rev-parse HEAD 2>/dev/null || echo 'not-a-git-repo'),GOOGLE_API_KEY=YOUR_API_KEY,GOOGLE_CLOUD_PROJECT=YOUR_PROJECT_ID,GOOGLE_CLOUD_LOCATION=us-central1" \
		$(if $(IAP),--iap) \
		$(if $(PORT),--port=$(PORT))
```

**Replace**:
- `YOUR_API_KEY` with your actual Google API key
- `YOUR_PROJECT_ID` with your GCP project ID

---

## Step 9: Set Up Google Cloud Project

```bash
# Set your GCP project
gcloud config set project YOUR_PROJECT_ID

# Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com

# Verify project is set
gcloud config get-value project
```

---

## Step 10: Test Locally (Optional)

```bash
# Install dependencies locally
uv sync --dev

# Test the agent locally
make local-backend

# In another terminal, test the endpoint
curl http://localhost:8000/docs
```

---

## Step 11: Deploy to Cloud Run

```bash
# Deploy using Makefile
make deploy

# Or deploy manually
PROJECT_ID=$(gcloud config get-value project)
gcloud beta run deploy flight-agent \
  --source . \
  --memory "4Gi" \
  --project $PROJECT_ID \
  --region "us-central1" \
  --allow-unauthenticated \
  --no-cpu-throttling \
  --set-env-vars \
  "GOOGLE_API_KEY=YOUR_API_KEY,GOOGLE_CLOUD_PROJECT=$PROJECT_ID,GOOGLE_CLOUD_LOCATION=us-central1"
```

**Expected output**:
```
Building and deploying...
Service [flight-agent] revision [flight-agent-0000X-xxx] has been deployed
Service URL: https://flight-agent-XXXXX.us-central1.run.app
```

---

## Step 12: Verify Deployment

```bash
# Get service URL
gcloud run services describe flight-agent \
  --region us-central1 \
  --format "value(status.url)"

# Test service accessibility
curl -I https://YOUR_SERVICE_URL.dev-ui/

# Check service logs
gcloud run services logs read flight-agent \
  --region us-central1 \
  --limit 50

# Check service status
gcloud run services describe flight-agent \
  --region us-central1 \
  --format "value(status.conditions[0].status)"
```

---

## Step 13: Access the Flight Agent

### Dev UI Interface
```
https://YOUR_SERVICE_URL/dev-ui/
```

### API Documentation
```
https://YOUR_SERVICE_URL/docs
```

### Root Endpoint
```
https://YOUR_SERVICE_URL/
```

---

## Complete Command Sequence

Here's the complete sequence of commands from start to finish:

```bash
# 1. Create ADK project
adk create flight-agent
cd flight-agent

# 2. Clone MCP server
git clone https://github.com/opspawn/Google-Flights-MCP-Server.git

# 3. Install MCP dependencies locally (for testing)
cd Google-Flights-MCP-Server
pip install -r requirements.txt
playwright install
cd ..

# 4. Update pyproject.toml
# [Add MCP dependencies manually or via editor]

# 5. Update Dockerfile
# [Add COPY and RUN commands for MCP server]

# 6. Create config.py
# [Create config.py file]

# 7. Update flight_agent/agent.py
# [Add MCP configuration]

# 8. Update Makefile
# [Add environment variables]

# 9. Set up GCP
gcloud config set project YOUR_PROJECT_ID
gcloud services enable run.googleapis.com

# 10. Deploy
make deploy

# 11. Verify
gcloud run services describe flight-agent --region us-central1
```

---

## Environment Variables Summary

The following environment variables are configured in Cloud Run:

| Variable | Value | Purpose |
|----------|-------|---------|
| `GOOGLE_API_KEY` | Your API key | Google AI API access |
| `GOOGLE_CLOUD_PROJECT` | Your project ID | Vertex AI project |
| `GOOGLE_CLOUD_LOCATION` | us-central1 | Vertex AI region |
| `COMMIT_SHA` | Git commit hash | Version tracking |

---

## Troubleshooting

### Issue: "No module named 'fast_flights'"
**Solution**: Ensure `COPY ./Google-Flights-MCP-Server` is in Dockerfile before `RUN uv sync`

### Issue: "Missing key inputs argument"
**Solution**: Ensure `GOOGLE_CLOUD_PROJECT` and `GOOGLE_CLOUD_LOCATION` are set in Makefile

### Issue: "Playwright browsers not found"
**Solution**: Ensure `RUN uv run playwright install` is in Dockerfile after `RUN uv sync`

### Issue: "403 Forbidden"
**Solution**: Add `--allow-unauthenticated` flag in Makefile

---

## Verification Checklist

- [ ] ADK project created
- [ ] MCP server cloned
- [ ] MCP dependencies added to `pyproject.toml`
- [ ] Dockerfile updated with MCP server copy
- [ ] Playwright browsers installation added to Dockerfile
- [ ] `config.py` created
- [ ] Agent configured with MCPToolset
- [ ] Makefile updated with environment variables
- [ ] GCP project configured
- [ ] Service deployed successfully
- [ ] Service accessible via URL
- [ ] Dev UI loads without errors

---

## Success Indicators

✅ Service shows as "Ready" in Cloud Run console
✅ Dev UI accessible at `/dev-ui/`
✅ API docs accessible at `/docs`
✅ No errors in service logs
✅ Agent can interact with MCP tools
✅ Flight searches work correctly

---

## Quick Reference

**Deploy**: `make deploy`
**Logs**: `gcloud run services logs read flight-agent --region us-central1`
**Status**: `gcloud run services describe flight-agent --region us-central1`
**URL**: Available in deployment output or Cloud Console

---

**Last Updated**: Based on successful deployment configuration
**Status**: ✅ Verified Working
**Revision**: flight-agent-00005-h4c
