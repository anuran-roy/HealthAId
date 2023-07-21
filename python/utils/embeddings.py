from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)  # Choosing MiniLM for the speed gains while retaining quality (Refer https://www.sbert.net/docs/pretrained_models.html)


def generate_chunk_embeddings(text):
    return model.encode(text).tolist()
