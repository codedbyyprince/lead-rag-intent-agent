import os 
import json

file_name = 'knowledge.json'
file_path = os.path.join(os.getcwd(), file_name)

def greeting(query):
    return "Hello how are you doing today"

def fetech_info(query):
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
        return data  

def collect_lead(query):
    # Database logic    
    pass

def mock_lead_capture(name, email, platform):
    print(f"Lead captured successfully: {name}, {email}, {platform}")