from django.conf import settings
from django.db import models


class Conversation(models.Model):
    # utilisateur facultatif (si un jour tu ajoutes l’auth)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="conversations"
    )
    # clé de session qui “possède” la conversation
    session_key = models.CharField(max_length=40, db_index=True, null=True, blank=True)

    title       = models.CharField(max_length=120, default="Nouvelle conversation")
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    def _str_(self):
        return f"{self.title} ({self.session_key or self.user})"


class Message(models.Model):
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="messages"
    )
    sender       = models.CharField(max_length=10, choices=[("user", "user"),
                                                            ("assistant", "assistant")])
    content      = models.TextField()
    created_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def _str_(self):
        return f"{self.sender[:1].upper()}:{self.content[:30]}…"