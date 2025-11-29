"""TODO: rajouter la partie TKinter, voir si les info irrécupérable par VM peuvent être quand même analyser (demander au SCT), """

"""Dernière modif du code, (Noa) /Plus de placeholder, couleur rouge sur les erreurs, recharegment par un bouton (pour éviter des crashs), Réarangement des badges, --gui et --sans-, /"""

import argparse
import time
from pathlib import Path
from collecte_systeme import prendre_tout
from templates_rapport import PAGE_MODELE, PAGE_DONNEES, faire_rapport


# Fonction principale qui gère toute l'interface Tkinter (mode --gui)
def lancer_interface_graphique(options=None):
    from tkinter import Tk, Menu, Canvas, Scrollbar
    from tkinter import ttk
    from tkinter.scrolledtext import ScrolledText
    from datetime import datetime
    import webbrowser
    import re

    # Petite fonction pour enlever les balises HTML avant d'afficher dans Tkinter
    def nettoyer_html(texte):
        """Enlève les balises HTML pour l'affichage dans Tkinter."""
        propre = re.sub(r"<[^>]+>", "", str(texte))
        propre = propre.replace("&nbsp;", " ")
        return propre.strip()
    
    root = Tk()
    root.geometry('620x500')
    root.title("Rapport Système")
    root.resizable(False, True)

    scrollble_zone = Canvas(root)
    scrollbar = Scrollbar(root, orient="vertical", command=scrollble_zone.yview)
    scrollbar.pack(side="right", fill="y")
    scrollble_zone.pack(side="left", fill="both", expand=True)
    scrollble_zone.configure(yscrollcommand=scrollbar.set, bg="#0b1020")

    window = ttk.Frame(scrollble_zone)
    scrollble_zone.create_window((0, 0), window=window, anchor="nw")

    style = ttk.Style()
    style.theme_use("default")
    style.configure("TLabel", background="#0b1020", foreground="white", font=("Roboto", 12))
    style.configure("Titre.TLabel", font=("Audiowide", 16, "bold"), background="#0b1020", foreground="white")

    # Fonction pour changer rapidement le thème clair/sombre de la fenêtre
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

    # Bouton pratique pour descendre directement en bas de la zone scrollable
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

    zones_scrolled = []

    cadre_contenu = ttk.Frame(window)
    cadre_contenu.pack(fill="both", expand=True)

    # Affiche un bloc (titre + texte scrollable) pour un groupe de données
    def afficher_bloc(parent, titre, contenu):
        ttk.Label(parent, text=titre, style="TLabel").pack(anchor="w", padx=10, pady=(10, 0))
        zone = ScrolledText(parent, height=6, wrap="word", font=("Consolas", 10), fg="black", bg="white")
        zone.insert("1.0", contenu)
        zone.configure(state="disabled")
        zone.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        zones_scrolled.append(zone)

    # Rafraîchit les données dans l'interface toutes les X secondes
    def mettre_a_jour():
        try:
            jeton = prendre_tout(options)
            for i, (cle, val) in enumerate(jeton.items()):
                if i >= len(zones_scrolled):
                    break
                zone = zones_scrolled[i]
                zone.configure(state="normal")
                zone.delete("1.0", "end")
                zone.insert("1.0", nettoyer_html(val) if cle in JETONS_BRUTS else str(val))
                zone.configure(state="disabled")
            label_maj.config(text=f"Dernière mise à jour : {datetime.now().strftime('%H:%M:%S')}")
        except Exception as e:
            label_maj.config(text=f"Erreur de mise à jour : {e}")
        finally:
            intervalle = getattr(options, "intervalle", 2.0) if options is not None else 2.0
            try:
                ms = int(float(intervalle) * 1000)
            except Exception:
                ms = 2000
            root.after(ms, mettre_a_jour)

    # Initialisation de l'affichage au lancement du mode graphique
    def init():
        try:
            jeton = prendre_tout(options)
        except Exception as e:
            label_maj.config(text=f"Erreur initiale : {e}")
            return

        for widget in cadre_contenu.winfo_children():
            widget.destroy()
        zones_scrolled.clear()

        for cle, val in jeton.items():
            afficher_bloc(
                cadre_contenu,
                cle.replace("_", " ").title(),
                nettoyer_html(val) if cle in JETONS_BRUTS else str(val),
            )

        label_maj.config(text=f"Dernière mise à jour : {datetime.now().strftime('%H:%M:%S')}")
        mettre_a_jour()

    # Fonction pour exporter rapidement les données dans un petit rapport HTML simple
    def exporter_html():
        try:
            jeton = prendre_tout(options)
            with open("rapport.html", "w", encoding="utf-8") as f:
                f.write("<html><head><title>Rapport système</title></head><body>")
                f.write("<h1>Rapport système</h1>")
                for cle, val in jeton.items():
                    f.write(f"<h2>{cle.replace('_', ' ').title()}</h2>")
                    f.write(f"<pre>{val}</pre>")
                f.write("</body></html>")
            label_maj.config(text="Export HTML effectué ✔")
            webbrowser.open("rapport.html")
        except Exception as e:
            label_maj.config(text=f"Erreur export HTML : {e}")

    menubar = Menu(root)
    root.config(menu=menubar)
    fichier_menu = Menu(menubar, tearoff=0)
    fichier_menu.add_command(label="Exporter HTML", command=exporter_html)
    fichier_menu.add_separator()
    fichier_menu.add_command(label="Quitter", command=root.quit)
    menubar.add_cascade(label="Fichier", menu=fichier_menu)

    # Bouton pour remonter tout en haut de la fenêtre
    def remonter():
        scrollble_zone.yview_moveto(0)

    ttk.Button(window, text="Haut", command=remonter).pack(pady=5)

    # À chaque changement de taille, on recalcule la zone scrollable
    def ajuster_fenetre(_):
        scrollble_zone.configure(scrollregion=scrollble_zone.bbox("all"))

    window.bind("<Configure>", ajuster_fenetre)
    init()
    root.mainloop()

