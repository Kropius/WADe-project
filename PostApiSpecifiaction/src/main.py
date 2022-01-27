import functions_framework

from exceptions.precondition_failed_exception import PreconditionFailedException
from adaptors import gcloud_storage_adapter, gcloud_datastore_adapter
from extractors import extractor
from parsers import parser


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


@functions_framework.errorhandler(PreconditionFailedException)
def precondition_failed(e):
    return str(e), 412


@functions_framework.http
def post_api(request):
    if request.method == 'OPTIONS':
        return options(request)
    if request.method == 'POST':
        return post(request)
    raise ZeroDivisionError()
