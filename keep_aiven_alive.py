import os
import requests

AIVEN_TOKEN = os.getenv("AIVEN_TOKEN")
PROJECT_NAME = "budgetwisely123"  # From your screenshot
SERVICE_NAME = "postgresql"        # From your screenshot

headers = {
    "Authorization": f"aivenbearer {AIVEN_TOKEN}",
    "Content-Type": "application/json"
}

url = f"https://api.aiven.io/v1/project/{PROJECT_NAME}/service/{SERVICE_NAME}"

if AIVEN_TOKEN:
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        service_data = response.json().get("service", {})
        state = service_data.get("state")
        
        # State can be 'RUNNING', 'POWERED_OFF', 'REBUILDING', etc.
        if state == "POWERED_OFF":
            print(f"Service '{SERVICE_NAME}' is currently POWERED OFF. Powering it on...")
            
            # Send API update request to power on the service
            update_payload = {"power_on": True}
            patch_response = requests.put(url, json=update_payload, headers=headers)
            
            if patch_response.status_code == 200:
                print("Power-on request sent successfully!")
            else:
                print(f"Failed to power on service: {patch_response.status_code} - {patch_response.text}")
        else:
            print(f"Service '{SERVICE_NAME}' is active ({state}). No action needed.")
    else:
        print(f"Failed to fetch service details: {response.status_code} - {response.text}")
else:
    print("AIVEN_TOKEN environment variable not set.")