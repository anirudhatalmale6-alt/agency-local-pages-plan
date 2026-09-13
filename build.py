# -*- coding: utf-8 -*-
"""
Le plan de pages locales de l'agence, genere.

  python3 build.py   -> ecrit les .html a cote de ce fichier

Une page par VILLE et une page par SERVICE. Pas une page par synonyme et par
ville : c'est la difference entre un site local et une ferme de pages.
"""
import html
import os

from donnees import (BASELINE, ETAPES, GRILLE, IMAGES, MARQUE, SERVICES,
                     TEL_AFFICHE, TERMES, TRAVAUX, VARIABLES, VIDE,
                     WHATSAPP)
from villes import PAYS_NOM, REGIONS, TOUTES

RACINE = os.path.dirname(os.path.abspath(__file__))
VERSION_CSS = 9
E = html.escape
ECRITES = set()


def ciel(nb=110):
    """Le pavillon etoile. Positions TIREES UNE FOIS avec une graine fixe :
    sans elle, chaque generation deplacerait les etoiles et deux captures
    prises a dix minutes d'intervalle ne se ressembleraient pas."""
    import random as _r
    rnd = _r.Random(20260911)
    pts = []
    for _ in range(nb):
        # y**1.7 concentre les etoiles vers le HAUT : c'est un pavillon, pas
        # un fond spatial.
        y = round((rnd.random() ** 1.7) * 78, 2)
        x = round(rnd.random() * 100, 2)
        taille = rnd.choice([1, 1, 1, 1.5, 1.5, 2, 2.5])
        o1 = round(rnd.uniform(.06, .22), 2)
        o2 = round(rnd.uniform(.45, .95), 2)
        duree = round(rnd.uniform(2.2, 6.5), 1)
        retard = round(rnd.uniform(0, 5), 1)
        classe = "et"
        d = rnd.random()
        if d < 0.16:
            classe += " chaud"
        elif d < 0.20:
            classe += " vert"
        pts.append(
            f'<span class="{classe}" style="left:{x}%;top:{y}%;'
            f'width:{taille}px;height:{taille}px;--o1:{o1};--o2:{o2};'
            f'--d:{duree}s;--r:{retard}s"></span>')
    return '<div class="ciel" aria-hidden="true">' + "".join(pts) + "</div>"


def n(x):
    return f"{x:,}".replace(",", " ")


def tbd():
    return f'<span class="tbd">{VIDE}</span>'


# LE MENU PRINCIPAL. Il a entoure « Locations » et « The plan » en rouge avec
# « Remove this » : les deux sortent du menu.
#
# LES PAGES, ELLES, RESTENT. Les 250 pages de ville sont la couche SEO — il l'a
# dit lui-meme — et une page sans aucun lien interne est une page que personne
# ne trouve, ni un visiteur ni un moteur. Elles passent donc dans le PIED DE
# PAGE, qui est exactement ou un site range ses pages de localite.
MENU = [("index.html", "Studio"), ("index.html#work", "Work"),
        ("services.html", "Services"), ("images.html", "Images")]

REG_NOM = {cle: nom for cle, nom, _ in REGIONS}
VILLES_PAR_REGION = {cle: liste for cle, _, liste in REGIONS}


def pays_nom(code):
    return PAYS_NOM[code]


# --- LES META DESCRIPTIONS -------------------------------------------------
# Il les a demandees nommement. Deux regles :
#   1. UNE PAR PAGE, differente des 249 autres. Google remplace une
#      description dupliquee par un extrait de son choix : ecrire la meme
#      partout revient a n'en ecrire aucune.
#   2. AUCUNE AFFIRMATION. Pas d'anciennete, pas de nombre de clients, pas de
#      « leader » : rien que personne ne m'a donne.
# La variete vient de l'angle de service, qui tourne, et des elements reels de
# la ville (division, pays, langues) — pas d'adjectifs empiles.
ANGLES = [
    "Websites and applications built to order",
    "Web design and development",
    "Business web applications",
    "Taking over and stabilising an existing site",
    "Full-stack web development",
]


def meta_ville(v, rang):
    slug, nom, division, pays, langues, region = v
    angle = ANGLES[rang % len(ANGLES)]
    lg = ", ".join(LANGUES_NOM.get(l, l) for l in langues[:2])
    return (f"{angle} in {nom}, {division}, {pays_nom(pays)}. "
            f"Four services, reachable in {lg}. "
            f"{REG_NOM[region].replace('&amp;', '&')} coverage.")


