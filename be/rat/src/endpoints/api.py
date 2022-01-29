import json

from exceptions.resource_not_found_exception import ResourceNotFoundException
from adaptors import gcloud_datastore_adapter
from extractors import extractor

headers = {
    'Access-Control-Allow-Origin': '*',
    'Content-Type': 'application/json'
}


def get(request):
    _id = extractor.extract_id(request)

    response = gcloud_datastore_adapter.get(_id)

    if response is None:
        raise ResourceNotFoundException("Resource with id {} not found".format(_id))

    return json.dumps(response), 200, headers
