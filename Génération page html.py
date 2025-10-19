import argparse, re, datetime

TEMPLATE =  r"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width,initial-scale=1" />
    <title>Rapport Linux</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Audiowide&family=Roboto:ital,wght@0,100..900;1,100..900&display=swap" rel="stylesheet">
    <style>
        :root{
            --ok:#1f9d55; --warn:#c07f00; --err:#d64545;
            --mono: ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace;
        }
        html,body{
            margin:0;
            padding:0;
            background: linear-gradient(rgb(11, 16, 32));
            font-family:system-ui,-apple-system,Segoe UI,Roboto,Ubuntu,Arial,sans-serif;
            scroll-behavior: smooth;
        }
        a{
            text-decoration:none;
        }
        a:hover{
            transform: scale(1.1);
        } 
        header{
            position:sticky;
            top:0;
            padding-bottom: 1vw;
            display: flex;
            background: linear-gradient(180deg,rgba(11, 16, 32,0.95),rgba(11, 16, 32,0.7));
            backdrop-filter:blur(5px);
            z-index:3;
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
            align-items:flex-start;
        }
        .texte-navigateur{
            font-family: "Audiowide", sans-serif;
            color:#4ca3cb;
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
        .texte-navigateur:nth-child(8) { animation-delay: 2.8s; }
        
        main{
            max-width:55vw;
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
        section:target, section:target{
            animation: mis-en-évidence 0.3s ease-out;
        }
        section:target .spans{
            animation: bordur-évidence 1s linear;
        }
        section:target .spans2{
            animation: bordur-évidence 1s linear;
        }
        section:target .spanserr{
            animation: bordur-évidence-err 1s linear;
        }
        .spans{
            background-color: rgba(24, 35, 58, 0.733);
            padding: 1vw;
            border-radius: 1em;
            border: 1px solid #5e7d8aab;
            display: flex;
            flex-direction: column;
        }
        .spans2{
            background-color: rgba(24, 35, 58, 0);
            padding-bottom: 1vw;
            border-radius: 1em;
            border: 1px solid #5e7d8aab;
            display: flex;
            flex-direction: column;
        }
        .spanserr{
            border-left: 3px solid var(--err);
            padding: 1vw;
            border-radius:12px;
            background:rgba(214,69,69,.08);
            margin-bottom:1vw;
        }
        .spans:hover{
            box-shadow: 0px 0px 3px 3px #2c627a;
        }
        .spanserr:hover{
            box-shadow: 0px 0px 3px 3px #7a2c2c;
        }
        .label{
            color: #91c2d89a;
            font-family: var(--mono);
            padding-bottom: 1vw;
            user-select: none;
        }
        .value{
            color: #c9d1ff;
            font-family: var(--mono);
        }
        .grid1{
            display:grid;
            grid-template-columns:repeat(3,1fr);
            gap:16px;
        }
        .grid2{
            display:grid;
            grid-template-columns:repeat(2,1fr);
            gap:16px;
        }
        table{
            width:100%;
            border-collapse:collapse;
        }
        th,td{
            padding: 1vw;
            border-bottom:1px solid #1c2347;
            text-align:left;
            color:#c9d1ff;
        }
        th{
            font-weight: 0.8vw;
            color:#c9d1ff;
        }
        li{
            font-weight: 0.8vw;
            color:#c9d1ff;
        }
        #erreur-texte{
            color: #a12828;
        }
        footer{
            color:#a8b0d9;
            font-size: 0.8vw;
            text-align:center;
            margin: 1vw;
        }
        .badge{
            display:inline-block;
            padding:.15rem .5rem;
            border-radius:999px;
            font-size:.8rem;
            border:1px solid #2a366b;
            background:#0e1430;
            color:var(--muted)
        }
        .ok{
            color:#d6ffe6;
            border-color:rgba(31,157,85,.45);
            background:rgba(31,157,85,.08)
        }
        .warn{
            color:#fff4d6;
            border-color:rgba(192,127,0,.45);
            background:rgba(192,127,0,.08)
        }
        .err{
            color:#ffe1e1;
            border-color:rgba(214,69,69,.45);
            background:rgba(214,69,69,.08)
        }  

        @keyframes mis-en-évidence {
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
        @keyframes bordur-évidence {
            0%{
                border-color: white;
                outline: 2px solid white;
                outline-offset: 0.3vw;
            }
            90%{
                border-color: white;
                outline: 2px solid white;
                outline-offset: 0.3vw;
            }
            100%{
                border-color: #5e7d8aab;
                outline: 0px solid #5e7d8aab;
                outline-offset: 0vw;
            }
        }
        @keyframes bordur-évidence-err {
            0%{
                border-color: var(--err);
                outline: 2px solid var(--err);
                outline-offset: 0.3vw;
            }
            90%{
                border-color: var(--err);
                outline: 2px solid var(--err);
                outline-offset: 0.3vw;
            }
            100%{
                border-color: var(--err);
                outline: 2px solid var(--err);
                outline-offset: 0vw;
            }
        }

        @keyframes entrer-nav-text {
            0%{
                top: 100px;
                opacity: 0;
            }
            100%{
                top: 0px;
                opacity: 1;
            }
        }
    </style>
</head>
<body>
    <header>
        <h1 id="texte-titre">Rapport système – <span>%%HOSTNAME%%</span></h1>
        <nav id="navigateur">
            <a href="#overview" class="texte-navigateur">Vue d’ensemble</a>
            <a href="#hardware" class="texte-navigateur">Matériel</a>
            <a href="#memory" class="texte-navigateur">Mémoire</a>
            <a href="#disks" class="texte-navigateur">Disques</a>
            <a href="#processes" class="texte-navigateur">Processus</a>
            <a href="#network" class="texte-navigateur">Réseau</a>
            <a href="#web" class="texte-navigateur">Services web</a>
            <a href="#errors" class="texte-navigateur">Erreurs</a>
        </nav>
    </header>
    <main>
        <section id="overview" class="section">
            <h2>Vue d’ensemble</h2>
            <div class="grid1">
                <div class="spans">
                    <span class="label">Date de génération</span>
                    <span class="value">%%DATETIME%%</span>
                </div>
                <div class="spans">
                    <span class="label">Noyau</span>
                    <span class="value">%%KERNEL%%</span>
                </div>
                <div class="spans">
                    <span class="label">Uptime</span>
                    <span class="value">%%UPTIME%%</span>
                </div>
            </div>
        </section>
        <section id="hardware" class="section">
            <h2>Matériel &amp; alimentation</h2>
            <div class="grid2">
                <div class="spans">
                    <div class="label">Températures</div>
                    <div class="table-wrap">
                        <table>
                            <thead><tr><th>Capteur</th><th>Température</th><th>État</th></tr></thead>
                            <tbody>
                                %%TEMPS_ROWS%%
                            </tbody>
                        </table>
                    </div>
                </div>
                <div class="spans">
                    <div class="label">Alimentation</div>
                    <ul>
                        %%POWER_ITEMS%%
                    </ul>
                </div>
            </div>
        </section>
        <section id="memory" class="section">
            <h2>Mémoire</h2>
            <div class="grid1">
                <div class="spans">
                    <span class="label">Totale</span>
                    <span class="value">%%MEM_TOTAL%%</span>
                </div>
                <div class="spans">
                    <span class="label">Utilisée</span>
                    <span class="value">%%MEM_USED%% (%%MEM_USED_PCT%%)</span>
                </div>
                <div class="spans">
                    <span class="label">Libre + cache</span>
                    <span class="value">%%MEM_FREE_CACHE%%</span>
                </div>
            </div>
        </section>
        <section id="disks" class="section">
            <h2>Disques</h2>
            <div class="spans2">
                <table>
                    <thead><tr><th>Périphérique</th><th>Montage</th><th>Utilisation</th><th>Espace libre</th><th>Type</th></tr></thead>
                    <tbody>
                        %%DISK_ROWS%%
                    </tbody>
                </table>
            </div>
        </section>
        <section id="processes" class="section">
            <h2>Processus actifs</h2>
            <div class="spans2">
                <table>
                    <thead><tr><th>PID</th><th>Utilisateur</th><th>CPU %</th><th>RAM %</th><th>Commande</th></tr></thead>
                    <tbody>
                        %%PROC_ROWS%%
                    </tbody>
                </table>
            </div>
        </section>
        <section id="network" class="section">
            <h2>Réseau</h2>
                <div class="grid2">
                    <div class="spans">
                        <div class="label">Interfaces</div>
                        <div class="table-wrap" role="region" aria-label="Interfaces réseau">
                            <table>
                                <thead><tr><th>Interface</th><th>IPv4</th><th>IPv6</th><th>RX/TX</th><th>État</th></tr></thead>
                                <tbody>
                                    %%NET_IF_ROWS%%
                                </tbody>
                            </table>
                        </div>
                    </div>
                    <div class="spans">
                        <div class="label">Connexions</div>
                        <ul>
                            %%NET_CONN_ITEMS%%
                        </ul>
                    </div>
                </div>
        </section>
        <section id="web" class="section">
            <h2>Services web</h2>
            <div class="spans2">
                <table>
                    <thead><tr><th>Hôte</th><th>Titre</th><th>Favicon</th><th>Serveur</th><th>Proto/TLS</th><th>Statut</th></tr></thead>
                    <tbody>
                        %%WEB_ROWS%%
                    </tbody>
                </table>
            </div>
        </section>
        <section id="errors" class="section">
            <h2 id="erreur-texte">Erreurs de collecte</h2>
            <div class="spanserr">
                <ul>
                    %%ERROR_ITEMS%%
                </ul>
            </div>
        </section>
    </main>
    <footer>
        Généré le <span class="value">%%DATETIME%%</span>
    </footer>
</body>
</html>"""


def render_report(tpl: str, tokens: dict,) -> str:
    out = tpl
    for k, v in tokens.items():
        out = out.replace("%%" + k + "%%", v)
    return out

def data():
    return {
        "HOSTNAME": "demo-machine",
        "DATETIME": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "KERNEL": "Linux demo 6.1.0-demo #1 SMP PREEMPT x86_64 GNU/Linux",
        "UPTIME": "3 days, 05:12:44",
        "MEM_TOTAL": "16 Go",
        "MEM_USED": "9.1 Go",
        "MEM_USED_PCT": "56.9%",
        "MEM_FREE_CACHE": "7.3 Go",
        "FAVICON_DATAURL": "data:;base64,",
        "TEMPS_ROWS": "<tr><td>CPU</td><td>63.2&nbsp;°C</td><td><span class='badge warn'>élevée</span></td></tr><tr><td>GPU</td><td>54.0&nbsp;°C</td><td><span class='badge ok'>ok</span></td></tr>",
        "POWER_ITEMS": "<li>Alimentation: secteur — <span class='badge ok'>OK</span></li>",
        "DISK_ROWS": "<tr><td>/dev/sda1</td><td>/</td><td>71%</td><td>11.2&nbsp;Go</td><td>ext4</td></tr><tr><td>/dev/sdb1</td><td>/data</td><td>42%</td><td>212.5&nbsp;Go</td><td>xfs</td></tr>",
        "PROC_ROWS": "<tr><td>1</td><td>root</td><td>0.0</td><td>0.1</td><td>/sbin/init</td></tr><tr><td>2345</td><td>www-data</td><td>12.3</td><td>1.2</td><td>nginx: worker</td></tr><tr><td>4567</td><td>alice</td><td>3.2</td><td>0.8</td><td>python3 script.py</td></tr>",
        "NET_IF_ROWS": "<tr><td>eth0</td><td>192.168.1.10</td><td>fe80::1</td><td>1.2G / 850M</td><td><span class='badge ok'>UP</span></td></tr><tr><td>wlan0</td><td>—</td><td>—</td><td>0 / 0</td><td><span class='badge'>DOWN</span></td></tr>",
        "NET_CONN_ITEMS": "<li>:80 LISTEN (nginx)</li><li>:443 LISTEN (apache2)</li>",
        "WEB_ROWS": "<tr><td>localhost:80</td><td>Page d'accueil</td><td><img alt='favicon localhost' src='data:;base64,' width='16' height='16'></td><td>nginx/1.24</td><td>HTTP/1.1</td><td><span class='badge ok'>200</span></td></tr><tr><td>localhost:443</td><td>Welcome</td><td><img alt='favicon localhost' src='data:;base64,' width='16' height='16'></td><td>Apache/2.4</td><td>TLS 1.3</td><td><span class='badge ok'>200</span></td></tr>",
        "ERROR_ITEMS": "<li>Aucune erreur — démonstration</li>",
    }


def cli(argv=None):
    p = argparse.ArgumentParser(description="Génère un rapport HTML")
    p.add_argument("--output",default=r"C:\Users\Sensh\OneDrive\Documents\sfvzeg\rapport_supkrellm_demo.html")
    args = p.parse_args(argv)
    tokens = data()
    html = render_report(TEMPLATE, tokens)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(html)
    print("Rapport HTML:", args.output)

cli()