LANGUES_NOM = {
    "en": "English", "fr": "French", "es": "Spanish", "de": "German",
    "it": "Italian", "nl": "Dutch", "pt": "Portuguese", "sv": "Swedish",
    "da": "Danish", "no": "Norwegian", "fi": "Finnish", "pl": "Polish",
    "cs": "Czech", "hu": "Hungarian", "ro": "Romanian", "bg": "Bulgarian",
    "el": "Greek", "hr": "Croatian", "ar": "Arabic", "he": "Hebrew",
    "tr": "Turkish", "ja": "Japanese", "zh": "Chinese", "ko": "Korean",
    "hi": "Hindi", "th": "Thai", "id": "Indonesian", "ms": "Malay",
    "tl": "Tagalog", "vi": "Vietnamese", "si": "Sinhala", "bn": "Bengali",
    "ur": "Urdu",
}


def page(fichier, titre, description, corps, actuel=None, alternates=""):
    nav = "".join(
        f'<a href="{f}"{" aria-current=\"page\"" if f == (actuel or fichier) else ""}>{E(t)}</a>'
        for f, t in MENU)
    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(titre)}</title>
<meta name="description" content="{E(description)}">
<meta name="robots" content="noindex,nofollow">
{alternates}<link rel="icon" type="image/svg+xml" href="assets/modersly-favicon.svg">
<link rel="apple-touch-icon" href="assets/modersly-icone.svg">
<link rel="stylesheet" href="assets/site.css?v={VERSION_CSS}">
<script>
/* Pose le mode choisi AVANT que la page ne se peigne. Sans ce script ici, un
   visiteur qui a choisi le clair verrait un eclair noir a chaque page : la
   feuille s'applique d'abord, le choix seulement apres le chargement. */
(function(){{try{{var m=localStorage.getItem("modersly-mode");
if(m==="light"||m==="dark"){{document.documentElement.setAttribute("data-theme",m);}}
}}catch(e){{}}}})();
</script>
</head>
<body>

<div class="avert"><div class="wrap">
  <b>Preview.</b> The studio name and legal entity are not settled, and the
  location pages are still templates waiting on real local material. Every
  page is <code>noindex</code> until then &mdash;
  <a href="plan.html">why, and the numbers</a>.
</div></div>

<header class="top"><div class="wrap bar">
  <a class="marque" href="index.html" aria-label="{E(MARQUE)}, home">
    <img class="sombre" src="assets/modersly-logo-sombre.svg" alt="{E(MARQUE)}"
         width="150" height="39">
    <img class="clair" src="assets/modersly-logo-clair.svg" alt="{E(MARQUE)}"
         width="150" height="39">
  </a>
  <nav class="nav">{nav}</nav>
  <button class="bascule" type="button" id="bascule"
          aria-label="Switch between light and dark">
    <svg class="soleil" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 17a5 5 0 1 1 0-10 5 5 0 0 1 0 10zm0-13a1 1 0 0 1-1-1V1a1 1 0 1 1 2 0v2a1 1 0 0 1-1 1zm0 19a1 1 0 0 1-1-1v-2a1 1 0 1 1 2 0v2a1 1 0 0 1-1 1zM4 13H2a1 1 0 1 1 0-2h2a1 1 0 1 1 0 2zm18 0h-2a1 1 0 1 1 0-2h2a1 1 0 1 1 0 2zM5.6 6.99a1 1 0 0 1-.7-.29L3.49 5.28a1 1 0 0 1 1.41-1.41L6.31 5.3a1 1 0 0 1-.71 1.7zm12.79 12.8a1 1 0 0 1-.71-.3l-1.4-1.41a1 1 0 1 1 1.41-1.41l1.41 1.41a1 1 0 0 1-.71 1.7zM18.4 6.99a1 1 0 0 1-.71-1.7l1.41-1.42a1 1 0 1 1 1.41 1.41L19.1 6.7a1 1 0 0 1-.7.29zM5.6 19.79a1 1 0 0 1-.71-1.71l1.41-1.41a1 1 0 1 1 1.41 1.41L6.3 19.5a1 1 0 0 1-.7.29z"/></svg>
    <svg class="lune" viewBox="0 0 24 24" aria-hidden="true"><path d="M12.3 22a10 10 0 0 1-1.3-19.92 1 1 0 0 1 1.1 1.35 8 8 0 0 0 9.47 10.5 1 1 0 0 1 1.15 1.35A10 10 0 0 1 12.3 22z"/></svg>
  </button>
