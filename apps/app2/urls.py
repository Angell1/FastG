from django.urls import path
from .views import TestView


app_name = 'app2'

urlpatterns = [
    path('test/',TestView.as_view()),
]