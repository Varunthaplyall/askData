import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.ai_client import AIClient


def resolve_metric(user_metric: str) -> str:
    print(f"Resolving metric for: {user_metric}")
    system_prompt = """
                    You are a helpful assistant for a data analysis system. Given a user-provided metric like 'rainfall', 'temperature', or 'pollution', 
                    respond with the single best matching backend category used in our system. The allowed categories are:

                    - climate
                    - pollution
                    - population
                    - agriculture
                    - economy

                    Respond with only one of these words. Do not add explanations or any extra text.
                    """
    user_prompt = f"What backend module best fits the metric '{user_metric}'?"
    
    try:
        client = AIClient()
        resolved = client.call_ai_model(system_prompt=system_prompt, user_prompt=user_prompt, model="qwen/qwen-2.5-72b-instruct:free")
        
        resolved = resolved.strip().lower()
        print(f"Resolved metric: {resolved}")
        
        allowed_modules = {"climate", "pollution", "population", "agriculture", "economy"}
        if resolved not in allowed_modules:
            raise ValueError(f"Unrecognized resolved metric: {resolved}")
        return resolved
    except Exception as e:
        raise RuntimeError(f"Failed to resolve metric '{user_metric}': {e}")

# --- Example Usage ---
if __name__ == '__main__':
    
    metrics_to_test = ["temperature", "air quality index", "crop yields", "unemployment rate", "city growth", "rainfall"]
    
    for metric in metrics_to_test:
        try:
            category = resolve_metric(metric)
            print(f"The metric '{metric}' resolved to: **{category}**")
        except RuntimeError as e:
            print(e)
