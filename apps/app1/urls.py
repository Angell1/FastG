from django.urls import path
from .views import TestView


app_name = 'app1'

urlpatterns = [
    path('test/',TestView.as_view()),
]