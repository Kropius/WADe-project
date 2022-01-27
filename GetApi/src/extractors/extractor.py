from validators import validator


def extract(request):
    validator.validate(request)

    return request.args.get('id')
