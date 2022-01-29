from google.cloud import datastore


def get(_id):
    datastore_client = datastore.Client()
    key = datastore_client.key("Api", _id)

    return datastore_client.get(key)


def query():
    datastore_client = datastore.Client()
    _query = datastore_client.query(kind="Api")
    return list(_query.fetch())


def put(_id, body):
    datastore_client = datastore.Client()
    kind = "Api"
    key = datastore_client.key(kind, _id)
    fields = datastore.Entity(key=key)

    for key in body.keys():
        fields[key] = body[key]

    datastore_client.put(fields)

    return None
