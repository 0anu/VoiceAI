from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

class EmbeddingsManager:

    def __init__(self, model_name="sentence-transformers/all-mpnet-base-v2"):
        self.embeddings = HuggingFaceEmbeddings(model_name=model_name)

        self.vector_store = InMemoryVectorStore(self.embeddings)

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            add_start_index=True
        )

    def load_csv_documents(self, csv_path, source_column="description"):
        return CSVLoader(csv_path, source_column=source_column).load()
    
    def add_documents(self, documents):
        return self.vector_store.add_documents(
            documents = self.text_splitter.split_documents(documents)
        )
    
    def retrive_context(self, query, k=2):
        docs = self.vector_store.similarity_search(query, k=k)

        serialized = "\n\n".join(
            f"Source: {d.metadata}\nContent: {d.page_content}" for d in docs
        )

        return serialized, docs
    
    