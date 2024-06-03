from django.urls import path
from chatting.views import ListAllMessages
from django.contrib.auth.decorators import login_required


urlpatterns=[
    path("", ListAllMessages.as_view(), name="messages"),
    path('like/', ListAllMessages.as_view(), name='like_message')
]