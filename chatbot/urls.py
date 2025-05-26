# chatbot/urls.py
from django.urls import path
from .views import ConversationListCreate, ConversationDetail
from .views_ui import ChatUI

urlpatterns = [
    path("chat-ui/", ChatUI.as_view(), name="chat-ui"),   # ← nouvelle page
    path("chat/",           ConversationListCreate.as_view()),
    path("chat/<int:conv_id>/", ConversationDetail.as_view()),
]