</div></header>

<main>
{corps}
</main>

<a class="wa" href="{WHATSAPP}" target="_blank" rel="noopener"
   aria-label="Write to us on WhatsApp, {E(TEL_AFFICHE)}">
  <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M17.47 14.38c-.3-.15-1.76-.87-2.03-.97-.27-.1-.47-.15-.67.15-.2.3-.77.96-.94 1.16-.17.2-.35.22-.65.08-.3-.15-1.26-.46-2.4-1.48-.89-.79-1.49-1.76-1.66-2.06-.17-.3-.02-.46.13-.61.14-.13.3-.35.45-.52.15-.17.2-.3.3-.5.1-.2.05-.37-.02-.52-.08-.15-.67-1.61-.92-2.2-.24-.58-.49-.5-.67-.51h-.57c-.2 0-.52.07-.79.37-.27.3-1.04 1.02-1.04 2.48s1.06 2.88 1.21 3.08c.15.2 2.1 3.2 5.08 4.49.71.3 1.26.49 1.69.63.71.22 1.36.19 1.87.12.57-.09 1.76-.72 2.01-1.41.25-.7.25-1.29.17-1.42-.07-.13-.27-.2-.57-.35zM12.04 2A9.96 9.96 0 0 0 2.08 12c0 1.76.46 3.42 1.28 4.86L2 22l5.26-1.38a9.9 9.9 0 0 0 4.78 1.22h.01A9.96 9.96 0 0 0 22 12 9.96 9.96 0 0 0 12.04 2z"/></svg>
  <span class="txt">WhatsApp</span>
</a>

<footer class="pied"><div class="wrap">
  <div class="pied-liens">
    <a href="{WHATSAPP}" target="_blank" rel="noopener">WhatsApp {E(TEL_AFFICHE)}</a>
    <a href="villes.html">Locations &mdash; {len(TOUTES)} cities</a>
    <a href="services.html">Services</a>
    <a href="images.html">Images</a>
    <a href="plan.html">The plan</a>
  </div>
  <p style="margin:18px 0 0">{E(MARQUE)} &mdash; {E(BASELINE.lower())}. No price
  list, no invented client, no fabricated testimonial. Every project shown is
  live and linked.</p>
</div></footer>

<script>
/* Les effets ne s'activent QUE si le visiteur accepte les animations, et le
   contenu est visible par defaut : la classe qui le cache n'est posee que si
   l'observateur existe vraiment. Un effet qui cache le contenu quand il
   echoue n'est pas un effet, c'est une panne. */
(function () {{
  var bouge = window.matchMedia
    && !window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (!bouge || !('IntersectionObserver' in window)) return;

  document.documentElement.classList.add('anime');
  var vus = new IntersectionObserver(function (entrees) {{
    entrees.forEach(function (e) {{
      if (e.isIntersecting) {{ e.target.classList.add('vu'); vus.unobserve(e.target); }}
    }});
  }}, {{ rootMargin: '0px 0px -8% 0px', threshold: 0.08 }});
  document.querySelectorAll('.rev').forEach(function (el) {{ vus.observe(el); }});
}})();

/* La bascule clair / sombre. Le choix est garde d'une page a l'autre ; sans
   ca il faudrait le refaire a chaque clic dans le menu. */
(function () {{
  var b = document.getElementById('bascule');
  if (!b) return;
  b.addEventListener('click', function () {{
    var r = document.documentElement;
    var actuel = r.getAttribute('data-theme');
    if (!actuel) {{
      var sysClair = window.matchMedia
        && window.matchMedia('(prefers-color-scheme: light)').matches;
      actuel = sysClair ? 'light' : 'dark';
    }}
    var suivant = actuel === 'light' ? 'dark' : 'light';
    r.setAttribute('data-theme', suivant);
    try {{ localStorage.setItem('modersly-mode', suivant); }} catch (e) {{}}
  }});
}})();
</script>

