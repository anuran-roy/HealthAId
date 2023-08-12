from typing import Any
from elasticsearch import helpers

def send_to_elasticsearch(client, documents: dict[str, Any], index: str) -> Any:
    response = helpers.bulk(
        client,
        documents,
        index=index
    )
    return response


def vector_search(client, content_vector: list[float], index: str, field: str, limit: int=10) -> list[dict]:
    script_query = {
        "knn":{
            "k": 10,
            "num_candidates": limit,
            "field": field,
            "query_vector": content_vector
        }
    }
    
    response = client.knn_search(
        body=script_query,
        index=index,
    )["hits"]["hits"]
    
    return response

# new_docs[0]["Symptoms_vector"]
# vector_search(client, content_vector=new_docs[0]["Symptoms_vector"], index="mayoclinic_index", field="Symptoms_vector")
def total_search(client, content_vector: list[float], fields=[], threshold: float=0.6, index="mayoclinic_index", limit=10):
    all_results: list[dict] = []

    for field in fields:
        all_results += vector_search(client, content_vector=content_vector, index=index, field=f"{field}_vector", limit=limit)

    return list(filter(lambda doc: doc["_score"] > threshold, all_results))
