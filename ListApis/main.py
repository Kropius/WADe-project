import functions_framework


def options(request):
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'OPTIONS,GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600'
    }

    return '', 204, headers


def post(request):
    headers = {
        'Access-Control-Allow-Origin': '*'
    }

    return "Hello world!", 200, headers


@functions_framework.errorhandler(ZeroDivisionError)
def handle_zero_division(e):
    return "I'm a teapot", 418


@functions_framework.http
def list_apis(request):
    if request.method == 'OPTIONS':
        return options(request)
    if request.method == 'GET':
        return post(request)
    raise ZeroDivisionError()
