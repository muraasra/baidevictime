from django.shortcuts import render

# core/views.py
from rest_framework import viewsets
from .models import (Category, Service, Question, Choice,QuestionTransversale,
    SoinsMedicaux,
    AppuiPsychosocial,
    PoliceSecurity,
    AssistanceJuridique,
    SanteMentale,
    ReinsertionEconomique,
)
from .serializers import (CategorySerializer, ServiceSerializer, QuestionSerializer, ChoiceSerializer, UserSerializer, QuestionTransversaleSerializer,
    SoinsMedicauxSerializer,
    AppuiPsychosocialSerializer,
    PoliceSecuritySerializer,
    AssistanceJuridiqueSerializer,
    SanteMentaleSerializer,
    ReinsertionEconomiqueSerializer,
)
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser,IsAuthenticated,AllowAny,IsAuthenticatedOrReadOnly
import os
from django.http import HttpResponse, Http404
from django.views import View
from django.contrib.auth import get_user_model

User = get_user_model()

from rest_framework.viewsets import ModelViewSet

@method_decorator(csrf_exempt,name='dispatch')
class userViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
@method_decorator(csrf_exempt,name='dispatch')
class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    permission_classes= [IsAuthenticated,IsAdminUser]
    serializer_class = ServiceSerializer

    # Optionnel : action personnalisée ou filtre par catégorie
    def get_queryset(self):
        """
        Filtrer les services par catégorie via ?category=<id> 
        """
        qs = Service.objects.all()
        category_id = self.request.query_params.get('category')
        if category_id:
            qs = qs.filter(category__id=category_id)
        return qs

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    

class QuestionTransversaleViewSet(ModelViewSet):
    queryset = QuestionTransversale.objects.all()
    serializer_class = QuestionTransversaleSerializer


class SoinsMedicauxViewSet(ModelViewSet):
    queryset = SoinsMedicaux.objects.all()
    serializer_class = SoinsMedicauxSerializer


class AppuiPsychosocialViewSet(ModelViewSet):
    queryset = AppuiPsychosocial.objects.all()
    serializer_class = AppuiPsychosocialSerializer


class PoliceSecurityViewSet(ModelViewSet):
    queryset = PoliceSecurity.objects.all()
    serializer_class = PoliceSecuritySerializer


class AssistanceJuridiqueViewSet(ModelViewSet):
    queryset = AssistanceJuridique.objects.all()
    serializer_class = AssistanceJuridiqueSerializer


class SanteMentaleViewSet(ModelViewSet):
    queryset = SanteMentale.objects.all()
    serializer_class = SanteMentaleSerializer


class ReinsertionEconomiqueViewSet(ModelViewSet):
    queryset = ReinsertionEconomique.objects.all()
    serializer_class = ReinsertionEconomiqueSerializer
class FrontendAppView(View):
    """
    Vue qui sert l'application React (le fichier index.html compilé).
    """
    def get(self, request):
        try:
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            index_path = os.path.join(BASE_DIR, 'core', 'static', 'frontend', 'index.html')
            with open(index_path, 'r', encoding='utf-8') as f:
                return HttpResponse(f.read())
        except FileNotFoundError:
            raise Http404("Le build frontend n'existe pas. Exécutez npm run build.")

from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.decorators import login_required
import logging

from .models import (
    QuestionTransversale,
    SoinsMedicaux,
    AppuiPsychosocial,
    AssistanceJuridique,
    PoliceSecurity,
    SanteMentale,
    ReinsertionEconomique
)

# Configuration du logger
logger = logging.getLogger(__name__)

# Mappement des catégories vers les modèles spécifiques
CATEGORY_MODEL_MAP = {
    "Soins médicaux": SoinsMedicaux,
    "Appui psychosocial": AppuiPsychosocial,
    "Assistance juridique": AssistanceJuridique,
    "Police / Sécurité": PoliceSecurity,
    "Santé mentale": SanteMentale,
    "Réinsertion économique": ReinsertionEconomique,
}

@csrf_exempt  # À remplacer par @csrf_protect en production
 # Si vous voulez que seuls les utilisateurs connectés puissent soumettre

