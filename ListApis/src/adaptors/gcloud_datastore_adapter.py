from google.cloud import datastore


def query():
    datastore_client = datastore.Client()
    _query = datastore_client.query(kind="Api")
    return list(_query.fetch())
