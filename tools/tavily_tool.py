import os
from tavily import TavilyClient
from dotenv import load_dotenv

# Load environment variables - Tavily API key
load_dotenv()

# Fetch the API key from environment variables
api_key = os.getenv("TAVILY_API_KEY")

#initializing the client if the key exists
client = None
if api_key:
    client = TavilyClient(api_key=api_key)

def tavily_search(query):
    # Fallback check if the API key wasn't loaded properly
    if not client:
        return "Error: TAVILY_API_KEY is missing or invalid in your environment variables."

    try:
        # Getting response from the client
        response = client.search(
            query=query,
            max_results=5
        )
        
        # Safely handle empty or missing results dictionary key
        if not response or "results" not in response:
            return f"No results found for query: '{query}'"

        results = []
        for i, r in enumerate(response["results"], 1):
            title = r.get("title", "Unknown")
            url = r.get("url", "")
            snippet = r.get("content", "").strip()

            # Keep only the first 300 characters to avoid wall-of-text
            if len(snippet) > 300:
                snippet = snippet[:300].rsplit(" ", 1)[0] + "..."
                
            results.append(f"{i}. **{title}**\n   URL: {url}\n   Snippet: {snippet}")
            
        return "\n\n".join(results)

    except Exception as e:
        # Catch Tavily API errors gracefully so your LangGraph agent doesn't crash
        return f"Tavily Search API Error: {str(e)}"

