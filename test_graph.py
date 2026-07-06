from graph import graph


result = graph.invoke(

    {

        "question": "Tell me about Leave Policy",

        "route": "",

        "documents": [],

        "context": "",

        "answer": ""

    }

)


print("\n========================")

print(result["answer"])