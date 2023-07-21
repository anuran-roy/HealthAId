from db.postgres.models import models
from utils.embeddings import generate_chunk_embeddings

def get_condition_from_mayoclinic(query: str) -> str:
    embedding1 = generate_chunk_embeddings(query)
    