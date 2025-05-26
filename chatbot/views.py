from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import APIException
import logging 
logger = logging.getLogger(__name__)# en haut du fichier

from .models import Conversation, Message
from .serializers import ConversationSerializer
from .chatbot_logic import generate_reply

MAX_HISTORY = 40  # messages totaux (20 échanges)

# ---------------- util ----------------
def get_session_key(request):
    if not request.session.session_key:
        request.session.save()
    return request.session.session_key
# --------------------------------------

class ConversationListCreate(APIView):
    """GET = liste ; POST = nouveau chat + 1er message."""
    authentication_classes = []   # aucune auth
    permission_classes     = []

    def get(self, request):
        sk = get_session_key(request)
        qs = Conversation.objects.filter(session_key=sk).order_by("-updated_at")
        return Response(ConversationSerializer(qs, many=True).data)

    def post(self, request):
        msg = request.data.get("message")
        if not msg:
            return Response({"error": "message is required"}, status=400)

        sk = get_session_key(request)
        conv = Conversation.objects.create(
            session_key=sk,
            title=msg[:60] or "Nouvelle conversation"
        )

        Message.objects.create(conversation=conv, sender="user", content=msg)
        reply = generate_reply([], msg)
        Message.objects.create(conversation=conv, sender="assistant", content=reply)

        return Response(ConversationSerializer(conv).data, status=201)


class ConversationDetail(APIView):
    """GET = historique ; POST = ajouter un message + réponse."""
    authentication_classes = []
    permission_classes     = []

    def _get_conv(self, request, conv_id):
        sk = get_session_key(request)
        return get_object_or_404(Conversation, id=conv_id, session_key=sk)

    def get(self, request, conv_id):
        conv = self._get_conv(request, conv_id)
        return Response(ConversationSerializer(conv).data)

    def post(self, request, conv_id):
        conv = self._get_conv(request, conv_id)
        msg  = request.data.get("message")
        if not msg:
            return Response({"error": "message is required"}, status=400)

        Message.objects.create(conversation=conv, sender="user", content=msg)

        history_qs = conv.messages.all().order_by("-created_at")[:MAX_HISTORY]
        hist = [{"role": m.sender, "content": m.content} for m in reversed(history_qs)]
        try:
            reply = generate_reply(hist, msg)
        except Exception as exc:
            logger.exception(exc, request)
            # 500 JSON lisible par le front
            raise APIException("Erreur interne du chatbot, réessaie plus tard.")

        Message.objects.create(conversation=conv, sender="assistant", content=reply)
        conv.save(update_fields=["updated_at"])

        return Response({"reply": reply}, status=201)