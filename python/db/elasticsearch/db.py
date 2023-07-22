from elasticsearch import Elasticsearch

client = Elasticsearch(
    #     # "https://first-elastic-cloud-deployment.es.ap-south-1.aws.elastic-cloud.com",
    #     cloud_id="first-elastic-cloud-deployment:YXAtc291dGgtMS5hd3MuZWxhc3RpYy1jbG91ZC5jb206NDQzJGIxMTM4YmNlNjU5NjQ2ZDhhNWY3ZmY1ZTdkMzM3NjU1JGRiOWJkNDQ0MzFiODQ1OGU4MTg1MGUxZWU3ZGFhODk4",
    #     api_key=("Elastic.co API Key", "UDZHN1NvZ0JHeFRLNXZ2ZEtNRHg6VTFvTk1xY0NUMUtXWURyczNTNWFzZw==")
    # )
    # "https://6v0z0skrmr:m9qbspe27d@vectorsearch-demo-4233748040.us-east-1.bonsaisearch.net:443")
    "http://localhost:9200"
)

mapping_mayoclinic = {
    "mappings": {
        # "dynamic": True,
        # "_source": {
        #     "enabled": True
        # },
        "properties": {
            # "user_id": {"type": "unsigned_long"},
            "Name": {"type": "text"},
            "Overview": {"type": "text"},
            "Symptoms": {"type": "text"},
            "Causes": {"type": "text"},
            "Complications": {"type": "text"},
            "Prevention": {"type": "text"},
            "Related": {"type": "text"},
            "Risk_factors": {"type": "text"},
            "Types": {"type": "text"},
            "Name_vector": {
                "type": "dense_vector",
                "dims": 768,
                "index": True,
                "similarity": "l2_norm",
            },
            "Overview_vector": {
                "type": "dense_vector",
                "dims": 768,
                "index": True,
                "similarity": "l2_norm",
            },
            "Symptoms_vector": {
                "type": "dense_vector",
                "dims": 768,
                "index": True,
                "similarity": "l2_norm",
            },
            "Causes_vector": {
                "type": "dense_vector",
                "dims": 768,
                "index": True,
                "similarity": "l2_norm",
            },
            "Complications_vector": {
                "type": "dense_vector",
                "dims": 768,
                "index": True,
                "similarity": "l2_norm",
            },
            "Prevention_vector": {
                "type": "dense_vector",
                "dims": 768,
                "index": True,
                "similarity": "l2_norm",
            },
            "Related_vector": {
                "type": "dense_vector",
                "dims": 768,
                "index": True,
                "similarity": "l2_norm",
            },
            "Risk_factors_vector": {
                "type": "dense_vector",
                "dims": 768,
                "index": True,
                "similarity": "l2_norm",
            },
            "Types_vector": {
                "type": "dense_vector",
                "dims": 768,
                "index": True,
                "similarity": "l2_norm",
            },
        }
    }
}

mapping_drugs_com = {
    "mappings": {
        # "dynamic": True,
        # "_source": {
        #     "enabled": True
        # },
        "properties": {
            # "user_id": {"type": "unsigned_long"},
            "name": {"type": "text"},
            "overview": {"type": "text"},
            "symptoms": {"type": "text"},
            "causes": {"type": "text"},
            "omplications": {"type": "text"},
            "Prevention": {"type": "text"},
            "Related": {"type": "text"},
            "Risk_factors": {"type": "text"},
            "Types": {"type": "text"},
            "name_vector": {
                "type": "dense_vector",
                "dims": 768,
                "index": True,
                "similarity": "l2_norm",
            },
            "overview_vector": {
                "type": "dense_vector",
                "dims": 768,
                "index": True,
                "similarity": "l2_norm",
            },
            "symptoms_vector": {
                "type": "dense_vector",
                "dims": 768,
                "index": True,
                "similarity": "l2_norm",
            },
            "causes_vector": {
                "type": "dense_vector",
                "dims": 768,
                "index": True,
                "similarity": "l2_norm",
            },
            "complications_vector": {
                "type": "dense_vector",
                "dims": 768,
                "index": True,
                "similarity": "l2_norm",
            },
            "prevention_vector": {
                "type": "dense_vector",
                "dims": 768,
                "index": True,
                "similarity": "l2_norm",
            },
            "related_vector": {
                "type": "dense_vector",
                "dims": 768,
                "index": True,
                "similarity": "l2_norm",
            },
            "risk_factors_vector": {
                "type": "dense_vector",
                "dims": 768,
                "index": True,
                "similarity": "l2_norm",
            },
            "types_vector": {
                "type": "dense_vector",
                "dims": 768,
                "index": True,
                "similarity": "l2_norm",
            },
        }
    }
}


def create_index():
    response_mayoclinic = client.indices.create(
        index="mayoclinic_dense_index",
        mappings=mapping_mayoclinic,
        ignore=400,  # ignore 400 already exists code
    )

    # response_drugs_com = client.indices.create(
    #     index="drugs_com_dense_index",
    #     mappings=mapping_drugs_com,
    #     # ignore=400,  # ignore 400 already exists code
    # )

create_index()