from exceptions.precondition_failed_exception import PreconditionFailedException


def validate(request):
    if request.args.get('id') is None:
        raise PreconditionFailedException("id was not provided.")
