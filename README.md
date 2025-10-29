# Flight Agent with Google Flights MCP Server

A sophisticated flight search agent powered by Google ADK (Agent Development Kit) and integrated with the Google Flights MCP Server.

## Features

- ✈️ Real-time flight search using Google Flights data
- 🔍 One-way and round-trip flight searches
- 💰 Price comparison and cheapest flight finder
- 📅 Date range search capabilities
- 🗣️ Natural language conversation interface
- 🤖 Powered by Gemini 2.5 Flash model

## Requirements

- Python 3.8+
- Google Cloud project (for Vertex AI)
- Google Flights MCP Server configured
- Required Python packages (see installation)

## Installation

1. **Install dependencies:**
   ```bash
   pip install google-adk vertexai mcp
   ```

2. **Set up environment variables:**
   ```bash
   export GOOGLE_API_KEY="your-api-key"
   export GOOGLE_CLOUD_PROJECT="your-project-id"
   export GOOGLE_CLOUD_LOCATION="us-central1"
   ```

3. **Ensure Google Flights MCP Server is set up:**
   - The MCP server should be located at `Google-Flights-MCP-Server/server.py`
   - Make sure all dependencies are installed in the conda environment

## Usage

### Basic Usage

```python
from flight_agent.agent import root_agent

# Process a flight request
response = await root_agent.process("Find flights from San Francisco to New York on December 15th")
print(response)
```

### Running the Agent Engine

```python
from flight_agent.agent import startup

# Start the agent engine
app = startup()
```

## Agent Capabilities

The flight agent can handle:

1. **One-way flights**: Search for flights on specific dates
   - Example: "Find flights from SFO to JFK on December 15th"

2. **Round-trip flights**: Search for return flights
   - Example: "I need flights from LAX to NYC, departing December 20th and returning December 27th"

3. **Price comparison**: Compare multiple flight options
   - Example: "What are the cheapest flights from Denver to Miami?"

4. **Date range searches**: Find flights within a date range
   - Example: "Show me flights from Seattle to Boston between December 10th and 20th"

## Configuration

Edit `config.py` to customize:
- Model settings (temperature, model name)
- MCP timeout settings
- Logging levels
- Google Cloud project settings

## MCP Server Integration

The agent connects to the Google Flights MCP Server via stdio transport. The server provides three main tools:

1. `get_flights_on_date` - One-way flight search
2. `get_round_trip_flights` - Round-trip flight search
3. `find_all_flights_in_range` - Date range search

## Notes

- The agent automatically formats flight results into readable tables
- Past dates are automatically converted to future dates
- Airport codes are automatically converted from city names
- All responses are in natural language - no raw JSON or tool calls shown to users
