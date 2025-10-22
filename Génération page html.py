import argparse
import datetime
import html

MODELE_HTML = r"""<!DOCTYPE html>
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
        :root {
            --ok: #1f9d55;
            --warn: #c07f00;
            --err: #d64545;
            --mono: ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace;
        }

        html, body {
            margin: 0;
            padding: 0;
            background-color: rgb(11, 16, 32);
            font-family: system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Arial, sans-serif;
            scroll-behavior: smooth;
        }

        a {
            text-decoration: none;
        }

        a:hover {
            transform: scale(1.1);
        }

        header {
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

        #texte-titre {
            font-family: "Audiowide", sans-serif;
            color: white;
        }

        #navigateur {
            display: flex;
            gap: 2vw;
            align-items: flex-start;
        }

        .texte-navigateur {
            font-family: "Audiowide", sans-serif;
            color: #4ca3cb;
            position: relative;
            animation: entrer-nav-text 1.5s forwards;
            opacity: 0;
        }

        .texte-navigateur:nth-child(1) { animation-delay: 0s; }
        .texte-navigateur:nth-child(2) { animation-delay: 0.4s; }
        .texte-navigateur:nth-child(3) { animation-delay: 0.8s; }
        .texte-navigateur:nth-child(4) { animation-delay: 1.2s; }
        .texte-navigateur:nth-child(5) { animation-delay: 1.6s; }
        .texte-navigateur:nth-child(6) { animation-delay: 2s; }
        .texte-navigateur:nth-child(7) { animation-delay: 2.4s; }
        .texte-navigateur:nth-child(8) { animation-delay: 2.8s; color: var(--err); }

        main {
            max-width: 55vw;
            margin: 0 auto;
            padding: 0;
        }

        h2 {
            display: inline-block;
            color: #287da1;
        }

        .section {
            scroll-margin-top: 7vw;
        }

        section:target {
            animation: mis-en-evidence 0.3s ease-out;
        }

        section:target .grille3,
        section:target .grille2,
        section:target .bloc-table {
            animation: bordure-evidence 1s linear;
        }

        section:target .bloc-erreurs {
            animation: bordure-evidence-err 1s linear;
        }

        .bloc {
            background-color: rgba(24, 35, 58, 0.733);
            padding: 1vw;
            border-radius: 1em;
            border: 1px solid #5e7d8aab;
            display: flex;
            flex-direction: column;
        }

        .bloc-table {
            background-color: rgba(24, 35, 58, 0);
            padding-bottom: 1vw;
            border-radius: 1em;
            border: 1px solid #5e7d8aab;
            display: flex;
            flex-direction: column;
        }

        .bloc-erreurs {
            border-left: 3px solid var(--err);
            padding: 1vw;
            border-radius: 1em;
            background: rgba(214, 69, 69, .08);
            margin-bottom: 1vw;
        }

        .bloc:hover {
            box-shadow: 0 0 3px 3px #2c627a;
        }

        .bloc-erreurs:hover {
            box-shadow: 0 0 3px 3px #7a2c2c;
        }

        .etiquette {
            color: #91c2d89a;
            font-family: var(--mono);
            padding-bottom: 1vw;
            user-select: none;
        }

        .valeur {
            color: #c9d1ff;
            font-family: var(--mono);
        }

        .grille3 {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 16px;
            border-radius: 1em;
        }

        .grille2 {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 16px;
            border-radius: 1em;
        }

        table {
            width: 100%;
            border-collapse: collapse;
        }

        th, td {
            padding: 1vw;
            border-bottom: 1px solid #1c2347;
            text-align: left;
            color: #c9d1ff;
        }

        th {
            color: #c9d1ff;
        }

        li {
            color: #c9d1ff;
        }

        ul, ol {
            margin-left: 1vw;
            padding-left: 1.2rem;
        }

        #texte-erreurs {
            color: #a12828;
        }

        footer {
            color: #a8b0d9;
            font-size: 0.8vw;
            text-align: center;
            margin: 1vw;
        }

        .badge {
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

        @keyframes mis-en-evidence {
            0% { transform: scale(1); }
            40% { transform: scale(1.1); }
            100% { transform: scale(1); }
        }

        @keyframes bordure-evidence {
            0% { outline: 2px solid #5e7d8aab; outline-offset: 0.3vw; }
            90% { outline: 1px solid #5e7d8aab; outline-offset: 0.3vw; }
            100% { outline: 0; outline-offset: 0; }
        }

        @keyframes bordure-evidence-err {
            0% { outline: 2px solid var(--err); outline-offset: 0.3vw; }
            90% { outline: 1px solid var(--err); outline-offset: 0.3vw; }
            100% { outline: 0; outline-offset: 0; }
        }

        @keyframes entrer-nav-text {
            0% { top: 100px; opacity: 0; }
            100% { top: 0; opacity: 1; }
        }

        @media (max-width: 767px) {
            #texte-titre { font-size: 4vw; }
            #navigateur { gap: 1vw; }
            .texte-navigateur, th, td, li, footer { font-size: 2vw; }
            main { max-width: 90vw; }
            h2 { font-size: 3vw; }
            .section { scroll-margin-top: 10vw; }
            .bloc, .bloc-table, .bloc-erreurs, .grille3, .grille2 { border-radius: 0.5em; }
            .etiquette, .badge { font-size: 1.7vw; }
            .valeur { font-size: 2.3vw; }
            .grille3, .grille2 { gap: 7px; }
        }

        @media (min-width: 768px) and (max-width: 1023px) {
            #texte-titre { font-size: 3vw; }
            #navigateur { gap: 2vw; }
            .texte-navigateur, th, td, li, footer { font-size: 1.5vw; }
            main { max-width: 80vw; }
            h2 { font-size: 2.7vw; }
            .section { scroll-margin-top: 9vw; }
            .bloc, .bloc-table, .bloc-erreurs, .grille3, .grille2 { border-radius: 0.5em; }
            .etiquette, .badge { font-size: 1.3vw; }
            .valeur { font-size: 1.8vw; }
            .grille3, .grille2 { gap: 10px; }
        }
    </style>
</head>
<body>
    <header>
        <h1 id="texte-titre">Rapport système – <span>%%NOM_HOTE%%</span></h1>
        <nav id="navigateur">
            <a href="#apercu" class="texte-navigateur">Vue d’ensemble</a>
            <a href="#materiel" class="texte-navigateur">Matériel</a>
            <a href="#memoire" class="texte-navigateur">Mémoire</a>
            <a href="#disques" class="texte-navigateur">Disques</a>
            <a href="#processus" class="texte-navigateur">Processus</a>
            <a href="#reseau" class="texte-navigateur">Réseau</a>
            <a href="#web" class="texte-navigateur">Services web</a>
            <a href="#erreurs" class="texte-navigateur">Erreurs</a>
        </nav>
    </header>

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

    </main>
</body>
</html>"""

