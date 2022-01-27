from google.cloud import storage

BUCKET_NAME = "open_api_v3_specifications"


def put(body, path):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(BUCKET_NAME)
    blob = bucket.blob(path)

    blob.upload_from_string(body)

    return "https://storage.googleapis.com/{}/{}".format(BUCKET_NAME, path)
