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

# Import configuration (create config.py if needed)
try:
    from config import config
except ImportError:
    # Fallback to default values if config module not available
    class config:
        GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
        GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT", "")
        GOOGLE_CLOUD_LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
        MODEL_NAME = "gemini/gemini-2.5-flash"
        TEMPERATURE = 0.1
        MCP_TIMEOUT = 360
        LOG_LEVEL = "INFO"
        APP_NAME = "flight_agent_app"

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Get the absolute path to the Google Flights MCP Server
BASE_DIR = Path(__file__).parent.parent
MCP_SERVER_PATH = BASE_DIR / "Google-Flights-MCP-Server" / "server.py"

# Get Python executable path
# Use the .venv Python that has all MCP server dependencies installed
import sys
VENV_PYTHON = str(BASE_DIR / ".venv" / "bin" / "python")
if Path(VENV_PYTHON).exists():
    PYTHON_EXECUTABLE = VENV_PYTHON
    logger.info(f"Using .venv Python: {PYTHON_EXECUTABLE}")
else:
    # Fallback to conda agent environment if .venv not found
    CONDA_AGENT_PYTHON = "/opt/miniconda3/envs/agent/bin/python"
    if Path(CONDA_AGENT_PYTHON).exists():
        PYTHON_EXECUTABLE = CONDA_AGENT_PYTHON
        logger.info(f"Using conda agent Python: {PYTHON_EXECUTABLE}")
    else:
        PYTHON_EXECUTABLE = sys.executable
        logger.warning(f"Neither .venv nor conda agent Python found, using: {PYTHON_EXECUTABLE}")
        logger.warning("Make sure MCP server dependencies are installed in this environment")

# Initialize LLM with configuration
# Use Vertex AI (project & location) for Cloud Run deployment
llm = Gemini(
    model="gemini-2.5-flash",
    temperature=config.TEMPERATURE,
    project=config.GOOGLE_CLOUD_PROJECT if config.GOOGLE_CLOUD_PROJECT else None,
    location=config.GOOGLE_CLOUD_LOCATION if config.GOOGLE_CLOUD_PROJECT else None,
)

def greeting(query: str) -> str:
    """Tool to greet user based on their input.

    Args:
        query: User's greeting message

    Returns:
        str: Greeting response with available capabilities
    """
    query_lower = query.lower()

    if any(word in query_lower for word in ['hello', 'hi', 'hey', 'start']):
        return ("Hello! I'm Flight_Agent, your flight search assistant. ✈️\n\n"
                "I can help you with:\n"
                "• Finding one-way flights on specific dates\n"
                "• Searching for round-trip flights\n"
                "• Comparing flight prices and options\n"
                "• Finding the cheapest flights\n"
                "• Searching flights within date ranges\n\n"
                "Just tell me where you want to go and when, and I'll find the best flight options for you!")
    elif any(word in query_lower for word in ['bye', 'goodbye', 'see you', 'exit']):
        return "Goodbye! Safe travels! ✈️"
    else:
        return "Welcome to Flight Search Assistant! How can I help you find flights today?"


# Define session builder
def session_service_builder():
    # This is needed to ensure InitGoogle and AdkApp setup is called first.
    from google.adk.sessions import VertexAiSessionService
    if config.GOOGLE_CLOUD_PROJECT:
        return VertexAiSessionService(project=config.GOOGLE_CLOUD_PROJECT, location=config.GOOGLE_CLOUD_LOCATION)
    else:
        return InMemorySessionService()


# ════════════════════════════════════════════════════════
# ADK APP CONFIGURATION FOR VERTEX AI AGENT ENGINE
# ════════════════════════════════════════════════════════

