from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


def main():

    print("=" * 60)
    print("Creating Vector Database...")
    print("=" * 60)

    # -----------------------------------------
    # Load PDF
    # -----------------------------------------

    loader = PyPDFLoader(
        "rag/data/company_policy.pdf"
    )

    documents = loader.load()

    print(f"Total Pages : {len(documents)}")


    # -----------------------------------------
    # Split Documents
    # -----------------------------------------

    text_splitter = RecursiveCharacterTextSplitter(

        chunk_size=1000,

        chunk_overlap=200

    )

    chunks = text_splitter.split_documents(documents)

    print(f"Total Chunks : {len(chunks)}")


    # -----------------------------------------
    # Embedding Model
    # -----------------------------------------

    embedding_model = HuggingFaceEmbeddings(

        model_name="BAAI/bge-m3"

    )


    # -----------------------------------------
    # Create FAISS Vector Database
    # -----------------------------------------

    vector_db = FAISS.from_documents(

        chunks,

        embedding_model

    )


    # -----------------------------------------
    # Save Vector Database
    # -----------------------------------------

    vector_db.save_local(

        "rag/vector_store"

    )

    print("\n✅ Vector Database Created Successfully!")
    print("Saved inside: rag/vector_store/")


if __name__ == "__main__":

    main()