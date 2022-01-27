import functions_framework
import os

from adaptors import gcloud_storage_adapter, gcloud_datastore_adapter
from extractors import extractor
from parsers import parser


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'avid-airway-337117-d28d91542407.json'


def options(_):
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'OPTIONS,POST',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600'
    }

    return '', 204, headers


def post(request):
    headers = {
        'Access-Control-Allow-Origin': '*'
    }

    _id, open_api_specification = extractor.extract(request)

    body = parser.parse(open_api_specification)

    spec_url = gcloud_storage_adapter.put(path=_id, body=open_api_specification)

    body['spec_url'] = spec_url

    gcloud_datastore_adapter.put(_id=_id, body=body)

    return "", 201, headers


@functions_framework.http
def post_api(request):
    if request.method == 'OPTIONS':
        return options(request)
    if request.method == 'POST':
        return post(request)
    return "{} is not supported on this endpoint".format(request.method), 405