</body>
</html>
"""
    with open(os.path.join(RACINE, fichier), "w", encoding="utf-8") as f:
        f.write(doc)
    ECRITES.add(fichier)
    return len(doc)


# Ce que produit REELLEMENT le plan qu'il a fixe le 11 septembre.
PROPOSE = {
    "villes": len(TOUTES),
    "services": len(SERVICES),
    "fixes": 5,          # studio, work, services, locations, plan
    "regions": len(REGIONS),
}
PROPOSE["total"] = (PROPOSE["villes"] + PROPOSE["services"]
                    + PROPOSE["fixes"] + PROPOSE["regions"])


# ---------------------------------------------------------------------------
def bloc_projet(t, rang):
    cle, nom, url, controles, resume, points = t
    lis = "".join(f"<li>{E(p)}</li>" for p in points)
    return f"""<a class="proj" href="{E(url)}" target="_blank" rel="noopener">
  <span>
    <span class="num">{rang:02d} &mdash; live</span>
    <h3>{E(nom)}</h3>
    <p>{E(resume)}</p>
    <ul>{lis}</ul>
  </span>
  <span class="meta">
    <span class="ctrl">{controles}</span>
    <span class="ctrl-l">automatic checks</span>
    <span class="voir">Open the live site &rarr;</span>
  </span>
</a>"""


def accueil():
    projets = "".join(bloc_projet(t, i) for i, t in enumerate(TRAVAUX, start=1))
    services = "".join(f"""<div class="carte">
      <span class="num">{i:02d}</span>
      <h3>{s[1]}</h3><p>{E(s[2])}</p>
      <p class="aussi">Also called: {', '.join(E(a) for a in s[3])}</p></div>"""
                       for i, s in enumerate(SERVICES, start=1))
    etapes = "".join(f"""<div class="carte"><span class="num">{i:02d}</span>
      <h3>{E(nom)}</h3><p>{txt}</p></div>"""
                     for i, (nom, txt) in enumerate(ETAPES, start=1))
    total_controles = sum(t[3] for t in TRAVAUX)

    return f"""
<section class="hero">
  {ciel()}
  <div class="wrap">
  <h1 class="monte">We build the web, <em>and we prove it works.</em></h1>
  <p class="lede monte">A small studio that ships sites and applications with
  the checks that show they behave &mdash; run against the published site, not
  against a copy on someone's laptop.</p>
  <div class="actions monte">
    <a class="btn" href="#work">See the work</a>
    <a class="btn btn-b" href="services.html">What we do</a>
  </div>
  <div class="chiffres">
    <div class="chiffre"><div class="v">{len(TRAVAUX)}</div>
      <div class="l">Projects live</div></div>
    <div class="chiffre"><div class="v">{total_controles}</div>
      <div class="l">Checks behind them</div></div>
    <div class="chiffre"><div class="v">{n(len(TOUTES))}</div>
      <div class="l">Cities covered</div></div>
    <div class="chiffre"><div class="v">0</div>
      <div class="l">Invented clients</div></div>
  </div>
</div></section>

<section class="sec" id="work"><div class="wrap">
  <span class="oeil rev">Selected work</span>
  <div class="sec-h rev"><h2>Everything here is live, and linked</h2></div>
  <p class="chapeau rev" style="margin-bottom:26px">No case study for a client
  we never had, no logo wall, no testimonial we wrote ourselves.
  {len(TRAVAUX)} projects, {total_controles} automatic checks behind them, and
  every link opens the real thing.</p>
  <div class="travail rev">{projets}</div>
  <div class="encadre rev" style="margin-top:26px"><p style="margin:0">
  <b>Why the check counts are on the page.</b> A studio figure nobody can
  recount is an invented figure that merely sounds modest. Each number above is
  the size of that project's own check suite, and each suite ships with its
  project.</p></div>
</div></section>

<section class="sec"><div class="wrap">
  <span class="oeil rev">What we do</span>
  <div class="sec-h rev"><h2>Four services, eleven ways clients name them</h2>
    <a class="plus" href="services.html">Details &rarr;</a></div>
  <div class="grille g4 rev">{services}</div>
</div></section>

<section class="sec"><div class="wrap">
  <span class="oeil rev">How it goes</span>
  <div class="sec-h rev"><h2>Four steps, no discourse</h2></div>
  <div class="grille g4 rev">{etapes}</div>
</div></section>

<section class="appel"><div class="wrap">
  <h2 class="rev">Tell us what it has to do.</h2>
  <p class="lede">There is no price list here, because a figure quoted before
  the scope is known is wrong in one direction or the other. Five things move
  it, and they are on the services page.</p>
  <div class="actions">
    <a class="btn" href="services.html">See what moves a quote</a>
    <a class="btn btn-b" href="villes.html">Where we work</a>
  </div>
</div></section>
"""


def page_travail():
    projets = "".join(bloc_projet(t, i) for i, t in enumerate(TRAVAUX, start=1))
    total = sum(t[3] for t in TRAVAUX)
    return f"""
