from google.cloud import datastore


def get(_id):
    datastore_client = datastore.Client()
    key = datastore_client.key("Api", _id)

    return datastore_client.get(key)