CLES_BRUTES = {
    "LIGNES_TEMPERATURES", "ELEMENTS_ALIM", "LIGNES_DISQUES", "LIGNES_PROCESSUS",
    "LIGNES_INTERFACES", "ELEMENTS_CONNEXIONS", "LIGNES_WEB", "ELEMENTS_ERREURS"
}

def generer_rapport(modele: str, jetons: dict) -> str:
    sortie = modele
    for cle, valeur in jetons.items():
        texte = valeur if cle in CLES_BRUTES else html.escape(str(valeur), quote=True)
        sortie = sortie.replace("%%" + cle + "%%", texte)
    return sortie

def lire_fichier(chemin):
    try:
        with open(chemin, "r", encoding="utf-8", errors="ignore") as f:
            return f.read().strip(), None
    except Exception as e:
        return None, f"{chemin}: {e}"

def formater_duree(secondes_flottantes):
    s = int(secondes_flottantes)
    h, s = divmod(s, 3600)
    m, s = divmod(s, 60)
    j, h = divmod(h, 24)
    if j > 0:
        return f"{j} jours, {h:02d}:{m:02d}:{s:02d}"
    return f"{h:02d}:{m:02d}:{s:02d}"

def analyser_meminfo():
    texte, err = lire_fichier("/proc/meminfo")
    if err:
        return None, err
    kv = {}
    for ligne in texte.splitlines():
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
    reclaimable = ko_vers_gio(kv.get("SReclaimable", "0 kB"))
    shmem = ko_vers_gio(kv.get("Shmem", "0 kB"))

    libre_cache = libre + tampons + cache + reclaimable - shmem
    utilisee = max(0.0, total - libre - tampons - cache - reclaimable + shmem)
    pct = (utilisee / total * 100.0) if total > 0 else 0.0

    return {
        "MEM_TOTALE": f"{total:.1f} Go",
        "MEM_UTILISEE": f"{utilisee:.1f} Go",
        "MEM_UTILISEE_PCT": f"{pct:.1f}%",
        "MEM_LIBRE_CACHE": f"{libre_cache:.1f} Go",
    }, None

