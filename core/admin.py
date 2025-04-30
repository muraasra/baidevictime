from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Category, Service, Question, Choice

admin.site.register(Category)
admin.site.register(Service)
admin.site.register(Question)
admin.site.register(Choice)