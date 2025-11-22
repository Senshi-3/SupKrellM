"""TODO: rajouter la partie TKinter, voir si les info irrécupérable par VM peuvent être quand même analyser (demander au SCT), """

"""Dernière modif du code, (Noa) /Plus de placeholder, couleur rouge sur les erreurs, recharegment par un bouton (pour éviter des crashs), Réarangement des badges, --gui et --sans-, /"""

import argparse
import datetime
import glob
import html
import http.client
import json
import re
import ssl
import subprocess
import time
from pathlib import Path


PAGE_MODELE = r"""
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title>Rapport système - %%NOM_HOTE%%</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="icon" href="https://friconix.com/png/fi-cnsuxx-linux.png">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Audiowide&family=Roboto:ital,wght@0,100..900;1,100..900&display=swap">
    <style>
        :root{
            --ok: #1f9d55;
            --warn: #c07f00;
            --err: #d64545;
            --mono: ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace;
        }

        html, body{
            margin: 0;
            padding: 0;
            height: 100%;
            background-color: rgb(11, 16, 32);
            font-family: system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Arial, sans-serif;
            scroll-behavior: smooth;
            overflow-y: hidden;
        }

        a{
            text-decoration: none;
        }

        a:hover{
            transform: scale(1.1);
        }

        header{
            position: sticky;
            top: 0;
            padding-bottom: 1vw;
            display: flex;
            background: linear-gradient(180deg, rgba(11, 16, 32, 0.95), rgba(11, 16, 32, 0.7));
            backdrop-filter: blur(5px);
            z-index: 3;
            border-bottom: 1px solid rgb(33, 50, 107);
            text-align: center;
            align-items: center;
            flex-direction: column;
            animation: page-allumage 1s forwards;
            overflow: hidden;
        }

        #texte-titre{
            font-family: "Audiowide", sans-serif;
            color: white;
        }

        #navigateur{
            display: flex;
            gap: 2vw;
            align-items: flex-start;
        }

        .texte-navigateur{
            font-family: "Audiowide", sans-serif;
            color: #4ca3cb;
            position: relative;
            animation: entrer-nav-text 1.5s forwards;
            opacity: 0;
        }

        .texte-navigateur:nth-child(1) {animation-delay: 0s;}
        .texte-navigateur:nth-child(2) {animation-delay: 0.4s;}
        .texte-navigateur:nth-child(3) {animation-delay: 0.8s;}
        .texte-navigateur:nth-child(4) {animation-delay: 1.2s; }
        .texte-navigateur:nth-child(5) {animation-delay: 1.6s;}
        .texte-navigateur:nth-child(6) {animation-delay: 2s}
        .texte-navigateur:nth-child(7) {animation-delay: 2.4s;}
        .texte-navigateur:nth-child(8) {animation-delay: 2.8s; color: var(--err);}

        main{
            max-width: 100vw;
            margin: 0 auto;
            padding: 0;
        }

        h2{
            display: inline-block;
            color: #287da1;
        }

        .section{
            scroll-margin-top: 7vw;
        }

        section:target{
            animation: mis-en-evidence 0.3s ease-out;
        }

        section:target .grille3,
        section:target .grille2,
        section:target .bloc-table{
            animation: bordure-evidence 1s linear;
        }

        section:target .bloc-erreurs{
            animation: bordure-evidence-err 1s linear;
        }

        .bloc{
            background-color: rgba(24, 35, 58, 0.733);
            padding: 1vw;
            border-radius: 1em;
            border: 1px solid #5e7d8aab;
            display: flex;
            flex-direction: column;
        }

        .bloc-table{
            background-color: rgba(24, 35, 58, 0);
            padding-bottom: 1vw;
            border-radius: 1em;
            border: 1px solid #5e7d8aab;
            display: flex;
            flex-direction: column;
        }

        .bloc-erreurs{
            border-left: 3px solid var(--err);
            padding: 1vw;
            border-radius: 1em;
            background: rgba(214, 69, 69, .08);
            margin-bottom: 1vw;
        }

        .bloc:hover{
            box-shadow: 0 0 3px 3px #2c627a;
        }

        .bloc-erreurs:hover{
            box-shadow: 0 0 3px 3px #7a2c2c;
        }

        .etiquette{
            color: #91c2d89a;
            font-family: var(--mono);
            padding-bottom: 1vw;
            user-select: none;
        }

        .valeur{
            color: #c9d1ff;
            font-family: var(--mono);
        }

        .grille3{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 16px;
            border-radius: 1em;
        }

        .grille2{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 16px;
            border-radius: 1em;
        }

        table{
            width: 100%;
            border-collapse: collapse;
        }

        th, td{
            padding: 1vw;
            border-bottom: 1px solid #1c2347;
            text-align: left;
            color: #c9d1ff;
        }

        th{
            color: #c9d1ff;
        }

        li{
            color: #c9d1ff;
        }

        ul, ol{
            margin-left: 1vw;
            padding-left: 1.2rem;
        }

        #texte-erreurs{
            color: #a12828;
        }

        footer{
            color: #a8b0d9;
            position: sticky;
            bottom: 0;
            font-size: 0.8vw;
            text-align: center;
            margin: 1vw;
            padding: 1vw;
            z-index: 10;
        }
        hr{
            box-shadow: 0 0 20px 50px rgb(11, 16, 32);
            color: transparent;
            position: sticky;
            bottom: 0;
            z-index: 9;
        }

        .badge{
            display: inline-block;
            padding: 0.15rem 0.5rem;
            border-radius: 3em;
            font-size: 0.6vw;
            text-align: center;
            border: 1px solid #2a366b;
            background: #0e1430;
            color: #a8b0d9;
        }

        .ok {
            color: #d6ffe6;
            border-color: rgba(31,157,85,.45);
            background: rgba(31,157,85,.08);
        }

        .warn {
            color: #fff4d6;
            border-color: rgba(192,127,0,.45);
            background: rgba(192,127,0,.08);
        }

        .err {
            color: #ffe1e1;
            border-color: rgba(214,69,69,.45);
            background: rgba(214,69,69,.08);
        }

        iframe{
            -ms-overflow-style: none;
            scrollbar-width: none;
        }
        iframe::-webkit-scrollbar{
            display: none;
        }

        #bouton-rafraichir{
            margin-left: 1vw;
            padding: 0.2rem 0.8rem;
            border-radius: 999px;
            border: 1px solid #2a366b;
            background: #0e1430;
            color: #a8b0d9;
            font-family: inherit;
            font-size: 0.8vw;
            outline: 0px solid white;
            outline-offset: 0.6vw;
            transition: all 0.05s ease-in-out;
            display: inline-flex;
            align-items: center;
            gap: 0.4vw;
            vertical-align: middle;
        }

        #bouton-rafraichir:hover{
            background: none;
            border: 0px solid #2a366b;
            outline: 2px solid white;
            outline-offset: 0.3vw;
            transition: all 0.05s ease-in-out; 
        }
        #bouton-rafraichir:active{
            background: none;
            border: 0px solid #2a366b;
            outline: 2px solid white;
            outline-offset: 0.3vw;
            transition: all 0.01s ease-in-out; 
        }
        #bouton-rafraichir:hover #logo-rafraichir{
            animation: rotation-logo-rafraichir 1s forwards;
        }

        @keyframes rotation-logo-rafraichir{
            0%{
                transform: rotate(0deg);
            }
            100%{ 
                transform: rotate(359deg); 
            }
        }

        @keyframes mis-en-evidence{
            0%{
                transform: scale(1);
            }
            40%{ 
                transform: scale(1.1); 
            }
            100%{ 
                transform: scale(1); 
            }
        }

        @keyframes bordure-evidence{
            0%{ 
                outline: 2px solid #5e7d8aab;
                outline-offset: 0.3vw; 
            }
            90%{ 
                outline: 1px solid #5e7d8aab; 
                outline-offset: 0.3vw; 
            }
            100%{ 
                outline: 0; 
                outline-offset: 0; 
            }
        }

        @keyframes bordure-evidence-err{
            0%{ 
                outline: 2px solid var(--err); 
                outline-offset: 0.3vw; 
            }
            90%{ 
                outline: 1px solid var(--err); 
                outline-offset: 0.3vw; 
            }
            100%{ 
                outline: 0; 
                outline-offset: 0; 
            }
        }

        @keyframes entrer-nav-text{
            0%{ 
                top: 100px; 
                opacity: 0; 
            }
            100%{ 
                top: 0; 
                opacity: 1; 
            }
        }
        

        @media (max-width: 767px){
            #texte-titre{ 
                font-size: 4vw;
            }
            #navigateur{ 
                gap: 1vw; 
            }
            .texte-navigateur, th, td, li, footer{ 
                font-size: 2vw; 
            }
            main{ 
                max-width: 90vw; 
            }
            h2{
                font-size: 3vw; 
            }
            .section{ 
                scroll-margin-top: 10vw;
            }
            .bloc, .bloc-table, .bloc-erreurs, .grille3, .grille2{ 
                border-radius: 0.5em;
            }
            .etiquette, .badge{
                font-size: 1.7vw;
            }
            .valeur{
                font-size: 2.3vw;
            }
            .grille3, .grille2{
                gap: 7px;
            }
        }

        @media (min-width: 768px) and (max-width: 1023px){
            #texte-titre{ 
                font-size: 3vw; 
            }
            #navigateur{
                gap: 2vw; 
            }
            .texte-navigateur, th, td, li, footer{
                font-size: 1.5vw; 
            }
            main{
                max-width: 80vw;
            }
            h2{
                font-size: 2.7vw;
            }
            .section{
                scroll-margin-top: 9vw;
            }
            .bloc, .bloc-table, .bloc-erreurs, .grille3, .grille2 {
                border-radius: 0.5em;
            }
            .etiquette, .badge{
                font-size: 1.3vw;
            }
            .valeur{ 
                font-size: 1.8vw;
            }
            .grille3, .grille2{
                gap: 10px;
            }
        }
    </style>
</head>
<body>
    <header>
        <h1 id="texte-titre">Rapport système – <span>%%NOM_HOTE%%</span></h1>
        <nav id="navigateur">
             <a href="donnees_systeme.html#apercu"   target="zone-donnees" class="texte-navigateur">Vue d’ensemble</a>
            <a href="donnees_systeme.html#materiel" target="zone-donnees" class="texte-navigateur">Matériel</a>
            <a href="donnees_systeme.html#memoire"  target="zone-donnees" class="texte-navigateur">Mémoire</a>
            <a href="donnees_systeme.html#disques"  target="zone-donnees" class="texte-navigateur">Disques</a>
            <a href="donnees_systeme.html#processus" target="zone-donnees" class="texte-navigateur">Processus</a>
            <a href="donnees_systeme.html#reseau"   target="zone-donnees" class="texte-navigateur">Réseau</a>
            <a href="donnees_systeme.html#web"      target="zone-donnees" class="texte-navigateur">Services web</a>
            <a href="donnees_systeme.html#erreurs"  target="zone-donnees" class="texte-navigateur">Erreurs</a>
        </nav>
    </header>
    <main>
        <iframe src="donnees_systeme.html" name="zone-donnees" style="width:100%; height:100vh; border:none; scroll-margin-top: 7vw;"></iframe>
    </main>
    <footer>
        Généré le <span class="valeur">%%DATE%%</span>
        <a id="bouton-rafraichir" href="donnees_systeme.html" target="zone-donnees">Rafraîchir les données
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" id="logo-rafraichir" viewBox="0 0 16 16">
                <path d="M11.534 7h3.932a.25.25 0 0 1 .192.41l-1.966 2.36a.25.25 0 0 1-.384 0l-1.966-2.36a.25.25 0 0 1 .192-.41m-11 2h3.932a.25.25 0 0 0 .192-.41L2.692 6.23a.25.25 0 0 0-.384 0L.342 8.59A.25.25 0 0 0 .534 9"/>
                <path fill-rule="evenodd" d="M8 3c-1.552 0-2.94.707-3.857 1.818a.5.5 0 1 1-.771-.636A6.002 6.002 0 0 1 13.917 7H12.9A5 5 0 0 0 8 3M3.1 9a5.002 5.002 0 0 0 8.757 2.182.5.5 0 1 1 .771.636A6.002 6.002 0 0 1 2.083 9z"/>
            </svg>
        </a>
    </footer>
    <hr/>
</body>
</html>"""

