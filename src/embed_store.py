import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from src.config import CHROMA_PATH, COLLECTION_NAME, EMBEDDING_MODEL

def get_collection():
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    ef = SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL)
    return client.get_or_create_collection(name=COLLECTION_NAME, embedding_function=ef)

def store_entries(collection, entries, texts):
    collection.upsert(
        documents=texts,
        metadatas=entries,
        ids=[e['title'] for e in entries]
    )