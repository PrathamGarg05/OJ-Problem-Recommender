from src.embed_store import get_collection
from src.config import TOP_K

def retrieve(query, top_k = TOP_K):
    collection = get_collection()
    result = collection.query(
        query_texts=[query],
        n_results=top_k
    )
    return result

