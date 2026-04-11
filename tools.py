import os
import json
from supabase_client import supabase

file_name = 'knowledge.json'
file_path = os.path.join(os.getcwd(), file_name)

def fetch_info():
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

def mock_lead_capture(name, email, platform):
    print(f"Lead captured successfully: {name}, {email}, {platform}")
    supabase.table("Lead-info").insert({
        "name": name,
        "email_address": email,
        "platform": platform
    }).execute()