# Fonction principale du script (point d'entrée ligne de commande)
def main():
    parseur = argparse.ArgumentParser()
    parseur.add_argument("--page", dest="page", default="rapport_supkrellm.html")
    parseur.add_argument("--donnees", default="donnees_systeme.html")
    parseur.add_argument("--intervalle", type=int, default=2)
    parseur.add_argument("--dossier", default=".")
    parseur.add_argument("--gui", action="store_true")
    parseur.add_argument("--sans-memoire", action="store_true")
    parseur.add_argument("--sans-disques", action="store_true")
    parseur.add_argument("--sans-processus", action="store_true")
    parseur.add_argument("--sans-reseau", action="store_true")
    parseur.add_argument("--sans-web", action="store_true")
    parseur.add_argument("--sans-materiel", action="store_true")

    args = parseur.parse_args()

    if args.gui:
        lancer_interface_graphique(args)
        return

    base = Path(args.dossier)
    try:
        base.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass

    page_path = base / args.page
    donnees_path = base / args.donnees
    modele_page = PAGE_MODELE
    modele_donnees = PAGE_DONNEES
    jetons_init = prendre_tout(args)
    rendu_page = faire_rapport(modele_page, jetons_init)
    page_path.write_text(rendu_page, encoding="utf-8")
    print(f"Rapport -> {page_path.resolve()}")

    try:
        while True:
            jetons = prendre_tout(args)
            rendu_donnees = faire_rapport(modele_donnees, jetons)
            tmp_path = donnees_path.with_suffix(donnees_path.suffix + ".tmp")
            tmp_path.write_text(rendu_donnees, encoding="utf-8")
            tmp_path.replace(donnees_path)
            time.sleep(args.intervalle)
    except KeyboardInterrupt:
        print("L'arrêt a était demandé.")


if __name__ == "__main__":
    main()