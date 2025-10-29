# Flight Agent

A flight search assistant powered by Google's Agent Development Kit (ADK) with MCP server integration for real-time flight data.

## About Agent-Starter-Pack

This project is built using [Google's Agent Development Kit (ADK) Starter Pack](https://github.com/GoogleCloudPlatform/agent-starter-pack), which provides:

### 🚀 **Rapid Development Framework**
- **Pre-configured infrastructure**: Terraform configurations for Google Cloud
- **CI/CD pipelines**: Automated deployment with Cloud Build
- **Production-ready setup**: Monitoring, logging, and security built-in
- **Best practices**: Following Google Cloud's recommended patterns

### 🛠️ **Key Benefits of Agent-Starter-Pack**

1. **Faster Time-to-Market**
   - Skip weeks of infrastructure setup
   - Focus on your agent's business logic
   - Pre-built deployment pipelines

2. **Production-Ready Architecture**
   - Cloud Run for scalable deployment
   - Vertex AI integration
   - Cloud Logging and Monitoring
   - IAM and security configurations

3. **Developer Experience**
   - Local development environment
   - Hot-reload capabilities
   - Comprehensive testing framework
   - Documentation templates

4. **Enterprise Features**
   - Terraform infrastructure as code
   - Multi-environment support (dev/staging/prod)
   - Load testing integration
   - Security scanning

### 📁 **Starter Pack Structure**

```
flight-agent/
├── flight_agent/          # Your agent code
├── deployment/            # Terraform infrastructure
├── .cloudbuild/          # CI/CD pipelines
├── tests/                # Testing framework
├── notebooks/            # Development notebooks
├── Dockerfile            # Container configuration
├── Makefile             # Build and deploy commands
└── pyproject.toml       # Dependencies and configuration
```

## Flight Agent Features

- **Real-time flight search** using Google Flights data via MCP server
- **Natural language conversation** interface
- **MCP (Model Context Protocol) integration** for external data sources
- **Cloud Run deployment** with automatic scaling
- **Vertex AI powered** responses with Gemini model
- **Playwright integration** for web scraping capabilities

## Quick Start

### Prerequisites
- Google Cloud SDK
- Python 3.10-3.13
- Docker (for local testing)

### 1. Clone and Setup
```bash
git clone https://github.com/bhanuprakashd/Flight_Agent.git
cd Flight_Agent
```

### 2. Deploy to Cloud Run
```bash
# Set your GCP project
gcloud config set project YOUR_PROJECT_ID

# Deploy
make deploy
```

### 3. Access Your Agent
- **Dev UI**: https://your-service-url/dev-ui/
- **API Docs**: https://your-service-url/docs

## Documentation

- **[Complete Deployment Guide](COMPLETE_DEPLOYMENT_GUIDE.md)** - Step-by-step setup from scratch
- **[Testing Guide](TESTING_GUIDE.md)** - How to test and verify deployment
- **[Quick Reference](QUICK_REFERENCE.sh)** - Essential commands

## Architecture

### Agent-Starter-Pack Components

| Component | Purpose | Technology |
|-----------|---------|------------|
| **Agent Engine** | Core agent logic | Google ADK |
| **MCP Server** | External data integration | Model Context Protocol |
| **Web Interface** | User interaction | FastAPI + Dev UI |
| **Infrastructure** | Cloud deployment | Terraform + Cloud Run |
| **CI/CD** | Automated deployment | Cloud Build |
| **Monitoring** | Observability | Cloud Logging + Tracing |

### MCP Integration

This agent extends the starter pack with:
- **Google Flights MCP Server** for real-time flight data
- **Playwright integration** for web scraping
- **Custom flight search tools** via MCP protocol

## Development

### Local Development
```bash
# Install dependencies
make install

# Run locally
make local-backend

# Access at http://localhost:8000
```

### Testing
```bash
# Run tests
make test

# Code quality checks
make lint
```

## Deployment

The agent-starter-pack provides multiple deployment options:

### 1. Quick Deploy (Recommended)
```bash
make deploy
```

### 2. CI/CD Pipeline
```bash
# Trigger Cloud Build
gcloud builds submit --config .cloudbuild/staging.yaml
```

### 3. Infrastructure Setup
```bash
# Set up development environment
make setup-dev-env
```

## Why Agent-Starter-Pack?

### Without Starter Pack
- ❌ Weeks of infrastructure setup
- ❌ Manual CI/CD configuration
- ❌ Security and monitoring setup
- ❌ Deployment complexity
- ❌ No standardized patterns

### With Agent-Starter-Pack
- ✅ **Minutes to deploy** instead of weeks
- ✅ **Production-ready** from day one
- ✅ **Best practices** built-in
- ✅ **Scalable architecture** out of the box
- ✅ **Focus on your agent** not infrastructure

## Contributing

This project follows agent-starter-pack conventions:
- Use the provided testing framework
- Follow the established CI/CD patterns
- Maintain infrastructure as code with Terraform
- Document changes in the deployment guide

## Learn More

- [Agent Development Kit Documentation](https://googlecloudplatform.github.io/agent-starter-pack/)
- [Google Cloud AI Platform](https://cloud.google.com/vertex-ai)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Agent Starter Pack Repository](https://github.com/GoogleCloudPlatform/agent-starter-pack)

## License

This project is built on the agent-starter-pack framework and follows Google Cloud's open source guidelines.