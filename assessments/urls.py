from django.urls import path
from . import views

app_name = 'assessments'

urlpatterns = [
    path('', views.assessment_start, name='start'),
    path('take/', views.take_assessment, name='take'),
    path('result/<int:pk>/', views.assessment_result, name='result'),
    path('my-results/', views.my_results, name='my_results'),
]

