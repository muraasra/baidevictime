

# Create your models here.
# core/models.py
from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=100)  # ex: "Santé", "Justice", etc.
    description = models.TextField(blank=True)

    def _str_(self):
        return self.name

class Service(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='services')
    address = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    latitude = models.FloatField()   # Stockage de la latitude en degrés décimaux
    longitude = models.FloatField()  # Stockage de la longitude en degrés décimaux
    author= models.ForeignKey(User,on_delete=models.CASCADE,null=True, blank=True)
    

    
    def get_address_phone(self):
        return f"{self.address} ({self.phone})" if self.phone else self.address
    def _str_(self):
        return f"{self.name} ({self.category.name})"

class Question(models.Model):
    text = models.CharField(max_length=255)  # Intitulé de la question
    # On pourrait ajouter un champ 'order' pour trier les questions, etc.
    def _str_(self):
        return self.text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=255)      # Intitulé du choix de réponse
    recommended_category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    # On pourrait ajouter un champ 'next_question' si le questionnaire a plusieurs étapes.

    def _str_(self):
        # Affiche la question et le texte du choix
        return f"{self.question.text} -> {self.text}"

from django.db import models
from django.utils.translation import gettext_lazy as _

class QuestionsSpecifiques(models.Model):
    categorie = models.CharField(max_length=255)  # Ex: 'Soins médicaux'
    medicaments_disponibles = models.TextField(null=True, blank=True)  # Exemple de champ spécifique
    # Ajoutez d'autres champs spécifiques ici

    def __str__(self):
        return self.categorie

class QuestionTransversale(models.Model):
    """Questions transversales communes à tous les services"""
    

    nom_structure = models.CharField(max_length=255)
    fonction_repondant = models.CharField(max_length=255,default='None')
    nom_repondant = models.CharField(max_length=255)
    telephone_repondant = models.CharField(max_length=20)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    site_web = models.URLField(null=True, blank=True)
    langues_parlees = models.JSONField(default=list)  # Stocke les langues sous forme de liste
    jours_ouverture = models.JSONField(default=list)  # Stocke les jours sous forme de liste
    heures_ouverture = models.TimeField(null=True, blank=True)
    gratuit = models.JSONField(default=list)  # Stocke les options de gratuité sous forme de liste

    author= models.ForeignKey(User,on_delete=models.CASCADE,null=True, blank=True)
    
    class Meta:
        verbose_name = _('Question Transversale')
        verbose_name_plural = _('Questions Transversales')
        
    def __str__(self):
        return self.nom_structure