PAGE_DONNEES = r"""
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="utf-8">
    <title>Données système</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="icon" href="https://friconix.com/png/fi-cnsuxx-linux.png">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Audiowide&family=Roboto:ital,wght@0,100..900;1,100..900&display=swap">
    <style>
        :root{
            --ok: #1f9d55;
            --warn: #c07f00;
            --err: #d64545;
            --mono: ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace;
        }

        html, body{
            margin: 0;
            padding: 0;
            background-color: rgb(11, 16, 32);
            font-family: system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Arial, sans-serif;
            scroll-behavior: smooth; 
            -ms-overflow-style: none;
            scrollbar-width: none;
        }

        main{
            max-width: 55vw;
            margin: 0 auto;
            padding: 1vw 0;
        }

        h2{
            display: inline-block;
            color: #287da1;
        }

        section{
            scroll-margin-top: 7vw;
        }

        .bloc{
            background-color: rgba(24, 35, 58, 0.733);
            padding: 1vw;
            border-radius: 1em;
            border: 1px solid #5e7d8aab;
            display: flex;
            flex-direction: column;
        }

        .bloc-table{
            background-color: rgba(24, 35, 58, 0);
            padding-bottom: 1vw;
            border-radius: 1em;
            border: 1px solid #5e7d8aab;
            display: flex;
            flex-direction: column;
        }
        #erreurs{
            margin-bottom: 20%;
        }
        .bloc-erreurs{
            border-left: 3px solid var(--err);
            padding: 1vw;
            border-radius: 1em;
            background: rgba(214, 69, 69, .08);
            margin-bottom: 1vw;
        }

        .etiquette{
            color: #91c2d89a;
            font-family: var(--mono);
            padding-bottom: 1vw;
            user-select: none;
        }

        .valeur{
            color: #c9d1ff;
            font-family: var(--mono);
        }

        .grille3{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 16px;
            border-radius: 1em;
        }

        .grille2{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 16px;
            border-radius: 1em;
        }

        table{
            width: 100%;
            border-collapse: collapse;
        }

        th, td{
            padding: 1vw;
            border-bottom: 1px solid #1c2347;
            text-align: left;
            color: #c9d1ff;
        }

        th{
            color: #c9d1ff;
        }

        li{
            color: #c9d1ff;
        }

        ul, ol{
            margin-left: 1vw;
            padding-left: 1.2rem;
        }

        .badge{
            display: inline-block;
            padding: 0.15rem 0.5rem;
            border-radius: 3em;
            font-size: 0.6vw;
            text-align: center;
            border: 1px solid #2a366b;
            background: #0e1430;
            color: #a8b0d9;
        }

        .ok{
            color: #d6ffe6;
            border-color: rgba(31,157,85,.45);
            background: rgba(31,157,85,.08);
        }

        .warn{
            color: #fff4d6;
            border-color: rgba(192,127,0,.45);
            background: rgba(192,127,0,.08);
        }

        .err{
            color: #ffe1e1;
            border-color: rgba(214,69,69,.45);
            background: rgba(214,69,69,.08);
        }
        section:target{
            animation: mis-en-evidence 0.3s ease-out;
        }

        section:target .grille3,  section:target .grille2, section:target .bloc-table{
            animation: bordure-evidence 1s linear;
        }

        section:target .bloc-erreurs{
            animation: bordure-evidence-err 1s linear;
        }
        @keyframes mis-en-evidence{
            0%{
                transform: scale(1);
            }
            40%{
                transform: scale(1.1);
            }
            100%{
                transform: scale(1);
            }
        }

        @keyframes bordure-evidence {
            0%{
                outline: 2px solid #5e7d8aab; 
                outline-offset: 0.3vw; 
            }
            90%{ 
                outline: 1px solid #5e7d8aab; 
                outline-offset: 0.3vw; 
            }
            100%{ 
                outline: 0; 
                outline-offset: 0; 
            }
        }

        @keyframes bordure-evidence-err {
            0%{ 
                outline: 2px solid var(--err); 
                outline-offset: 0.3vw; 
            }
            90%{ 
                outline: 1px solid var(--err); 
                outline-offset: 0.3vw;
            }
            100%{ 
                outline: 0; 
                outline-offset: 0; 
            }
        }
    </style>
</head>
<body>
    <main>
        <section id="apercu" class="section">
            <h2>Vue d’ensemble</h2>
            <div class="grille3">
                <div class="bloc">
                    <span class="etiquette">Date de génération</span>
                    <span class="valeur">%%DATE_HEURE%%</span>
                </div>
                <div class="bloc">
                    <span class="etiquette">Noyau</span>
                    <span class="valeur">%%NOYAU%%</span>
                </div>
                <div class="bloc">
                    <span class="etiquette">Uptime</span>
                    <span class="valeur">%%DUREE_FONCTIONNEMENT%%</span>
                </div>
            </div>
        </section>

        <section id="materiel" class="section">
            <h2>Matériel – Alimentation</h2>
            <div class="grille2">
                <div class="bloc">
                    <div class="etiquette">Températures</div>
                    <div class="table-wrap">
                        <table>
                            <thead><tr><th>Capteur</th><th>Température</th><th>État</th></tr></thead>
                            <tbody>
                                %%LIGNES_TEMPERATURES%%
                            </tbody>
                        </table>
                    </div>
                </div>
                <div class="bloc">
                    <div class="etiquette">Alimentation</div>
                    <ul>
                        %%ELEMENTS_ALIM%%
                    </ul>
                </div>
            </div>
        </section>

        <section id="memoire" class="section">
            <h2>Mémoire</h2>
            <div class="grille3">
                <div class="bloc">
                    <span class="etiquette">Totale</span>
                    <span class="valeur">%%MEM_TOTALE%%</span>
                </div>
                <div class="bloc">
                    <span class="etiquette">Utilisée</span>
                    <span class="valeur">%%MEM_UTILISEE%% (%%MEM_UTILISEE_PCT%%)</span>
                </div>
                <div class="bloc">
                    <span class="etiquette">Libre + cache</span>
                    <span class="valeur">%%MEM_LIBRE_CACHE%%</span>
                </div>
            </div>
        </section>

        <section id="disques" class="section">
            <h2>Disques</h2>
            <div class="bloc-table">
                <table>
                    <thead><tr><th>Périphérique</th><th>Montage</th><th>Utilisation</th><th>Espace libre</th><th>Type</th></tr></thead>
                    <tbody>
                        %%LIGNES_DISQUES%%
                    </tbody>
                </table>
            </div>
        </section>

        <section id="processus" class="section">
            <h2>Processus actifs</h2>
            <div class="bloc-table">
                <table>
                    <thead><tr><th>PID</th><th>Utilisateur</th><th>CPU %</th><th>RAM %</th><th>Commande</th></tr></thead>
                    <tbody>
                        %%LIGNES_PROCESSUS%%
                    </tbody>
                </table>
            </div>
        </section>

        <section id="reseau" class="section">
            <h2>Réseau</h2>
            <div class="grille2">
                <div class="bloc">
                    <div class="etiquette">Interfaces</div>
                    <div class="table-wrap" role="region" aria-label="Interfaces réseau">
                        <table>
                            <thead><tr><th>Interface</th><th>IPv4</th><th>IPv6</th><th>RX/TX</th><th>État</th></tr></thead>
                            <tbody>
                                %%LIGNES_INTERFACES%%
                            </tbody>
                        </table>
                    </div>
                </div>
                <div class="bloc">
                    <div class="etiquette">Connexions</div>
                    <ul>
                        %%ELEMENTS_CONNEXIONS%%
                    </ul>
                </div>
            </div>
        </section>

        <section id="web" class="section">
            <h2>Services Web</h2>
            <div class="bloc-table">
                <table>
                    <thead><tr><th>Hôte</th><th>Titre</th><th>Favicon</th><th>Serveur</th><th>Proto/TLS</th><th>Statut</th></tr></thead>
                    <tbody>
                        %%LIGNES_WEB%%
                    </tbody>
                </table>
            </div>
        </section>

        <section id="erreurs" class="section">
            <h2 id="texte-erreurs">Erreurs</h2>
            <div class="bloc-erreurs">
                <ul>
                    %%ELEMENTS_ERREURS%%
                </ul>
            </div>
        </section>
    </main>
</body>
</html>
"""


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


