from validator import validate


def extract(request):
    body = request.get_json()
    validate(body)

    return body['id'], body['url'], body['open_api_specification']
