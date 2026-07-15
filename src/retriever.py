from src.embed_store import get_collection
from src.config import TOP_K

def retrieve(query, top_k = TOP_K):
    collection = get_collection()
    result = collection.query(
        query_texts=[query],
        n_results=top_k
    )
    return result

result = retrieve("Given a string s, find the longest palindromic subsequence's length in s.A subsequence is a sequence that can be derived from another sequence by deleting some or no elements without changing the order of the remaining elements.", top_k=3)
print(result)