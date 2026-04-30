from django.http import JsonResponse
from django.urls import path


def websocket_status(_request):
    return JsonResponse({"status": "ok", "service": "websocket"})


urlpatterns = [
    path("status/", websocket_status, name="websocket_status"),
]