def submit_form(request):
    """
    Vue pour gérer la soumission des formulaires avec données transversales et spécifiques.
    Reçoit les données JSON, les valide et les enregistre dans les modèles appropriés.
    """
    if request.method != "POST":
        return JsonResponse({"error": "Méthode non autorisée"}, status=405)
    
    try:
        # Décoder les données JSON
        data = json.loads(request.body)
        
        # Récupérer les données spécifiques et transversales
        specifiques_data = data.get("specifiques", {})
        transversales_data = data.get("transversales", {})
        user_instance = User.objects.get(pk=transversales_data.get('author'))
        
        # Vérifier la catégorie
        category = specifiques_data.get("categorie")
        if not category:
            return JsonResponse({"error": f"Catégorie non spécifiée "}, status=400)
        
        # Obtenir le modèle spécifique correspondant à la catégorie
        SpecificModel = CATEGORY_MODEL_MAP.get(category)
        if not SpecificModel:
            return JsonResponse({"error": f"Catégorie invalide: {category}"}, status=400)
        
        # Utiliser une transaction pour garantir l'atomicité
        with transaction.atomic():
            # Préparation des données transversales
            # Traitement des champs JSON
            langues_parlees = transversales_data.get('langues_parlees', [])
            jours_ouverture = transversales_data.get('jours_ouverture', [])
            gratuit = transversales_data.get('gratuit', [])
            
            # Création de l'entrée pour les questions transversales sans sauvegarder immédiatement
            
            question_transversale = QuestionTransversale(
                nom_structure=transversales_data.get('nom_structure', ''),
                fonction_repondant=transversales_data.get('fonction_repondant', ''),
                nom_repondant=transversales_data.get('nom_repondant', ''),
                telephone_repondant=transversales_data.get('telephone_repondant', ''),
                latitude=transversales_data.get('latitude'),
                longitude=transversales_data.get('longitude'),
                email=transversales_data.get('email', ''),
                site_web=transversales_data.get('site_web', ''),
                langues_parlees=langues_parlees,
                jours_ouverture=jours_ouverture,
                heures_ouverture=transversales_data.get('heures_ouverture'),
                gratuit=gratuit,
                author=user_instance
               
            )
            
            # Associer l'utilisateur actuel si authentifié
            if request.user.is_authenticated:
                question_transversale.author = request.user
            
            # Préparation des données spécifiques
            # Retirer la catégorie du dictionnaire car c'est utilisé pour la sélection du modèle
            if "categorie" in specifiques_data:
                del specifiques_data["categorie"]
            
            # Création (sans sauvegarde) de l'instance spécifique selon le modèle
            if SpecificModel == SoinsMedicaux:
                specific_instance = create_soins_medicaux(question_transversale, specifiques_data)
            elif SpecificModel == AppuiPsychosocial:
                specific_instance = create_appui_psychosocial(question_transversale, specifiques_data)
            elif SpecificModel == AssistanceJuridique:
                specific_instance = create_assistance_juridique(question_transversale, specifiques_data)
            elif SpecificModel == PoliceSecurity:
                specific_instance = create_police_security(question_transversale, specifiques_data)
            elif SpecificModel == SanteMentale:
                specific_instance = create_sante_mentale(question_transversale, specifiques_data)
            elif SpecificModel == ReinsertionEconomique:
                specific_instance = create_reinsertion_economique(question_transversale, specifiques_data)
            else:
                # Cas général (ne devrait pas arriver avec la validation précédente)
                specific_instance = SpecificModel(
                    question_transversale=question_transversale,
                    **specifiques_data
                )
            
            # Sauvegarder dans le bon ordre pour éviter les dépendances circulaires
            question_transversale.save()  # Sauvegarde d'abord question_transversale
            specific_instance.question_transversale = question_transversale  # Mise à jour de la relation
            specific_instance.save()  # Sauvegarde de l'instance spécifique
            question_transversale.question_specifique = specific_instance  # Mise à jour de la relation inverse
            question_transversale.save()  # Sauvegarde à nouveau question_transversale
            
            # Retourner une réponse de succès avec les IDs créés
            return JsonResponse({
                "success": True,
                "message": "Formulaire soumis avec succès",
                "transversale_id": question_transversale.id,
                "specifique_id": specific_instance.id,
                "categorie": category
            }, status=201)
        
    except KeyError as e:
        logger.error(f"Champ obligatoire manquant: {str(e)}")
        return JsonResponse({"error": f"Champ obligatoire manquant: {str(e)}"}, status=400)
    except ValueError as e:
        logger.error(f"Erreur de validation: {str(e)}")
        return JsonResponse({"error": f"Erreur de validation: {str(e)}"}, status=400)
    except Exception as e:
        logger.error(f"Erreur lors de la soumission du formulaire: {str(e)}")
        return JsonResponse({"error": f"Erreur lors du traitement: {str(e)}"}, status=500)
