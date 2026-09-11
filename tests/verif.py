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

from donnees import GRILLE, PROPOSE, SERVICES, TERMES, VILLES

BASE = (sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8941").rstrip("/")
TABLEUR = os.path.normpath(os.path.join(RACINE, "..", "Websites platform.xlsx"))

ok, ko = 0, []


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

    # ---- 3. une page par VILLE, pas une par synonyme x ville -------------
    pg.goto(f"{BASE}/villes.html", wait_until="networkidle")
    liens = pg.evaluate("() => [...document.querySelectorAll('a.carte')]"
                        ".map(a => a.getAttribute('href'))")
    verif("villes : une page par ville, ni plus ni moins",
          len(liens) == len(VILLES), f"{len(liens)} vs {len(VILLES)}")
    verif("villes : aucune page ne combine un synonyme et une ville",
          not any(re.search(r"ville-.*-(services|development)\.html", l) for l in liens),
          str(liens[:3]))

    # ---- 4. chaque page de ville dit ce qui lui manque -------------------
    # C'est la raison d'etre de la page : sans cette section, elle serait
    # exactement la page satellite que le plan denonce.
    for v in VILLES:
        pg.goto(f"{BASE}/ville-{v[0]}.html", wait_until="domcontentloaded")
        c = pg.inner_text("body")
        bas = c.lower()
        verif(f"ville-{v[0]} : nomme la ville", v[1] in c)
        verif(f"ville-{v[0]} : porte le bloc de ce qui manque",
              "needs local input" in bas, "bloc absent")
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
              "service-web-development.html"):
        pg.goto(f"{BASE}/{f}", wait_until="domcontentloaded")
        robots = pg.evaluate("() => document.querySelector('meta[name=robots]')"
                             "?.getAttribute('content')")
        verif(f"{f} : noindex", robots and "noindex" in robots, str(robots))
        verif(f"{f} : le bandeau dit que ce n'est pas en ligne",
              "pas un site en ligne" in pg.inner_text("body"))

    # ---- 6. aucun tarif --------------------------------------------------
    # Regle deja posee sur le site de l'agence : aucune somme affichee.
    for f in ("index.html", "plan.html", "service-web-development.html",
              "ville-montreal.html"):
        pg.goto(f"{BASE}/{f}", wait_until="domcontentloaded")
        c = pg.inner_text("body")
        verif(f"{f} : aucun montant affiche",
              not re.search(r"[€$£]\s?\d|\d+\s?(CAD|USD|EUR)\b", c),
              (re.findall(r"[€$£]\s?\d+|\d+\s?(?:CAD|USD|EUR)", c) or [""])[0])

    # ---- 7. aucun lien mort ----------------------------------------------
    liens = set()
    for f in ("index.html", "services.html", "villes.html", "plan.html",
              "ville-toronto.html", "service-web-engineering.html"):
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
    for f in ("index.html", "plan.html", "ville-new-york.html"):
        pg.set_viewport_size({"width": 390, "height": 800})
        pg.goto(f"{BASE}/{f}", wait_until="networkidle")
        pg.wait_for_timeout(200)
        deb = pg.evaluate("() => document.documentElement.scrollWidth"
                          " - document.documentElement.clientWidth")
        verif(f"{f} : pas de debordement a 390 px", deb <= 0, str(deb))
    pg.set_viewport_size({"width": 1280, "height": 900})

    verif("aucune erreur JavaScript", not erreurs, str(erreurs[:2]))

    D = "/var/lib/freelancer/projects/40478471/"
    for f, nom in (("index.html", "seo-1-accueil"), ("plan.html", "seo-2-plan"),
                   ("ville-montreal.html", "seo-3-ville")):
        pg.goto(f"{BASE}/{f}", wait_until="networkidle")
        pg.wait_for_timeout(300)
        pg.screenshot(path=D + nom + ".png")
    nav.close()

print(f"\n{ok + len(ko)} verifications, {len(ko)} echec(s)")
for nom, detail in ko:
    print("  -", nom, detail)
sys.exit(1 if ko else 0)
