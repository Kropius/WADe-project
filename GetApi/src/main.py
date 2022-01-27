import json

import functions_framework
import os

from adaptors import gcloud_datastore_adapter
from exceptions.precondition_failed_exception import PreconditionFailedException

from extractors import extractor

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'avid-airway-337117-d28d91542407.json'


def options(request):
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'OPTIONS,GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600'
    }

    return '', 204, headers


def get(request):
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
    }

    _id = extractor.extract(request)

    response = gcloud_datastore_adapter.get(_id)

    if response is None:
        return json.dumps({"message": "Resource with id {} not found".format(_id)}), 404, headers

    return json.dumps(response), 200, headers


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

    return json.dumps({"message": "Something went wrong. Please try again...{}".format(e)}), 500, headers


@functions_framework.http
def get_api(request):
    if request.method == 'OPTIONS':
        return options(request)
    if request.method == 'GET':
        return get(request)
    raise NotImplementedError
