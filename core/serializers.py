# core/serializers.py
from rest_framework import serializers
from .models import (Category, Service, Question, Choice,QuestionTransversale,
    SoinsMedicaux,
    AppuiPsychosocial,
    PoliceSecurity,
    AssistanceJuridique,
    SanteMentale,
    ReinsertionEconomique,)
from django.contrib.auth.models import User 


class UserSerializer2(serializers.ModelSerializer):
    author_services = serializers.PrimaryKeyRelatedField(many=True,read_only=True, source='service_set')
    class Meta:
        model = User
        fields = ['id','username','email','last_name','author_services']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class ServiceSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)  # Include category details
    category_id = serializers.PrimaryKeyRelatedField(source='category', queryset=Category.objects.all(), write_only=True)
    get_address_phone = serializers.SerializerMethodField()
    author = UserSerializer2(read_only=True)  # Use the full UserSerializer for detailed author info

    class Meta:
        model = Service
        fields = ['id', 'name', 'category', 'category_id', 'address', 'phone', 'latitude', 'longitude', 'get_address_phone', 'author']
        read_only_fields = ['author']  # Explicitly make 'author' a read-only field

    def get_address_phone(self, obj):
        return obj.get_address_phone()

    def create(self, validated_data):
        # Automatically set the author to the currently authenticated user
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            validated_data['author'] = request.user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Ensure the author field is not updated
        validated_data.pop('author', None)
        return super().update(instance, validated_data)
    
class UserSerializer(serializers.ModelSerializer):
    # Utiliser un ServiceSerializer imbriqué pour afficher tous les détails des services créés par l'utilisateur
    author_services = ServiceSerializer(many=True, read_only=True, source='service_set')

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'last_name', 'author_services']
        # Utilise `service_set` qui est la relation inversée du modèle Service vers User.

    
class ChoiceSerializer(serializers.ModelSerializer):
    recommended_category = CategorySerializer(read_only=True)
    recommended_category_id = serializers.PrimaryKeyRelatedField(source='recommended_category', queryset=Category.objects.all(), write_only=True)
    class Meta:
        model = Choice
        fields = ['id', 'text', 'recommended_category', 'recommended_category_id']

class QuestionSerializer(serializers.ModelSerializer):
    # on imbrique les choix dans la question
    choices = ChoiceSerializer(many=True, read_only=True)
    class Meta:
        model = Question
        fields = ['id', 'text', 'choices']
        
        
        
  
class SoinsMedicauxSerializer(serializers.ModelSerializer):

    class Meta:
        model = SoinsMedicaux
        fields = '__all__'


class AppuiPsychosocialSerializer(serializers.ModelSerializer):

    class Meta:
        model = AppuiPsychosocial
        fields = '__all__'


class PoliceSecuritySerializer(serializers.ModelSerializer):

    class Meta:
        model = PoliceSecurity
        fields = '__all__'


class AssistanceJuridiqueSerializer(serializers.ModelSerializer):

    class Meta:
        model = AssistanceJuridique
        fields = '__all__'


class SanteMentaleSerializer(serializers.ModelSerializer):

    class Meta:
        model = SanteMentale
        fields = '__all__'


class ReinsertionEconomiqueSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReinsertionEconomique
        fields = '__all__'

      
class QuestionTransversaleSerializer(serializers.ModelSerializer):
    
    category = CategorySerializer(read_only=True)  # Include category details
    category_id = serializers.PrimaryKeyRelatedField(source='category', queryset=Category.objects.all(), write_only=True)
    soins_medicaux = SoinsMedicauxSerializer(read_only=True)
    appui_psychosocial = AppuiPsychosocialSerializer(read_only=True)
    police_securite = PoliceSecuritySerializer(read_only=True)
    assistance_juridique = AssistanceJuridiqueSerializer(read_only=True)
    sante_mentale = SanteMentaleSerializer(read_only=True)
    reinsertion_economique = ReinsertionEconomiqueSerializer(read_only=True)

    class Meta:
        model = QuestionTransversale
        fields = '__all__'
         # Explicitly make 'author' a read-only field

    def create(self, validated_data):
        # Automatically set the author to the currently authenticated user
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            validated_data['author'] = request.user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Ensure the author field is not updated
        validated_data.pop('author', None)
        return super().update(instance, validated_data)