def faire_rapport(modele: str, jetons: dict) -> str:
    rendu = modele
    for cle, val in jetons.items():
        if cle in JETONS_BRUTS:
            texte = str(val)
        else:
            texte = html.escape(str(val), quote=True)
        rendu = rendu.replace("%%" + cle + "%%", texte)
    rendu = re.sub(r"%%[A-Z0-9_]+%%", "", rendu)
    return rendu


def lire_fichier(chemin: str):
    try:
        with open(chemin, "r", encoding="utf-8", errors="ignore") as f:
            return f.read().strip(), None
    except Exception as err:
        return None, f"{chemin}: {err}"


def format_duree(sec_f: float) -> str:
    s = int(sec_f)
    h, s = divmod(s, 3600)
    m, s = divmod(s, 60)
    j, h = divmod(h, 24)
    if j > 0:
        return f"{j} jours, {h:02d}:{m:02d}:{s:02d}"
    return f"{h:02d}:{m:02d}:{s:02d}"


def lire_memoire():
    txt, err = lire_fichier("/proc/meminfo")
    if err:
        return None, err
    kv = {}
    for ligne in txt.splitlines():
        if ":" in ligne:
            k, v = ligne.split(":", 1)
            kv[k.strip()] = v.strip()

    def ko_vers_gio(texte_val, defaut=0.0):
        try:
            return float(texte_val.split()[0]) / (1024 * 1024)
        except Exception:
            return defaut

    total = ko_vers_gio(kv.get("MemTotal", "0 kB"))
    libre = ko_vers_gio(kv.get("MemFree", "0 kB"))
    tampons = ko_vers_gio(kv.get("Buffers", "0 kB"))
    cache = ko_vers_gio(kv.get("Cached", "0 kB"))
    reclaim = ko_vers_gio(kv.get("SReclaimable", "0 kB"))
    shmem = ko_vers_gio(kv.get("Shmem", "0 kB"))
    libre_cache = libre + tampons + cache + reclaim - shmem
    utilise = max(0.0, total - libre - tampons - cache - reclaim + shmem)
    pct = (utilise / total * 100.0) if total > 0 else 0.0
    return {
        "MEM_TOTALE": f"{total:.1f} Go",
        "MEM_UTILISEE": f"{utilise:.1f} Go",
        "MEM_UTILISEE_PCT": f"{pct:.1f}%",
        "MEM_LIBRE_CACHE": f"{libre_cache:.1f} Go",
    }, None


