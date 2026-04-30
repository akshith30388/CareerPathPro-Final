from django.urls import path
from . import views

app_name = 'recommendations'

urlpatterns = [
    path('', views.recommendation_list, name='list'),
    path('<int:pk>/', views.recommendation_detail, name='detail'),
    path('generate/<int:result_pk>/', views.generate_from_result, name='generate'),
]

