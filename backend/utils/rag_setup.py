import chromadb
import torch
from sentence_transformers import SentenceTransformer
from chromadb.config import Settings
import json

class BGEEmbeddingFunction:
    def __init__(self):
        device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
        print(f"Using device: {device}")
        self.device = device
        self.model = SentenceTransformer("BAAI/bge-large-en", device=device)
    
    def __call__(self, input: list[str]) -> list[list[float]]:
        if isinstance(input, str):
            input = [input]
        embeddings = self.model.encode(input, normalize_embeddings=True)
        return embeddings.tolist()

def init_chroma(embedding_function):
    client = chromadb.PersistentClient(
        path="./chroma_db",
        settings=Settings(
            anonymized_telemetry=False,
            allow_reset=True,
            persist_directory="./chroma_db",
        )
    )
    
    collection = client.get_or_create_collection(
        name="conversations",
        embedding_function=embedding_function,
        metadata={"description": "Conversation QA pairs"}
    )
    
    return collection

# Initialize embedding function and collection
embedding_function = BGEEmbeddingFunction()
collection = init_chroma(embedding_function)