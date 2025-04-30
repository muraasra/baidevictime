# aide_victimes/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from core import views
from rest_framework.authtoken.views import obtain_auth_token

from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import CustomTokenObtainPairView

from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


schema_view = get_schema_view(
   openapi.Info(
      title="Cartographie des services de prise en charge API",
      default_version='',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="wilfriedtayou6@gmail.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
   path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
  
]

urlpatterns += [
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

router = routers.DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'services', views.ServiceViewSet)
router.register(r'questions', views.QuestionViewSet)
router.register(r'choices', views.ChoiceViewSet)
router.register(r'user', views.userViewSet,basename='user')
router.register(r'question-transversale', views.QuestionTransversaleViewSet, basename='question-transversale')
router.register(r'soins-medicaux', views.SoinsMedicauxViewSet, basename='soins-medicaux')
router.register(r'appui-psychosocial', views.AppuiPsychosocialViewSet, basename='appui-psychosocial')
router.register(r'police-security', views.PoliceSecurityViewSet, basename='police-security')
router.register(r'assistance-juridique', views.AssistanceJuridiqueViewSet, basename='assistance-juridique')
router.register(r'sante-mentale', views.SanteMentaleViewSet, basename='sante-mentale')
router.register(r'reinsertion-economique', views.ReinsertionEconomiqueViewSet, basename='reinsertion-economique')


urlpatterns += [
    path('api/api-token-auth/',obtain_auth_token,name='api_token_auth'),
    
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/submit-form/', views.submit_form, name='submit_form'),
    # Optionnel: route pour le frontend React (voir section Intégration React)
    path('', views.FrontendAppView.as_view()),  # on y reviendra
]

from core.views import FrontendAppView

urlpatterns += [
    path('', FrontendAppView.as_view(), name='frontend'),
]