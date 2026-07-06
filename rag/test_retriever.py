from rag.retriever import get_retriever

retriever = get_retriever()

docs = retriever.invoke("Tell me about Leave Policy")

print(f"Retrieved {len(docs)} documents\n")

for i, doc in enumerate(docs, start=1):
    print(f"----- Document {i} -----")
    print(doc.page_content[:300])
    print()