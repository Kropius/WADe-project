import json

import functions_framework
import os

from adaptors import gcloud_datastore_adapter

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'avid-airway-337117-d28d91542407.json'


def options(request):
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'OPTIONS,GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600'
    }

    return '', 204, headers


def query(request):
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
    }

    response = {
        "apis": gcloud_datastore_adapter.query()
    }

    return json.dumps(response), 200, headers


@functions_framework.errorhandler(NotImplementedError)
def handle_405(e):
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
    }

    return json.dumps({"message": "Method not allowed"}), 405, headers


@functions_framework.errorhandler(Exception)
def handle_500(e):
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
    }

    return json.dumps({"message": "Something went wrong. Please try again..."}), 500, headers


@functions_framework.http
def list_apis(request):
    if request.method == 'OPTIONS':
        return options(request)
    if request.method == 'GET':
        return query(request)
    raise NotImplementedError
