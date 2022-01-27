import os
from google.cloud import datastore

BUCKET_NAME = "open_api_v3_specifications"

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'avid-airway-337117-d28d91542407.json'


def put(_id, body):
    datastore_client = datastore.Client()
    kind = "Api"
    key = datastore_client.key(kind, _id)
    fields = datastore.Entity(key=key)

    for key in body.keys():
        fields[key] = body[key]

    datastore_client.put(fields)

    return None
