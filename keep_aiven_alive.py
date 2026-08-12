import os
import requests

AIVEN_TOKEN = os.getenv("AIVEN_TOKEN")
PROJECT_NAME = "budgetwisely123"
SERVICE_NAME = "postgresql"

# ✅ Fixed header format (changed 'aivenbearer' to 'aivenv1')
headers = {
    "Authorization": f"aivenv1 {AIVEN_TOKEN}",
    "Content-Type": "application/json"
}

url = f"https://api.aiven.io/v1/project/{PROJECT_NAME}/service/{SERVICE_NAME}"

if AIVEN_TOKEN:
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        service_data = response.json().get("service", {})
        state = service_data.get("state")
        
        if state in ["POWERED_OFF", "POWERING_OFF"]:
            print(f"Service '{SERVICE_NAME}' is currently {state}. Powering it on...")
            
            # Correct payload to power on Aiven services
            update_payload = {"powered": True}
            put_response = requests.put(url, json=update_payload, headers=headers)
            
            if put_response.status_code == 200:
                print("Power-on request accepted! Service is starting up.")
            else:
                print(f"Failed to power on service: {put_response.status_code} - {put_response.text}")
        else:
            print(f"Service '{SERVICE_NAME}' is active ({state}). No action needed.")
    else:
        print(f"Failed to fetch service details: {response.status_code} - {response.text}")
else:
    print("AIVEN_TOKEN environment variable not set.")