def prendre_temperatures() -> str:
    lignes = []
    zones = sorted(glob.glob("/sys/class/thermal/thermal_zone*/temp"))
    for tz in zones:
        try:
            with open(tz, "r") as f:
                brut = f.read().strip()
            t_milli = int(brut)
            t_c = t_milli / 1000.0
            nom = Path(tz).parent.name
            lignes.append("<tr><td>"f"{nom}</td><td>{t_c:.1f} °C</td>""<td><span class='badge ok'>OK</span></td></tr>")
        except Exception:
            lignes.append("<tr><td>capteur inconnu</td>""<td style='color:#d64545'>Impossible de lire la température</td>""<td><span class='badge err'>Erreur</span></td></tr>")
    if not lignes:
        lignes.append("<tr><td><span style='color:#d64545'>Donnée introuvable</span></td>""<td style='color:#d64545'>Aucun capteur détecté</td>""<td><span class='badge err'>Erreur</span></td></tr>")
    return "\n".join(lignes)


def prendre_alim() -> str:
    lignes = []
    bats = sorted(glob.glob("/sys/class/power_supply/BAT*"))
    if not bats:
        return "<li style='color:#d64545'>Aucune batterie détectée</li>"
    for bat in bats:
        try:
            with open(f"{bat}/status", "r") as f:
                etat = f.read().strip()
        except Exception:
            etat = "<span style='color:#d64545'>Donnée introuvable</span>"
        try:
            with open(f"{bat}/capacity", "r") as f:
                cap = f.read().strip()
        except Exception:
            cap = "<span style='color:#d64545'>Donnée introuvable</span>"
        nom = Path(bat).name
        lignes.append(f"<li>{nom}: {etat} — {cap}%</li>")
    return "\n".join(lignes)


