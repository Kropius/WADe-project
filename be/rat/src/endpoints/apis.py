import json

from adaptors import gcloud_datastore_adapter
from adaptors import gcloud_storage_adapter
from extractors import extractor
from parsers import parser

headers = {
    'Access-Control-Allow-Origin': '*',
    'Content-Type': 'application/json'
}


def query(request):
    response = {
        "apis": gcloud_datastore_adapter.query()
    }

    return json.dumps(response), 200, headers


def post(request):
    _id, open_api_specification = extractor.extract_api_spec(request)

    body = parser.parse(open_api_specification)

    spec_url = gcloud_storage_adapter.put(path=_id, body=open_api_specification)

    body['spec_url'] = spec_url
    body['id'] = _id

    gcloud_datastore_adapter.put(_id=_id, body=body)

    return json.dumps(body), 201, headers

