from django.contrib import admin
from .models import Conversation, Message

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ("id", "session_key", "title", "created_at", "updated_at")
    search_fields = ("title", "session_key")

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "conversation", "sender", "short_content", "created_at")
    list_filter  = ("sender",)
    search_fields = ("content",)

    def short_content(self, obj):
        return (obj.content[:60] + "…") if len(obj.content) > 60 else obj.content
    short_content.short_description = "Contenu"