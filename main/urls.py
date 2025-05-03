from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('quiz/<int:student_id>/', quiz, name='quiz'),
]