<section class="sec"><div class="wrap">
  <span class="oeil">Work</span>
  <h1 class="titre">Everything here is live, and linked</h1>
  <p class="chapeau">No case study for a client we never had, no logo wall, no
  testimonial we wrote ourselves. {len(TRAVAUX)} projects, {total} automatic
  checks behind them, and every link opens the real thing.</p>
</div></section>

<section class="sec" style="padding-top:0"><div class="wrap">
  <div class="travail">{projets}</div>
  <div class="encadre" style="margin-top:26px"><p style="margin:0">
  <b>Why the check counts are on the page.</b> A studio figure nobody can
  recount is an invented figure that merely sounds modest. Each number above is
  the size of that project's own check suite, and each suite ships with its
  project.</p></div>
</div></section>
"""


def services_index():
    lignes = "".join(f"""<a class="carte" href="service-{s[0]}.html">
      <span class="num">{i:02d}</span>
      <h3>{s[1]}</h3><p>{E(s[2])}</p></a>"""
                     for i, s in enumerate(SERVICES, start=1))
    tous = "".join(f"<li>{E(t)}</li>" for t in TERMES)
    variables = "".join(f"<li>{E(v)}</li>" for v in VARIABLES)
    return f"""
<section class="sec"><div class="wrap">
  <span class="oeil">Services</span>
  <h1 class="titre">Four services</h1>
  <p class="chapeau">One page each. Every page names the variants people
  actually type, which covers the vocabulary without multiplying pages.</p>
  <div class="grille g4" style="margin-top:26px">{lignes}</div>
</div></section>

<section class="sec"><div class="wrap">
  <div class="sec-h"><h2>What moves a quote</h2></div>
  <p class="chapeau">Instead of a price list &mdash; which would be wrong in one
  direction or the other before the scope is known &mdash; the five things that
  decide it.</p>
  <div class="encadre" style="margin-top:18px"><ol>{variables}</ol></div>
</div></section>

<section class="sec"><div class="wrap">
  <div class="sec-h"><h2>The eleven terms</h2></div>
  <p class="chapeau">These are the words clients use for the four services
  above. They describe four needs, not eleven.</p>
  <ul class="liste2" style="margin-top:16px">{tous}</ul>
</div></section>
"""


def page_service(s):
    slug, nom, phrase, variantes = s
    exemples = "".join(f'<a href="ville-{v[0]}.html">{E(v[1])}</a>'
                       for v in TOUTES[:10])
    regions = "".join(f'<a href="region-{cle}.html">{nom}</a>'
                      for cle, nom, _ in REGIONS)
    return f"""
<section class="sec"><div class="wrap">
  <nav class="fil"><a href="index.html">Studio</a> /
    <a href="services.html">Services</a> / {nom}</nav>
  <h1 class="titre">{nom}</h1>
  <p class="chapeau">{E(phrase)}</p>

  <div class="sec-h" style="margin-top:34px"><h2>Also called</h2></div>
  <p class="chapeau">{', '.join(E(v) for v in variantes)}. Same projects; the
  name changes from one client to the next.</p>

  <div class="sec-h" style="margin-top:34px"><h2>What this page will hold</h2></div>
  <div class="encadre"><p style="margin:0">{tbd()}<br>
  What the team does, how a project runs, and what moves a quote. The studio
  pages already carry that text: it will be pulled in here rather than
  rewritten, so it exists in one place only.</p></div>

  <div class="sec-h" style="margin-top:34px"><h2>Where</h2></div>
  <div class="villes-liens">{regions}</div>
  <div class="villes-liens" style="margin-top:10px">{exemples}</div>
</div></section>
"""


def page_images():
    lignes = ""
    for nom, role, l, h, consigne in IMAGES:
        lignes += f"""<div class="carte" style="margin-bottom:14px">
          <span class="num">{l} &times; {h} px</span>
          <h3 style="font-family:var(--mono);font-size:15px">{E(nom)}</h3>
          <p style="margin-bottom:12px">{role}</p>
          <div class="encadre" style="background:var(--noir2);padding:14px">
            <p style="margin:0;font-family:var(--mono);font-size:13.5px;
              line-height:1.62;color:var(--txt)">{E(consigne)}</p>
          </div>
        </div>"""
    return f"""
