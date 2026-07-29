import os
import requests
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

#Using aviation stack api for the travel to check flights
def search_flights(query):
    url = "http://api.aviationstack.com/v1/flights"
    
    #Fetch the actual key value from environment variables
    api_key = os.getenv("AVIATION_STACK_API_KEY")
    
    if not api_key:
        return "Error: AVIATION_STACK_API_KEY environment variable is not set."

    params = {
        "access_key": api_key,
        "limit": 5,
        "dep_city": query # Uses your query to filter by departure city
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status() # Raises an exception for HTTP error codes
        result = response.json()
    except requests.exceptions.RequestException as e:
        return f"API Connection Error: {e}"

    # Handling API errors returned inside a successful HTTP response
    if "error" in result:
        return f"Aviationstack Error: {result['error'].get('message')}"

    flights = []
    if "data" in result:
        for flight in result["data"]:
            airline = flight.get("airline", {}).get("name", "Unknown")
            departure = flight.get("departure", {}).get("airport", "Unknown")
            arrival = flight.get("arrival", {}).get("airport", "Unknown")
            status = flight.get("flight_status", "Unknown")

            # Cleaned up indentation using strip() for better console formatting
            flight_info = f"""
Airline: {airline}
Departure: {departure}
Arrival: {arrival}
Status: {status}
-----------------------------"""
            flights.append(flight_info)
            
    if not flights:
        return f"No active flights found departing from '{query}'."
        
    return "\n".join(flights)

