import functions_framework
import json
import os

from exceptions.precondition_failed_exception import PreconditionFailedException
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
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
    }

    _id, open_api_specification = extractor.extract(request)

    body = parser.parse(open_api_specification)

    spec_url = gcloud_storage_adapter.put(path=_id, body=open_api_specification)

    body['spec_url'] = spec_url

    gcloud_datastore_adapter.put(_id=_id, body=body)

    return "", 201, headers


@functions_framework.errorhandler(NotImplementedError)
def handle_405(e):
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
    }

    return json.dumps({"message": "Method not allowed"}), 405, headers


@functions_framework.errorhandler(PreconditionFailedException)
def handle_412(e):
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
    }

    return json.dumps({"message": e.message}), 412, headers


@functions_framework.errorhandler(Exception)
def handle_500(e):
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
    }

    return json.dumps({"message": "Something went wrong. Please try again..."}), 500, headers


@functions_framework.http
def post_api(request):
    if request.method == 'OPTIONS':
        return options(request)
    if request.method == 'POST':
        return post(request)
    raise NotImplementedError
