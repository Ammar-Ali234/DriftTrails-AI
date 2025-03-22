from keys import *
from crewai import Agent, Task
from langchain_groq import ChatGroq
from textwrap import dedent
from datetime import date
import os


from tools.browser_tools import BrowserTools
from tools.calculator_tools import CalculatorTools
from tools.search_tools import SearchTools

# Initialize Groq API via LangChain
os.environ["GROQ_API_KEY"] = groq_API_KEY
llm = ChatGroq(model="llama3-70b-8192", temperature=0.7)

class TripAgents:
    def city_selection_agent(self):
        return Agent(
            role='DriftTrails City Scout',
            goal='Pinpoint the ultimate city for an unforgettable trip based on weather, season, and costs',
            backstory="A savvy explorer powered by DriftTrails AI, skilled in sifting through travel data to find the perfect destination",
            tools=[
                SearchTools.search_internet,
                BrowserTools.scrape_and_summarize_website,
            ],
            llm=llm,  # Use Groq API
            verbose=True
        )

    def local_expert(self):
        return Agent(
            role='DriftTrails Local Sage',
            goal='Unveil the deepest insights and hidden gems of the chosen city',
            backstory="A wise local guide under DriftTrails AI, with a treasure trove of knowledge on city attractions, customs, and secrets",
            tools=[
                SearchTools.search_internet,
                BrowserTools.scrape_and_summarize_website,
            ],
            llm=llm,
            verbose=True
        )

    def travel_concierge(self):
        return Agent(
            role='DriftTrails Journey Weaver',
            goal="Craft seamless 7-day itineraries with budget breakdowns, packing tips, and curated experiences",
            backstory="A master planner from DriftTrails AI, with decades of expertise in weaving travel dreams into reality",
            tools=[
                SearchTools.search_internet,
                BrowserTools.scrape_and_summarize_website,
                CalculatorTools.calculate,
            ],
            llm=llm,
            verbose=True
        )

class TripTasks:
    def identify_task(self, agent, origin, cities, interests, range):
        return Task(
            description=dedent(f"""
                Analyze and select the best city for a DriftTrails AI adventure based on weather, seasonal events, and travel costs. Compare multiple cities, factoring in current conditions, upcoming events, and expenses.
                
                Deliver a detailed report on the chosen city, including flight costs, weather forecasts, and must-see attractions.
                {self.__tip_section()}

                Traveling from: {origin}
                City Options: {cities}
                Trip Date: {range}
                Traveler Interests: {interests}
            """),
            agent=agent,
            expected_output="Detailed report on the chosen city including flight costs, weather forecast, and attractions"
        )

    def gather_task(self, agent, origin, interests, range):
        return Task(
            description=dedent(f"""
                As a DriftTrails AI Local Sage, compile an in-depth guide for an epic trip to the selected city. Gather info on key attractions, local customs, special events, and daily recommendations—highlighting spots only locals know.
                
                The guide should offer a rich overview, including hidden gems, cultural hotspots, landmarks, weather forecasts, and high-level costs.
                {self.__tip_section()}

                Trip Date: {range}
                Traveling from: {origin}
                Traveler Interests: {interests}
            """),
            agent=agent,
            expected_output="Comprehensive city guide including hidden gems, cultural hotspots, and practical travel tips"
        )

    def plan_task(self, agent, origin, interests, range):
        return Task(
            description=dedent(f"""
                Expand the city guide into a full 7-day DriftTrails AI itinerary, with detailed daily plans, weather forecasts, dining options, packing suggestions, and a budget breakdown.
                
                Recommend specific places to visit, hotels to stay at, and restaurants to dine in, explaining why each choice enhances the journey.
                
                Deliver a complete travel plan in markdown, covering arrival to departure, with daily schedules, anticipated weather, clothing/items to pack, and a detailed budget for THE BEST TRIP EVER.
                {self.__tip_section()}

                Trip Date: {range}
                Traveling from: {origin}
                Traveler Interests: {interests}
            """),
            agent=agent,
            expected_output="Complete expanded travel plan with daily schedule, weather conditions, packing suggestions, and budget breakdown"
        )

    def __tip_section(self):
        return "If you craft a stellar plan, DriftTrails AI will tip you $100!"

# Example usage
if __name__ == "__main__":
    agents = TripAgents()
    tasks = TripTasks()

    # Define inputs
    origin = "New York"
    cities = ["Paris", "Tokyo", "Cape Town"]
    interests = ["art", "food", "adventure"]
    travel_range = "2025-06-01 to 2025-06-07"

    # Create agents
    city_selector = agents.city_selection_agent()
    print(city_selector)
    local_expert = agents.local_expert()
    concierge = agents.travel_concierge()

    # Create tasks
    identify_task = tasks.identify_task(city_selector, origin, cities, interests, travel_range)
    gather_task = tasks.gather_task(local_expert, origin, interests, travel_range)
    plan_task = tasks.plan_task(concierge, origin, interests, travel_range)

    