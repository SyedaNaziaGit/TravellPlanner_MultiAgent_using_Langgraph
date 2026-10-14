# TravellPlanner_MultiAgent_using_Langgrap

# AI Journey Buddy 

**A multi-agent AI travel planning app built with a LangGraph backend and a Streamlit frontend.**
AI Journey Buddy a travel planning app built using streamlit frontend and langgraph backend.
Tell Journey Buddy where you want to go, and a team of specialised AI agents works together to research destinations and build a complete trip plan, shown in a clean, purple-themed web interface.

---

## Overview

Planning a trip usually means bouncing between flight sites, hotel listings, weather apps, and travel blogs. **AI Journey Buddy** brings that into one place: a LangGraph-powered multi-agent backend splits a travel request into focused tasks, each handled by an agent with its own tools, and the results are merged into a single structured plan that the Streamlit frontend presents.

## Features

- **Multi-agent planning** with LangGraph, where each agent owns one part of the trip
- **Tool-powered agents** that fetch real information instead of relying on model memory
- **Streamlit web UI** with a hero section, a floating search card, and destination cards
- **Structured trip plans** returned in a consistent response format
- **Saved travel plans** stored in the `travel_plans/` folder

<!-- VERIFY: add or remove features (flights, hotels, weather, budget, itinerary, PDF export, etc.) to match what the app really does -->

## Architecture

```
┌────────────────────┐   travel request   ┌──────────────────────────┐
│  Streamlit UI      │ ─────────────────▶ │   LangGraph Backend      │
│ (streamlit_        │                    │ (langgraph_backend.py)   │
│  frontend.py)      │                    └────────────┬─────────────┘
└────────────────────┘                                 │
          ▲                          ┌─────────────────┼─────────────────┐
          │                          ▼                 ▼                 ▼
          │                     Agent 1            Agent 2           Agent 3
          │                   (e.g. research)    (e.g. planning)   (e.g. summary)
          │                          │                 │                 │
          │                          └────── tools/ (external APIs) ─────┘
          │                                            │
          │          structured plan                   ▼
          └────────────────────────────────── travel_plans/ (saved output)
```

<!-- VERIFY: rename the agents above to match your graph nodes in langgraph_backend.py -->

**Flow:** the user submits a trip request in the UI → the LangGraph backend routes it through the agents → agents call tools for live data → the final plan follows the format defined in `response format.txt` → the UI renders the result.

## Project Structure

```
TravellPlanner_MultiAgent_using_Langgraph/
├── tools/                   # Tools the agents can call (APIs, search, etc.)
├── travel_plans/            # Generated travel plans
├── langgraph_backend.py     # Multi-agent graph: nodes, routing, and execution
├── streamlit_frontend.py    # Streamlit web interface
├── response format.txt      # Expected structure of the trip plan output
├── requirements.txt         # Python dependencies
└── README.md
```

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python |
| Agent orchestration | LangGraph, LangChain |
| LLM | <!-- VERIFY: e.g. Groq / OpenAI --> |
| External data | <!-- VERIFY: e.g. Tavily search, weather and flight APIs --> |
| Frontend | Streamlit |

## Prerequisites

- Python 3.10+
- Git
- API keys for your LLM provider and any tools used in `tools/` <!-- VERIFY: list each API with its signup link -->

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/SyedaNaziaGit/TravellPlanner_MultiAgent_using_Langgraph.git
cd TravellPlanner_MultiAgent_using_Langgraph
```

### 2. Create and activate a virtual environment

```bash
python -m venv myenv
```

Windows:

```bash
myenv\Scripts\activate
```

macOS / Linux:

```bash
source myenv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
# Replace with the keys your project actually uses
GROQ_API_KEY=your_llm_api_key
TAVILY_API_KEY=your_search_api_key
```

>  **Never commit your `.env` file or your virtual environment.** Keep both listed in `.gitignore`.

## Running the App

```bash
streamlit run streamlit_frontend.py
```

The app opens at `http://localhost:8501`.

## Example Prompts

```
Plan a 5-day trip to Goa for two people under ₹30,000.
```

```
Suggest a 7-day Japan itinerary with sightseeing, food spots, and weather tips.
```

```
I have a long weekend. Where can I go from Bengaluru for a relaxing getaway?
```

## UI looks like this:

<img width="975" height="542" alt="image" src="https://github.com/user-attachments/assets/eb399142-63ba-4f30-8198-38c0537002bf" />

<img width="975" height="388" alt="image" src="https://github.com/user-attachments/assets/1885cdc7-1c36-4dc3-9760-0bc784b9342f" />
  
<img width="975" height="417" alt="image" src="https://github.com/user-attachments/assets/e0226b24-3b2c-40ae-990b-156903e3064c" />

<img width="975" height="380" alt="image" src="https://github.com/user-attachments/assets/6e6d9deb-f499-4ceb-b05c-56a65a6abbd5" />

<img width="975" height="284" alt="image" src="https://github.com/user-attachments/assets/a86ddf93-eb95-4b23-a24e-c245cb59c382" />

<img width="975" height="435" alt="image" src="https://github.com/user-attachments/assets/c37be921-1c3c-4b1c-bf53-7a660b1f2972" />

<img width="975" height="358" alt="image" src="https://github.com/user-attachments/assets/c9c448f8-aece-48fa-9c31-4909b8fb0f49" />

##PROJECT STRUCTURE:

<img width="460" height="617" alt="image" src="https://github.com/user-attachments/assets/7b4f4978-cd8d-48f9-8cc2-04530eef7c86" />
 
#RUN STREAMLIT
streamlit run .\streamlit_frontend.py

