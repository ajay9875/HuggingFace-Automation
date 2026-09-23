import os
import sys
import requests
from datetime import datetime, timezone

# ---------------------------------------------------------------------------
# TaskCare360 Push Scheduler — GitHub Actions trigger
#
# Hits the /api/send-step-push endpoint on PythonAnywhere with a secret
# stored in GitHub repository secrets.
#
# Required environment variables:
#   SCHEDULER_SECRET  — must match the value in PythonAnywhere's .env
# ---------------------------------------------------------------------------

BASE_URL = "https://TaskCare360.pythonanywhere.com"
ENDPOINT = "/api/send-step-push"
TIMEOUT = 30  # seconds


def main() -> int:
    # --- 1. Read the secret from environment ---
    secret = os.environ.get("SCHEDULER_SECRET", "").strip()
    if not secret:
        print("❌ SCHEDULER_SECRET is not set in the environment")
        return 1

    # --- 2. Build the request URL ---
    url = f"{BASE_URL}{ENDPOINT}"

    print(f"🚀 Triggering at {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print(f"🌐 URL: {url}?secret=***")

    # --- 3. Fire the request ---
    try:
        response = requests.get(url, params={"secret": secret}, timeout=TIMEOUT)

        print(f"HTTP Status: {response.status_code}")
        print(f"Response Body:")
        print(response.text)
        print()

        if response.status_code != 200:
            print(f"❌ Request failed with HTTP {response.status_code}")
            return 1

        print("✅ Push scheduler triggered successfully")
        return 0

    except requests.exceptions.Timeout:
        print(f"❌ Request timed out after {TIMEOUT} seconds")
        return 1

    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        return 1

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())