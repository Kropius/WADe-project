import json

from exceptions.precondition_failed_exception import PreconditionFailedException


def get_allowed_operations(spec):
    allowed_operations = {
        'DELETE': set(),
        'PATCH': set(),
        'POST': set(),
        'PUT': set(),
        'GET': set(),
    }
    for path in spec['paths'].keys():
        subject = get_subject(path)
        for verb in spec['paths'][path].keys():
            if verb in ['get', 'post', 'put', 'delete', 'patch']:
                allowed_operations[verb.upper()].add(subject)

    for verb in allowed_operations.keys():
        allowed_operations[verb] = list(allowed_operations[verb])

    return allowed_operations


def get_allowed_attributes(spec):
    allowed_attributes = {}

    for path in spec['paths'].keys():
        subject = get_subject(path)
        if subject not in allowed_attributes:
            allowed_attributes[subject] = set()
        for verb in spec['paths'][path].keys():
            if verb in ['get', 'post', 'put', 'delete', 'patch']:
                if 'parameters' in spec['paths'][path][verb]:
                    allowed_attributes[subject].update(parse_parameters(spec['paths'][path][verb]['parameters']))
                if 'requestBody' in spec['paths'][path][verb]:
                    body_attrs = parse_request_body(spec['paths'][path][verb]['requestBody'])
                    allowed_attributes[subject].update(body_attrs)
            elif verb == 'parameters':
                allowed_attributes[subject].update(
                    parse_parameters(spec['paths'][path][verb]))

    for subject in allowed_attributes.keys():
        allowed_attributes_subject = []
        for attribute in allowed_attributes[subject]:
            allowed_attributes_subject += [json.loads(attribute)]
        allowed_attributes[subject] = allowed_attributes_subject

    return allowed_attributes


def parse_request_body(request_body):
    allowed_attributes = set()
    if 'application/json' in request_body['content']:
        schema = request_body['content']['application/json']['schema']
        while 'items' in schema:
            schema = schema['items']

        if 'properties' in schema:
            properties = schema['properties']

            for _property in properties.keys():
                allowed_attributes.add(json.dumps({_property: "body"}))
    return allowed_attributes


def parse_parameters(parameters):
    allowed_attributes = set()

    for parameter in parameters:
        allowed_attributes.add(json.dumps({parameter['name']: parameter['in']}))

    return allowed_attributes


def get_subject(path):
    path_elems = path.split("/")
    if len(path_elems[0]) > 0:
        return path_elems[0]
    return path_elems[1]


def explode_paths(spec):
    spec['paths'] = explode_dict(spec['paths'], spec)
    return spec


def explode_ref(path, spec):
    if path[:2] != "#/":
        raise PreconditionFailedException("$ref path must begin with #/. Other forms not supported.")
    path_elems = path[2:].split('/')
    ref_dict = spec
    for k in path_elems:
        if k not in ref_dict.keys():
            raise PreconditionFailedException("$ref path is invalid.")
        ref_dict = ref_dict[k]
    return explode_dict(ref_dict, spec)


def explode_dict(d, spec):
    if "$ref" in d.keys():
        return explode_ref(d["$ref"], spec)

    d_copy = {}
    for k, v in d.items():
        if isinstance(v, dict):
            d_copy[k] = explode_dict(v, spec)
        elif isinstance(v, list):
            d_copy[k] = explode_list(v, spec)
        else:
            d_copy[k] = v
    return d_copy


def explode_list(l, spec):
    l_copy = [None for _ in range(len(l))]
    for k, v in enumerate(l):
        if isinstance(v, dict):
            l_copy[k] = explode_dict(v, spec)
        elif isinstance(v, list):
            l_copy[k] = explode_list(v, spec)
        else:
            l_copy[k] = v
    return l_copy


def parse(spec):
    spec = json.loads(spec)
    spec = explode_paths(spec)

    return {
        'allowed_operations': get_allowed_operations(spec),
        'allowed_attributes': get_allowed_attributes(spec),
        'url': spec['servers'][0]['url']
    }
