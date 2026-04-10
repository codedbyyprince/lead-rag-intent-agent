import os
import json
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from tools import greeting, fetech_info, mock_lead_capture

load_dotenv() 

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in .env")

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.1,
    google_api_key=api_key,
)

# load knowledge
knowledge_data = fetech_info("")

system_prompt = """You are AutoStream's AI assistant. Your job is to:

1. Greet users warmly
2. Answer questions about AutoStream pricing and features using the knowledge base below
3. Detect if a user has high intent to buy
4. Collect lead information (name, email, platform) when appropriate

**Knowledge Base:**
{knowledge}

**Rules:**
- Only provide information from the knowledge base
- If asked about something not in the knowledge base, say you don't have that information
- Detect high-intent signals like "want to try", "ready to buy", "subscribe", "sign up"
- When you detect high-intent, explicitly ask for: name, email, and creator platform
- Only call lead capture when ALL three pieces of information are provided
- Keep responses concise and natural"""

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{query}")
])

# conversation history
conversation = []

print("Chat with AutoStream. Type 'quit' to exit.\n")

while True:
    query = input("You: ")
    
    if query == 'quit':
        break
    
    # add to history
    conversation.append(("user", query))
    
    # format messages for model
    messages = chat_prompt.format_messages(
        query=query,
        knowledge=json.dumps(knowledge_data, indent=2)
    )
    
    # add conversation history
    for role, text in conversation[:-1]:  # exclude current message
        if role == "user":
            messages.insert(-1, {"role": "user", "content": text})
        else:
            messages.insert(-1, {"role": "assistant", "content": text})
    
    # get response
    response = model.invoke(messages)
    response_text = response.content
    
    # add to history
    conversation.append(("assistant", response_text))
    
    print(f"Assistant: {response_text}\n")
