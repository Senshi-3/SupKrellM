import datetime
import glob
import html
import http.client
import json
import ssl
import subprocess
from pathlib import Path
from utils import lire_fichier, format_duree

# Récupère et calcule toutes les infos de mémoire (totale, utilisée, libre+cache)
def lire_memoire():
    txt, err = lire_fichier("/proc/meminfo")
    if err:
        return None, err
    kv = {}
    for ligne in txt.splitlines():
        if ":" in ligne:
            k, v = ligne.split(":", 1)
            kv[k.strip()] = v.strip()

    # Petite fonction interne pour convertir des kB en Gio
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

# Cherche les températures dans /sys/class/thermal/... et fabrique les lignes HTML du tableau
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

# Récupère les infos d’alimentation (batterie) dans /sys/class/power_supply et les affiche en liste HTML
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

# Utilise la commande df -T -hP pour récupérer les infos de disques et construit le tableau HTML
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

# Utilise ps aux --sort=-%cpu pour afficher les 10 processus les plus gourmands en CPU
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

# Récupère les interfaces réseau (IP, RX/TX, état) en combinant ip -j addr, /proc/net/dev et /sys/class/net
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
        return "<tr><td colspan='5' style='color:#d64545'>Aucune interface réseau détectée</td></tr>"
    return "\n".join(lignes)

# Liste les connexions réseau (ports ouverts, etc.) avec la commande ss -tuln
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

# Analyse une ligne de sortie de ss pour extraire l’hôte et le port locaux
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

# Se connecte à un service HTTP/HTTPS pour récupérer titre, favicon, serveur, protocole, statut HTTP
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
        except Exception:
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

# Scanne les ports 80/443 détectés par ss et construit le tableau HTML des services web
def prendre_web() -> str:
    lignes = []
    try:
        res = subprocess.run(
            ["ss", "-ntlp"],
            capture_output=True,
            text=True,
            timeout=2,
        )
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
                titre, favicon, serveur, proto_tls, statut = sonder_service_http(
                    host, port, use_https=use_https
                )
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

# Récupère toutes les métriques (général, mémoire, matériel, réseau, etc.) et renvoie le dict de jetons
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
