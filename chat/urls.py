from django.urls import path
from . import views

urlpatterns = [  # Fixed typo: was 'urlpaterns'
    path('', views.user_list, name='user_list'),
    path('<int:receiver_id>/', views.chatroom, name='chatroom'),
    path('messages/<int:receiver_id>/', views.get_messages, name='get_messages'),
]