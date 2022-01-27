import os
from google.cloud import storage

BUCKET_NAME = "open_api_v3_specifications"

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'avid-airway-337117-d28d91542407.json'


def put(body, path):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(BUCKET_NAME)
    blob = bucket.blob(path)

    blob.upload_from_string(body)

    return "https://storage.cloud.google.com/{}/{}".format(BUCKET_NAME, path)
