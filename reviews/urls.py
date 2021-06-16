from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("user_input/", views.user_input, name='user-input'),
    path("user_input/<int:user_input_id>/",
         views.temp_result, name='temp-result'),
    path("user_input/<int:user_input_id>/k/",
         views.kakao_result, name='kakao-result'),
]