def prendre_disques() -> str:
    try:
        res = subprocess.run(
            ["df", "-T", "-hP"],
            capture_output=True,
            text=True,
            timeout=3,
        )
        lignes = []
        for line in res.stdout.splitlines()[1:]:
            parts = line.split()
            if len(parts) >= 7:
                dev, fstype, size, used, free, pcent, mnt = parts[:7]
                lignes.append(
                    "<tr>"
                        f"<td>{dev}</td><td>{mnt}</td><td>{pcent}</td>"
                        f"<td>{free}</td><td>{fstype}</td>"
                    "</tr>"
                )
        if not lignes:
            return ("<tr><td colspan='5'>""<span style='color:#d64545'>Donnée introuvable</span></td></tr>")
        return "\n".join(lignes)
    except Exception:
        return ("<tr><td colspan='5'>""<span style='color:#d64545'>Donnée introuvable</span></td></tr>")


def prendre_processus() -> str:
    try:
        res = subprocess.run(
            ["ps", "aux", "--sort=-%cpu"],
            capture_output=True,
            text=True,
            timeout=3,
        )
        lignes = []
        for line in res.stdout.splitlines()[1:11]:
            parts = line.split(None, 10)
            if len(parts) >= 11:
                user, pid, cpu, mem, vsz, rss, tty, stat, start, t, cmd = parts
                cmd_ok = html.escape(cmd)[:120]
                lignes.append(
                    "<tr>"
                        f"<td>{pid}</td><td>{user}</td>"
                        f"<td>{cpu}%</td><td>{mem}%</td>"
                        f"<td>{cmd_ok}</td>"
                    "</tr>"
                )
        if not lignes:
            return ("<tr><td colspan='5'>""<span style='color:#d64545'>Donnée introuvable</span></td></tr>")
        return "\n".join(lignes)
    except Exception:
        return ("<tr><td colspan='5'>""<span style='color:#d64545'>Donnée introuvable</span></td></tr>")


