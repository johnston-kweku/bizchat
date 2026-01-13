from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.home, name='chat-home'),
    path('<str:username>/', views.chat, name='chat'),
    path('ajax/inbox/', views.inbox_ajax, name='inbox_ajax'),
    path('ajax/heartbeat/', views.update_last_seen, name='heartbeat'),
    path('ajax/read/<str:username>/', views.mark_read, name='mark_read'),
    path('ajax/<str:username>/', views.ajax_chat, name='chat_ajax'),
]