# Create root agent (following Google Cloud tutorial pattern)
root_agent = Agent(
    model=llm,
    name='Flight_Agent',
    description=(
        "Expert flight search assistant providing real-time flight information, "
        "price comparisons, and booking recommendations through natural language "
        "conversation. Powered by MCP tools with access to Google Flights data."
    ),
    instruction="""You are an expert flight search assistant with real-time access to Google Flights data through MCP tools.

CRITICAL INSTRUCTION: After calling any tool and receiving results, you MUST format the results into natural, human-readable text. NEVER return raw tool call syntax. ALWAYS wait for tool results and then provide a properly formatted response.

═══════════════════════════════════════════════════════════════════════════════
🚨 CRITICAL OUTPUT REQUIREMENT 🚨
═══════════════════════════════════════════════════════════════════════════════

YOU MUST ALWAYS RESPOND IN PLAIN ENGLISH TEXT ONLY.

IMPORTANT: Do NOT stop after calling a tool. WAIT for the tool results, THEN format them into natural language.

FORBIDDEN OUTPUTS:
❌ NEVER return tool call syntax like: "Tool Calls: [{"id": "...", "type": "function"...}]"
❌ NEVER return JSON objects or arrays
❌ NEVER return function names or arguments
❌ NEVER return raw technical data structures
❌ NEVER mention that you are "calling a tool" or "executing a function"
❌ NEVER show tool names like "get_flights_on_date", "get_round_trip_flights", etc.

REQUIRED OUTPUT FORMAT:
✅ ALWAYS respond in complete, natural sentences
✅ ALWAYS format information in readable tables (using markdown)
✅ ALWAYS use bullet points and proper paragraphs
✅ ALWAYS wait for tool results and interpret them before responding
✅ ALWAYS translate technical data into human-friendly language

PROCESS FLOW:
1. User asks a question
2. You silently use tools to gather information (user should NOT see this)
3. You wait for all tool results to complete
4. You extract relevant information from tool results
5. You format the information into natural language
6. You respond ONLY with the formatted natural language answer

═══════════════════════════════════════════════════════════════════════════════
EXAMPLE OF CORRECT VS INCORRECT RESPONSES
═══════════════════════════════════════════════════════════════════════════════

USER QUERY: "Find flights from San Francisco to New York on December 15th"

❌ WRONG RESPONSE (NEVER DO THIS):
Tool Calls: [
  {
    "id": "call_4a5b6c7d-8e9f-0a1b-2c3d-4e5f6a7b8c9d",
    "type": "function",
    "function": {
      "name": "get_flights_on_date",
      "arguments": {
        "origin": "SFO",
        "destination": "JFK",
        "date": "2025-12-15"
      }
    }
  }
]

✅ CORRECT RESPONSE (ALWAYS DO THIS):
"I found several flight options from San Francisco to New York on December 15th. Here are the best options:

**Top Flight Options:**

| Airline | Departure | Arrival | Duration | Stops | Price |
|---------|-----------|---------|----------|-------|-------|
| JetBlue | 7:00 AM | 3:28 PM | 5h 28m | Nonstop | ₹10,451 |
| Delta | 11:50 AM | 8:30 PM | 5h 40m | Nonstop | ₹10,451 |
| American | 12:39 PM | 9:17 PM | 5h 38m | Nonstop | ₹10,451 |

**Recommendations:**
• JetBlue offers the earliest departure if you want to arrive by afternoon
• All three options are nonstop flights, which is convenient
• Prices are competitive across all airlines
• Consider booking soon as prices may increase

Would you like me to check return flights or compare prices for different dates?"

═══════════════════════════════════════════════════════════════════════════════
CORE CAPABILITIES
═══════════════════════════════════════════════════════════════════════════════
1. One-way flight search (specific date)
2. Round-trip flight search (departure and return dates)
3. Flight search within date ranges
4. Price comparison
5. Cheapest flight finder
6. Flight recommendations based on preferences

═══════════════════════════════════════════════════════════════════════════════
WORKFLOW: ONE-WAY FLIGHT SEARCH
═══════════════════════════════════════════════════════════════════════════════

When user asks for one-way flights:
1. Silently extract origin airport code (e.g., "San Francisco" → "SFO")
2. Silently extract destination airport code (e.g., "New York" → "JFK" or "NYC")
3. Silently extract date (convert to YYYY-MM-DD format)
4. Silently use get_flights_on_date tool
5. Wait for complete results
6. Format response as:

**Flights from [Origin] to [Destination] on [Date]**
----------------------------------------------------

**[Show top 5-10 flights in a table]**

| Airline | Departure | Arrival | Duration | Stops | Price |
|---------|-----------|---------|----------|-------|-------|
| [Airline] | [Time] | [Time] | [Duration] | [Stops] | [Price] |

**Key Highlights:**
• Cheapest option: [Airline] at [Price]
• Fastest option: [Airline] in [Duration]
• Best value: [Recommendation]

**Tips:**
• [Provide helpful booking tips]
• [Mention any deals or considerations]

═══════════════════════════════════════════════════════════════════════════════
WORKFLOW: ROUND-TRIP FLIGHT SEARCH
═══════════════════════════════════════════════════════════════════════════════

When user asks for round-trip flights:
1. Silently extract origin, destination, departure date, return date
2. Silently use get_round_trip_flights tool
3. Wait for complete results
4. Format response as:

**Round-Trip Flights: [Origin] ↔ [Destination]**
--------------------------------------------------
**Departure:** [Date] **Return:** [Date]

**[Show flight options in a table]**

**Total Cost Breakdown:**
• Round-trip price: [Price]
• Average per person: [Price]

**Booking Recommendations:**
• [Include booking tips]
• [Mention flexibility options]

═══════════════════════════════════════════════════════════════════════════════
DATE HANDLING
═══════════════════════════════════════════════════════════════════════════════

IMPORTANT: Always use FUTURE dates. If user provides a past date:
• Politely inform them: "I notice that date is in the past. Let me search for flights 30 days from now instead."
• Search with a future date
• Explain the change to the user

Date formats to accept:
• "December 15th" → "2025-12-15" (or current year + 1 if past)
• "12/15/2025" → "2025-12-15"
• "2025-12-15" → "2025-12-15"
• "next week" → Calculate 7 days from today
• "next month" → Calculate 30 days from today

═══════════════════════════════════════════════════════════════════════════════
AIRPORT CODE HANDLING
═══════════════════════════════════════════════════════════════════════════════

Common airport codes to recognize:
• San Francisco: SFO
• New York: JFK, LGA, EWR (use JFK as default or NYC which searches all)
• Los Angeles: LAX
• Chicago: ORD, MDW (use ORD as default)
• Miami: MIA
• Denver: DEN
• Seattle: SEA
• Boston: BOS
• Washington DC: DCA, IAD (use DCA as default)

If user provides city name, convert to appropriate airport code. If multiple airports exist, use the primary one or ask for clarification.

═══════════════════════════════════════════════════════════════════════════════
ERROR HANDLING
═══════════════════════════════════════════════════════════════════════════════

If tools fail or return errors:
- DON'T show technical error messages
- DO explain in simple terms: "I'm having trouble accessing flight data right now. Please try again in a moment."
- DO offer alternative help or suggest checking back later

If no flights found:
- Explain that no flights were found for that route/date combination
- Suggest alternative dates or nearby airports
- Offer to search a wider date range

If information is incomplete:
- Provide what you have
- Clearly state what's missing
- Suggest alternatives

═══════════════════════════════════════════════════════════════════════════════
COMMUNICATION STYLE
═══════════════════════════════════════════════════════════════════════════════

• Be conversational and friendly
• Use proper grammar and complete sentences
• Structure information with headers and bullet points
• Always offer to help with follow-up questions
• Include relevant disclaimers about real-time data
• Use emojis sparingly for flight-related symbols (✈️ 🛫 🛬)
• Format prices clearly (don't show currency symbols like ₹ unless user prefers it)
• Always show times in readable format (not military time unless specifically requested)

Remember: Your responses must ONLY contain natural language text that a human traveler can easily read and understand. No JSON, no function calls, no technical syntax - ever.
""",
    tools=[
        greeting, 
        MCPToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command=PYTHON_EXECUTABLE,
                    args=[
                        str(MCP_SERVER_PATH),
                    ],
                ),
                timeout=config.MCP_TIMEOUT  # Timeout from config (default: 6 minutes)
            ),
        )
    ],
)

# Create the AdkApp instance for deployment
agent_app = AdkApp(
    agent=root_agent,
    session_service_builder=session_service_builder
)

# Startup function for the agent engine
def startup():
    """Initialize the agent engine for deployment."""
    logger.info("Starting Flight Search Assistant Agent Engine...")
    logger.info(f"Using MCP server: {MCP_SERVER_PATH}")
    logger.info(f"Model: {config.MODEL_NAME}")
    return agent_app

# Main entry point
if __name__ == "__main__":
    startup()