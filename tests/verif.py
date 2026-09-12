# -*- coding: utf-8 -*-
"""
Controles du plan de pages locales, AU RENDU.

Le controle qui compte : les nombres affiches sur la page « Le plan » sont
recalcules depuis SON TABLEUR, pas depuis donnees.py. Si je me trompe en
recopiant ses termes, ou s'il change son fichier, le controle tombe. Un
chiffre faux dans un argument destine a le faire changer d'avis est pire que
pas d'argument du tout.

Usage : python3 tests/verif.py http://127.0.0.1:8941
"""
import os
import re
import sys
import urllib.error
import urllib.request

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RACINE)

from playwright.sync_api import sync_playwright

from build import PROPOSE
from donnees import GRILLE, IMAGES, MARQUE, SERVICES, TERMES, TRAVAUX
from villes import REGIONS, TOUTES

BASE = (sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8941").rstrip("/")
TABLEUR = os.path.normpath(os.path.join(RACINE, "..", "Websites platform.xlsx"))

ok, ko = 0, []


def _absent(url):
    """Vrai si l'adresse ne repond PAS 200."""
    try:
        with urllib.request.urlopen(url) as r:
            return r.status != 200
    except urllib.error.HTTPError:
        return True
    except Exception:
        return True


def verif(nom, condition, detail=""):
    global ok
    if condition:
        ok += 1
    else:
        ko.append((nom, detail))
        print("  ECHEC ", nom, " ", detail)


def n(x):
    return f"{x:,}".replace(",", " ")


# --- recalcul INDEPENDANT depuis son tableur -------------------------------
import openpyxl

wb = openpyxl.load_workbook(TABLEUR, data_only=True)
lignes = [[("" if c is None else str(c).strip()) for c in r]
          for r in wb.worksheets[0].iter_rows(values_only=True)]
modeles_xlsx = [r[0] for r in lignes[1:17] if r[0]]
termes_xlsx = [r[0] for r in lignes[29:41] if r[0]]

attendu_mondial = len(modeles_xlsx) * 195 * 20 * 3
attendu_na = len(termes_xlsx) * 200
attendu_fr = len(termes_xlsx) * 100
attendu_total = attendu_mondial + attendu_na + attendu_fr

with sync_playwright() as p:
    nav = p.chromium.launch()
    pg = nav.new_page()
    pg.set_viewport_size({"width": 1280, "height": 900})
    erreurs = []
    pg.on("pageerror", lambda e: erreurs.append(str(e)))

    # ---- 1. les termes affiches sont EXACTEMENT les siens -----------------
    # ---- 0. LE NOM ET LA LANGUE ------------------------------------------
    # Il a donne les deux le 11 septembre : « Modersly / Is the name » et
    # « Langue anglaise ».
    pg.goto(f"{BASE}/index.html", wait_until="networkidle")
    verif("le nom du studio est celui qu'il a donne",
          MARQUE == "Modersly", MARQUE)
    verif("index : la marque est affichee",
          MARQUE in pg.inner_text(".marque"), pg.inner_text(".marque"))
    verif("index : la page est declaree en anglais",
          pg.evaluate("() => document.documentElement.lang") == "en",
          pg.evaluate("() => document.documentElement.lang"))
    # Aucun reste de francais dans le corps des pages principales : le client
    # a demande l'anglais, et une page a moitie traduite se voit tout de suite.
    FR = [" ville", " villes ", "Accueil", "Aucun ", " et le calcul",
          "Ce qui manque", "prestations", "Toutes les"]
    for f in ("index.html", "services.html", "villes.html", "images.html",
              "plan.html", "ville-toronto.html", "region-europe.html"):
        pg.goto(f"{BASE}/{f}", wait_until="domcontentloaded")
        c = pg.inner_text("body")
        restes = [m for m in FR if m in c]
        verif(f"{f} : aucun reste de francais", not restes, str(restes[:3]))

    # ---- 0b. LE TRAVAIL MONTRE EST REEL ET EN LIGNE -----------------------
    # Un site d'agence se juge sur ses realisations. Celles-ci sont de vrais
    # livrables : la suite OUVRE chaque lien et exige un 200. Un portfolio qui
    # pointe vers une page morte est pire qu'un portfolio vide.
    # Le portfolio est desormais SUR L'ACCUEIL (« add the portfolio directly
    # on the same link »). On le cherche donc la, dans la section #work.
    pg.goto(f"{BASE}/index.html", wait_until="networkidle")
    c = pg.inner_text("body")
    verif("le portfolio est sur l'accueil, pas sur une page separee",
          pg.locator("#work").count() == 1, str(pg.locator("#work").count()))
    verif("l'ancienne page work.html n'existe plus",
          _absent(f"{BASE}/work.html"), "work.html repond encore")
    for cle, nom, url, controles, resume, points in TRAVAUX:
        verif(f"work : « {nom} » est presente", nom in c)
        verif(f"work : le nombre de controles de {cle} est affiche",
              str(controles) in c, str(controles))
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                code = r.status
        except Exception as e:
            code = str(e)
        verif(f"work : le projet {cle} est REELLEMENT en ligne", code == 200,
              f"{url} -> {code}")
    faux = pg.evaluate("""() => ({
        citations: document.querySelectorAll('blockquote, .temoignage, .quote').length,
        logos: document.querySelectorAll('.logos img, .logo-wall img').length })""")
    verif("work : aucune citation attribuee ni mur de logos",
          faux["citations"] == 0 and faux["logos"] == 0, str(faux))
    # Et tout projet montre porte un lien SORTANT vers le site reel.
    liens_proj = pg.evaluate("""() => [...document.querySelectorAll('a.proj')]
        .map(a => a.getAttribute('href'))""")
    verif("work : chaque projet pointe vers un site externe reel",
          len(liens_proj) == len(TRAVAUX)
          and all(l.startswith("https://") for l in liens_proj),
          str(liens_proj[:2]))

    verif("les onze termes recopies sont ceux du tableur",
          TERMES == termes_xlsx,
          str([t for t in termes_xlsx if t not in TERMES][:3]))

    pg.goto(f"{BASE}/services.html", wait_until="networkidle")
    liste = pg.evaluate("() => [...document.querySelectorAll('.liste2 li')]"
                        ".map(l => l.textContent.trim())")
    verif("la page Services affiche les onze termes du tableur",
          liste == termes_xlsx, str(liste[:3]))

    # ---- 2. L'ARITHMETIQUE, contre le tableur ----------------------------
    pg.goto(f"{BASE}/plan.html", wait_until="networkidle")
    corps = pg.inner_text("body")
    for libelle, valeur in (("mondial", attendu_mondial), ("Canada+US", attendu_na),
                            ("variante FR", attendu_fr), ("total", attendu_total)):
        verif(f"plan : le nombre « {libelle} » vaut celui recalcule du tableur",
              n(valeur) in corps, f"{n(valeur)} absent")
    verif("plan : le total de la grille est bien celui du tableur",
          GRILLE["total"] == attendu_total,
          f'{GRILLE["total"]} vs {attendu_total}')
    verif("plan : le total propose est affiche",
          n(PROPOSE["total"]) in corps, n(PROPOSE["total"]))
    verif("plan : le plan propose est bien plus petit que la grille",
          PROPOSE["total"] * 100 < GRILLE["total"],
          f'{PROPOSE["total"]} vs {GRILLE["total"]}')

    # ---- 3. le compte de villes est celui qu'IL a fixe -------------------
    attendus_regions = {"amerique-nord": 100, "europe": 50,
                        "moyen-orient": 50, "asie": 50}
    for cle, nom, liste in REGIONS:
        verif(f"region {cle} : le nombre de villes est celui demande",
              len(liste) == attendus_regions[cle],
              f"{len(liste)} vs {attendus_regions[cle]}")
        pg.goto(f"{BASE}/region-{cle}.html", wait_until="networkidle")
        cartes = pg.locator("a.carte").count()
        verif(f"region {cle} : la page liste toutes ses villes",
              cartes == len(liste), f"{cartes} vs {len(liste)}")
    verif("250 villes au total", len(TOUTES) == 250, str(len(TOUTES)))
    verif("aucune page ne combine un synonyme et une ville",
          not any("-services.html" in f"ville-{v[0]}.html" for v in TOUTES))

    # ---- 4. chaque page de ville dit ce qui lui manque -------------------
    # C'est la raison d'etre de la page : sans cette section, elle serait
    # exactement la page satellite que le plan denonce.
    echantillon = [TOUTES[0], TOUTES[60], TOUTES[99], TOUTES[100],
                   TOUTES[140], TOUTES[150], TOUTES[190], TOUTES[200],
                   TOUTES[249]]
    for v in echantillon:
        pg.goto(f"{BASE}/ville-{v[0]}.html", wait_until="domcontentloaded")
        c = pg.inner_text("body")
        bas = c.lower()
        verif(f"ville-{v[0]} : nomme la ville", v[1] in c)
        verif(f"ville-{v[0]} : porte le bloc de ce qui manque",
              "needs local input" in bas, "bloc absent")
        verif(f"ville-{v[0]} : le titre est en anglais",
              "Web development in" in c, c[:60])
        verif(f"ville-{v[0]} : les quatre services y figurent",
              all(s[1].replace("&amp;", "&") in c for s in SERVICES),
              str([s[1] for s in SERVICES if s[1].replace("&amp;", "&") not in c]))
        # AUCUNE AFFIRMATION LOCALE INVENTEE. Une date d'implantation, un
        # nombre de clients ou un nom d'entreprise dans cette ville seraient
        # des faits que personne ne m'a donnes.
        verif(f"ville-{v[0]} : n'invente ni anciennete ni volume",
              not re.search(r"\bdepuis (19|20)\d\d\b", bas)
              and not re.search(r"\b\d+\s+(clients|projets|entreprises)\b", bas),
              (re.findall(r"depuis (19|20)\d\d|\d+\s+(?:clients|projets|entreprises)",
                          bas) or [""])[0])

    # ---- 5. rien n'est indexable tant que c'est vide ----------------------
    for f in ("index.html", "plan.html", "villes.html", "ville-toronto.html",
              "region-asie.html", "service-web-development.html"):
        pg.goto(f"{BASE}/{f}", wait_until="domcontentloaded")
        robots = pg.evaluate("() => document.querySelector('meta[name=robots]')"
                             "?.getAttribute('content')")
        verif(f"{f} : noindex", robots and "noindex" in robots, str(robots))
        verif(f"{f} : le bandeau dit que c'est un apercu",
              "Preview." in pg.inner_text("body"))

    # ---- 6. aucun tarif --------------------------------------------------
    # Regle deja posee sur le site de l'agence : aucune somme affichee.
    for f in ("index.html", "images.html", "plan.html",
              "service-web-development.html", "ville-montreal.html"):
        pg.goto(f"{BASE}/{f}", wait_until="domcontentloaded")
        c = pg.inner_text("body")
        verif(f"{f} : aucun montant affiche",
              not re.search(r"[€$£]\s?\d|\d+\s?(CAD|USD|EUR)\b", c),
              (re.findall(r"[€$£]\s?\d+|\d+\s?(?:CAD|USD|EUR)", c) or [""])[0])

    # ---- 7. aucun lien mort ----------------------------------------------
    liens = set()
    for f in ("index.html", "services.html", "villes.html", "images.html",
              "plan.html", "ville-toronto.html", "service-web-engineering.html"):
        pg.goto(f"{BASE}/{f}", wait_until="domcontentloaded")
        for href in pg.evaluate("() => [...document.querySelectorAll('a')]"
                                ".map(a => a.getAttribute('href'))"):
            if href and not href.startswith(("http", "#", "mailto:")):
                liens.add(href.split("#")[0])
    morts = []
    for href in sorted(liens):
        try:
            with urllib.request.urlopen(f"{BASE}/{href}") as r:
                if r.status != 200:
                    morts.append((href, r.status))
        except urllib.error.HTTPError as e:
            morts.append((href, e.code))
    verif(f"aucun lien mort parmi les {len(liens)} liens internes", not morts,
          str(morts[:4]))
    absent = None
    try:
        urllib.request.urlopen(f"{BASE}/page-inexistante.html")
    except urllib.error.HTTPError as e:
        absent = e.code
    verif("la sonde de liens voit une page absente", absent == 404, str(absent))

    # ---- 8. mobile --------------------------------------------------------
    for f in ("index.html", "plan.html", "ville-dubai.html", "region-europe.html"):
        pg.set_viewport_size({"width": 390, "height": 800})
        pg.goto(f"{BASE}/{f}", wait_until="networkidle")
        pg.wait_for_timeout(200)
        deb = pg.evaluate("() => document.documentElement.scrollWidth"
                          " - document.documentElement.clientWidth")
        verif(f"{f} : pas de debordement a 390 px", deb <= 0, str(deb))
    pg.set_viewport_size({"width": 1280, "height": 900})

    # ---- 9. LES META DESCRIPTIONS ----------------------------------------
    # Il les a demandees nommement. Une par page, TOUTES DIFFERENTES : une
    # description dupliquee est ignoree par le moteur, qui la remplace par un
    # extrait de son choix. L'ecrire une fois pour toutes revient a ne pas
    # l'ecrire. On les lit sur les 262 pages servies, pas dans le generateur.
    import glob
    fichiers = sorted(os.path.basename(f)
                      for f in glob.glob(os.path.join(RACINE, "*.html")))
    descriptions = {}
    vides, courtes = [], []
    for f in fichiers:
        with urllib.request.urlopen(f"{BASE}/{f}") as r:
            texte = r.read().decode("utf-8")
        m = re.search(r'<meta name="description" content="([^"]*)"', texte)
        d = m.group(1) if m else ""
        if not d:
            vides.append(f)
        elif len(d) < 50:
            courtes.append((f, len(d)))
        descriptions.setdefault(d, []).append(f)

    verif(f"les {len(fichiers)} pages ont une meta description",
          not vides, str(vides[:4]))
    doublons = {d: fs for d, fs in descriptions.items() if len(fs) > 1}
    verif("aucune meta description n'est repetee d'une page a l'autre",
          not doublons,
          str([(fs[0], fs[1]) for fs in list(doublons.values())[:2]]))
    verif("aucune meta description n'est trop courte",
          not courtes, str(courtes[:3]))
    verif("autant de descriptions distinctes que de pages",
          len(descriptions) == len(fichiers),
          f"{len(descriptions)} vs {len(fichiers)}")
    # Controle positif : la lecture des descriptions trouve bien quelque chose.
    verif("la lecture des descriptions n'est pas vide",
          len(descriptions) > 200, str(len(descriptions)))

    # ---- 10. LE THEME NOIR -----------------------------------------------
    # Demande le 11 septembre. Lu sur la couleur CALCULEE par le navigateur.
    for f in ("index.html", "images.html", "ville-dubai.html", "plan.html"):
        pg.goto(f"{BASE}/{f}", wait_until="networkidle")
        fond = pg.evaluate("() => getComputedStyle(document.body).backgroundColor")
        txt = pg.evaluate("() => getComputedStyle(document.body).color")
        rgb = [int(x) for x in re.findall(r"\d+", fond)[:3]]
        rgbt = [int(x) for x in re.findall(r"\d+", txt)[:3]]
        verif(f"{f} : le fond est noir", max(rgb) < 40, fond)
        verif(f"{f} : le texte est clair sur ce fond", min(rgbt) > 180, txt)

    # ---- 11. LE CIEL ETOILE ----------------------------------------------
    # « Add stars in the main slider like a RR phantom » + « Rooftop ».
    # Le ciel etoile de Rolls-Royce est dans le PAVILLON : les etoiles doivent
    # donc etre concentrees EN HAUT. Un semis uniforme serait un fond spatial.
    pg.set_viewport_size({"width": 1280, "height": 900})
    pg.goto(f"{BASE}/index.html", wait_until="networkidle")
    pg.wait_for_timeout(400)
    etoiles = pg.evaluate("""() => [...document.querySelectorAll('.hero .ciel .et')]
        .map(e => parseFloat(e.style.top))""")
    verif("le hero porte un ciel etoile", len(etoiles) > 60, str(len(etoiles)))
    haut = sum(1 for t in etoiles if t < 40)
    verif("les etoiles sont concentrees en haut, comme un pavillon",
          haut > len(etoiles) * 0.6, f"{haut}/{len(etoiles)} au-dessus de 40%")
    verif("aucune etoile ne depasse la moitie basse du hero",
          max(etoiles) < 85, f"la plus basse est a {max(etoiles)}%")
    # Elles doivent etre VISIBLES, pas seulement presentes dans le HTML.
    opacite = pg.evaluate("""() => {
        const e = document.querySelector('.hero .ciel .et');
        const s = getComputedStyle(e);
        return { op: parseFloat(s.opacity), w: s.width, pos: s.position }; }""")
    verif("les etoiles sont reellement visibles", opacite["op"] > 0.02,
          str(opacite))
    verif("le ciel ne capte pas les clics",
          pg.evaluate("() => getComputedStyle(document.querySelector('.ciel'))"
                      ".pointerEvents") == "none")

    # ---- 12. LES EFFETS DEGRADENT PROPREMENT ------------------------------
    # La classe qui cache les elements n'est posee QUE par le script. Si le
    # JavaScript ne part pas, tout doit rester visible : un effet qui cache le
    # contenu quand il echoue n'est pas un effet, c'est une panne.
    visibles = pg.evaluate("""() => [...document.querySelectorAll('.rev')]
        .filter(e => getComputedStyle(e).opacity === '0'
                  && e.getBoundingClientRect().top < window.innerHeight).length""")
    verif("aucun element revele ne reste invisible dans l'ecran",
          visibles == 0, str(visibles))

    # SANS JAVASCRIPT, rien ne doit rester invisible.
    # Attention : inner_text renvoie le texte d'un element a opacity:0. Une
    # verification « le texte est present » ne peut donc PAS echouer sur ce
    # defaut — je l'ai ecrite ainsi une premiere fois et le controle positif
    # est passe au vert alors que j'avais casse le repli. On mesure donc
    # l'OPACITE CALCULEE, la seule chose qui distingue lisible d'invisible.
    sans_js = nav.new_context(java_script_enabled=False)
    pj = sans_js.new_page()
    pj.set_viewport_size({"width": 1280, "height": 900})
    pj.goto(f"{BASE}/index.html", wait_until="domcontentloaded")
    pj.wait_for_timeout(300)
    invisibles = pj.evaluate("""() => [...document.querySelectorAll('.rev')]
        .filter(e => parseFloat(getComputedStyle(e).opacity) < 0.99)
        .map(e => e.className)""")
    verif("sans JavaScript : aucun element revele n'est masque",
          not invisibles, str(invisibles[:3]))
    verif("sans JavaScript : la classe d'animation n'est pas posee",
          "anime" not in pj.evaluate("() => document.documentElement.className"),
          pj.evaluate("() => document.documentElement.className"))
    corps_sans_js = pj.inner_text("body")
    for t in TRAVAUX:
        verif(f"sans JavaScript : « {t[1]} » reste dans la page",
              t[1] in corps_sans_js, t[1])
    pj.close(); sans_js.close()

    # ---- 13. LES CONSIGNES D'IMAGES ---------------------------------------
    pg.goto(f"{BASE}/images.html", wait_until="networkidle")
    c = pg.inner_text("body")
    for nom, role, l, h, consigne in IMAGES:
        verif(f"images : {nom} est listee", nom in c, nom)
        verif(f"images : {nom} donne ses dimensions",
              f"{l} × {h}" in c or f"{l} x {h}" in c, f"{l}x{h}")
    # Les trois interdits doivent figurer DANS CHAQUE consigne : c'est ce qui
    # empeche un visage genere ou un faux logo d'arriver dans le site.
    for nom, role, l, h, consigne in IMAGES:
        bas_c = consigne.lower()
        verif(f"images : {nom} interdit les visages",
              "no people" in bas_c or "no faces" in bas_c, consigne[-60:])
        verif(f"images : {nom} interdit logo et texte",
              "no logo" in bas_c and "no text" in bas_c, consigne[-60:])
    verif("images : la page rappelle les trois regles",
          "No recognisable faces" in c and "No logos" in c
          and "No invented screenshots" in c)

    verif("aucune erreur JavaScript", not erreurs, str(erreurs[:2]))

    D = "/var/lib/freelancer/projects/40478471/"
    for f, nom in (("index.html", "mo-1-accueil"), ("images.html", "mo-2-images"),
                   ("ville-dubai.html", "mo-3-ville"),
                   ("plan.html", "mo-4-plan")):
        pg.goto(f"{BASE}/{f}", wait_until="networkidle")
        pg.wait_for_timeout(300)
        pg.screenshot(path=D + nom + ".png")
    nav.close()

print(f"\n{ok + len(ko)} verifications, {len(ko)} echec(s)")
for nom, detail in ko:
    print("  -", nom, detail)
sys.exit(1 if ko else 0)
