import os
import requests
import psycopg2
import pymysql

AIVEN_TOKEN = os.getenv("AIVEN_TOKEN")
PROJECT_NAME = "budgetwisely123"

# Configuration list for all Aiven services to keep alive
SERVICES = [
    {
        "name": "postgresql",
        "type": "postgres",
        "uri": os.getenv("DATABASE_URL")
    },
    {
        "name": "mysql-312585f1",
        "type": "mysql",
        "uri": os.getenv("MYSQL_URL")  # Optional: Connection string for MySQL
    }
]

headers = {
    "Authorization": f"aivenv1 {AIVEN_TOKEN}",
    "Content-Type": "application/json"
}

if not AIVEN_TOKEN:
    print("Error: AIVEN_TOKEN environment variable is missing.")
    exit(1)

for service in SERVICES:
    service_name = service["name"]
    db_type = service["type"]
    db_uri = service["uri"]
    url = f"https://api.aiven.io/v1/project/{PROJECT_NAME}/service/{service_name}"

    print(f"\n--- Processing Service: {service_name} ({db_type.upper()}) ---")
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        state = response.json().get("service", {}).get("state")

        if state in ["POWEROFF", "POWERED_OFF", "POWERING_OFF"]:
            print(f"Service '{service_name}' is currently {state}. Sending power-on request...")
            put_response = requests.put(url, json={"powered": True}, headers=headers)
            if put_response.status_code == 200:
                print(f"Power-on request accepted for '{service_name}'!")
            else:
                print(f"Failed to power on '{service_name}': {put_response.status_code} - {put_response.text}")
        else:
            print(f"Service '{service_name}' is active ({state}).")
            
            # Send keep-alive query if connection URL is configured
            if db_uri:
                try:
                    if db_type == "postgres":
                        conn = psycopg2.connect(db_uri, connect_timeout=5)
                        cur = conn.cursor()
                        cur.execute("SELECT 1;")
                        cur.close()
                        conn.close()
                        print(f"PostgreSQL keep-alive query successful for '{service_name}'!")

                    elif db_type == "mysql":
                        conn = pymysql.connect(dsn=db_uri, connect_timeout=5)
                        cur = conn.cursor()
                        cur.execute("SELECT 1;")
                        cur.close()
                        conn.close()
                        print(f"MySQL keep-alive query successful for '{service_name}'!")

                except Exception as e:
                    print(f"Keep-alive DB query failed for '{service_name}': {e}")
            else:
                print(f"No DB URI provided for '{service_name}'. API check complete.")
    else:
        print(f"Failed to fetch status for '{service_name}': {response.status_code} - {response.text}")