class SoinsMedicaux(models.Model):
    """Service de soins médicaux"""
    question_transversale = models.OneToOneField(
        QuestionTransversale, 
        on_delete=models.CASCADE,
        related_name='soins_medicaux'
    )
    
    # Questions spécifiques aux soins médicaux
    protocole_viol = models.BooleanField(_('Protocole de prise en charge médicale des cas de viol'), default=False)
    
    # Personnel
    infirmiers_hommes = models.IntegerField(_('Nombre d\'infirmiers hommes'), default=0)
    infirmiers_femmes = models.IntegerField(_('Nombre d\'infirmiers femmes'), default=0)
    matrones_hommes = models.IntegerField(_('Nombre de matrones hommes'), default=0)
    matrones_femmes = models.IntegerField(_('Nombre de matrones femmes'), default=0)
    sagefemmes_hommes = models.IntegerField(_('Nombre de sages-femmes hommes'), default=0)
    sagefemmes_femmes = models.IntegerField(_('Nombre de sages-femmes femmes'), default=0)
    medecins_hommes = models.IntegerField(_('Nombre de médecins hommes'), default=0)
    medecins_femmes = models.IntegerField(_('Nombre de médecins femmes'), default=0)
    gyn_hommes = models.IntegerField(_('Nombre de gynécologues hommes'), default=0)
    gyn_femmes = models.IntegerField(_('Nombre de gynécologues femmes'), default=0)
    autres_agents = models.TextField(_('Autres agents de santé'), blank=True)
    
    # Infrastructures
    salle_privee = models.BooleanField(_('Salle privée avec rideau et accès toilette'), default=False)
    table_examen = models.BooleanField(_('Table d\'examen disponible'), default=False)
    eclairage_fixe = models.BooleanField(_('Éclairage fixe disponible'), default=False)
    autoclave = models.BooleanField(_('Autoclave disponible'), default=False)
    aucun_meuble = models.BooleanField(_('Aucun meuble disponible'), default=False)
    
    # Médicaments
    kit_ist = models.BooleanField(_('Kit IST disponible'), default=False)
    pep_vih = models.BooleanField(_('PEP VIH disponible'), default=False)
    contraceptifs_urgence = models.BooleanField(_('Contraceptifs d\'urgence disponibles'), default=False)
    anatoxine = models.BooleanField(_('Anatoxine tétanique / Immunoglobuline disponible'), default=False)
    vaccin_hepatiteb = models.BooleanField(_('Vaccin hépatite B disponible'), default=False)
    antalgiques = models.BooleanField(_('Antalgiques disponibles'), default=False)
    anesthesiques = models.BooleanField(_('Anesthésiques locaux disponibles'), default=False)
    antibiotiques = models.BooleanField(_('Antibiotiques / Antiseptiques disponibles'), default=False)
    
    # Matériel
    speculums = models.BooleanField(_('Spéculums disponibles'), default=False)
    rubans = models.BooleanField(_('Rubans à mesurer disponibles'), default=False)
    seringues = models.BooleanField(_('Seringues / Aiguilles papillon disponibles'), default=False)
    kit_suture = models.BooleanField(_('Kit de suture disponible'), default=False)
    couvertures = models.BooleanField(_('Couvertures / Draps disponibles'), default=False)
    fournitures_sanitaires = models.BooleanField(_('Fournitures sanitaires disponibles'), default=False)
    fournitures_protection = models.BooleanField(_('Fournitures de protection disponibles'), default=False)
    
    # Fournitures administratives
    fiche_examen = models.BooleanField(_('Fiche d\'examen avec pictogrammes disponible'), default=False)
    fiche_suivi = models.BooleanField(_('Fiche de suivi médical disponible'), default=False)
    fiche_consentement = models.BooleanField(_('Fiche de consentement disponible'), default=False)
    fiche_referencement = models.BooleanField(_('Fiche de référencement disponible'), default=False)
    classement_securise = models.BooleanField(_('Espace de classement sécurisé / Ordinateur protégé'), default=False)
    
    # Services SRMNE
    planning_familial = models.BooleanField(_('Planification familiale disponible'), default=False)
    soins_prenataux = models.BooleanField(_('Soins prénataux disponibles'), default=False)
    accouchement = models.BooleanField(_('Accouchement avec partogramme disponible'), default=False)
    soins_postpartum = models.BooleanField(_('Soins post-partum disponibles'), default=False)
    suivi_croissance = models.BooleanField(_('Suivi croissance nourrissons disponible'), default=False)
    vaccination = models.BooleanField(_('Vaccination disponible'), default=False)
    pcime = models.BooleanField(_('PCIME disponible'), default=False)
    depistage_cancer = models.BooleanField(_('Dépistage cancer col utérus disponible'), default=False)
    sante_adolescents = models.BooleanField(_('Santé des adolescents disponible'), default=False)
    autres_services_srmne = models.TextField(_('Autres services SRMNE'), blank=True)
    
    # Capacités
    salle_lits_travail = models.BooleanField(_('Salle et lits de travail disponibles'), default=False)
    salle_accouchement = models.BooleanField(_('Salle d\'accouchement disponible'), default=False)
    salle_lits_postpartum = models.BooleanField(_('Salle et lits de post-partum disponibles'), default=False)
    equipement_accouchement = models.BooleanField(_('Équipement minimum pour accouchements disponible'), default=False)
    laboratoire = models.BooleanField(_('Laboratoire avec examens standards disponible'), default=False)
    bloc_operatoire = models.BooleanField(_('Bloc opératoire fonctionnel'), default=False)
    autres_equipements = models.TextField(_('Autres équipements'), blank=True)
    
    # Formations
    formation_viol = models.BooleanField(_('Formation sur la gestion clinique du viol'), default=False)
    formation_conjugale = models.BooleanField(_('Formation sur la prise en charge des violences conjugales'), default=False)
    formation_enfants = models.BooleanField(_('Formation sur la prise en charge des enfants survivants'), default=False)
    principes_directeurs = models.BooleanField(_('Formation sur les principes directeurs'), default=False)
    cadre_normatif = models.BooleanField(_('Formation sur le cadre normatif'), default=False)
    formation_eas = models.BooleanField(_('Formation sur la prévention EAS/HS'), default=False)
    autres_formations = models.TextField(_('Autres formations'), blank=True)
    
    # Kit médico-légal
    kit_preuve_medico = models.BooleanField(_('Kit de collecte des preuves médico-légales'), default=False)
    
    # Difficultés
    difficultes_service = models.TextField(_('Difficultés rencontrées'), blank=True)
    
    class Meta:
        verbose_name = _('Service Soins Médicaux')
        verbose_name_plural = _('Services Soins Médicaux')
        
    def __str__(self):
        return f"Soins Médicaux - {self.question_transversale.nom_structure}"


