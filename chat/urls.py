from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('counselors/', views.counselors_list, name='counselors'),
    path('<int:user_pk>/', views.conversation, name='conversation'),
    path('send/', views.send_message, name='send'),
    path('poll/<int:user_pk>/', views.get_new_messages, name='poll'),
]

