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


def get(request):
    headers = {
        'Access-Control-Allow-Origin': '*'
    }

    url_elems = request.url.split('?')[0].strip('/').split('/')
    _id = url_elems[-1]
    check = url_elems[-2]
    domain = url_elems[-3]
    # todo: add better validators
    if check != 'apis' and domain[:4] != 'http':
        return "Endpoint not found", 404, headers

    response = gcloud_datastore_adapter.get(_id)

    if response is None:
        return "Resource with id {} not found".format(_id), 404, headers

    return json.dumps(response), 200, headers


@functions_framework.http
def get_api(request):
    if request.method == 'OPTIONS':
        return options(request)
    if request.method == 'GET':
        return get(request)
    return "{} is not supported on this endpoint".format(request.method), 405
