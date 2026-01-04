from backend import charger_faq, chercher_reponse, generer_suggestions_contextuelles

def lancer_test():
    base = charger_faq()
    if base is None:
        print("Erreur : fichier faq.json introuvable.")
        return

    print("===========================================")
    print("   TEST DU CHATBOT ESAG-NDE (V2 - PRO)    ")
    print("===========================================")
    print("Instructions : Posez votre question ou tapez 'quitter'.")
    
    while True:
        print("\n" + "-"*40)
        phrase = input("Vous : ")
        
        if phrase.lower() == "quitter":
            print("Fin du test. À bientôt !")
            break
            
        # 1. Recherche de la réponse
        reponse = chercher_reponse(phrase, base)
        print(f"\nBot : {reponse}")
        
        # 2. Génération et affichage des suggestions intelligentes
        suggestions = generer_suggestions_contextuelles(reponse, base)
        print("\n[Suggestions d'aide] :")
        for i, s in enumerate(suggestions, 1):
            print(f"  {i}. {s}")

if __name__ == "__main__":
    lancer_test()