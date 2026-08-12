import os
import requests
from huggingface_hub import HfApi

token = os.getenv("HF_TOKEN")
space_id = "ajay0987/AI-Powered-Document-Analyser"
space_url = f"https://{space_id.replace('/', '-')}.hf.space"

if token:
    api = HfApi(token=token)
    runtime = api.get_space_runtime(repo_id=space_id)

    if runtime.stage in ["SLEEPING", "PAUSED", "STOPPED"]:
        print(f"Space is currently {runtime.stage}. Triggering restart...")
        api.restart_space(repo_id=space_id)
    else:
        # Send HTTP traffic to force HF to reset the 48-hour inactivity timer
        print(f"Space is active ({runtime.stage}). Sending ping to reset timer...")
        try:
            requests.get(space_url, timeout=10)
            print("Ping successful! Timer reset.")
        except Exception as e:
            print(f"Ping failed: {e}")
else:
    # Fallback HTTP ping
    requests.get(space_url, timeout=10)
    print("Fallback ping sent.")