from agents.router_agent import router_agent

state = {

    "question": "Tell me about Leave Policy",

    "route": "",

    "documents": [],

    "answer": ""

}

result = router_agent(state)

print("\nFinal State")

print(result)