from typing import Optional
from smolagents import CodeAgent, tool, HfApiModel
import os
from huggingface_hub import login

hf_token = os.environ.get("HUGGINGFACE_API_TOKEN")
if not hf_token:
    raise ValueError("Error: Hugging Face API token is missing!")


login(hf_token)  # Authenticate Hugging Face API


@tool
def get_travel_duration(start_location: str, destination_location: str, transportation_mode: Optional[str] = None) -> str:

    """Gets travel time estimate between two places:

    Args:
        start_location: place start
        destination_location: place of arrival
        transportation_mode: driving, walking, bicycle
    """
    import os #imports
    import googlemaps
    from datetime import datetime
    from huggingface_hub import InferenceClient



#
# Authenticate with Hugging Face
#client = InferenceClient(model="Qwen/Qwen2.5-Coder-32B-Instruct", token=hf_token)

    try:

        # Load the token from environment variable
        gmaps_token = os.environ.get("GOOGLEMAPS_API_TOKEN")
        if not gmaps_token:
            raise ValueError("Error: Google Maps API token is missing!")


        gmaps = googlemaps.Client(gmaps_token)

        print("Google Maps client initialized successfully.")
    except Exception as e:
        print(f"Error initializing Google Maps client: {e}")

    if transportation_mode is None:
        transportation_mode = "driving"
    try:
        directions_result = gmaps.directions(
            start_location,
            destination_location,
            mode=transportation_mode,
            departure_time=datetime.now())
        if len(directions_result) == 0:
            return "No way found between these two locations"
        return directions_result[0]['legs'][0]['duration']['text']
    except Exception as e:
        print("Error:", e)



agent = CodeAgent(tools=[get_travel_duration], model=HfApiModel(), additional_authorized_imports=["datetime"])

agent.run("Can you give me nice travel destinations between Cupertino, California and Los Angeles, California?")