def create_soins_medicaux(question_transversale, data):
    """Crée une instance de SoinsMedicaux avec les données fournies (sans sauvegarder)"""
    return SoinsMedicaux(  # Retourne une instance non sauvegardée
        question_transversale=question_transversale,
        protocole_viol=data.get('protocole_viol', False),
        infirmiers_hommes=data.get('infirmiers_hommes', 0),
        infirmiers_femmes=data.get('infirmiers_femmes', 0),
        matrones_hommes=data.get('matrones_hommes', 0),
        matrones_femmes=data.get('matrones_femmes', 0),
        sagefemmes_hommes=data.get('sagefemmes_hommes', 0),
        sagefemmes_femmes=data.get('sagefemmes_femmes', 0),
        medecins_hommes=data.get('medecins_hommes', 0),
        medecins_femmes=data.get('medecins_femmes', 0),
        gyn_hommes=data.get('gyn_hommes', 0),
        gyn_femmes=data.get('gyn_femmes', 0),
        autres_agents=data.get('autres_agents', ''),
        salle_privee=data.get('salle_privee', False),
        table_examen=data.get('table_examen', False),
        eclairage_fixe=data.get('eclairage_fixe', False),
        autoclave=data.get('autoclave', False),
        aucun_meuble=data.get('aucun_meuble', False),
        kit_ist=data.get('kit_ist', False),
        pep_vih=data.get('pep_vih', False),
        contraceptifs_urgence=data.get('contraceptifs_urgence', False),
        anatoxine=data.get('anatoxine', False),
        vaccin_hepatiteb=data.get('vaccin_hepatiteb', False),
        antalgiques=data.get('antalgiques', False),
        anesthesiques=data.get('anesthesiques', False),
        antibiotiques=data.get('antibiotiques', False),
        speculums=data.get('speculums', False),
        rubans=data.get('rubans', False),
        seringues=data.get('seringues', False),
        kit_suture=data.get('kit_suture', False),
        couvertures=data.get('couvertures', False),
        fournitures_sanitaires=data.get('fournitures_sanitaires', False),
        fournitures_protection=data.get('fournitures_protection', False),
        fiche_examen=data.get('fiche_examen', False),
        fiche_suivi=data.get('fiche_suivi', False),
        fiche_consentement=data.get('fiche_consentement', False),
        fiche_referencement=data.get('fiche_referencement', False),
        classement_securise=data.get('classement_securise', False),
        planning_familial=data.get('planning_familial', False),
        soins_prenataux=data.get('soins_prenataux', False),
        accouchement=data.get('accouchement', False),
        soins_postpartum=data.get('soins_postpartum', False),
        suivi_croissance=data.get('suivi_croissance', False),
        vaccination=data.get('vaccination', False),
        pcime=data.get('pcime', False),
        depistage_cancer=data.get('depistage_cancer', False),
        sante_adolescents=data.get('sante_adolescents', False),
        autres_services_srmne=data.get('autres_services_srmne', ''),
        salle_lits_travail=data.get('salle_lits_travail', False),
        salle_accouchement=data.get('salle_accouchement', False),
        salle_lits_postpartum=data.get('salle_lits_postpartum', False),
        equipement_accouchement=data.get('equipement_accouchement', False),
        laboratoire=data.get('laboratoire', False),
        bloc_operatoire=data.get('bloc_operatoire', False),
        autres_equipements=data.get('autres_equipements', ''),
        formation_viol=data.get('formation_viol', False),
        formation_conjugale=data.get('formation_conjugale', False),
        formation_enfants=data.get('formation_enfants', False),
        principes_directeurs=data.get('principes_directeurs', False),
        cadre_normatif=data.get('cadre_normatif', False),
        formation_eas=data.get('formation_eas', False),
        autres_formations=data.get('autres_formations', ''),
        kit_preuve_medico=data.get('kit_preuve_medico', False),
        difficultes_service=data.get('difficultes_service', '')
    )

