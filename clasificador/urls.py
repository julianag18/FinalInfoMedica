from django.urls import path
from . import views

urlpatterns = [
    path('', views.predecir_grd, name='predecir_grd'),
]
