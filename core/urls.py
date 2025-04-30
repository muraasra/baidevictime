# aide_victimes/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from core import views
from rest_framework.routers import DefaultRouter
from .views import (
    QuestionTransversaleViewSet,
    SoinsMedicauxViewSet,
    AppuiPsychosocialViewSet,
    PoliceSecurityViewSet,
    AssistanceJuridiqueViewSet,
    SanteMentaleViewSet,
    ReinsertionEconomiqueViewSet,
)

router = DefaultRouter()
urlpatterns = [
    path('', include(router.urls)),
]
