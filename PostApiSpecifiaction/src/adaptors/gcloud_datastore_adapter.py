from google.cloud import datastore


def put(_id, body):
    datastore_client = datastore.Client()
    kind = "Api"
    key = datastore_client.key(kind, _id)
    fields = datastore.Entity(key=key)

    for key in body.keys():
        fields[key] = body[key]
    fields['id'] = _id

    datastore_client.put(fields)

    return None