def create_appui_psychosocial(question_transversale, data):
    """Crée une instance d'AppuiPsychosocial avec les données fournies (sans sauvegarder)"""
    return AppuiPsychosocial(  # Retourne une instance non sauvegardée
        question_transversale=question_transversale,
        soutien_psy_base=data.get('soutien_psy_base', False),
        appui_individuel=data.get('appui_individuel', False),
        appui_groupe=data.get('appui_groupe', False),
        gestion_enfants=data.get('gestion_enfants', False),
        gestion_adultes=data.get('gestion_adultes', False),
        kits_dignite=data.get('kits_dignite', False),
        aide_financiere=data.get('aide_financiere', False),
        autres_appuis=data.get('autres_appuis', ''),
        service_gratuit=data.get('service_gratuit', True),
        cout_service=data.get('cout_service'),
        gest_enfant_hommes=data.get('gest_enfant_hommes', 0),
        gest_enfant_femmes=data.get('gest_enfant_femmes', 0),
        gest_vbg_hommes=data.get('gest_vbg_hommes', 0),
        gest_vbg_femmes=data.get('gest_vbg_femmes', 0),
        superviseurs_hommes=data.get('superviseurs_hommes', 0),
        superviseurs_femmes=data.get('superviseurs_femmes', 0),
        aps_hommes=data.get('aps_hommes', 0),
        aps_femmes=data.get('aps_femmes', 0),
        autres_pers_hommes=data.get('autres_pers_hommes', 0),
        autres_pers_femmes=data.get('autres_pers_femmes', 0),
        form_gest_enfant_hommes=data.get('form_gest_enfant_hommes', 0),
        form_gest_enfant_femmes=data.get('form_gest_enfant_femmes', 0),
        form_gest_vbg_hommes=data.get('form_gest_vbg_hommes', 0),
        form_gest_vbg_femmes=data.get('form_gest_vbg_femmes', 0),
        form_eas_hommes=data.get('form_eas_hommes', 0),
        form_eas_femmes=data.get('form_eas_femmes', 0),
        form_psychosocial_hommes=data.get('form_psychosocial_hommes', 0),
        form_psychosocial_femmes=data.get('form_psychosocial_femmes', 0),
        salle_ecoute=data.get('salle_ecoute', False),
        espace_enfants=data.get('espace_enfants', False),
        outils_gestion_cas=data.get('outils_gestion_cas', False),
        securite_dossiers=data.get('securite_dossiers', False),
        bien_etre_staff=data.get('bien_etre_staff', False),
        protocole_gestion=data.get('protocole_gestion', False),
        referencement=data.get('referencement', False),
        mecanisme_eas=data.get('mecanisme_eas', False),
        autres_infrastructures=data.get('autres_infrastructures', ''),
        difficultes_service=data.get('difficultes_service', '')
    )

def create_police_security(question_transversale, data):
    """Crée une instance de PoliceSecurity avec les données fournies (sans sauvegarder)"""
    return PoliceSecurity(  # Retourne une instance non sauvegardée
        question_transversale=question_transversale,
        medicaments_disponibles=data.get('medicaments_disponibles', {}),
        reception_plainte=data.get('reception_plainte', False),
        enquete_arrestation=data.get('enquete_arrestation', False),
        autres_appuis=data.get('autres_appuis', ''),
        salle_confidentielle=data.get('salle_confidentielle', False),
        classement_securise=data.get('classement_securise', False),
        ordinateur_protege=data.get('ordinateur_protege', False),
        fournitures_admin=data.get('fournitures_admin', False),
        autres_infrastructures=data.get('autres_infrastructures', ''),
        effectif_hommes=data.get('effectif_hommes', 0),
        effectif_femmes=data.get('effectif_femmes', 0),
        opj_hommes=data.get('opj_hommes', 0),
        opj_femmes=data.get('opj_femmes', 0),
        form_enfants_hommes=data.get('form_enfants_hommes', 0),
        form_enfants_femmes=data.get('form_enfants_femmes', 0),
        form_vbg_hommes=data.get('form_vbg_hommes', 0),
        form_vbg_femmes=data.get('form_vbg_femmes', 0),
        service_gratuit=data.get('service_gratuit', True),
        items_payants=data.get('items_payants', ''),
        difficultes_service=data.get('difficultes_service', '')
    )

