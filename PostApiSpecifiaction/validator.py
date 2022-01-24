import json

from exceptions import PreconditionFailedException
from openapi_spec_validator import validate_spec
from openapi_spec_validator.exceptions import OpenAPIValidationError


def validate(body):
    validate_all_fields_exist(body)
    validate_spec_is_json(body['open_api_specification'])
    validate_spec_is_open_api_v3(body['open_api_specification'])


def validate_all_fields_exist(body):
    if not body or 'id' not in body \
            or 'url' not in body \
            or 'open_api_specification' not in body:
        raise PreconditionFailedException("missing required field in body.")


def validate_spec_is_json(spec):
    try:
        json.loads(spec)
    except Exception:
        raise PreconditionFailedException("open_api_specification is not a valid json.")


def validate_spec_is_open_api_v3(spec):
    try:
        validate_spec(json.loads(spec))
    except OpenAPIValidationError as e:
        raise PreconditionFailedException("""open_api_specification is not a valid OpenApi v3 specification.
        Please use https://editor.swagger.io/ to convert it.
        OpenAPIValidationError: {}""".format(e.message))
