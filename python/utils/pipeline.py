from utils.elasticsearch import total_search, vector_search, send_to_elasticsearch
from utils.embeddings import generate_chunk_embeddings
from db.elasticsearch.db import client

def get_data(query: str, source: str = "mayoclinic", threshold: float = 0.002, limit: int=10) -> str:
    query_embedding = generate_chunk_embeddings(query)

    required_fields = [
        "Name",
        "Overview",
        "Symptoms",
        "Causes",
        "Complications",
        "Prevention",
        "Related",
        "Risk_factors",
        "Types"
    ]
    results = total_search(content_vector=query_embedding, fields=required_fields, index=f"{source}_index", client=client, threshold=threshold, limit=limit)

    print([x["_score"] for x in results])
    relevant_results = list(map(lambda x: x["_source"], results))

    print("Total results = ", len(results))
    print("Relevant results = ", len(relevant_results))

    joined_res = []
    for relevant_result in relevant_results:
        joined_data = "".join(
            f"\n```{key}\n{value}\n```\n"
            for key, value in relevant_result.items()
            if key in required_fields
        )
        joined_res.append(joined_data)

    final_str = "\n\n".join(joined_res).replace("\nNULL\n```", "\n```")

    return final_str[:min(len(final_str), 1500)]

if __name__ == "__main__":
    data = get_data("I have a high temperature on my head.")
    print(data[:200])