def prendre_interfaces() -> str:
    ip4 = {}
    ip6 = {}
    try:
        res = subprocess.run(
            ["ip", "-j", "addr"],
            capture_output=True,
            text=True,
            timeout=2,
        )
        for ifc in json.loads(res.stdout):
            nom = ifc.get("ifname")
            for adr in ifc.get("addr_info", []):
                fam = adr.get("family")
                if fam == "inet":
                    ip4.setdefault(nom, []).append(adr.get("local"))
                elif fam == "inet6":
                    ip6.setdefault(nom, []).append(adr.get("local"))
    except Exception:
        pass

    rxtx = {}
    try:
        with open("/proc/net/dev", "r") as f:
            for line in f.readlines()[2:]:
                if ":" not in line:
                    continue
                iface, rest = line.split(":", 1)
                nom = iface.strip()
                nums = rest.split()
                rx = int(nums[0]) if nums else 0
                tx = int(nums[8]) if len(nums) > 8 else 0
                rxtx[nom] = (rx, tx)
    except Exception:
        pass

    lignes = []
    noms = sorted(set(list(rxtx.keys()) + list(ip4.keys()) + list(ip6.keys())))
    for nom in noms:
        ip_v4 = ", ".join(ip4.get(nom, [])) or "—"
        ip_v6 = ", ".join(ip6.get(nom, [])) or "—"
        rx, tx = rxtx.get(nom, (0, 0))

        try:
            with open(f"/sys/class/net/{nom}/operstate", "r") as f:
                brut = f.read().strip()
        except Exception:
            brut = ""

        if nom == "lo" and brut == "unknown":
            etat_texte = "Boucle locale"
            classe = "warn"
        elif brut == "up":
            etat_texte = "Actif"
            classe = "ok"
        elif brut == "down":
            etat_texte = "Inactif"
            classe = "err"
        else:
            etat_texte = brut or "Inconnu"
            classe = "err"

        lignes.append(
            "<tr>"
                f"<td>{nom}</td>"
                f"<td>{ip_v4}</td>"
                f"<td>{ip_v6}</td>"
                f"<td>{rx//1024}K / {tx//1024}K</td>"
                f"<td><span class='badge {classe}'>{etat_texte}</span></td>"
            "</tr>"
        )

    if not lignes:
        return "<tr><td colspan='5'>N/A</td></tr>"
    return "\n".join(lignes)


