import os
from typing import Annotated, TypedDict
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph import StateGraph, END, START
import requests
from langchain.agents import create_agent
from bs4 import BeautifulSoup
from typing import List
import json
from datetime import datetime
# Load environment variables from .env file
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# -------------------- Tool Definitions --------------------



@tool
def fetch_credly_certifications_with_score(username: str) -> str:
    """
    Fetch all certifications from a Credly user profile, display details of each badge,
    and calculate credit score for active certifications listed in data.json.
    """
    api_url = f"https://www.credly.com/users/{username}/badges.json"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        # Fetch badges from Credly
        response = requests.get(api_url, headers=headers)
        if response.status_code != 200:
            return f"Failed to fetch data. Status code: {response.status_code}"

        data = response.json()
        badges = data.get("data", [])

        if not badges:
            return "No certifications found."

        # Load scoring rules from data.json
        json_path = os.path.join(os.path.dirname(__file__), "data.json")
        with open(json_path, "r") as file:
            rules = json.load(file)

        # Prepare scoring dictionary for exact match (case-insensitive)
        rules_dict = {rule["certificate_name"].strip().lower(): float(rule["credit_points"]) for rule in rules}

        today = datetime.today().date()
        total_score = 0
        report_lines = []

        for badge in badges:
            title = badge.get("badge_template", {}).get("name")
            issued_at = badge.get("issued_at")
            expires_raw = badge.get("expires_at_date") or badge.get("expires_at")
            state = badge.get("state", "").lower()

            # Skip badges without a title
            if not title:
                continue

            # Check if badge is active
            is_active = True
            if state not in ["accepted", "issued"]:
                is_active = False
            if expires_raw:
                try:
                    expires_date = datetime.fromisoformat(expires_raw).date()
                    if expires_date < today:
                        is_active = False
                except:
                    is_active = False

            # Calculate credit score if active and present in data.json
            score = 0
            if is_active and title.strip().lower() in rules_dict:
                score = rules_dict[title.strip().lower()]
                total_score += score

            # Add badge details to report
            report_lines.append(
                f"- {title} | Issued: {issued_at or 'N/A'} | Expires: {expires_raw or 'N/A'} | State: {state} | Active: {is_active} | Credit Points: {score}"
            )

        if not report_lines:
            return "No certifications found."

        result = (
            f" Certification Details for '{username}':\n\n"
            + "\n".join(report_lines)
            + f"\n\n Total Credit Score (Active & Listed in data.json): {total_score}"
        )
        return result

    except Exception as e:
        return f"Error fetching or processing certifications: {str(e)}"

# List of available tools
tools = [fetch_credly_certifications_with_score]

# Initialize LLM and bind tools to the model (create_react_agent expects bound tools or matching tools)
llm = ChatGroq(groq_api_key=GROQ_API_KEY, model="llama-3.3-70b-versatile")
llm_with_tools = llm.bind_tools(tools)

# Create the agent graph using the LLM (with tools bound) and the tools list
# `create_react_agent` was removed/renamed; use `create_agent` from langchain.agents
graph = create_agent(llm_with_tools, tools)