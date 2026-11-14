from rest_framework.views import exception_handler


def portal_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None and response.status_code == 404:
        response.data = {"detail": "This record is no longer available or is not shared with you. Return to the list to see available records."}
    return response
