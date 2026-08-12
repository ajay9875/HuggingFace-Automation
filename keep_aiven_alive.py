import os
import requests
import psycopg2

AIVEN_TOKEN = os.getenv("AIVEN_TOKEN")
PROJECT_NAME = "budgetwisely123"
SERVICE_NAME = "postgresql"
DB_URI = os.getenv("DATABASE_URL") # Add your Aiven Postgres connection string

headers = {
    "Authorization": f"aivenv1 {AIVEN_TOKEN}",
    "Content-Type": "application/json"
}

url = f"https://api.aiven.io/v1/project/{PROJECT_NAME}/service/{SERVICE_NAME}"

if AIVEN_TOKEN:
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        state = response.json().get("service", {}).get("state")
        
        if state in ["POWEROFF", "POWERED_OFF", "POWERING_OFF"]:
            print(f"Service is {state}. Powering it on...")
            requests.put(url, json={"powered": True}, headers=headers)
        else:
            print(f"Service is {state}. Sending keep-alive query...")
            # Query DB to log activity and keep it active
            if DB_URI:
                try:
                    conn = psycopg2.connect(DB_URI, connect_timeout=5)
                    cur = conn.cursor()
                    cur.execute("SELECT 1;")
                    cur.close()
                    conn.close()
                    print("DB Query successful! Inactivity timer reset.")
                except Exception as e:
                    print(f"DB Ping failed: {e}")