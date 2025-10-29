#!/usr/bin/env python
"""Test Google Flights MCP Server with future dates"""
import asyncio
import sys
import os
import json

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from server import get_flights_on_date, get_round_trip_flights

async def test_future_flights():
    """Test the MCP server with future flight dates"""
    
    print("=" * 70)
    print("Testing Google Flights MCP Server (Future Dates)")
    print("=" * 70)
    
    # Test 1: One-way flight search (using December 2025)
    print("\n[Test 1] One-way flight: SFO -> JFK on 2025-12-15")
    print("-" * 70)
    try:
        result1 = await get_flights_on_date(
            origin="SFO",
            destination="JFK",
            date="2025-12-15",
            adults=1,
            seat_type="economy",
            return_cheapest_only=False
        )
        result_data = json.loads(result1)
        if "error" in result_data:
            print(f"Error: {result_data['error']['message']}")
        elif "flights" in result_data:
            flights = result_data["flights"]
            print(f"✓ Found {len(flights)} flights!")
            print(f"\nTop 3 flights:")
            for i, flight in enumerate(flights[:3], 1):
                print(f"\n  Flight {i}:")
                print(f"    Airline: {flight.get('name', 'N/A')}")
                print(f"    Departure: {flight.get('departure', 'N/A')}")
                print(f"    Arrival: {flight.get('arrival', 'N/A')}")
                print(f"    Duration: {flight.get('duration', 'N/A')}")
                print(f"    Stops: {flight.get('stops', 'N/A')}")
                print(f"    Price: {flight.get('price', 'N/A')}")
        else:
            print("Unexpected result format:")
            print(result1)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 2: Round-trip flight search (using future dates)
    print("\n[Test 2] Round-trip: LAX -> NYC (2025-12-20 to 2025-12-27), cheapest only")
    print("-" * 70)
    try:
        result2 = await get_round_trip_flights(
            origin="LAX",
            destination="NYC",
            departure_date="2025-12-20",
            return_date="2025-12-27",
            adults=1,
            seat_type="economy",
            return_cheapest_only=True
        )
        result_data = json.loads(result2)
        if "error" in result_data:
            print(f"Error: {result_data['error']['message']}")
        elif "cheapest_round_trip_option" in result_data:
            flight = result_data["cheapest_round_trip_option"][0]
            print(f"✓ Found cheapest round-trip option:")
            print(f"    Airline: {flight.get('name', 'N/A')}")
            print(f"    Departure: {flight.get('departure', 'N/A')}")
            print(f"    Arrival: {flight.get('arrival', 'N/A')}")
            print(f"    Duration: {flight.get('duration', 'N/A')}")
            print(f"    Stops: {flight.get('stops', 'N/A')}")
            print(f"    Price: {flight.get('price', 'N/A')}")
        else:
            print("Unexpected result format:")
            print(result2)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 70)
    print("Testing complete!")
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(test_future_flights())
