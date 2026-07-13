from src.kb_loader import entry_to_text
from src.embed_store import get_collection, store_entries
import os
import json
from src.config import KB_DIR

def load_all_entries():
    entries=[]
    for filename in os.listdir(KB_DIR):
        if filename.endswith(".json"):
            with open(f"{KB_DIR}/{filename}") as f:
                entries.append(json.load(f))
    return entries

entries = load_all_entries()
texts = [entry_to_text(entry) for entry in entries]

collection = get_collection()
store_entries(collection, entries, texts)
print(f"Stored {len(entries)} entries in the knowledge base.")