def prendre_connexions() -> str:
    try:
        res = subprocess.run(
            ["ss", "-tuln"],
            capture_output=True,
            text=True,
            timeout=2,
        )
        lignes = []
        for line in res.stdout.splitlines()[1:]:
            lignes.append(f"<li>{html.escape(line)}</li>")
        if not lignes:
            return "<li style='color:#d64545'>Aucune connexion</li>"
        return "\n".join(lignes)
    except Exception:
        return "<li><span style='color:#d64545'>Donnée introuvable</span></li>"


def analyser_ligne_ss(ligne):
    try:
        parts = ligne.split()
        if len(parts) < 5:
            return None, None
        local = parts[3]
        if ":" not in local:
            return None, None
        host_part, port = local.rsplit(":", 1)
        host = host_part
        if host in ("*", "0.0.0.0", "[::]", "::"):
            host = "127.0.0.1"
        host = host.strip("[]")
        return host, port
    except Exception:
        return None, None


def sonder_service_http(hote: str, port: str, use_https: bool = False):
    titre_page = "Titre indisponible"
    chemin_favicon = "Favicon inconnu"
    nom_serveur = "Inconnu"
    statut_http = "N/A"
    protocole = "HTTP"
    delai = 2
    if use_https:
        try:
            contexte = ssl._create_unverified_context()
            connexion = http.client.HTTPSConnection(hote, int(port), timeout=delai, context=contexte)
            protocole = "HTTPS"
        except Exception as e:
            return titre_page, chemin_favicon, nom_serveur, protocole, statut_http
    else:
        try:
            connexion = http.client.HTTPConnection(hote, int(port), timeout=delai)
            protocole = "HTTP"
        except Exception:
            return titre_page, chemin_favicon, nom_serveur, protocole, statut_http

    try:
        connexion.request("GET", "/")
        reponse = connexion.getresponse()
        statut_http = str(reponse.status)
        nom_serveur = reponse.getheader("Server") or "Inconnu"
        corps = reponse.read(4096).decode("utf-8", errors="ignore")

        debut_titre = corps.lower().find("<title>")
        fin_titre = corps.lower().find("</title>")

        if debut_titre != -1 and fin_titre != -1 and fin_titre > debut_titre:
            brut = corps[debut_titre + 7:fin_titre]
            titre_page = brut.strip()
        chemin_favicon = "/favicon.ico"

    except Exception:
        pass
    finally:
        try:
            connexion.close()
        except Exception:
            pass
    return titre_page, chemin_favicon, nom_serveur, protocole, statut_http

def prendre_web() -> str:
    lignes = []
    try:
        res = subprocess.run(["ss", "-ntlp"],capture_output=True,text=True,timeout=2,)
        deja_vus = set()
        for ligne in res.stdout.splitlines():
            if ":80 " in ligne or ":443 " in ligne:
                host, port = analyser_ligne_ss(ligne)
                if not host or not port:
                    continue
                cle = (host, port)
                if cle in deja_vus:
                    continue
                deja_vus.add(cle)
                use_https = (port == "443")
                titre, favicon, serveur, proto_tls, statut = sonder_service_http(host, port, use_https=use_https)
                lignes.append(
                    "<tr>"
                        f"<td>{html.escape(host)}:{port}</td>"
                        f"<td>{html.escape(titre)}</td>"
                        f"<td>{html.escape(favicon)}</td>"
                        f"<td>{html.escape(serveur)}</td>"
                        f"<td>{html.escape(proto_tls)}</td>"
                        f"<td><span class='badge ok'>{html.escape(statut)}</span></td>"
                    "</tr>"
                )
        if not lignes:
            return ("<tr><td colspan='6' style='color:#d64545'>""Aucun service web détecté</td></tr>")
        return "\n".join(lignes)
    except Exception:
        return ("<tr><td colspan='6'>""<span style='color:#d64545'>Donnée introuvable</span></td></tr>")


