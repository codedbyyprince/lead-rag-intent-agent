import os
import json
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from tools import fetch_info, mock_lead_capture

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in .env")

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.1,
    google_api_key=api_key,
)

knowledge_data = fetch_info()

SYSTEM_PROMPT = f"""You are AutoStream's friendly AI assistant. AutoStream is a SaaS product that provides automated video editing tools for content creators.

Your job:
1. Greet users warmly
2. Answer questions about AutoStream using ONLY the knowledge base below
3. Detect high intent to buy (signals: "want to try", "sign up", "ready to buy", "get started", "subscribe")
4. When high intent detected, collect name, email, and creator platform ONE AT A TIME
5. Only call LEAD_CAPTURE after collecting all three

Knowledge Base:
{json.dumps(knowledge_data, indent=2)}

Rules:
- Only answer from knowledge base for product questions
- For general questions about what you can do, explain you help with AutoStream pricing and features
- When collecting lead info, ask for one field at a time
- When you have all three (name, email, platform), respond with exactly:
  LEAD_CAPTURE::name::email::platform
- Never trigger LEAD_CAPTURE early
- Keep responses short and natural"""

conversation_history = []
lead_captured = False

WELCOME_MESSAGE = "Hi, I'm the AutoStream assistant. Ask about pricing, features, or getting started."

def chat_once(query):
    global lead_captured

    conversation_history.append(HumanMessage(content=query))

    messages = [SystemMessage(content=SYSTEM_PROMPT)] + conversation_history
    response = model.invoke(messages)
    response_text = response.content

    if "LEAD_CAPTURE::" in response_text and not lead_captured:
        try:
            parts = response_text.strip().split("::")
            name = parts[1]
            email = parts[2]
            platform = parts[3]
            mock_lead_capture(name, email, platform)
            lead_captured = True
            response_text = f"Perfect! I've captured your details successfully. Welcome to AutoStream, {name}! We'll be in touch at {email} soon."
        except Exception:
            response_text = "I had trouble saving your details. Could you please share your name, email, and platform again."

    conversation_history.append(AIMessage(content=response_text))
    return response_text


def run_cli():
    print("Chat with AutoStream. Type 'quit' to exit.\n")

    while True:
        query = input("You: ").strip()

        if query.lower() == "quit":
            break

        response_text = chat_once(query)
        print(f"Assistant: {response_text}\n")


if __name__ == "__main__":
    run_cli()
