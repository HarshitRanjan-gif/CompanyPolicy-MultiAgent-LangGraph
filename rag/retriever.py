from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


def get_retriever():

    # -----------------------------------------
    # Load Embedding Model
    # -----------------------------------------

    embedding_model = HuggingFaceEmbeddings(
        model_name="BAAI/bge-m3"
    )

    # -----------------------------------------
    # Load FAISS Vector Store
    # -----------------------------------------

    vector_db = FAISS.load_local(
        "rag/vector_store",
        embedding_model,
        allow_dangerous_deserialization=True
    )

    # -----------------------------------------
    # Create Retriever
    # -----------------------------------------

    retriever = vector_db.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 4,
            "fetch_k": 10,
            "lambda_mult": 0.7
        }
    )

    return retriever