# Testing Flight Agent at https://flight-agent-519243981219.us-central1.run.app

## Service Status

**URL**: https://flight-agent-519243981219.us-central1.run.app
**Status**: Deployed and running
**Authentication**: Required (403 Forbidden without auth)
**Container Port**: 8080

## Testing Methods

### 1. **Basic Connectivity Test**

```bash
# Check if service is reachable
curl -I https://flight-agent-519243981219.us-central1.run.app

# Expected: HTTP/2 403 (authentication required)
```

### 2. **Authenticated Testing**

```bash
# Get authentication token
TOKEN=$(gcloud auth print-identity-token)

# Test with authentication
curl -H "Authorization: Bearer $TOKEN" \
     https://flight-agent-519243981219.us-central1.run.app/

# Test health endpoint (if available)
curl -H "Authorization: Bearer $TOKEN" \
     https://flight-agent-519243981219.us-central1.run.app/health
```

### 3. **Service Information**

```bash
# Get service details
gcloud run services describe flight-agent \
  --region us-central1 \
  --format "value(status.url,status.conditions[0].status)"

# Check service logs
gcloud run services logs read flight-agent \
  --region us-central1 \
  --limit 50
```

### 4. **Testing with Browser**

1. **Authenticate with Google Cloud**:
   ```bash
   gcloud auth login
   gcloud auth application-default login
   ```

2. **Open browser and navigate to**:
   ```
   https://flight-agent-519243981219.us-central1.run.app
   ```

3. **You should be redirected to Google authentication**

### 5. **Testing Agent Functionality**

Since this is a Flight Agent with MCP integration, test with flight-related queries:

```bash
# Test flight search (if API endpoint available)
curl -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query": "Find flights from New York to Los Angeles"}' \
  https://flight-agent-519243981219.us-central1.run.app/chat
```

## Expected Responses

### Without Authentication:
```html
HTTP/2 403 Forbidden
<html>
<head>
<meta http-equiv="content-type" content="text/html;charset=utf-8">
<title>403 Forbidden</title>
</head>
<body text=#000000 bgcolor=#ffffff>
<h1>Error: Forbidden</h1>
<h2>Your client does not have permission to get URL from this server.</h2>
</body>
</html>
```

### With Authentication:
- Should return agent interface or API response
- May show FastAPI documentation at `/docs`
- Health endpoint may return `{"status": "healthy"}`

## Troubleshooting

### Issue: 403 Forbidden
**Cause**: Service requires authentication
**Solution**: Use `gcloud auth print-identity-token` and include in Authorization header

### Issue: Connection timeout
**Cause**: Service may be starting up or having issues
**Solution**: Check service logs and status

### Issue: 404 Not Found
**Cause**: Endpoint doesn't exist
**Solution**: Check available endpoints at `/docs` or service logs

## Service Configuration

Based on the deployment:
- **Memory**: 4Gi (from Makefile)
- **Region**: us-central1
- **Authentication**: Required (`--no-allow-unauthenticated`)
- **CPU Throttling**: Disabled
- **Port**: 8080 (container), 443 (external)

## Available Endpoints

Check these common endpoints:

```bash
# Root endpoint
curl -H "Authorization: Bearer $TOKEN" \
     https://flight-agent-519243981219.us-central1.run.app/

# Health check
curl -H "Authorization: Bearer $TOKEN" \
     https://flight-agent-519243981219.us-central1.run.app/health

# API documentation
curl -H "Authorization: Bearer $TOKEN" \
     https://flight-agent-519243981219.us-central1.run.app/docs

# Chat endpoint (if available)
curl -H "Authorization: Bearer $TOKEN" \
     https://flight-agent-519243981219.us-central1.run.app/chat
```

## Testing Script

Create a test script:

```bash
#!/bin/bash
# test_flight_agent.sh

URL="https://flight-agent-519243981219.us-central1.run.app"
TOKEN=$(gcloud auth print-identity-token)

echo "Testing Flight Agent at $URL"
echo "================================"

echo "1. Testing connectivity..."
curl -I "$URL"

echo -e "\n2. Testing with authentication..."
curl -H "Authorization: Bearer $TOKEN" -s "$URL" | head -10

echo -e "\n3. Testing health endpoint..."
curl -H "Authorization: Bearer $TOKEN" -s "$URL/health"

echo -e "\n4. Testing docs endpoint..."
curl -H "Authorization: Bearer $TOKEN" -s "$URL/docs" | head -5

echo -e "\nTest complete!"
```

## Next Steps

1. **Verify service is running**: Check logs for any errors
2. **Test authentication**: Ensure you can access with proper auth
3. **Test agent functionality**: Try flight search queries
4. **Check MCP integration**: Verify MCP server is working
5. **Monitor performance**: Check response times and resource usage

## Service Management

```bash
# Update service (if needed)
make deploy

# Check service status
gcloud run services describe flight-agent --region us-central1

# View real-time logs
gcloud run services logs tail flight-agent --region us-central1

# Update service configuration
gcloud run services update flight-agent \
  --region us-central1 \
  --memory 8Gi \
  --timeout 360
```