<section class="sec"><div class="wrap">
  <span class="oeil">Images</span>
  <h1 class="titre">{len(IMAGES)} images to generate</h1>
  <p class="chapeau">You generate them, I place them. Each block below gives
  the exact file name, the exact pixel size and the prompt to paste. Send them
  back with those names and they drop straight in.</p>
</div></section>

<section class="sec" style="padding-top:0"><div class="wrap">
  <div class="encadre encadre--alerte" style="margin-bottom:26px">
    <p><b>Three rules that are in every prompt, and they are not decoration.</b></p>
    <ul>
      <li><b>No recognisable faces.</b> A generated face on a studio site reads
      as a team photo &mdash; an invented person presented as a colleague.</li>
      <li><b>No logos, no brands, no text inside the image.</b> A generated
      logo always resembles somebody's real one, and generated lettering comes
      out deformed.</li>
      <li><b>No invented screenshots of a project.</b> The three real projects
      already have real pages; a fake interface beside them would discredit
      the real ones.</li>
    </ul>
    <p class="note">Everything asked for below is abstract, dark, and works
    behind white text.</p>
  </div>
  {lignes}
</div></section>

<section class="sec"><div class="wrap">
  <div class="sec-h"><h2>What the site does without them</h2></div>
  <p class="chapeau">Nothing on the site is broken while these are missing.
  The star field in the header is drawn in code, not from a photograph &mdash;
  a 400&nbsp;KB sky for an effect that dots and a gradient produce would be
  wasted on the very first thing a visitor downloads. The images above add
  texture; they do not hold the layout up.</p>
</div></section>
"""


def villes_index():
    blocs = ""
    for cle, nom, liste in REGIONS:
        apercu = "".join(f'<a href="ville-{v[0]}.html">{E(v[1])}</a>'
                         for v in liste[:14])
        blocs += f"""<div class="sec-h" style="margin-top:30px">
            <h2>{nom}</h2>
            <a class="plus" href="region-{cle}.html">All {len(liste)} cities &rarr;</a></div>
          <div class="villes-liens">{apercu}</div>"""
    return f"""
<section class="sec"><div class="wrap">
  <span class="oeil">Locations</span>
  <h1 class="titre">Where we work</h1>
  <p class="chapeau">{n(len(TOUTES))} cities: {len(REGIONS[0][2])} across the
  United States and Canada, {len(REGIONS[1][2])} in Europe,
  {len(REGIONS[2][2])} in the Middle East and {len(REGIONS[3][2])} in Asia.
  One page per city, each covering all four services &mdash; not one page per
  keyword per city.</p>
  {blocs}
</div></section>
"""


def page_region(cle, nom, liste):
    par_pays = {}
    for v in liste:
        par_pays.setdefault(v[3], []).append(v)
    blocs = ""
    for code in sorted(par_pays, key=lambda c: -len(par_pays[c])):
        cartes = "".join(f"""<a class="carte" href="ville-{v[0]}.html">
          <h3>{E(v[1])}</h3><p>{E(v[2])}<br>
          <span class="lg">{' / '.join(v[4][:2])}</span></p></a>"""
                         for v in par_pays[code])
        blocs += (f'<div class="sec-h" style="margin-top:26px">'
                  f'<h2>{E(pays_nom(code))}</h2>'
                  f'<span class="note">{len(par_pays[code])} cities</span></div>'
                  f'<div class="grille g4">{cartes}</div>')
    return f"""
<section class="sec"><div class="wrap">
  <nav class="fil"><a href="index.html">Studio</a> /
    <a href="villes.html">Locations</a> / {nom}</nav>
  <h1 class="titre">{nom}</h1>
  <p class="chapeau">{len(liste)} cities, grouped by country.</p>
  {blocs}
</div></section>
"""


def page_ville(v, rang):
    slug, nom, division, pays, langues, region = v
    services = "".join(f"""<div class="carte"><h3>{s[1]}</h3>
      <p>{E(s[2])}</p>
      <p class="aussi"><a href="service-{s[0]}.html">La page du service &rarr;</a></p>
      </div>""" for s in SERVICES)

    voisines = [o for o in VILLES_PAR_REGION[region] if o[0] != slug][:18]
    autres = "".join(f'<a href="ville-{o[0]}.html">{E(o[1])}</a>' for o in voisines)

    alt = ""
    if len(langues) > 1:
        alt = ('<p class="note">Multilingual city (' +
               ", ".join(LANGUES_NOM.get(l, l) for l in langues) +
               '). Les versions se declarent en <code>hreflang</code> sur une '
               'seule page, pas en dupliquant l\'adresse.</p>')

    return f"""
