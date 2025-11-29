#Lis un fichier texte et renvoie se qu'il contient (avec une erreur si ça rate)
def lire_fichier(chemin: str):
    try:
        with open(chemin, "r", encoding="utf-8", errors="ignore") as f:
            return f.read().strip(), None
    except Exception as err:
        return None, f"{chemin}: {err}"

#Transforme un nombre de secondes en durée lisible (jours:heures:minutes:secondes)
def format_duree(sec_f: float) -> str:
    s = int(sec_f)
    h, s = divmod(s, 3600)
    m, s = divmod(s, 60)
    j, h = divmod(h, 24)
    if j > 0:
        return f"{j} jours, {h:02d}:{m:02d}:{s:02d}"
    return f"{h:02d}:{m:02d}:{s:02d}"
