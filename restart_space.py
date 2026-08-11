import os
import requests
from huggingface_hub import HfApi

token = os.getenv("HF_TOKEN")
space_id = "ajay0987/AI-Powered-Document-Analyser"  # Replace with actual space ID

if token:
    api = HfApi(token=token)
    runtime = api.get_space_runtime(repo_id=space_id)

    if runtime.stage in ["SLEEPING", "PAUSED", "STOPPED"]:
        print(f"Space is currently {runtime.stage}. Triggering restart...")
        api.restart_space(repo_id=space_id)
    else:
        print(f"Space is active ({runtime.stage}).")
else:
    # Fallback HTTP ping
    url = f"https://{space_id.replace('/', '-')}.hf.space"
    requests.get(url)
    print("Ping sent to Space URL.")