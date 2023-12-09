from django.http import JsonResponse


def handler(request, exception):
    message = 'this path not found'
    response = JsonResponse(data={'error': message})
    response.status_code = 404
    return response


def handler_505(request):
    message = 'your internet not good'
    response = JsonResponse(data={'error': message})
    response.status_code = 505
    return response
