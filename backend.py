import json
import random
import os
from difflib import SequenceMatcher # Utilisé pour comparer la ressemblance entre deux mots

def charger_faq():
    """
    Tente d'ouvrir le fichier faq.json et de récupérer les données.
    Retourne la liste des questions ou None si le fichier est absent.
    """
    if not os.path.exists("faq.json"):
        return None
    
    # Ouverture avec encodage utf-8 pour bien gérer les accents français
    with open("faq.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["faq"]

def similitude(a, b):
    """
    Calcule un score entre 0 et 1 représentant la ressemblance 
    textuelle entre le mot 'a' et le mot 'b'.
    """
    return SequenceMatcher(None, a, b).ratio()

def nettoyer_et_filtrer(texte):
    """
    Prépare la phrase de l'utilisateur :
    1. Passage en minuscules.
    2. Suppression de la ponctuation.
    3. Filtrage des 'mots vides' (mots qui n'apportent pas de sens).
    """
    ponctuation = "?!.,;:"
    mots_vides = ["le", "la", "les", "de", "des", "du", "je", "tu", "un", "une", "est", "quels", "quelles", "comment", "pour", "avez", "vous", "sont", "bonjour", "salut"]
    
    texte = texte.lower()
    for p in ponctuation:
        texte = texte.replace(p, "")
    
    mots = texte.split()
    # On ne garde que les mots porteurs de sens (ex: 'inscription', 'frais')
    return [m for m in mots if m not in mots_vides]

def chercher_reponse(question_utilisateur, base_faq):
    mots_utilisateur = nettoyer_et_filtrer(question_utilisateur)
    
    if not mots_utilisateur:
        bienvenue = [
            "Je vous écoute ! Comment puis-je vous aider ?",
            "Bonjour ! Je suis prêt à répondre à vos questions sur l'ESAG-NDE.",
            "Posez-moi vos questions sur les inscriptions, les filières ou les tarifs."
        ]
        return random.choice(bienvenue)

    meilleure_reponse = None
    score_max = 0

    for categorie in base_faq:
        for q_a in categorie["questions"]:
            score_actuel = 0
            # On calcule l'intersection entre les mots de l'utilisateur et les mots-clés
            for mot_u in mots_utilisateur:
                for mot_cle in q_a["keywords"]:
                    # Exact match (poids fort)
                    if mot_u == mot_cle.lower():
                        score_actuel += 2 
                    # Similitude (poids moyen)
                    elif similitude(mot_u, mot_cle.lower()) > 0.85:
                        score_actuel += 1.5
                    # Contenu (poids faible)
                    elif mot_u in mot_cle.lower() and len(mot_u) > 3:
                        score_actuel += 1

            # Bonus : si la catégorie correspond aussi, on augmente le score
            if any(similitude(mot_u, categorie["categorie"].lower()) > 0.8 for mot_u in mots_utilisateur):
                score_actuel += 0.5

            if score_actuel > score_max:
                score_max = score_actuel
                meilleure_reponse = q_a["reponse"]

    # Seuil de confiance plus strict
    if score_max >= 1.5:
        return meilleure_reponse
    
    return "Je ne suis pas sûr d'avoir compris. Parlez-vous des 'filières', des 'frais de scolarité' ou des 'conditions d'admission' ?"
def generer_suggestions_contextuelles(reponse_donnee, base_faq):
    """
    Génère des suggestions de manière aléatoire parmi les thèmes 
    majeurs de l'ESAG-NDE pour dynamiser la conversation.
    """
    # Liste globale de toutes les questions possibles basées sur vos thèmes essentiels
    toutes_suggestions = [
        "Quelles sont les filières BTS ?",
        "Quelles sont les filières Licence ?",
        "Parlez-moi du cycle Master",
        "Cursus Expertise Comptable",
        "Certification MikroTik",
        "Partenariat avec la BRVM",
        "Documents à fournir pour l'inscription",
        "Où se situe l'école ?",
        "Contact de la scolarité",
        "Qui est la Directrice de l'école ?",
        "Formations avec le Maroc"
    ]
    
    # On mélange et on en prend 2 ou 3 au hasard
    # On s'assure de ne pas suggérer quelque chose qui est déjà dans la réponse
    suggestions_finales = [s for s in toutes_suggestions if s.lower() not in reponse_donnee.lower()]
    
    return random.sample(suggestions_finales, 3)