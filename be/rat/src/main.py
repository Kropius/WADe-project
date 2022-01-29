import functions_framework
import json
import os

from exceptions.precondition_failed_exception import PreconditionFailedException
from exceptions.resource_not_found_exception import ResourceNotFoundException
from endpoints.apis import query as apis_endpoint_query
from endpoints.apis import post as apis_endpoint_post
from endpoints.api import get as api_endpoint_get

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'avid-airway-337117-d28d91542407.json'


def options(methods):
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': methods,
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600'
    }

    return '', 204, headers


@functions_framework.errorhandler(ResourceNotFoundException)
def handle_404(e):
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
    }

    return json.dumps({
        "message": e.message,
        "code": 404
    }), 404, headers


@functions_framework.errorhandler(NotImplementedError)
def handle_405(e):
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
    }

    return json.dumps({
        "message": "Method not allowed",
        "code": 405
    }), 405, headers


@functions_framework.errorhandler(PreconditionFailedException)
def handle_412(e):
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
    }

    return json.dumps({
        "message": e.message,
        "code": 412
    }), 412, headers


@functions_framework.errorhandler(Exception)
def handle_500(e):
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
    }

    return json.dumps({
        "message": "Something went wrong. Please try again...{}".format(e),
        "code": 500
    }), 500, headers


@functions_framework.http
def api_endpoint(request):
    if request.method == 'OPTIONS':
        return options('OPTIONS,GET')
    if request.method == 'GET':
        return api_endpoint_get(request)
    raise NotImplementedError


@functions_framework.http
def apis_endpoint(request):
    if request.method == 'OPTIONS':
        return options('OPTIONS,GET,POST')
    if request.method == 'GET':
        return apis_endpoint_query(request)
    if request.method == 'POST':
        return apis_endpoint_post(request)
    raise NotImplementedError
