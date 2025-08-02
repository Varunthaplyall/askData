import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.ai_client import AIClient


def query_nlp(prompt: str) -> dict:
    system_prompt = """
    You are an AI assistant for a data analysis application. Your job is to extract structured JSON from a user's natural language question. The expected fields are:\n\n1. **metric**: A concise identifier for the type of data requested. Use lowercase with underscores (e.g., \"air_quality\", \"population\", \"temperature\").\n\n2. **location**: A city, state, region, or country the user is referring to.\n\n3. **date_range**: A JSON object with `start_date` and `end_date` in `YYYY-MM-DD` format. If a relative time (e.g., \"since 2010\", \"last year\") is given, resolve it into absolute dates. If no end date is mentioned, use today’s date.\n\n4. **months** (optional): If the user refers to a **season** (e.g., \"winter\", \"monsoon\") or specific months, include this field as an array of full month names (e.g., [\"December\", \"January\", \"February\"]).\n\n5. If the user's query is **too vague** or lacks essential information (like a metric or location), return a JSON with only the fields you can confidently extract.\n\n### Examples:\n\n**User**: \"Show me air quality in Delhi during winters since 2015\"\n**Output**:\n```json\n{\n  \"metric\": \"air_quality\",\n  \"location\": \"Delhi\",\n  \"date_range\": {\n    \"start_date\": \"2015-12-01\",\n    \"end_date\": \"2025-08-02\"\n  },\n  \"months\": [\"December\", \"January\", \"February\"]\n}\n```\n\n**User**: \"Rainfall in Maharashtra\"\n**Output**:\n```json\n{\n  \"metric\": \"rainfall\",\n  \"location\": \"Maharashtra\"\n}\n```\n\n**User**: \"Compare population in India and China from 2000 to 2020\"\n**Output**:\n```json\n{\n  \"metric\": \"population\",\n  \"location\": [\"India\", \"China\"],\n  \"date_range\": {\n    \"start_date\": \"2000-01-01\",\n    \"end_date\": \"2020-12-31\"\n  }\n}\n```\n\nNow extract a JSON from the following query
    """
    
    ai = AIClient()
    response = ai.call_ai_model(system_prompt=system_prompt, user_prompt=prompt)
    try:
        return response
    except Exception:
        raise ValueError("Failed to parse AI response into JSON")


# Testing
if __name__ == "__main__":
    user_input = "Show the temperature of Delhi in winters from 2024 to now"
    result = query_nlp(user_input)
    print("Parsed Response:")
    print(result)