def prendre_tout(options=None):
    erreurs = []
    date_heure = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date = datetime.datetime.now().strftime("%Y-%m-%d")

    nom_hote, err = lire_fichier("/proc/sys/kernel/hostname")
    if err:
        erreurs.append(err)
    if not nom_hote:
        nom_hote = "inconnu"

    noyau, err = lire_fichier("/proc/version")
    if err:
        erreurs.append(err)
    if not noyau:
        noyau = "Version du noyau non disponible"

    txt_uptime, err = lire_fichier("/proc/uptime")
    if err:
        erreurs.append(err)
        duree = "n/a"
    else:
        try:
            secs = float(txt_uptime.split()[0])
            duree = format_duree(secs)
        except Exception as e:
            duree = "n/a"
            erreurs.append(f"/proc/uptime: {e}")

    if options and getattr(options, "sans_memoire", False):
        mem = {
            "MEM_TOTALE": "Section désactivée",
            "MEM_UTILISEE": "Section désactivée",
            "MEM_UTILISEE_PCT": "Section désactivée",
            "MEM_LIBRE_CACHE": "Section désactivée",
        }
    else:
        mem, err = lire_memoire()
        if err:
            erreurs.append(err)
            mem = {
                "MEM_TOTALE": "Donnée non disponible",
                "MEM_UTILISEE": "Donnée non disponible",
                "MEM_UTILISEE_PCT": "Donnée non disponible",
                "MEM_LIBRE_CACHE": "Donnée non disponible",
            }

    if options and getattr(options, "sans_materiel", False):
        lignes_t = ("<tr><td colspan='3'>Section désactivée par les paramètres</td></tr>")
        elements_alim = ("<li>Section désactivée par les paramètres</li>")
    else:
        lignes_t = prendre_temperatures()
        elements_alim = prendre_alim()
    if options and getattr(options, "sans_disques", False):
        lignes_disques = ("<tr><td colspan='5'>Section désactivée par les paramètres</td></tr>")
    else:
        lignes_disques = prendre_disques()

    if options and getattr(options, "sans_processus", False):
        lignes_processus = ("<tr><td colspan='5'>Section désactivée par les paramètres</td></tr>")
    else:
        lignes_processus = prendre_processus()

    if options and getattr(options, "sans_reseau", False):
        lignes_interfaces = ("<tr><td colspan='5'>Section désactivée par les paramètres</td></tr>")
        elements_connexions = ("<li>Section désactivée par les paramètres</li>")
    else:
        lignes_interfaces = prendre_interfaces()
        elements_connexions = prendre_connexions()

    if options and getattr(options, "sans_web", False):
        lignes_web = ("<tr><td colspan='6'>Section désactivée par les paramètres</td></tr>")
    else:
        lignes_web = prendre_web()

    jetons = {
        "NOM_HOTE": nom_hote,
        "DATE_HEURE": date_heure,
        "DATE": date,
        "NOYAU": noyau,
        "DUREE_FONCTIONNEMENT": duree,
        "MEM_TOTALE": mem["MEM_TOTALE"],
        "MEM_UTILISEE": mem["MEM_UTILISEE"],
        "MEM_UTILISEE_PCT": mem["MEM_UTILISEE_PCT"],
        "MEM_LIBRE_CACHE": mem["MEM_LIBRE_CACHE"],
        "LIGNES_TEMPERATURES": lignes_t,
        "ELEMENTS_ALIM": elements_alim,
        "LIGNES_DISQUES": lignes_disques,
        "LIGNES_PROCESSUS": lignes_processus,
        "LIGNES_INTERFACES": lignes_interfaces,
        "ELEMENTS_CONNEXIONS": elements_connexions,
        "LIGNES_WEB": lignes_web,
        "ELEMENTS_ERREURS": (
            "\n".join(f"<li>{html.escape(e)}</li>" for e in erreurs)
            if erreurs
            else "<li>Aucune erreur</li>"
        ),
    }
    return jetons

def main():
    parseur = argparse.ArgumentParser()
    parseur.add_argument("--page", dest="page", default="rapport_supkrellm.html")
    parseur.add_argument("--donnees", default="donnees_systeme.html")
    parseur.add_argument("--intervalle", type=float, default=2.0)
    parseur.add_argument("--dossier", default=".")
    parseur.add_argument("--gui")

    parseur.add_argument("--sans-memoire", action="store_true")
    parseur.add_argument("--sans-disques", action="store_true")
    parseur.add_argument("--sans-processus", action="store_true")
    parseur.add_argument("--sans-reseau", action="store_true")
    parseur.add_argument("--sans-web", action="store_true")
    parseur.add_argument("--sans-materiel", action="store_true")

    args = parseur.parse_args()
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
