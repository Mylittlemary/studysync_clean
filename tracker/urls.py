from django.urls import path
from . import views

urlpatterns = [
    path('grafik/', views.study_time_chart, name='grafik'),
]

