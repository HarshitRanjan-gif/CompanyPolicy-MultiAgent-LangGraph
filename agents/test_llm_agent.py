from agents.llm_agent import llm_agent


state = {

    "question": "Explain Machine Learning",

    "route": "llm",

    "documents": [],

    "context": "",

    "answer": ""

}


result = llm_agent(state)

print("\n==========================")

print(result["answer"])