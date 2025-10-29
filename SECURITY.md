# Security Guidelines

## API Keys and Secrets

**IMPORTANT**: Never commit API keys or secrets to the repository.

### Environment Variables

Set your API keys as environment variables:

```bash
# Set your Google API key
export GOOGLE_API_KEY="your_actual_api_key_here"

# Set your GCP project
export GOOGLE_CLOUD_PROJECT="your_project_id_here"

# Set location
export GOOGLE_CLOUD_LOCATION="us-central1"
```

### Using .env file (Local Development)

1. Copy the example file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your actual values:
   ```bash
   GOOGLE_API_KEY=your_actual_api_key_here
   GOOGLE_CLOUD_PROJECT=your_project_id_here
   GOOGLE_CLOUD_LOCATION=us-central1
   ```

### Cloud Run Deployment

For Cloud Run deployment, set environment variables:

```bash
# Deploy with environment variables
GOOGLE_API_KEY="your_key" make deploy
```

### GitHub Secrets (CI/CD)

If using GitHub Actions, add secrets in repository settings:
- `GOOGLE_API_KEY`
- `GOOGLE_CLOUD_PROJECT`
- `GOOGLE_CLOUD_LOCATION`

## Files to Never Commit

- `.env`
- `.env.local`
- `*.env`
- Any file containing API keys
- Service account JSON files

## Verification

Before pushing to GitHub, verify no secrets are included:

```bash
# Check for API keys
grep -r "AIzaSy" . --exclude-dir=.git --exclude-dir=.venv

# Check for other common secrets
grep -r "sk-" . --exclude-dir=.git --exclude-dir=.venv
grep -r "Bearer " . --exclude-dir=.git --exclude-dir=.venv
```
