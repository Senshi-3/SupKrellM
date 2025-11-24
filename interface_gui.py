from tkinter import *
from tkinter import Tk, ttk
from datetime import datetime
from rapport_html import prendre_tout
from tkinter.scrolledtext import ScrolledText
import webbrowser
import argparse

def afficher_bloc(parent, titre, contenu):
    ttk.Label(parent, text=titre, style="TLabel").pack(anchor="w", padx=10, pady=(10, 0))
    zone = ScrolledText(parent, height=6, wrap="word", font=("Consolas", 10), fg="black", bg="white")
    zone.insert("1.0", contenu)
    zone.configure(state="disabled")
    zone.pack(fill="both", expand=True, padx=10, pady=(0, 10))

def lancer_interface_graphique():
    root = Tk()
    try:
        root.state('zoomed')
    except:
        root.attributes('-fullscreen', True)

    root.title("rapport_html")
    root.resizable(True,True)

    scrollble_zone = Canvas(root)
    scrollbar = Scrollbar(root, orient="vertical", command=scrollble_zone.yview)
    scrollbar.pack(side="right", fill="y")
    scrollble_zone.pack(side="left", fill="both", expand=True)
    scrollble_zone.configure(yscrollcommand=scrollbar.set, bg="#0b1020")
c
    window = ttk.Frame(scrollble_zone)
    scrollble_zone.create_window((0, 0), window=window, anchor="nw")  
    window.pack(fill="both", expand=True)
    
    style = ttk.Style()
    style.theme_use("default")
    style.configure("TLabel", background="#0b1020", foreground="white", font=("Roboto", 12))
    style.configure("Titre.TLabel", font=("Audiowide", 16, "bold"))

    def toggle_theme():
        current_bg = style.lookup("TLabel", "background")
        if current_bg == "#0b1020":
            style.configure("TLabel", background="white", foreground="black")
            style.configure("Titre.TLabel", background="white", foreground="black")
            root.configure(bg="white")
        else:
            style.configure("TLabel", background="#0b1020", foreground="white")
            style.configure("Titre.TLabel", background="#0b1020", foreground="white")
            root.configure(bg="#0b1020")

    ttk.Button(window, text="Changer thème", command=toggle_theme).pack(pady=5)
    ttk.Label(window, text="Rapport système", style="Titre.TLabel").pack(pady=20)

    label_maj = ttk.Label(window, text="", style="TLabel")
    label_maj.pack(pady=(0, 10))

    def remonter():
        scrollble_zone.yview_moveto(0)

    ttk.Button(window, text="Haut", command=remonter).pack(pady=5)

    def descendre():
        scrollble_zone.yview_moveto(1)

    ttk.Button(window, text="Bas", command=descendre).pack(pady=5)
    
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

    def mettre_a_jour():
        jeton = prendre_tout()
        for widget in cadre_contenu.winfo_children():
            widget.destroy()
        for cle, val in jeton.items():
                afficher_bloc(cadre_contenu, cle.replace("_", " ").title(), val if cle in JETONS_BRUTS else str(val))
    
        label_maj.config(text=f"Dernière mise à jour : {datetime.now().strftime('%H:%M')}")
        root.after(2000, mettre_a_jour)

    ttk.Button(window, text="Rafraîchir", command=mettre_a_jour).pack(pady=5)
        

    def exporter_html():
        jeton = prendre_tout()
        with open("rapport.html", "w", encoding="utf-8") as f:
            f.write("<html><head><title>Rapport système</title></head><body>")
            f.write("<h1>Rapport système</h1>")
            for cle, val in jeton.items():
                f.write(f"<h2>{cle.replace('_', ' ').title()}</h2>")
                f.write(f"<pre>{val}</pre>")
            f.write("</body></html>")
        label_maj.config(text="Export HTML effectué ✔")
        webbrowser.open("rapport.html")

    menubar = Menu(root)  
    root.config(menu=menubar)
    fichier_menu = Menu(menubar, tearoff=0)
    fichier_menu.add_command(label="Exporter HTML", command=exporter_html)
    fichier_menu.add_separator()
    fichier_menu.add_command(label="Quitter", command=root.quit)
    menubar.add_cascade(label="Fichier", menu=fichier_menu)
    
    def ajuster_fenetre(_):
        scrollble_zone.configure(scrollregion=scrollble_zone.bbox("all"))

    window.bind("<Configure>", ajuster_fenetre)
    mettre_a_jour()
    root.mainloop()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rapport système et interface graphique")
    parser.add_argument("--gui", action="store_true", help="Lancer l'interface graphique Tkinter")
    args = parser.parse_args()

    if args.gui:
        lancer_interface_graphique()
    else:
        jeton = prendre_tout()
        with open("rapport.html", "w", encoding="utf-8") as f:
            f.write("<html><head><title>Rapport système</title></head><body>")
            f.write("<h1>Rapport système</h1>")
            for cle, val in jeton.items():
                f.write(f"<h2>{cle.replace('_', ' ').title()}</h2>")
                f.write(f"<pre>{val}</pre>")
            f.write("</body></html>")
        print("Rapport HTML généré : rapport.html")
