from agents.rag_agent import rag_agent


state = {

    "question": "Tell me about Leave Policy",

    "route": "rag",

    "documents": [],

    "context": "",

    "answer": ""

}


result = rag_agent(state)

print("\n==========================")

print(result["answer"])