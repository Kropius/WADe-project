import json


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
                    allowed_attributes[subject].update(
                        parse_parameters(spec['paths'][path][verb]['parameters'], spec))
                if 'requestBody' in spec['paths'][path][verb]:
                    body_attrs = parse_request_body(spec['paths'][path][verb]['requestBody'], spec)
                    allowed_attributes[subject].update(body_attrs)
            elif verb == 'parameters':
                allowed_attributes[subject].update(
                    parse_parameters(spec['paths'][path][verb], spec))

    for subject in allowed_attributes.keys():
        allowed_attributes_subject = []
        for attribute in allowed_attributes[subject]:
            allowed_attributes_subject += [json.loads(attribute)]
        allowed_attributes[subject] = allowed_attributes_subject

    return allowed_attributes


def parse_request_body(request_body, spec):
    allowed_attributes = set()
    if 'application/json' in request_body['content']:
        schema = request_body['content']['application/json']['schema']

        if "$ref" in schema.keys():
            schema_ref = schema["$ref"].split('/')[-1]
            schema_deref = spec['components']['schemas'][schema_ref]
            properties = schema_deref['properties']
        else:
            properties = schema['properties']

        for _property in properties.keys():
            allowed_attributes.add(json.dumps({_property: "body"}))
    return allowed_attributes


def parse_parameters(parameters, spec):
    allowed_attributes = set()

    for parameter in parameters:
        if "$ref" in parameter.keys():
            parameter_ref = parameter["$ref"].split('/')[-1]
            parameter_deref = spec['components']['parameters'][parameter_ref]
            allowed_attributes.add(json.dumps({parameter_deref['name']: parameter_deref['in']}))
        else:
            allowed_attributes.add(json.dumps({parameter['name']: parameter['in']}))

    return allowed_attributes


def get_subject(path):
    path_elems = path.split("/")
    if len(path_elems[0]) > 0:
        return path_elems[0]
    return path_elems[1]


def parse(spec):
    spec = json.loads(spec)

    return {
        'allowed_operations': get_allowed_operations(spec),
        'allowed_attributes': get_allowed_attributes(spec),
        'url': spec['servers'][0]['url']
    }
