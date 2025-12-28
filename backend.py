import json
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
    """
    Parcourt la base de données pour trouver la réponse la plus pertinente.
    Utilise un système de score pour gérer la précision et les fautes de frappe.
    """
    # 1. Nettoyage de la question
    mots_utilisateur = nettoyer_et_filtrer(question_utilisateur)
    
    # Si l'utilisateur n'a rien écrit ou juste de la politesse
    if not mots_utilisateur:
        return "Bonjour ! Je suis l'assistant ESAG-NDE. Posez-moi une question sur les inscriptions, les diplômes ou les contacts."

    meilleure_reponse = None
    score_max = 0

    # 2. Parcours des catégories et des questions du JSON
    for categorie in base_faq:
        for q_a in categorie["questions"]:
            score_actuel = 0
            
            # Comparaison de chaque mot de l'utilisateur avec chaque mot-clé du JSON
            for mot_u in mots_utilisateur:
                for mot_cle in q_a["keywords"]:
                    # Cas A : Le mot est contenu dans le mot-clé (ex: 'inscri' dans 'inscription')
                    if mot_u in mot_cle or mot_cle in mot_u:
                        score_actuel += 1
                    # Cas B : Le mot ressemble fortement (gestion des fautes de frappe)
                    elif similitude(mot_u, mot_cle) > 0.8:
                        score_actuel += 0.8
            
            # 3. Mise à jour de la réponse si ce bloc a un meilleur score que les précédents
            if score_actuel > score_max:
                score_max = score_actuel
                meilleure_reponse = q_a["reponse"]

    # 4. Résultat final : si le score est suffisant, on répond, sinon erreur
    if score_max >= 0.8:
        return meilleure_reponse
    
    return "Désolé, je ne trouve pas d'information précise. Essayez avec des mots simples comme 'scolarité', 'CAMES' ou 'inscription'."