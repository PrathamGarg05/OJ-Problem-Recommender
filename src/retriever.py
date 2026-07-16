from src.embed_store import get_collection
from src.config import EXACT_MATCH_THRESHOLD, TOP_K, SIMILARITY_THRESHOLD

def retrieve(query, top_k = TOP_K):
    collection = get_collection()
    result = collection.query(
        query_texts=[query],
        n_results=top_k
    )
    print([d for d in result['distances'][0]])
    filtered_results = [i for i , d in enumerate(result['distances'][0]) if d < SIMILARITY_THRESHOLD and d > EXACT_MATCH_THRESHOLD]
    result['metadatas'][0] = [result['metadatas'][0][i] for i in filtered_results]
    result['documents'][0] = [result['documents'][0][i] for i in filtered_results]
    return result

