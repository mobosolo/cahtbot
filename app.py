import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import backend  # Assurez-vous que backend.py est présent
from datetime import datetime

class ChatbotESAG:
    def __init__(self, root):
        self.root = root
        self.root.title("ESAG-NDE Assistant")
        self.root.geometry("1100x750")
        
        # Configuration du thème
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # Palette de couleurs
        self.primary_color = "#0066FF"
        self.secondary_color = "#F5F7FA"
        self.user_bubble = "#0066FF"
        self.bot_bubble = "#FFFFFF"
        self.text_dark = "#1A1A1A"
        self.text_light = "#FFFFFF"
        self.border_color = "#E5E8EB"

        # Chargement de la FAQ
        self.base_faq = backend.charger_faq()
        if self.base_faq is None:
            messagebox.showerror("Erreur", "Le fichier faq.json est introuvable !")
            self.root.destroy()
            return

        # Gestion du Logo
        self.logo_size = 120
        try:
            # Charge l'image réelle
            img = Image.open("logo.png")
            self.logo_image = ctk.CTkImage(light_image=img, dark_image=img, size=(90, 90))
        except:
            self.logo_image = None

        self.messages = []
        self.creer_interface()
        
        # Message de bienvenue
        self.root.after(1000, lambda: self.afficher_message_bot(
            "Bonjour ! 👋\n\nJe suis l'assistant officiel de l'ESAG-NDE. Posez-moi vos questions sur les inscriptions, les filières ou les tarifs."
        ))

    def creer_interface(self):
        # ===== CONTENEUR PRINCIPAL =====
        main_container = ctk.CTkFrame(self.root, fg_color="#FFFFFF")
        main_container.pack(fill="both", expand=True)
        
        # ===== SIDEBAR =====
        sidebar = ctk.CTkFrame(main_container, width=280, fg_color=self.primary_color, corner_radius=0)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        
        # Logo Circulaire
        logo_outer = ctk.CTkFrame(sidebar, width=self.logo_size, height=self.logo_size, 
                                  fg_color="#FFFFFF", corner_radius=self.logo_size//2)
        logo_outer.pack(pady=(40, 10))
        logo_outer.pack_propagate(False)

        if self.logo_image:
            ctk.CTkLabel(logo_outer, image=self.logo_image, text="").place(relx=0.5, rely=0.5, anchor="center")
        else:
            ctk.CTkLabel(logo_outer, text="🎓", font=ctk.CTkFont(size=50)).place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(sidebar, text="ESAG-NDE", font=ctk.CTkFont(size=22, weight="bold"), text_color="#FFFFFF").pack()
        ctk.CTkLabel(sidebar, text="Assistant Virtuel", font=ctk.CTkFont(size=13), text_color="#A0C4FF").pack(pady=(0, 30))
        
        # Menu
        menu_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        menu_frame.pack(fill="both", expand=True, padx=20)
        
        ctk.CTkButton(menu_frame, text="💬  Nouvelle discussion", fg_color="#1A75FF", hover_color="#0052CC", 
                      command=self.nouvelle_conversation, height=45).pack(fill="x", pady=10)
        
        ctk.CTkButton(menu_frame, text="❓  Aide", fg_color="transparent", border_width=1, border_color="#FFFFFF",
                      hover_color="#1A75FF", command=self.afficher_aide, height=45).pack(fill="x")

        # ===== ZONE DE CHAT =====
        chat_area = ctk.CTkFrame(main_container, fg_color=self.secondary_color, corner_radius=0)
        chat_area.pack(side="right", fill="both", expand=True)
        
        # Header
        header = ctk.CTkFrame(chat_area, height=70, fg_color="#FFFFFF", corner_radius=0, border_width=1, border_color="#EEEEEE")
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(header, text="● Assistant en ligne", text_color="#2ECC71", font=ctk.CTkFont(size=14, weight="bold")).pack(side="left", padx=30)
        
        # Scrollable Frame
        self.scrollable_frame = ctk.CTkScrollableFrame(chat_area, fg_color="transparent", corner_radius=0)
        self.scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Input Area
        input_container = ctk.CTkFrame(chat_area, fg_color="#FFFFFF", height=100, corner_radius=0)
        input_container.pack(fill="x", side="bottom")
        input_container.pack_propagate(False)
        
        entry_bg = ctk.CTkFrame(input_container, fg_color="#F0F2F5", corner_radius=25)
        entry_bg.pack(fill="x", padx=30, pady=25)
        
        self.champ_saisie = ctk.CTkTextbox(entry_bg, height=40, fg_color="transparent", border_width=0, font=ctk.CTkFont(size=14), wrap="word")
        self.champ_saisie.pack(side="left", fill="both", expand=True, padx=20, pady=5)
        self.champ_saisie.bind("<Return>", self.envoyer_message_event)
        
        self.btn_envoyer = ctk.CTkButton(entry_bg, text="➤", width=45, height=45, corner_radius=22, 
                                        fg_color=self.primary_color, hover_color="#0052CC", command=self.envoyer_message)
        self.btn_envoyer.pack(side="right", padx=5)

    def afficher_message_utilisateur(self, texte):
        container = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        container.pack(fill="x", pady=8)
        
        bubble = ctk.CTkFrame(container, fg_color=self.user_bubble, corner_radius=18)
        bubble.pack(side="right", padx=10)
        
        ctk.CTkLabel(bubble, text=texte, font=ctk.CTkFont(size=14), text_color=self.text_light, 
                     wraplength=450, justify="left").pack(padx=15, pady=10)
        self.scroll_to_bottom()

    def afficher_message_bot(self, texte, suggestions=None):
        container = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        container.pack(fill="x", pady=8)
        
        bot_layout = ctk.CTkFrame(container, fg_color="transparent")
        bot_layout.pack(side="left", padx=10)

        # Avatar
        icon_circle = ctk.CTkFrame(bot_layout, width=35, height=35, fg_color=self.primary_color, corner_radius=17)
        icon_circle.pack(side="left", padx=(0, 10), anchor="s")
        icon_circle.pack_propagate(False)
        ctk.CTkLabel(icon_circle, text="🤖", font=ctk.CTkFont(size=16)).pack(expand=True)
        
        bubble = ctk.CTkFrame(bot_layout, fg_color=self.bot_bubble, corner_radius=18, border_width=1, border_color=self.border_color)
        bubble.pack(side="left")
        
        label = ctk.CTkLabel(bubble, text="", font=ctk.CTkFont(size=14), text_color=self.text_dark, 
                             wraplength=450, justify="left")
        label.pack(padx=15, pady=10)

        self.animer_texte(label, texte, 0, suggestions, container)

    def animer_texte(self, label, texte, index, suggestions, container):
        # On vérifie si le label existe toujours avec 'winfo_exists()'
        if label.winfo_exists():
            if index < len(texte):
                label.configure(text=texte[:index+1])
                self.scroll_to_bottom()
                # Programmer le caractère suivant
                self.root.after(15, lambda: self.animer_texte(label, texte, index+1, suggestions, container))
            elif suggestions:
                # Une fois fini, on vérifie aussi si le container existe pour les suggestions
                if container.winfo_exists():
                    self.afficher_suggestions(container, suggestions)
        else:
            # Si le label n'existe plus (ex: nouvelle discussion cliquée), 
            # on arrête simplement l'animation sans faire d'erreur.
            return

    def afficher_suggestions(self, container, suggestions):
        # Cadre parent pour les suggestions
        sug_frame = ctk.CTkFrame(container, fg_color="transparent")
        sug_frame.pack(fill="x", padx=(55, 20), pady=(0, 10)) 
        
        # Petit titre pour guider l'utilisateur
        lbl_info = ctk.CTkLabel(sug_frame, text="Questions suggérées :", 
                                font=ctk.CTkFont(size=11, slant="italic"), 
                                text_color="#7F8C8D")
        lbl_info.pack(anchor="w", padx=5, pady=(0, 5))

        # Création des boutons un par un verticalement
        for s in suggestions:
            btn = ctk.CTkButton(
                sug_frame, 
                text=f"  {s}  ", # Espaces pour l'esthétique
                height=35, 
                corner_radius=10, 
                fg_color="#FFFFFF", 
                border_width=1,
                border_color=self.primary_color, 
                text_color=self.primary_color, 
                hover_color="#E8F0FE",
                font=ctk.CTkFont(size=12), 
                anchor="w", # Aligne le texte du bouton à gauche
                command=lambda val=s: self.utiliser_suggestion(val)
            )
            # fill="x" permet au bouton de prendre toute la largeur disponible
            btn.pack(side="top", fill="x", padx=5, pady=3)
            
        self.scroll_to_bottom()

    

    def envoyer_message(self):
        msg = self.champ_saisie.get("1.0", "end-1c").strip()
        if not msg: return
        
        self.afficher_message_utilisateur(msg)
        self.champ_saisie.delete("1.0", "end")
        self.btn_envoyer.configure(state="disabled")
        
        def process():
            rep = backend.chercher_reponse(msg, self.base_faq)
            sug = backend.generer_suggestions_contextuelles(rep, self.base_faq)
            self.afficher_message_bot(rep, sug)
            self.btn_envoyer.configure(state="normal")
            self.champ_saisie.focus_set()
            
        self.root.after(400, process)

    def envoyer_message_event(self, event):
        if not (event.state & 0x1):
            self.root.after(10, self.envoyer_message)
            return "break"

    def utiliser_suggestion(self, s):
        # On simule la saisie et l'envoi
        self.champ_saisie.delete("1.0", "end")
        self.champ_saisie.insert("1.0", s)
        self.envoyer_message()

    def scroll_to_bottom(self):
        self.scrollable_frame.update_idletasks()
        self.scrollable_frame._parent_canvas.yview_moveto(1.0)

    def nouvelle_conversation(self):
        for w in self.scrollable_frame.winfo_children(): w.destroy()
        self.afficher_message_bot("Conversation réinitialisée. Comment puis-je vous aider ?")

    def afficher_aide(self):
        self.afficher_message_bot("Je peux vous renseigner sur :\n• Les inscriptions\n• Les filières (Licence, Master)\n• Les tarifs\n• Les contacts.")

if __name__ == "__main__":
    root = ctk.CTk()
    app = ChatbotESAG(root)
    root.mainloop()