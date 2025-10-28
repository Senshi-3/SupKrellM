import argparse
import datetime
import html
import json
import glob
import subprocess
from pathlib import Path

MODELE_HTML = r"""
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
    <footer>
        Généré le <span class="valeur">%%DATE_HEURE%%</span>
    </footer>
</body>
</html>"""

CLES_BRUTES = {
    "LIGNES_TEMPERATURES", "ELEMENTS_ALIM", "LIGNES_DISQUES", "LIGNES_PROCESSUS",
    "LIGNES_INTERFACES", "ELEMENTS_CONNEXIONS", "LIGNES_WEB", "ELEMENTS_ERREURS"
}

# -------------------------
# Fonctions utilitaires
# -------------------------
def generer_rapport(modele: str, jetons: dict) -> str:
    """Remplace les placeholders %%CLE%% par les valeurs.
       - Pour les clés 'brutes', on insère le HTML tel quel.
       - Pour les autres, on échappe le contenu.
       - On nettoie enfin les placeholders restants."""
    sortie = modele
    for cle, valeur in jetons.items():
        if cle in CLES_BRUTES:
            val = str(valeur)
        else:
            val = html.escape(str(valeur), quote=True)
        sortie = sortie.replace("%%" + cle + "%%", val)
    # supprimer placeholders restants (sécurité)
    import re
    sortie = re.sub(r"%%[A-Z0-9_]+%%", "", sortie)
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

# -------------------------
# Collecte Mémoire
# -------------------------
def analyser_meminfo():
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
    utilisee = max(0.0, total - libre - tampons - cache - reclaim + shmem)
    pct = (utilisee / total * 100.0) if total > 0 else 0.0
    return {
        "MEM_TOTALE": f"{total:.1f} Go",
        "MEM_UTILISEE": f"{utilisee:.1f} Go",
        "MEM_UTILISEE_PCT": f"{pct:.1f}%",
        "MEM_LIBRE_CACHE": f"{libre_cache:.1f} Go",
    }, None

# -------------------------
# Températures
# -------------------------
def collecter_temperatures():
    lignes = []
    zones = sorted(glob.glob("/sys/class/thermal/thermal_zone*/temp"))
    for tz in zones:
        try:
            with open(tz, "r") as f:
                raw = f.read().strip()
            temp_milli = int(raw)
            temp_c = temp_milli / 1000.0
            nom = Path(tz).parent.name
            lignes.append(f"<tr><td>{nom}</td><td>{temp_c:.1f} °C</td><td><span class='badge ok'>OK</span></td></tr>")
        except Exception:
            lignes.append(f"<tr><td>{tz}</td><td>N/A</td><td><span class='badge err'>N/A</span></td></tr>")
    if not lignes:
        lignes.append("<tr><td>—</td><td>N/A</td><td><span class='badge'>N/A</span></td></tr>")
    return "\n".join(lignes)

# -------------------------
# Alimentation / Batterie (sans os)
# -------------------------
def collecter_alimentation():
    lignes = []
    bats = sorted(glob.glob("/sys/class/power_supply/BAT*"))
    if not bats:
        return "<li>Aucune batterie détectée</li>"
    for bat in bats:
        try:
            with open(f"{bat}/status", "r") as f:
                status = f.read().strip()
        except Exception:
            status = "N/A"
        try:
            with open(f"{bat}/capacity", "r") as f:
                cap = f.read().strip()
        except Exception:
            cap = "N/A"
        nom = Path(bat).name
        lignes.append(f"<li>{nom}: {status} — {cap}%</li>")
    return "\n".join(lignes)

# -------------------------
# Disques (df)
# -------------------------
def collecter_disques():
    try:
        r = subprocess.run(["df", "-T", "-hP"], capture_output=True, text=True, timeout=3)
        lignes = []
        for line in r.stdout.splitlines()[1:]:
            parts = line.split()
            if len(parts) >= 7:
                device, fstype, size, used, avail, pcent, mount = parts[:7]
                # correspond aux colonnes du template (Périphérique, Montage, Utilisation, Espace libre, Type)
                lignes.append(f"<tr><td>{device}</td><td>{mount}</td><td>{pcent}</td><td>{avail}</td><td>{fstype}</td></tr>")
        if not lignes:
            return "<tr><td colspan='5'>N/A</td></tr>"
        return "\n".join(lignes)
    except Exception:
        return "<tr><td colspan='5'>N/A</td></tr>"

# -------------------------
# Processus (top 10 CPU)
# -------------------------
def collecter_processus():
    try:
        r = subprocess.run(["ps", "aux", "--sort=-%cpu"], capture_output=True, text=True, timeout=3)
        lignes = []
        for line in r.stdout.splitlines()[1:11]:
            parts = line.split(None, 10)
            if len(parts) >= 11:
                user, pid, cpu, mem, vsz, rss, tty, stat, start, timeu, command = parts
                cmd_safe = html.escape(command)[:120]
                lignes.append(f"<tr><td>{pid}</td><td>{user}</td><td>{cpu}%</td><td>{mem}%</td><td>{cmd_safe}</td></tr>")
        if not lignes:
            return "<tr><td colspan='5'>N/A</td></tr>"
        return "\n".join(lignes)
    except Exception:
        return "<tr><td colspan='5'>N/A</td></tr>"