<section class="sec"><div class="wrap">
  <nav class="fil"><a href="index.html">Studio</a> /
    <a href="villes.html">Locations</a> /
    <a href="region-{region}.html">{REG_NOM[region]}</a> / {E(nom)}</nav>
  <h1 class="titre">Web development in {E(nom)}</h1>
  <p class="chapeau">{E(division)}, {E(pays_nom(pays))} &middot;
    {", ".join(LANGUES_NOM.get(l, l) for l in langues)}</p>
  {alt}

  <div class="sec-h" style="margin-top:30px"><h2>What we do here</h2></div>
  <div class="grille g2">{services}</div>

  <div class="sec-h" style="margin-top:38px"><h2>What this page still needs</h2></div>
  <div class="encadre encadre--alerte">
    <p><b>This is the only part that matters, and it is empty.</b></p>
    <ul>
      <li>A project actually delivered in {E(nom)} or nearby &mdash; {tbd()}</li>
      <li>A client willing to be named &mdash; {tbd()}</li>
      <li>What genuinely differs here: working language, dominant sectors,
          local obligations &mdash; {tbd()}</li>
    </ul>
    <p class="note">Without at least one of those three, this page says the
    same thing as the other {n(len(TOUTES) - 1)}, city name aside. That is what
    search engines call a doorway page, and the penalty falls on the whole
    domain. Which is why every one of these is <code>noindex</code> today.</p>
  </div>

  <div class="sec-h" style="margin-top:38px"><h2>Other cities &mdash;
    {REG_NOM[region]}</h2>
    <a class="plus" href="region-{region}.html">All &rarr;</a></div>
  <div class="villes-liens">{autres}</div>
</div></section>
"""


def plan():
    g = GRILLE
    return f"""
