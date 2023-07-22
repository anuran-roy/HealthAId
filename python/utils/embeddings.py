from sentence_transformers import SentenceTransformer
import numpy as np
import tiktoken

enc = tiktoken.get_encoding("cl100k_base")

model = SentenceTransformer(
    "bert-base-nli-stsb-mean-tokens"
)  # Choosing MiniLM for the speed gains while retaining quality (Refer https://www.sbert.net/docs/pretrained_models.html)


def chunk_text(text: str) -> list[str]:
    return enc.encode(text)


def generate_chunk_embeddings(text):
    return model.encode(text).tolist()


def similarity_match(embedding_1, embedding_2) -> float:
    return np.dot(embedding_1, embedding_2) / (
        np.linalg.norm(embedding_1) * np.linalg.norm(embedding_2)
    )