# -------------------------
# Interfaces réseau
# -------------------------
def collecter_interfaces():
    # récup IP via `ip -j addr`, RX/TX via /proc/net/dev
    ipv4 = {}
    ipv6 = {}
    try:
        r = subprocess.run(["ip", "-j", "addr"], capture_output=True, text=True, timeout=2)
        for ifc in json.loads(r.stdout):
            name = ifc.get("ifname")
            for addr in ifc.get("addr_info", []):
                fam = addr.get("family")
                if fam == "inet":
                    ipv4.setdefault(name, []).append(addr.get("local"))
                elif fam == "inet6":
                    ipv6.setdefault(name, []).append(addr.get("local"))
    except Exception:
        pass

    rxtx = {}
    try:
        with open("/proc/net/dev", "r") as f:
            for line in f.readlines()[2:]:
                if ":" not in line:
                    continue
                iface, rest = line.split(":", 1)
                name = iface.strip()
                nums = rest.split()
                rx = int(nums[0]) if nums else 0
                tx = int(nums[8]) if len(nums) > 8 else 0
                rxtx[name] = (rx, tx)
    except Exception:
        pass

    lignes = []
    noms = sorted(set(list(rxtx.keys()) + list(ipv4.keys()) + list(ipv6.keys())))
    for n in noms:
        ip4 = ", ".join(ipv4.get(n, [])) or "—"
        ip6 = ", ".join(ipv6.get(n, [])) or "—"
        rx, tx = rxtx.get(n, (0, 0))
        try:
            with open(f"/sys/class/net/{n}/operstate", "r") as f:
                etat = f.read().strip()
        except Exception:
            etat = "N/A"
        lignes.append(f"<tr><td>{n}</td><td>{ip4}</td><td>{ip6}</td><td>{rx//1024}K / {tx//1024}K</td><td><span class='badge'>{etat}</span></td></tr>")
    if not lignes:
        return "<tr><td colspan='5'>N/A</td></tr>"
    return "\n".join(lignes)

# -------------------------
# Connexions et services Web (placeholder simple)
# -------------------------
def collecter_connexions():
    # Retourne une liste d'items HTML (ex: services à l'écoute)
    try:
        r = subprocess.run(["ss", "-tuln"], capture_output=True, text=True, timeout=2)
        lignes = []
        for line in r.stdout.splitlines()[1:]:
            lignes.append(f"<li>{html.escape(line)}</li>")
        if not lignes:
            return "<li>Aucune connexion</li>"
        return "\n".join(lignes)
    except Exception:
        return "<li>N/A</li>"

def collecter_services_web():
    # Placeholder: listage simple des ports 80/443 locaux (on peut enrichir avec urllib)
    rows = []
    try:
        r = subprocess.run(["ss", "-ntlp"], capture_output=True, text=True, timeout=2)
        for ligne in r.stdout.splitlines():
            if ":80 " in ligne or ":443 " in ligne:
                rows.append(f"<tr><td>{html.escape(ligne)}</td><td>—</td><td>—</td><td>—</td><td>—</td><td><span class='badge ok'>OK</span></td></tr>")
        if not rows:
            return "<tr><td colspan='6'>Aucun service web détecté</td></tr>"
        return "\n".join(rows)
    except Exception:
        return "<tr><td colspan='6'>N/A</td></tr>"

# -------------------------
# Collecte globale et composition des jetons
# -------------------------
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
        mem = {"MEM_TOTALE":"n/a","MEM_UTILISEE":"n/a","MEM_UTILISEE_PCT":"n/a","MEM_LIBRE_CACHE":"n/a"}

    jetons = {
        "NOM_HOTE": nom_hote,
        "DATE_HEURE": date_heure,
        "NOYAU": noyau,
        "DUREE_FONCTIONNEMENT": duree_fonctionnement,
        "MEM_TOTALE": mem["MEM_TOTALE"],
        "MEM_UTILISEE": mem["MEM_UTILISEE"],
        "MEM_UTILISEE_PCT": mem["MEM_UTILISEE_PCT"],
        "MEM_LIBRE_CACHE": mem["MEM_LIBRE_CACHE"],

        "LIGNES_TEMPERATURES": collecter_temperatures(),
        "ELEMENTS_ALIM": collecter_alimentation(),
        "LIGNES_DISQUES": collecter_disques(),
        "LIGNES_PROCESSUS": collecter_processus(),
        "LIGNES_INTERFACES": collecter_interfaces(),
        "ELEMENTS_CONNEXIONS": collecter_connexions(),
        "LIGNES_WEB": collecter_services_web(),

        "ELEMENTS_ERREURS": "\n".join(f"<li>{html.escape(e)}</li>" for e in erreurs) if erreurs else "<li>Aucune erreur</li>",
    }
    return jetons

def main():
    parseur = argparse.ArgumentParser(description="Génère un rapport HTML du système (Linux).")
    parseur.add_argument("--sortie", default="/home/senshi/rapport_supkrellm.html",
                         help="Chemin du fichier HTML de sortie")
    parseur.add_argument("--modele", help="Chemin vers un template HTML externe")  # <-- AJOUT

    args = parseur.parse_args()

    # <-- AJOUT : charger le template externe si fourni
    if args.modele:
        modele = Path(args.modele).read_text(encoding="utf-8")
    else:
        modele = MODELE_HTML

    jetons = collecter_donnees()
    html_final = generer_rapport(modele, jetons)

    Path(args.sortie).write_text(html_final, encoding="utf-8")
    print("Rapport HTML :", args.sortie)

if __name__ == "__main__":
    main()