class AppuiPsychosocial(models.Model):
    """Service d'appui psychosocial"""
    question_transversale = models.OneToOneField(
        QuestionTransversale, 
        on_delete=models.CASCADE,
        related_name='appui_psychosocial'
    )
    
    # Types de soutien
    soutien_psy_base = models.BooleanField(_('Soutien émotionnel de base / premiers secours psychologique'), default=False)
    appui_individuel = models.BooleanField(_('Appui psychosocial individuel'), default=False)
    appui_groupe = models.BooleanField(_('Appui psychosocial de groupe'), default=False)
    
    # Types d'activités
    gestion_enfants = models.BooleanField(_('Gestion des cas de violences pour les survivants enfants'), default=False)
    gestion_adultes = models.BooleanField(_('Gestion des cas de VBG/EAS pour les survivants adultes'), default=False)
    
    # Appui matériel et financier
    kits_dignite = models.BooleanField(_('Kits de dignité disponibles'), default=False)
    aide_financiere = models.BooleanField(_('Assistance financière ponctuelle pour besoins immédiats'), default=False)
    autres_appuis = models.TextField(_('Autres appuis pour la gestion de cas'), blank=True)
    
    # Coût
    service_gratuit = models.BooleanField(_('Service gratuit'), default=True)
    cout_service = models.DecimalField(_('Coût estimatif du service (FCFA)'), max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Personnel impliqué
    gest_enfant_hommes = models.IntegerField(_('Gestionnaires des cas de violences envers enfants hommes'), default=0)
    gest_enfant_femmes = models.IntegerField(_('Gestionnaires des cas de violences envers enfants femmes'), default=0)
    gest_vbg_hommes = models.IntegerField(_('Gestionnaires des cas de VBG/EAS hommes'), default=0)
    gest_vbg_femmes = models.IntegerField(_('Gestionnaires des cas de VBG/EAS femmes'), default=0)
    superviseurs_hommes = models.IntegerField(_('Superviseurs de gestion des cas de VBG hommes'), default=0)
    superviseurs_femmes = models.IntegerField(_('Superviseurs de gestion des cas de VBG femmes'), default=0)
    aps_hommes = models.IntegerField(_('Agents psychosociaux hommes'), default=0)
    aps_femmes = models.IntegerField(_('Agents psychosociaux femmes'), default=0)
    autres_pers_hommes = models.IntegerField(_('Autres personnes travaillant dans le service hommes'), default=0)
    autres_pers_femmes = models.IntegerField(_('Autres personnes travaillant dans le service femmes'), default=0)
    
    # Formation du personnel
    form_gest_enfant_hommes = models.IntegerField(_('Agents formés en gestion des cas de violences envers enfants hommes'), default=0)
    form_gest_enfant_femmes = models.IntegerField(_('Agents formés en gestion des cas de violences envers enfants femmes'), default=0)
    form_gest_vbg_hommes = models.IntegerField(_('Agents formés en gestion des cas de VBG/EAS hommes'), default=0)
    form_gest_vbg_femmes = models.IntegerField(_('Agents formés en gestion des cas de VBG/EAS femmes'), default=0)
    form_eas_hommes = models.IntegerField(_('Agents formés à la prévention des EAS hommes'), default=0)
    form_eas_femmes = models.IntegerField(_('Agents formés à la prévention des EAS femmes'), default=0)
    form_psychosocial_hommes = models.IntegerField(_('Agents formés à l\'accompagnement psychosocial des survivantes de VBG hommes'), default=0)
    form_psychosocial_femmes = models.IntegerField(_('Agents formés à l\'accompagnement psychosocial des survivantes de VBG femmes'), default=0)
    
    # Infrastructures et outils
    salle_ecoute = models.BooleanField(_('Salle d\'écoute confidentielle et confortable disponible'), default=False)
    espace_enfants = models.BooleanField(_('Espace sûr adapté pour les enfants disponible'), default=False)
    outils_gestion_cas = models.BooleanField(_('Outils de gestion de cas existants'), default=False)
    securite_dossiers = models.BooleanField(_('Équipements pour la sécurité des dossiers'), default=False)
    bien_etre_staff = models.BooleanField(_('Activités de bien-être pour le staff de gestion de cas'), default=False)
    protocole_gestion = models.BooleanField(_('Protocole de prise en charge psychosociale et de gestion de cas disponible'), default=False)
    referencement = models.BooleanField(_('Circuit de référencement vers d\'autres services'), default=False)
    mecanisme_eas = models.BooleanField(_('Mécanisme de réponse aux cas d\'EAS / harcèlement sexuel'), default=False)
    autres_infrastructures = models.TextField(_('Autres infrastructures pour la gestion des cas de VBG'), blank=True)
    
    # Difficultés
    difficultes_service = models.TextField(_('Difficultés rencontrées dans ce service'), blank=True)
    
    class Meta:
        verbose_name = _('Service Appui Psychosocial')
        verbose_name_plural = _('Services Appui Psychosocial')
        
    def __str__(self):
        return f"Appui Psychosocial - {self.question_transversale.nom_structure}"


class PoliceSecurity(models.Model):
    """Service de police et sécurité"""
    question_transversale = models.OneToOneField(
        QuestionTransversale, 
        on_delete=models.CASCADE,
        related_name='police_securite'
    )
    
    # Médicaments disponibles (stockés comme un JSON)
    medicaments_disponibles = models.JSONField(_('Médicaments disponibles'), default=dict)
    
    # Type d'appui
    reception_plainte = models.BooleanField(_('Réception et traitement des plaintes'), default=False)
    enquete_arrestation = models.BooleanField(_('Enquête sur et arrestation des bourreaux'), default=False)
    autres_appuis = models.TextField(_('Autres types d\'appui'), blank=True)
    
    # Infrastructures, outils, politiques
    salle_confidentielle = models.BooleanField(_('Salle/pratique d\'écoute confidentielle des cas de VBG'), default=False)
    classement_securise = models.BooleanField(_('Espace de classement sécurisé et verrouillé'), default=False)
    ordinateur_protege = models.BooleanField(_('Ordinateur protégé par mot de passe'), default=False)
    fournitures_admin = models.BooleanField(_('Fournitures administratives disponibles'), default=False)
    autres_infrastructures = models.TextField(_('Autres infrastructures ou équipements'), blank=True)
    
    # Effectifs
    effectif_hommes = models.IntegerField(_('Nombre total d\'agents hommes'), default=0)
    effectif_femmes = models.IntegerField(_('Nombre total d\'agents femmes'), default=0)
    opj_hommes = models.IntegerField(_('Nombre d\'OPJ hommes'), default=0)
    opj_femmes = models.IntegerField(_('Nombre d\'OPJ femmes'), default=0)
    
    # Formations du personnel
    form_enfants_hommes = models.IntegerField(_('Personnel formé sur les violences envers les enfants hommes'), default=0)
    form_enfants_femmes = models.IntegerField(_('Personnel formé sur les violences envers les enfants femmes'), default=0)
    form_vbg_hommes = models.IntegerField(_('Personnel formé sur les VBG / EAS hommes'), default=0)
    form_vbg_femmes = models.IntegerField(_('Personnel formé sur les VBG / EAS femmes'), default=0)
    
    # Coût
    service_gratuit = models.BooleanField(_('Service gratuit'), default=True)
    items_payants = models.TextField(_('Items payants pour les bénéficiaires'), blank=True)
    
    # Difficultés
    difficultes_service = models.TextField(_('Difficultés rencontrées dans ce service'), blank=True)
    
    class Meta:
        verbose_name = _('Service Police / Sécurité')
        verbose_name_plural = _('Services Police / Sécurité')
        
    def __str__(self):
        return f"Police / Sécurité - {self.question_transversale.nom_structure}"


class AssistanceJuridique(models.Model):
    """Service d'assistance juridique"""
    question_transversale = models.OneToOneField(
        QuestionTransversale, 
        on_delete=models.CASCADE,
        related_name='assistance_juridique'
    )
    
    # Types d'appui
    conseils_juridiques = models.BooleanField(_('Conseils juridiques disponibles'), default=False)
    assistance_juridique = models.BooleanField(_('Assistance pour les services juridiques'), default=False)
    representation_legale = models.BooleanField(_('Représentation légale disponible'), default=False)
    referencement_legale = models.TextField(_('Référencement pour la représentation légale'), blank=True)
    autres_appuis = models.TextField(_('Autres types d\'appui'), blank=True)
    
    # Infrastructures, outils et politiques
    formulaire_consentement = models.BooleanField(_('Utilisation d\'un formulaire de consentement'), default=False)
    espace_confidentiel = models.BooleanField(_('Espace sûr et confidentiel pour l\'écoute'), default=False)
    classement_securise = models.BooleanField(_('Espace de classement sécurisé / Ordinateur protégé'), default=False)
    fournitures_admin = models.BooleanField(_('Présence de fournitures administratives'), default=False)
    mecanisme_eas = models.BooleanField(_('Mécanisme de réponse aux cas d\'EAS / harcèlement sexuel'), default=False)
    protocole_juridique = models.BooleanField(_('Protocole de prise en charge des besoins juridiques'), default=False)
    
    # Ressources humaines
    juristes_hommes = models.IntegerField(_('Nombre de juristes / avocats hommes'), default=0)
    juristes_femmes = models.IntegerField(_('Nombre de juristes / avocats femmes'), default=0)
    para_juristes_hommes = models.IntegerField(_('Nombre de conseillers juridiques / para-juristes hommes'), default=0)
    para_juristes_femmes = models.IntegerField(_('Nombre de conseillers juridiques / para-juristes femmes'), default=0)
    form_enfants_hommes = models.IntegerField(_('Personnes formées sur les violences envers les enfants hommes'), default=0)
    form_enfants_femmes = models.IntegerField(_('Personnes formées sur les violences envers les enfants femmes'), default=0)
    form_vbg_hommes = models.IntegerField(_('Personnes formées sur la prévention des EAS / VBG hommes'), default=0)
    form_vbg_femmes = models.IntegerField(_('Personnes formées sur la prévention des EAS / VBG femmes'), default=0)
    
    # Collaboration
    collab_police = models.BooleanField(_('Collaboration avec les unités de police/gendarmerie'), default=False)
    nb_policiers_collab = models.IntegerField(_('Nombre d\'agents de police/gendarmerie collaborateurs'), default=0)
    collab_tribunaux = models.BooleanField(_('Collaboration avec les juridictions'), default=False)
    
    # Coût
    service_gratuit = models.BooleanField(_('Service gratuit'), default=True)
    items_payants = models.TextField(_('Items payants par le bénéficiaire'), blank=True)
    
    # Difficultés
    difficultes_service = models.TextField(_('Difficultés rencontrées dans ce service'), blank=True)
    
    class Meta:
        verbose_name = _('Service Assistance Juridique')
        verbose_name_plural = _('Services Assistance Juridique')
        
    def __str__(self):
        return f"Assistance Juridique - {self.question_transversale.nom_structure}"
from django.db import models
from django.utils.translation import gettext_lazy as _


class SanteMentale(models.Model):
    """Service de santé mentale"""
    question_transversale = models.OneToOneField(
        QuestionTransversale, 
        on_delete=models.CASCADE,
        related_name='sante_mentale'
    )
    
    # Types d'appui
    appui_pharma = models.BooleanField(_('Accompagnement pharmacologique (Disponibilité de médicaments psychotropes)'), default=False)
    appui_psy = models.BooleanField(_('Accompagnement psychologique (PM+, Gestion du stress, psychothérapie de soutien)'), default=False)
    appui_social = models.BooleanField(_('Accompagnement social (aide à la restauration de la dignité de la personne)'), default=False)
    autres_appuis = models.TextField(_('Autres types d\'appui'), blank=True)
    
    # Nombre de personnel
    nb_hommes = models.IntegerField(_('Nombre total de personnel hommes'), default=0)
    nb_femmes = models.IntegerField(_('Nombre total de personnel femmes'), default=0)
    
    # Spécialisation du personnel
    psychiatres_hommes = models.IntegerField(_('Psychiatres hommes'), default=0)
    psychiatres_femmes = models.IntegerField(_('Psychiatres femmes'), default=0)
    psychologues_hommes = models.IntegerField(_('Psychologues cliniciens hommes'), default=0)
    psychologues_femmes = models.IntegerField(_('Psychologues cliniciens femmes'), default=0)
    infirmiers_psy_hommes = models.IntegerField(_('Infirmiers en santé mentale hommes'), default=0)
    infirmiers_psy_femmes = models.IntegerField(_('Infirmiers en santé mentale femmes'), default=0)
    sociologues_hommes = models.IntegerField(_('Sociologues hommes'), default=0)
    sociologues_femmes = models.IntegerField(_('Sociologues femmes'), default=0)
    anthropologues_hommes = models.IntegerField(_('Anthropologues hommes'), default=0)
    anthropologues_femmes = models.IntegerField(_('Anthropologues femmes'), default=0)
    medecins_psy_hommes = models.IntegerField(_('Médecins formés en santé mentale hommes'), default=0)
    medecins_psy_femmes = models.IntegerField(_('Médecins formés en santé mentale femmes'), default=0)
    aps_hommes = models.IntegerField(_('Agents psychosociaux hommes'), default=0)
    aps_femmes = models.IntegerField(_('Agents psychosociaux femmes'), default=0)
    autres_personnel_hommes = models.IntegerField(_('Autres personnels offrant des soins en santé mentale hommes'), default=0)
    autres_personnel_femmes = models.IntegerField(_('Autres personnels offrant des soins en santé mentale femmes'), default=0)
    
    # Infrastructures et outils disponibles
    salle_ecoute_confidentielle = models.BooleanField(_('Salle d\'écoute et de gestion de cas confidentielle disponible'), default=False)
    espace_enfants = models.BooleanField(_('Présence d\'espaces sûrs adaptés pour les enfants'), default=False)
    securite_dossiers = models.BooleanField(_('Équipements pour la sécurité des dossiers (codes, armoires, clés, etc.)'), default=False)
    protocole_prise_en_charge = models.BooleanField(_('Protocole de prise en charge des besoins en santé mentale disponible'), default=False)
    autres_equipements = models.TextField(_('Autres équipements ou infrastructures'), blank=True)
    
    # Formations du personnel
    form_enfants_hommes = models.IntegerField(_('Personnel formé sur les violences envers les enfants hommes'), default=0)
    form_enfants_femmes = models.IntegerField(_('Personnel formé sur les violences envers les enfants femmes'), default=0)
    form_vbg_hommes = models.IntegerField(_('Personnel formé sur les VBG / EAS hommes'), default=0)
    form_vbg_femmes = models.IntegerField(_('Personnel formé sur les VBG / EAS femmes'), default=0)
    form_mhgap_hommes = models.IntegerField(_('Personnel médical formé sur le programme MhGAP hommes'), default=0)
    form_mhgap_femmes = models.IntegerField(_('Personnel médical formé sur le programme MhGAP femmes'), default=0)
    form_psp_hommes = models.IntegerField(_('Personnel formé au premier secours psychologique hommes'), default=0)
    form_psp_femmes = models.IntegerField(_('Personnel formé au premier secours psychologique femmes'), default=0)
    form_gestion_cas_hommes = models.IntegerField(_('Personnel formé à la gestion de cas hommes'), default=0)
    form_gestion_cas_femmes = models.IntegerField(_('Personnel formé à la gestion de cas femmes'), default=0)
    form_eas_hommes = models.IntegerField(_('Personnel formé à la prévention des EAS / harcèlement sexuel hommes'), default=0)
    form_eas_femmes = models.IntegerField(_('Personnel formé à la prévention des EAS / harcèlement sexuel femmes'), default=0)
    
    # Difficultés
    difficultes_service = models.TextField(_('Quelles sont les difficultés rencontrées dans ce service'), blank=True)
    
    class Meta:
        verbose_name = _('Service Santé mentale')
        verbose_name_plural = _('Services Santé mentale')
        
    def __str__(self):
        return f"Santé mentale - {self.question_transversale.nom_structure}"


class ReinsertionEconomique(models.Model):
    """Service de réinsertion économique"""
    question_transversale = models.OneToOneField(
        QuestionTransversale, 
        on_delete=models.CASCADE,
        related_name='reinsertion_economique'
    )
    
    # Types d'appui disponibles
    formation_metier = models.BooleanField(_('Offre de formation professionnelle sur des métiers'), default=False)
    aide_especes = models.BooleanField(_('Aide en espèces pour appuyer une activité génératrice de revenu'), default=False)
    avec = models.BooleanField(_('Association Villageoise d\'Épargne et de Crédit (AVEC) mise en place'), default=False)
    referencement_travail = models.BooleanField(_('Référencement / placement vers des opportunités de travail ou formation'), default=False)
    alphabetisation = models.BooleanField(_('Formation en alphabétisation disponible'), default=False)
    autres_appuis = models.TextField(_('Autres types d\'appui'), blank=True)
    
    # Ressources humaines disponibles
    agents_formation_hommes = models.IntegerField(_('Agents des services de formation professionnelle hommes'), default=0)
    agents_formation_femmes = models.IntegerField(_('Agents des services de formation professionnelle femmes'), default=0)
    aps_hommes = models.IntegerField(_('Agents psychosociaux hommes'), default=0)
    aps_femmes = models.IntegerField(_('Agents psychosociaux femmes'), default=0)
    agents_services_financiers_hommes = models.IntegerField(_('Agents des services financiers hommes'), default=0)
    agents_services_financiers_femmes = models.IntegerField(_('Agents des services financiers femmes'), default=0)
    volontaires_hommes = models.IntegerField(_('Volontaires communautaires hommes'), default=0)
    volontaires_femmes = models.IntegerField(_('Volontaires communautaires femmes'), default=0)
    agents_autonomisation_hommes = models.IntegerField(_('Agents en autonomisation économique/sociale & entrepreneuriat hommes'), default=0)
    agents_autonomisation_femmes = models.IntegerField(_('Agents en autonomisation économique/sociale & entrepreneuriat femmes'), default=0)
    agronomes_hommes = models.IntegerField(_('Agronomes / Vétérinaires hommes'), default=0)
    agronomes_femmes = models.IntegerField(_('Agronomes / Vétérinaires femmes'), default=0)
    formes_enfants_hommes = models.IntegerField(_('Personnes formées sur les violences envers les enfants hommes'), default=0)
    formes_enfants_femmes = models.IntegerField(_('Personnes formées sur les violences envers les enfants femmes'), default=0)
    formes_vbg_hommes = models.IntegerField(_('Personnes formées sur les VBG / EAS hommes'), default=0)
    formes_vbg_femmes = models.IntegerField(_('Personnes formées sur les VBG / EAS femmes'), default=0)
    formes_formation_hommes = models.IntegerField(_('Personnes formées comme agents des services de formation professionnelle hommes'), default=0)
    formes_formation_femmes = models.IntegerField(_('Personnes formées comme agents des services de formation professionnelle femmes'), default=0)
    formes_entreprenariat_hommes = models.IntegerField(_('Personnes formées sur l\'entrepreneuriat hommes'), default=0)
    formes_entreprenariat_femmes = models.IntegerField(_('Personnes formées sur l\'entrepreneuriat femmes'), default=0)
    formes_compta_hommes = models.IntegerField(_('Personnes formées en comptabilité de base hommes'), default=0)
    formes_compta_femmes = models.IntegerField(_('Personnes formées en comptabilité de base femmes'), default=0)
    
    # Mécanismes EAS/HS
    mecanisme_eas = models.BooleanField(_('Existe-t-il un mécanisme de réponse aux cas d\'EAS / harcèlement sexuel'), default=False)
    
    # Coût
    service_gratuit = models.BooleanField(_('Le service est-il gratuit'), default=True)
    items_payants = models.TextField(_('Éléments payants pour les bénéficiaires'), blank=True)
    
    # Difficultés
    difficultes_service = models.TextField(_('Quelles sont les principales difficultés rencontrées dans ce service'), blank=True)
    
    class Meta:
        verbose_name = _('Service Réinsertion économique')
        verbose_name_plural = _('Services Réinsertion économique')
        
    def __str__(self):
        return f"Réinsertion économique - {self.question_transversale.nom_structure}"