def collecter_donnees():
    erreurs = []

    date_heure = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    nom_hote, err = lire_fichier("/proc/sys/kernel/hostname")
    if err: erreurs.append(err)
    if not nom_hote: nom_hote = "inconnu"

    noyau, err = lire_fichier("/proc/version")
    if err: erreurs.append(err)
    if not noyau: noyau = "n/a"

    txt_uptime, err = lire_fichier("/proc/uptime")
    if err:
        erreurs.append(err)
        duree_fonctionnement = "n/a"
    else:
        try:
            secondes = float(txt_uptime.split()[0])
            duree_fonctionnement = formater_duree(secondes)
        except Exception as e:
            duree_fonctionnement = "n/a"
            erreurs.append(f"/proc/uptime: {e}")

    mem, err = analyser_meminfo()
    if err:
        erreurs.append(err)
        mem = {
            "MEM_TOTALE": "n/a",
            "MEM_UTILISEE": "n/a",
            "MEM_UTILISEE_PCT": "n/a",
            "MEM_LIBRE_CACHE": "n/a",
        }

    jetons = {
        "NOM_HOTE": nom_hote,
        "DATE_HEURE": date_heure,
        "NOYAU": noyau,
        "DUREE_FONCTIONNEMENT": duree_fonctionnement,
        "MEM_TOTALE": mem["MEM_TOTALE"],
        "MEM_UTILISEE": mem["MEM_UTILISEE"],
        "MEM_UTILISEE_PCT": mem["MEM_UTILISEE_PCT"],
        "MEM_LIBRE_CACHE": mem["MEM_LIBRE_CACHE"],

        "LIGNES_TEMPERATURES": "<tr><td>—</td><td>—</td><td><span class='badge'>N/A</span></td></tr>",
        "ELEMENTS_ALIM": "<li>N/A</li>",
        "LIGNES_DISQUES": "<tr><td>—</td><td>—</td><td>—</td><td>—</td><td>—</td></tr>",
        "LIGNES_PROCESSUS": "<tr><td>—</td><td>—</td><td>—</td><td>—</td><td>—</td></tr>",
        "LIGNES_INTERFACES": "<tr><td>—</td><td>—</td><td>—</td><td>—</td><td><span class='badge'>N/A</span></td></tr>",
        "ELEMENTS_CONNEXIONS": "<li>N/A</li>",
        "LIGNES_WEB": "<tr><td>—</td><td>—</td><td>—</td><td>—</td><td>—</td><td><span class='badge'>N/A</span></td></tr>",
        "ELEMENTS_ERREURS": "".join(f"<li>{html.escape(e)}</li>" for e in erreurs) if erreurs else "<li>Aucune erreur</li>",
    }
    return jetons

def main():
    parseur = argparse.ArgumentParser(description="Génère un rapport HTML du système (Linux).")
    parseur.add_argument("--sortie", default="/home/senshi/rapport_supkrellm.html", help="Chemin du fichier HTML de sortie")
    args = parseur.parse_args()

    jetons = collecter_donnees()
    html_final = generer_rapport(MODELE_HTML, jetons)

    with open(args.sortie, "w", encoding="utf-8") as f:
        f.write(html_final)

    print("Rapport HTML :", args.sortie)

if __name__ == "__main__":
    main()