def create_assistance_juridique(question_transversale, data):
    """Crée une instance d'AssistanceJuridique avec les données fournies (sans sauvegarder)"""
    return AssistanceJuridique(  # Retourne une instance non sauvegardée
        question_transversale=question_transversale,
        conseils_juridiques=data.get('conseils_juridiques', False),
        assistance_juridique=data.get('assistance_juridique', False),
        representation_legale=data.get('representation_legale', False),
        referencement_legale=data.get('referencement_legale', ''),
        autres_appuis=data.get('autres_appuis', ''),
        formulaire_consentement=data.get('formulaire_consentement', False),
        espace_confidentiel=data.get('espace_confidentiel', False),
        classement_securise=data.get('classement_securise', False),
        fournitures_admin=data.get('fournitures_admin', False),
        mecanisme_eas=data.get('mecanisme_eas', False),
        protocole_juridique=data.get('protocole_juridique', False),
        juristes_hommes=data.get('juristes_hommes', 0),
        juristes_femmes=data.get('juristes_femmes', 0),
        para_juristes_hommes=data.get('para_juristes_hommes', 0),
        para_juristes_femmes=data.get('para_juristes_femmes', 0),
        form_enfants_hommes=data.get('form_enfants_hommes', 0),
        form_enfants_femmes=data.get('form_enfants_femmes', 0),
        form_vbg_hommes=data.get('form_vbg_hommes', 0),
        form_vbg_femmes=data.get('form_vbg_femmes', 0),
        collab_police=data.get('collab_police', False),
        nb_policiers_collab=data.get('nb_policiers_collab', 0),
        collab_tribunaux=data.get('collab_tribunaux', False),
        service_gratuit=data.get('service_gratuit', True),
        items_payants=data.get('items_payants', ''),
        difficultes_service=data.get('difficultes_service', '')
    )

def create_sante_mentale(question_transversale, data):
    """Crée une instance de SanteMentale avec les données fournies (sans sauvegarder)"""
    return SanteMentale(  # Retourne une instance non sauvegardée
        question_transversale=question_transversale,
        appui_pharma=data.get('appui_pharma', False),
        appui_psy=data.get('appui_psy', False),
        appui_social=data.get('appui_social', False),
        autres_appuis=data.get('autres_appuis', ''),
        nb_hommes=data.get('nb_hommes', 0),
        nb_femmes=data.get('nb_femmes', 0),
        psychiatres_hommes=data.get('psychiatres_hommes', 0),
        psychiatres_femmes=data.get('psychiatres_femmes', 0),
        psychologues_hommes=data.get('psychologues_hommes', 0),
        psychologues_femmes=data.get('psychologues_femmes', 0),
        infirmiers_psy_hommes=data.get('infirmiers_psy_hommes', 0),
        infirmiers_psy_femmes=data.get('infirmiers_psy_femmes', 0),
        sociologues_hommes=data.get('sociologues_hommes', 0),
        sociologues_femmes=data.get('sociologues_femmes', 0),
        anthropologues_hommes=data.get('anthropologues_hommes', 0),
        anthropologues_femmes=data.get('anthropologues_femmes', 0),
        medecins_psy_hommes=data.get('medecins_psy_hommes', 0),
        medecins_psy_femmes=data.get('medecins_psy_femmes', 0),
        aps_hommes=data.get('aps_hommes', 0),
        aps_femmes=data.get('aps_femmes', 0),
        autres_personnel_hommes=data.get('autres_personnel_hommes', 0),
        autres_personnel_femmes=data.get('autres_personnel_femmes', 0),
        salle_ecoute_confidentielle=data.get('salle_ecoute_confidentielle', False),
        espace_enfants=data.get('espace_enfants', False),
        securite_dossiers=data.get('securite_dossiers', False),
        protocole_prise_en_charge=data.get('protocole_prise_en_charge', False),
        autres_equipements=data.get('autres_equipements', ''),
        form_enfants_hommes=data.get('form_enfants_hommes', 0),
        form_enfants_femmes=data.get('form_enfants_femmes', 0),
        form_vbg_hommes=data.get('form_vbg_hommes', 0),
        form_vbg_femmes=data.get('form_vbg_femmes', 0),
        form_mhgap_hommes=data.get('form_mhgap_hommes', 0),
        form_mhgap_femmes=data.get('form_mhgap_femmes', 0),
        form_psp_hommes=data.get('form_psp_hommes', 0),
        form_psp_femmes=data.get('form_psp_femmes', 0),
        form_gestion_cas_hommes=data.get('form_gestion_cas_hommes', 0),
        form_gestion_cas_femmes=data.get('form_gestion_cas_femmes', 0),
        form_eas_hommes=data.get('form_eas_hommes', 0),
        form_eas_femmes=data.get('form_eas_femmes', 0),
        difficultes_service=data.get('difficultes_service', '')
    )

