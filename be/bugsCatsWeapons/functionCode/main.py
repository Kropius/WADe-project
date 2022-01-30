import functions_framework
import json

from exceptions.precondition_failed_exception import PreconditionFailedException
from exceptions.resource_not_found_exception import ResourceNotFoundException


def feline_get(request, headers):
    query_parameters = request.full_path.split('?')[1] if '?' in request.full_path else 'None'
    return json.dumps({
        "message": 'Called GET on path /feline with parameters: ' + query_parameters
    }), 200, headers


def weapon_post(request, headers):
    request_body = str(request.get_json())
    return json.dumps({
        "message": 'Called POST on path /weapon with request body: ' + request_body
    }), 201, headers


def feline_patch(request, headers):
    request_body = str(request.get_json())
    return json.dumps({
        "message": 'Called PATCH on path /feline with request body: ' + request_body
    }), 200, headers


def feline_put(request, headers):
    request_body = str(request.get_json())
    return json.dumps({
        "message": 'Called PUT on path /feline with request body: ' + request_body
    }), 200, headers


def weapon_put(request, headers):
    request_body = str(request.get_json())
    return json.dumps({
        "message": 'Called PUT on path /weapon with request body: ' + request_body
    }), 200, headers


def feline_delete(request, headers):
    query_parameters = request.full_path.split('?')[1] if '?' in request.full_path else 'None'
    return json.dumps({
        "message": 'Called DELETE on path /feline with parameters: ' + query_parameters
    }), 200, headers


def bug_delete(request, headers):
    query_parameters = request.full_path.split('?')[1] if '?' in request.full_path else 'None'
    return json.dumps({
        "message": 'Called DELETE on path /bug with parameters: ' + query_parameters
    }), 200, headers


def options(methods):
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': methods,
        'Access-Control-Allow-Headers': 'Content-Type,X-API-KEY',
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
def bugs_cats_weapons(request):
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
    }
    if request.method == 'OPTIONS':
        return options('OPTIONS,GET,POST,PUT,PATCH,DELETE')
    if request.method == 'GET' and '/feline' in request.full_path:
        return feline_get(request, headers)
    if request.method == 'POST' and '/weapon' in request.full_path:
        return weapon_post(request, headers)
    if request.method == 'PATCH' and '/feline' in request.full_path:
        return feline_patch(request, headers)
    if request.method == 'PUT':
        if '/feline' in request.full_path:
            return feline_put(request, headers)
        if '/weapon' in request.full_path:
            return weapon_put(request, headers)
    if request.method == 'DELETE':
        if '/feline' in request.full_path:
            return feline_delete(request, headers)
        if '/bug' in request.full_path:
            return bug_delete(request, headers)
    raise NotImplementedError
