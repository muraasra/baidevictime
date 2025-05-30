# Generated by Django 5.0.6 on 2025-01-15 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0002_conversation_message_delete_chat'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='chat_images/'),
        ),
        migrations.AlterField(
            model_name='message',
            name='sender',
            field=models.CharField(max_length=10),
        ),
    ]