def create_reinsertion_economique(question_transversale, data):
    """Crée une instance de ReinsertionEconomique avec les données fournies (sans sauvegarder)"""
    return ReinsertionEconomique(  # Retourne une instance non sauvegardée
        question_transversale=question_transversale,
        formation_metier=data.get('formation_metier', False),
        aide_especes=data.get('aide_especes', False),
        avec=data.get('avec', False),
        referencement_travail=data.get('referencement_travail', False),
        alphabetisation=data.get('alphabetisation', False),
        autres_appuis=data.get('autres_appuis', ''),
        agents_formation_hommes=data.get('agents_formation_hommes', 0),
        agents_formation_femmes=data.get('agents_formation_femmes', 0),
        aps_hommes=data.get('aps_hommes', 0),
        aps_femmes=data.get('aps_femmes', 0),
        agents_services_financiers_hommes=data.get('agents_services_financiers_hommes', 0),
        agents_services_financiers_femmes=data.get('agents_services_financiers_femmes', 0),
        volontaires_hommes=data.get('volontaires_hommes', 0),
        volontaires_femmes=data.get('volontaires_femmes', 0),
        agents_autonomisation_hommes=data.get('agents_autonomisation_hommes', 0),
        agents_autonomisation_femmes=data.get('agents_autonomisation_femmes', 0),
        agronomes_hommes=data.get('agronomes_hommes', 0),
        agronomes_femmes=data.get('agronomes_femmes', 0),
        formes_enfants_hommes=data.get('formes_enfants_hommes', 0),
        formes_enfants_femmes=data.get('formes_enfants_femmes', 0),
        formes_vbg_hommes=data.get('formes_vbg_hommes', 0),
        formes_vbg_femmes=data.get('formes_vbg_femmes', 0),
        formes_formation_hommes=data.get('formes_formation_hommes', 0),
        formes_formation_femmes=data.get('formes_formation_femmes', 0),
        formes_entreprenariat_hommes=data.get('formes_entreprenariat_hommes', 0),
        formes_entreprenariat_femmes=data.get('formes_entreprenariat_femmes', 0),
        formes_compta_hommes=data.get('formes_compta_hommes', 0),
        formes_compta_femmes=data.get('formes_compta_femmes', 0),
        mecanisme_eas=data.get('mecanisme_eas', False),
        service_gratuit=data.get('service_gratuit', True),
        items_payants=data.get('items_payants', ''),
        difficultes_service=data.get('difficultes_service', '')
    )
    """Crée une instance de ReinsertionEconomique avec les données fournies"""
    return ReinsertionEconomique.objects.create(
        question_transversale=question_transversale,
        formation_metier=data.get('formation_metier', False),
        aide_especes=data.get('aide_especes', False),
        avec=data.get('avec', False),
        referencement_travail=data.get('referencement_travail', False),
        alphabetisation=data.get('alphabetisation', False),
        autres_appuis=data.get('autres_appuis', ''),
        agents_formation_hommes=data.get('agents_formation_hommes', 0),
        agents_formation_femmes=data.get('agents_formation_femmes', 0),
        aps_hommes=data.get('aps_hommes', 0),
        aps_femmes=data.get('aps_femmes', 0),
        agents_services_financiers_hommes=data.get('agents_services_financiers_hommes', 0),
        agents_services_financiers_femmes=data.get('agents_services_financiers_femmes', 0),
        volontaires_hommes=data.get('volontaires_hommes', 0),
        volontaires_femmes=data.get('volontaires_femmes', 0),
        agents_autonomisation_hommes=data.get('agents_autonomisation_hommes', 0),
        agents_autonomisation_femmes=data.get('agents_autonomisation_femmes', 0),
        agronomes_hommes=data.get('agronomes_hommes', 0),
        agronomes_femmes=data.get('agronomes_femmes', 0),
        formes_enfants_hommes=data.get('formes_enfants_hommes', 0),
        formes_enfants_femmes=data.get('formes_enfants_femmes', 0),
        formes_vbg_hommes=data.get('formes_vbg_hommes', 0),
        formes_vbg_femmes=data.get('formes_vbg_femmes', 0),
        formes_formation_hommes=data.get('formes_formation_hommes', 0),
        formes_formation_femmes=data.get('formes_formation_femmes', 0),
        formes_entreprenariat_hommes=data.get('formes_entreprenariat_hommes', 0),
        formes_entreprenariat_femmes=data.get('formes_entreprenariat_femmes', 0),
        formes_compta_hommes=data.get('formes_compta_hommes', 0),
        formes_compta_femmes=data.get('formes_compta_femmes', 0),
        mecanisme_eas=data.get('mecanisme_eas', False),
        service_gratuit=data.get('service_gratuit', True),
        items_payants=data.get('items_payants', ''),
        difficultes_service=data.get('difficultes_service', '')
    )