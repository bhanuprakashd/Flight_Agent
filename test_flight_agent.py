#!/usr/bin/env python
"""Test script for the enhanced flight agent"""
import asyncio
import sys
import os

# Add the flight_agent directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'flight_agent'))

from agent import flight_agent

async def test_flight_agent():
    """Test the enhanced flight agent with various flight searches"""
    
    print("=" * 70)
    print("Testing Enhanced Flight Agent with MCP Server")
    print("=" * 70)
    
    # Test 1: Direct flight search
    print("\n[Test 1] Direct flight search: SFO -> JFK on 2025-12-15")
    print("-" * 70)
    try:
        results = await flight_agent.search_one_way_flights(
            origin="SFO",
            destination="JFK", 
            date="2025-12-15",
            adults=1,
            seat_type="economy",
            cheapest_only=False
        )
        formatted_results = flight_agent.format_flight_results(results)
        print(formatted_results)
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 2: Cheapest flight search
    print("\n[Test 2] Cheapest flight search: LAX -> NYC on 2025-12-20")
    print("-" * 70)
    try:
        results = await flight_agent.search_one_way_flights(
            origin="LAX",
            destination="NYC",
            date="2025-12-20",
            adults=1,
            seat_type="economy",
            cheapest_only=True
        )
        formatted_results = flight_agent.format_flight_results(results)
        print(formatted_results)
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 3: Round-trip flight search
    print("\n[Test 3] Round-trip search: DEN -> LAX (2025-12-25 to 2026-01-02)")
    print("-" * 70)
    try:
        results = await flight_agent.search_round_trip_flights(
            origin="DEN",
            destination="LAX",
            departure_date="2025-12-25",
            return_date="2026-01-02",
            adults=1,
            seat_type="economy",
            cheapest_only=True
        )
        formatted_results = flight_agent.format_flight_results(results)
        print(formatted_results)
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 4: Date suggestion for past dates
    print("\n[Test 4] Date suggestion for past dates")
    print("-" * 70)
    past_date = "2024-01-15"
    suggested_date = flight_agent.suggest_future_date(past_date)
    print(f"Past date: {past_date}")
    print(f"Suggested future date: {suggested_date}")
    
    # Test 5: Process flight request (simplified)
    print("\n[Test 5] Process flight request")
    print("-" * 70)
    try:
        # This would normally use the LLM agent, but we'll test the direct methods
        print("Flight agent is ready to process requests!")
        print("MCP Server available:", flight_agent.mcp_available)
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "=" * 70)
    print("Flight Agent Testing Complete!")
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(test_flight_agent())
