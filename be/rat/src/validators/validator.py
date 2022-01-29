import json

from exceptions.precondition_failed_exception import PreconditionFailedException
from openapi_spec_validator.exceptions import OpenAPIValidationError
from openapi_spec_validator import validate_spec


def validate_id(request):
    if request.args.get('id') is None:
        raise PreconditionFailedException("id was not provided.")


def validate_api_spec(body):
    validate_all_fields_exist(body)
    validate_spec_is_json(body['open_api_specification'])
    validate_spec_is_open_api_v3(body['open_api_specification'])


def validate_all_fields_exist(body):
    if not body \
            or 'id' not in body \
            or 'open_api_specification' not in body:
        raise PreconditionFailedException("missing required field in body.")


def validate_spec_is_json(spec):
    try:
        if '\\n' in spec:
            raise Exception
        json.loads(spec)
    except Exception:
        raise PreconditionFailedException("open_api_specification is not a valid json.")


def validate_spec_is_open_api_v3(spec):
    spec = json.loads(spec)
    try:
        validate_spec(spec)
    except OpenAPIValidationError as e:
        raise PreconditionFailedException("""open_api_specification is not a valid OpenApi v3 specification.
        Please use https://editor.swagger.io/ to convert it.
        OpenAPIValidationError: {}""".format(e.message))

    if 'servers' not in spec \
            or len(spec['servers']) < 1 \
            or 'url' not in spec['servers'][0]:
        raise PreconditionFailedException("missing url entry under servers field.")