<section class="sec"><div class="wrap">
  <span class="oeil">The plan</span>
  <h1 class="titre">Why {n(PROPOSE['total'])} pages and not {n(g['total'])}</h1>
  <p class="chapeau">The arithmetic below comes from your own file,
  <code>Websites platform.xlsx</code>, with your own numbers. The plan is the
  one you set afterwards.</p>

  <div class="sec-h" style="margin-top:34px"><h2>What the grid asked for</h2></div>
  <div class="enroule"><table class="tab">
    <thead><tr><th>Block</th><th class="n">Calculation</th><th class="n">Pages</th></tr></thead>
    <tbody>
      <tr><td>Worldwide &mdash; {g['modeles_mondiaux']} keyword templates</td>
        <td class="n">{g['modeles_mondiaux']} &times; {g['pays']} &times;
          {g['villes_par_pays']} &times; {g['langues_par_pays']}</td>
        <td class="n">{n(g['total_mondial'])}</td></tr>
      <tr><td>Canada + United States</td>
        <td class="n">{g['termes_na']} &times; {g['villes_na']}</td>
        <td class="n">{n(g['total_na'])}</td></tr>
      <tr><td>French variant (Canada)</td>
        <td class="n">{g['termes_na']} &times; {g['villes_fr_ca']}</td>
        <td class="n">{n(g['total_fr'])}</td></tr>
      <tr class="total"><td><b>Total</b></td><td class="n"></td>
        <td class="n"><b>{n(g['total'])}</b></td></tr>
    </tbody>
  </table></div>

  <div class="sec-h" style="margin-top:38px"><h2>What is built</h2></div>
  <div class="enroule"><table class="tab">
    <thead><tr><th>Pages</th><th class="n">Count</th></tr></thead>
    <tbody>
      <tr><td>One page per city &mdash; 100 USA &amp; Canada, 50 Europe,
        50 Middle East, 50 Asia</td>
        <td class="n">{n(PROPOSE['villes'])}</td></tr>
      <tr><td>One page per region</td><td class="n">{PROPOSE['regions']}</td></tr>
      <tr><td>One page per service</td><td class="n">{PROPOSE['services']}</td></tr>
      <tr><td>Studio, work, services, locations, plan</td>
        <td class="n">{PROPOSE['fixes']}</td></tr>
      <tr class="total"><td><b>Total</b></td>
        <td class="n"><b>{n(PROPOSE['total'])}</b></td></tr>
    </tbody>
  </table></div>
  <p class="note" style="margin-top:16px">{g['total'] // PROPOSE['total']} times
  fewer pages than the grid &mdash; and pages that can actually be filled.</p>

  <div class="sec-h" style="margin-top:38px"><h2>Four reasons</h2></div>
  <div class="grille g2">
    <div class="carte"><span class="num">01</span>
      <h3>There were never {n(g['total'])} texts to write</h3>
      <p>There was one, repeated. &ldquo;Web Development&rdquo; and
      &ldquo;Website Development&rdquo; are not two trades, they are two
      spellings. One page per spelling per city is the same text
      {g['termes_na']} times in every city.</p></div>
    <div class="carte"><span class="num">02</span>
      <h3>The name of the thing</h3>
      <p>Search engines call them doorway pages, and the penalty lands on the
      <b>domain</b>, not the page. The risk is not &ldquo;these pages will not
      rank&rdquo;, it is &ldquo;the whole site disappears&rdquo;. For a studio
      that sells web work, that is the worst possible advertisement.</p></div>
    <div class="carte"><span class="num">03</span>
      <h3>Meta descriptions</h3>
      <p>One per page, all different &mdash; checked across all
      {n(PROPOSE['total'])}. A duplicated description is discarded and replaced
      by a snippet the engine picks, so writing one for all of them is the same
      as writing none.</p></div>
    <div class="carte"><span class="num">04</span>
      <h3>What cannot be invented</h3>
      <p>What makes a local page local is a client, a project, a number in that
      city. Writing &ldquo;serving Calgary businesses since 2019&rdquo; when
      nobody said so is not optimisation, it is a false claim published under
      your name.</p></div>
  </div>

  <div class="sec-h" style="margin-top:38px"><h2>What is needed to publish them</h2></div>
  <div class="encadre"><ol>
    <li>The cities where there is <b>genuinely</b> a delivered project, a
    client or a contact. Three is enough to start.</li>
    <li>For each: what was done there, and whether the client can be named.</li>
    <li>The studio's registered name and legal entity &mdash; the site still
    carries a name that has not been confirmed in writing.</li>
  </ol></div>
</div></section>
"""


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    with open(os.path.join(RACINE, "assets", "site.css"), encoding="utf-8") as f:
        css = f.read()
    assert css.count("/*") == css.count("*/"), "site.css : commentaires desequilibres"

    page("index.html", f"{MARQUE} — {BASELINE.lower()}",
         "A web studio that ships sites and applications with the automatic "
         "checks that prove they work. Three projects live on this page, "
         "all linked.",
         accueil())
    page("images.html", f"Images to generate — {MARQUE}",
         f"{len(IMAGES)} image briefs with exact file names, pixel sizes and "
         "prompts. No faces, no logos, no invented screenshots.",
         page_images())
    page("services.html", f"Services — {MARQUE}",
         "Four web development services, the eleven names clients give them, "
         "and the five things that move a quote.", services_index())
    page("villes.html", f"Locations — {MARQUE}",
         f"The {len(TOUTES)} cities covered: 100 across the USA and Canada, "
         "50 in Europe, 50 in the Middle East, 50 in Asia.", villes_index())
    page("plan.html", f"The plan and the numbers — {MARQUE}",
         "What the keyword grid asked for, what is built instead, and why one "
         "page per city rather than one per synonym.", plan())

    for cle, nom, liste in REGIONS:
        propre = nom.replace("&amp;", "&")
        page(f"region-{cle}.html", f"{propre} — {MARQUE}",
             f"Web development across {len(liste)} cities in {propre}. "
             "One page per city, grouped by country.",
             page_region(cle, nom, liste), actuel="villes.html")

    for s in SERVICES:
        propre = s[1].replace("&amp;", "&")
        page(f"service-{s[0]}.html", f"{propre} — {MARQUE}",
             f"{propre}: {s[2]} Also called {', '.join(s[3])}.",
             page_service(s), actuel="services.html")

    for rang, v in enumerate(TOUTES):
        page(f"ville-{v[0]}.html",
             f"Web development in {v[1]} — {MARQUE}",
             meta_ville(v, rang),
             page_ville(v, rang), actuel="villes.html")

    perimees = sorted(f for f in os.listdir(RACINE)
                      if f.endswith(".html") and f not in ECRITES)
    for f in perimees:
        os.remove(os.path.join(RACINE, f))
    if perimees:
        print(f"  {len(perimees)} page(s) perimee(s) supprimee(s)")

    print(f"{len(ECRITES)} pages ecrites")
    print(f"  sa grille : {n(GRILLE['total'])} | construites : {n(PROPOSE['total'])}")
