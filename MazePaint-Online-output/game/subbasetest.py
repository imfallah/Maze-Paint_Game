import os
import requests




MAZEPAINT_SUPABASE_URL="https://bxqnjxwmvcjdlgovyemo.supabase.co"
MAZEPAINT_SUPABASE_KEY="sb_publishable_7aDZmQH47Wj6TMz17Y4lZw_6_mMKXH0"


SUPABASE_URL = os.getenv("MAZEPAINT_SUPABASE_URL")
SUPABASE_KEY = os.getenv("MAZEPAINT_SUPABASE_KEY")

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
}

# تست اتصال
url = f"{SUPABASE_URL}/rest/v1/leaderboard?select=*"

response = requests.get(url, headers=headers)

print("Status:", response.status_code)
print("Data:", response.text)
