import os
from typing  import TypedDict, Annotated
import psycopg

from langgraph.graph import StateGraph,START,END
from langgraph.checkpoint.postgres import PostgresSaver
from langchain_core.messages import AnyMessage,SystemMessage,AIMessage,HumanMessage
from langchain_groq import ChatGroq
from langgraph.graph.message import  add_messages

from tools.tavily_tool import tavily_search
from tools.flight_tool import search_flights

from dotenv import load_dotenv

#----------------------------------ENV VARS ----------------------------------
load_dotenv()

DB_URL = os.getenv("DATABASE_URL")

#----------------------------------- LLM ---------------------------------------

llm = ChatGroq(model = "llama-3.3-70b-versatile") #defining a LLM using llama

#------------------------------------- LANGGRAPH----------------------------------
#defining Travel State 

class TravelState(TypedDict):
    messages : Annotated[list[AnyMessage],add_messages]
    user_query : str
    flight_results : str
    hotel_results : str
    itinerary : str
    
#------------------------------- GRAPH NODES -------------------------------
    
#flight node to get the state and results using tools
def flight_agent(state:TravelState):
    user_query = state["user_query"]
    #get flight data from tools to search flight using aviation stack 
    result = search_flights(user_query)
    return {
        "flight_results": result,
        "messages": [AIMessage(content=f"Flight results were fetched")]
    }

#Hotel agent tp  get the data for hotels using tavily search from the internet
def hotel_agent(state:TravelState):
    user_query = f"Best Hotels for {state["user_query"]}"
    result = tavily_search(user_query)
    return {
        "hotel_results": result,
        "messages" : [AIMessage(content="Hotel Information was fetched")]
    }

#using llm to get the itinerrary for the travel query
def itinerary_agent(state:TravelState):
    human_prompt = f"""
            Create a travel itinerary.
            User Query: {state['user_query']}
            Flight Results: {state['flight_results']}
            Hotel Results: {state['hotel_results']}
            """

    system_prompt = """
        Role: You are an expert AI travel agent and itinerary designer with 10 years of experience creating personalized, seamless, 
        and memorable trips.
        Objective: Help users plan custom travel itineraries, recommend hidden gems, suggest accommodations, and provide 
        practical local tips based on their specific needs.
        Guidelines:Ask clarifying questions if critical details (budget, dates, traveler type, interests) are missing.
        Balance popular sights with unique, off-the-beaten-path experiences.
        Structure itineraries day-by-day with estimated timelines and practical travel logic (e.g., efficient routing).
        Keep the tone friendly, professional, and enthusiastic.
        Required Output Format:
        Trip Overview: Summary of destination, duration, and vibe.Day-by-Day Itinerary: Morning, afternoon, and evening activities.
        Recommendations: Places to eat and stay.
    """
    #response from the llm
    response =  llm.invoke([
        SystemMessage(content=system_prompt),
            HumanMessage(content=human_prompt)
        ])
    return {
        "itinerary" : response.content,
        "messages" : [response]
    }    

#final agent which shows the complete travel plan and the itinerary for the user query
def travel_agent(state:TravelState):
    final_prompt = f"""
    You are an expert travel concierge. Your task is to synthesize raw travel data into a single, cohesive, and beautiful holiday package. 
    Do not just list options. Combine the flights, hotels, and itinerary into one unified, chronological travel plan.
    ### INPUT DATA:
    - Flight Options: {state['flight_results']}
    - Hotel Selection: {state['hotel_results']}
    - Base Itinerary: {state['itinerary']}

    ### INSTRUCTIONS:
    1. **Seamless Integration**: Integrate the flight arrival and departure times smoothly into Day 1 and the Final Day of the itinerary. 
    2. **Hotel Grounding**: Mention the chosen hotel on Day 1 during check-in, and use its location to anchor evening recommendations or daily starting points.
    3. **Clarity**: Eliminate all raw data formatting, API tags, and messy text. Present prices clearly with currency symbols.
    4. **Tone**: Keep it highly professional, exciting, and easy to read.
    
    ### EXPECTED OUTPUT FORMAT:
    # Your Dream Trip Overview
    *A brief, enthusiastic summary of the travel package.*

    ## ✈️ Flight Details
    - **Outbound**: [Airline] | [Departure Time] -> [Arrival Time] ([Direct/Layovers])
    - **Return**: [Airline] | [Departure Time] -> [Arrival Time] ([Direct/Layovers])

    ## 🏨 Accommodation
    - **Stay**: [Hotel Name] ([Star Rating])
    - **Perks**: [Mention 1-2 key perks like free breakfast, central location, etc.]

    ## 🗺️ Day-by-Day Unified Itinerary
    - **Day 1: Arrival & Settling In**
    - Incorporate the flight arrival time here.
    - Describe transit and checking into [Hotel Name].
    - Light afternoon/evening activity based on the base itinerary.
    - [Insert remaining days from the base itinerary dynamically...]
    - **Final Day: Farewell & Departure**
    - Breakfast at the hotel / checkout.
    - Last-minute souvenir shopping or sights.
    - Incorporate the departure flight timeline here.

    ## 💰 Total Estimated Investment
    - **Flights**: [Price]
    - **Hotel**: [Price]
    - **Estimated Total**: [Combined Price]
    """
    response = llm.invoke([HumanMessage(content=final_prompt)])
    return{
        "messages":[response]    
    }

#---------------------------------------------GRAPH---------------------------------    

graph = StateGraph(TravelState)

#adding nodes
graph.add_node("flight_agent",flight_agent)
graph.add_node("hotel_agent",hotel_agent)
graph.add_node("itinerary_agent",itinerary_agent)
graph.add_node("travel_agent",travel_agent)

#connecting graph edges
graph.add_edge(START,"flight_agent")
graph.add_edge("flight_agent","hotel_agent")
graph.add_edge("hotel_agent","itinerary_agent")
graph.add_edge("itinerary_agent","travel_agent")
graph.add_edge("travel_agent",END)

#----------------------------------CHECKPOINT-----------------------------
# Adding a checkpointer to track the state and for persistance using postgres db
# Persistent connection so both CLI and Streamlit can share the compiled app 
#defining the connection to DB
conn = psycopg.connect(DB_URL)

# FIX: Enable autocommit before calling setup
conn.autocommit = True 

# Persistent connection so both CLI and Streamlit can share the compiled app
checkpointer = PostgresSaver(conn)

#to set up the postgres db using setup method
checkpointer.setup()

#--------------------------------COMPILE----------------------------------
travel_app = graph.compile(checkpointer=checkpointer)

#-------------------------------------TESTING GRAPH --------------------------
"""
#defining config for the threads
config = { "configurable": {"thread_id": "Naz"}}

user_query = input("Enter travel request: ")

result = travel_app.invoke(
        {
            "messages": [
                HumanMessage(content= user_query)
            ],
            "user_query": user_query,
            "flight_results": "",
            "hotel_results": "",
            "itinerary": ""
        },
        config= config
    )
print("\nFINAL RESPONSE:\n")
for msg in result["messages"]:
    print(msg.content)
"""