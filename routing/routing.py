from django.urls import path

from .consumers import CounselorConsumer, StudentConsumer

websocket_urlpatterns = [
    path("ws/counselor/<int:counselor_id>/", CounselorConsumer.as_asgi()),
    path("ws/student/<int:student_id>/", StudentConsumer.as_asgi()),
]

