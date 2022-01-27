from validators import validator


def extract(request):
    body = request.get_json()
    validator.validate(body)

    return body['id'], body['open_api_specification']
