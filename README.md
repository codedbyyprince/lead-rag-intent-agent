# AutoStream AI Agent — Social-to-Lead Agentic Workflow

A conversational AI agent built for ServiceHive's assignment. The agent handles real product conversations for a fictional SaaS called AutoStream, detects user intent, answers questions from a knowledge base using RAG, and captures qualified leads directly into a Supabase database.

**Live Demo:** https://mlwithprince-lead-rag-intent-agent.hf.space/

---

## What This Does

Most chatbots just answer questions. This agent does more. It understands where a user is in their buying journey, answers accurately from a structured knowledge base, and when a user shows intent to sign up, it collects their details one at a time and stores them as a real lead in a database. The entire flow is conversational, not form-based.

---

## Features

- **Intent detection** — classifies every message as a greeting, product inquiry, or high-intent lead signal
- **RAG-powered responses** — answers pricing and policy questions strictly from a local JSON knowledge base, no hallucination
- **Lead capture flow** — collects name, email, and creator platform one field at a time, only after confirmed intent
- **Supabase integration** — every captured lead is stored in a live PostgreSQL database, exportable as CSV
- **Session memory** — retains full conversation context across 5 to 6 turns
- **Flask web UI** — clean chat interface with quick-reply buttons, deployed on Hugging Face Spaces via Docker

---

## Tech Stack

| Layer | Technology |
|---|---|
| LLM | Gemini 2.5 Flash via Google AI Studio |
| Agent framework | LangChain |
| Backend | Flask |
| Database | Supabase (PostgreSQL) |
| Deployment | Hugging Face Spaces + Docker |
| Language | Python 3.11 |

---

## Project Structure

```
langchain-lead-agent/
├── agent.py              # Core agent logic, LLM setup, conversation handling
├── app.py                # Flask server, routes, session management
├── tools.py              # fetch_info, mock_lead_capture with Supabase insert
├── supabase_client.py    # Supabase client initialisation
├── knowledge.json        # RAG knowledge base: pricing, features, policies
├── templates/
│   └── home.html         # Single page chat UI
├── requirements.txt
└── Dockerfile
```

---

## How to Run Locally

**1. Clone the repository**
```bash
git clone https://github.com/codedbyyprince/langchain-lead-agent
cd langchain-lead-agent
```

**2. Create a virtual environment and install dependencies**
```bash
python -m venv myenv
source myenv/bin/activate  # Windows: myenv\Scripts\activate
pip install -r requirements.txt
```

**3. Set up environment variables**

Create a `.env` file in the root directory:
```
GOOGLE_API_KEY=your_gemini_api_key
SUPABASE_URL=your_supabase_project_url
SUPABASE_ANON_KEY=your_supabase_anon_key
```

Get your Gemini API key free at https://aistudio.google.com
Get your Supabase credentials from your project dashboard at https://supabase.com

**4. Run the app**
```bash
python app.py
```

Open http://localhost:5000 in your browser.

---

## Architecture Explanation

The agent is built on LangChain with Google Gemini 2.5 Flash as the LLM. The architecture is intentionally simple and production-oriented.

**RAG implementation:** The knowledge base is stored in a local JSON file containing AutoStream pricing, features, and company policies. On startup, this data is loaded and injected directly into the system prompt. This approach is appropriate for a small, structured knowledge base where semantic search would add unnecessary complexity. The LLM is instructed to answer only from this context, which prevents hallucination.

**Intent detection and state management:** Rather than a separate classifier, intent detection is handled through the system prompt. When the LLM detects high-intent signals such as "want to try" or "get started", it begins collecting lead information. A structured signal format `LEAD_CAPTURE::name::email::platform` is used as a communication protocol between the LLM and the Python layer. The Python code watches for this signal and only then calls the tool. This keeps the LLM responsible for reasoning and Python responsible for execution, which is a clean separation of concerns.

**Memory:** Full conversation history is maintained using LangChain's `HumanMessage` and `AIMessage` objects, passed with every request. Sessions are managed per user in a server-side dictionary.

**Why LangChain over AutoGen:** LangChain provides straightforward message management and Gemini integration with minimal boilerplate. For a single-agent, single-tool workflow like this, LangChain is the right level of abstraction. AutoGen is better suited for multi-agent setups.

---

## WhatsApp Integration via Webhooks

To deploy this agent on WhatsApp, the following approach would work:

1. Register a WhatsApp Business account and enable the Meta Cloud API
2. Set a webhook URL pointing to a new Flask route, for example `/whatsapp`, with HTTPS (required by Meta)
3. When a user sends a WhatsApp message, Meta sends a POST request to that webhook containing the message body and the sender's phone number
4. The Flask route extracts the message, passes it to `chat_once()` along with the phone number as the session ID
5. The agent response is sent back using the WhatsApp API send message endpoint with the recipient's phone number
6. Session memory works identically, using phone number as the unique session key instead of a browser session ID

The existing agent logic, RAG pipeline, and Supabase lead capture require no changes for WhatsApp deployment. Only the input and output layer changes.

---

## Lead Capture Flow

```
User shows intent ("I want to sign up")
        ↓
Agent asks for name
        ↓
Agent asks for email
        ↓
Agent asks for creator platform
        ↓
mock_lead_capture() called
        ↓
Lead printed to server logs
        ↓
Lead inserted into Supabase Lead-info table
        ↓
Confirmation message shown to user
```

The tool is never triggered prematurely. All three fields must be present before execution.

---

## Knowledge Base

Stored in `knowledge.json`, the agent knows:

**Pricing:**
- Basic Plan: $29/month, 10 videos/month, 720p resolution
- Pro Plan: $79/month, unlimited videos, 4K resolution, AI captions

**Policies:**
- No refunds after 7 days
- 24/7 support available on Pro plan only

---

## Built By

**Prince Nagda**
Self-taught ML engineer, Madhya Pradesh, India

GitHub: https://github.com/codedbyyprince
Portfolio: https://princenagda.netlify.app
Email: princenagda35@gmail.com