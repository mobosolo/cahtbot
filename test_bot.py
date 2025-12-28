# On importe les fonctions logiques depuis notre fichier backend.py
from backend import charger_faq, chercher_reponse

def lancer_test():
    """
    Script de test interactif en console. 
    Permet de valider le moteur de recherche sans lancer l'interface Tkinter.
    """
    # Initialisation : chargement de la base JSON
    base = charger_faq()
    
    if base is None:
        print("ERREUR : Assurez-vous que le fichier 'faq.json' est dans le même dossier.")
        return

    print("=== TEST DU MOTEUR CHATBOT ESAG-NDE ===")
    print("Instructions : Tapez votre question. Tapez 'quitter' pour sortir.\n")

    while True:
        # Récupération de la saisie utilisateur
        phrase = input("Vous : ")
        
        # Condition de sortie
        if phrase.lower() == "quitter":
            print("Fin du test. Prêt pour l'étape suivante !")
            break
            
        # Appel du cerveau du bot (le backend)
        reponse = chercher_reponse(phrase, base)
        
        # Affichage du résultat
        print(f"Bot : {reponse}\n")

# Point d'entrée du script
if __name__ == "__main__":
    lancer_test()