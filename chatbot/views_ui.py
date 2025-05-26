# chatbot/views_ui.py
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt   # évite les soucis CSRF Ajax

@method_decorator(csrf_exempt, name="dispatch")
class ChatUI(TemplateView):
    template_name = "chatbot/chat.html"