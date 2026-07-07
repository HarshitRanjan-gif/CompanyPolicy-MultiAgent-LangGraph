# Company AI Assistant (LangGraph)

A **Multi-Agent AI Assistant** built using **LangGraph**, **LangChain**, **FAISS**, **Groq Llama 3.1**, **Tavily Search**, and **Streamlit**. The assistant intelligently routes user queries to specialized agents for company policy retrieval, web search, or general knowledge, providing accurate and context-aware responses.

---

## 📷 Application Screenshot

<img width="1907" height="882" alt="image" src="https://github.com/user-attachments/assets/01045b29-389b-4594-8ea0-dc86f8dd2221" />

---

## 🖥️ Live Demo

[Open App](https://companypolicy-multiagent-langgraph-zj3fnpxozltx7mvfjfderr.streamlit.app/)

---

# Features

- Multi-Agent architecture using LangGraph
- Intelligent Router Agent for query classification
- Retrieval-Augmented Generation (RAG) for company policy questions
- Web Search Agent using Tavily Search API
- LLM Agent for general knowledge and programming questions
- Query Rewriter for follow-up conversations
- Conversation memory with chat history
- FAISS vector database for semantic document retrieval
- HuggingFace BAAI/bge-m3 embedding model
- Groq Llama 3.1 8B Instant for response generation
- Displays retrieved context and source page numbers
- Response time measurement for every query
- Streamlit-based interactive user interface

---

# Tech Stack

- Python
- LangGraph
- LangChain
- FAISS
- HuggingFace Embeddings (BAAI/bge-m3)
- Groq (Llama 3.1 8B Instant)
- Tavily Search API
- Streamlit

---

# Project Structure

```text
CompanyPolicy_MultiAgent_LangGraph/
│
├── agents/
│   ├── formatter_agent.py
│   ├── llm_agent.py
│   ├── rag_agent.py
│   ├── router_agent.py
│   └── web_agent.py
│
├── rag/
│   ├── data/
│   │   └── company_policy.pdf
│   ├── vector_store/
│   │   ├── index.faiss
│   │   └── index.pkl
│   ├── create_vector_db.py
│   └── retriever.py
│
├── tools/
│   └── search.py
│
├── utils/
│   ├── chat_history.py
│   ├── conversation_utils.py
│   ├── helpers.py
│   └── query_rewriter.py
│
├── app.py
├── chatbot.py
├── graph.py
├── prompts.py
├── memory.py
├── state.py
├── styles.py
├── ui.py
├── requirements.txt
└── README.md
```

---

# How It Works

1. The user submits a question through the Streamlit interface.
2. The Query Rewriter converts follow-up questions into standalone queries.
3. The Router Agent determines the most suitable agent for the request.
4. Depending on the query, it is routed to:
   - **RAG Agent** for company policy questions.
   - **Web Search Agent** for current or external information.
   - **LLM Agent** for general knowledge, programming, AI, and reasoning tasks.
5. The selected agent generates a response.
6. The Formatter Agent prepares the final output.
7. The application displays the answer along with response time, retrieved context, and source page numbers (when applicable).

---

# Multi-Agent Workflow

```text
                User Query
                     │
                     ▼
             Query Rewriter
                     │
                     ▼
             Router Agent
                     │
      ┌──────────────┼──────────────┐
      ▼              ▼              ▼
 RAG Agent      Web Search      LLM Agent
      │              │              │
      └──────────────┼──────────────┘
                     ▼
             Formatter Agent
                     │
                     ▼
              Streamlit UI
```

---

# Future Improvements

- Dedicated Conversation Agent
- Named Entity Recognition (NER) for smarter routing
- Confidence-based routing
- Multi-document RAG support
- Voice-enabled interaction
- User authentication
- Database-backed chat history
- Docker containerization
- Cloud deployment with CI/CD

---

## 👨‍💻 Author

**Harshit Ranjan**

A portfolio project demonstrating a production-style **Multi-Agent AI Assistant** built using **LangGraph** and **LangChain**.
