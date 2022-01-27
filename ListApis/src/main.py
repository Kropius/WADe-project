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
        'Access-Control-Allow-Origin': '*'
    }

    response = {
        "apis": gcloud_datastore_adapter.query()
    }

    return json.dumps(response), 200, headers


@functions_framework.http
def list_apis(request):
    if request.method == 'OPTIONS':
        return options(request)
    if request.method == 'GET':
        return query(request)
    return "{} is not supported on this endpoint".format(request.method), 405
