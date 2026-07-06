from agents.web_agent import web_agent


state = {

    "question": "Latest AI News",

    "route": "web",

    "documents": [],

    "context": "",

    "answer": ""

}


result = web_agent(state)

print("\n========================")

print(result["answer"])