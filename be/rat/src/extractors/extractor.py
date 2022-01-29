from validators import validator


def extract_id(request):
    validator.validate_id(request)

    return request.args.get('id')


def extract_api_spec(request):
    body = request.get_json()
    validator.validate_api_spec(body)

    return body['id'], body['open_api_specification']
