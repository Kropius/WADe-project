import functions_framework

import gcloud_storage_adapter
import gcloud_datastore_adapter
from exceptions import PreconditionFailedException
from extractor import extract


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

    _id, url, open_api_specification = extract(request)

    spec_url = gcloud_storage_adapter.put(path=_id, body=open_api_specification)

    gcloud_datastore_adapter.put(_id=_id, body={
        "spec_url": spec_url,
        "url": url
    })

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
