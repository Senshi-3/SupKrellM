from tkinter import *
from tkinter import ttk
from datetime import datetime
from rapport_html import prendre_tout
from tkinter.scrolledtext import ScrolledText

def afficher_bloc(parent, titre, contenu):
    ttk.Label(parent, text=titre, style="TLabel").pack(anchor="w", padx=10, pady=(10, 0))
    zone = ScrolledText(parent, height=6, wrap="word", font=("Consolas", 10), fg="black")
    zone.insert("1.0", contenu)
    zone.configure(state="disabled")
    zone.pack(fill="both", expand=True, padx=10, pady=(0, 10))
    
def lancer_interface_graphique():
    root = Tk()
    root.title("rapport_html")
    root.geometry("615x500")
    root.resizable(False, True)

    scrollble_zone = Canvas(root)
    scrollbar = Scrollbar(root, orient="vertical", command=scrollble_zone.yview)
    scrollbar.pack(side="right", fill="y")
    scrollble_zone.pack(side="left", fill="both", expand=True)
    scrollble_zone.configure(yscrollcommand=scrollbar.set)
    window = ttk.Frame(scrollble_zone)
    scrollble_zone.create_window((0, 0), window=window, anchor="nw")  

    style = ttk.Style()
    style.theme_use("default")
    style.configure("TLabel", background="#0b1020", foreground="white", font=("Roboto", 12))
    style.configure("Titre.TLabel", font=("Audiowide", 16, "bold"))

    ttk.Label(window, text="Rapport système", style="Titre.TLabel").pack(pady=20)
    
    JETONS_BRUTS = {
        "LIGNES_TEMPERATURES",
        "ELEMENTS_ALIM",
        "LIGNES_DISQUES",
        "LIGNES_PROCESSUS",
        "LIGNES_INTERFACES",
        "ELEMENTS_CONNEXIONS",
        "LIGNES_WEB",
        "ELEMENTS_ERREURS",

    }
    cadre_contenu = ttk.Frame(window)
    cadre_contenu.pack(fill="both", expand=True)

    def ajuster_fenetre(_):
        scrollble_zone.configure(scrollregion=scrollble_zone.bbox("all"))  

    def mettre_a_jour():
        jetons = prendre_tout()

        for widget in cadre_contenu.winfo_children():
            widget.destroy()

        for cle, val in jetons.items():
            afficher_bloc(cadre_contenu, cle.replace("_", " ").title(), val if cle in JETONS_BRUTS else str(val))

        root.after(2000, mettre_a_jour)

    window.bind("<Configure>", ajuster_fenetre)
    mettre_a_jour()
    root.mainloop()

lancer_interface_graphique()