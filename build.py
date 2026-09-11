# -*- coding: utf-8 -*-
"""
Le plan de pages locales de l'agence, genere.

  python3 build.py   -> ecrit les .html a cote de ce fichier

Une page par VILLE et une page par SERVICE. Pas une page par synonyme et par
ville : c'est la difference entre un site local et une ferme de pages.
"""
import html
import os

from donnees import GRILLE, MARQUE, SERVICES, TERMES, VIDE
from villes import PAYS_NOM, REGIONS, TOUTES

RACINE = os.path.dirname(os.path.abspath(__file__))
VERSION_CSS = 2
E = html.escape
ECRITES = set()


def n(x):
    return f"{x:,}".replace(",", " ")


def tbd():
    return f'<span class="tbd">{VIDE}</span>'


MENU = [("index.html", "Accueil"), ("services.html", "Services"),
        ("villes.html", "Villes"), ("plan.html", "Le plan")]

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
    "Sites et applications sur mesure",
    "Conception et developpement web",
    "Applications web metier",
    "Reprise et fiabilisation de sites",
    "Developpement web complet",
]


def meta_ville(v, rang):
    slug, nom, division, pays, langues, region = v
    angle = ANGLES[rang % len(ANGLES)]
    lg = ", ".join(LANGUES_NOM.get(l, l) for l in langues[:2])
    return (f"{angle} a {nom}, {division}, {pays_nom(pays)}. "
            f"Quatre prestations, equipe jointe en {lg}. "
            f"Page {REG_NOM[region].replace('&amp;', '&')}.")


LANGUES_NOM = {
    "en": "anglais", "fr": "francais", "es": "espagnol", "de": "allemand",
    "it": "italien", "nl": "neerlandais", "pt": "portugais", "sv": "suedois",
    "da": "danois", "no": "norvegien", "fi": "finnois", "pl": "polonais",
    "cs": "tcheque", "hu": "hongrois", "ro": "roumain", "bg": "bulgare",
    "el": "grec", "hr": "croate", "ar": "arabe", "he": "hebreu",
    "tr": "turc", "ja": "japonais", "zh": "chinois", "ko": "coreen",
    "hi": "hindi", "th": "thai", "id": "indonesien", "ms": "malais",
    "tl": "tagalog", "vi": "vietnamien", "si": "cingalais", "bn": "bengali",
    "ur": "ourdou",
}


def page(fichier, titre, description, corps, actuel=None, alternates=""):
    nav = "".join(
        f'<a href="{f}"{" aria-current=\"page\"" if f == (actuel or fichier) else ""}>{E(t)}</a>'
        for f, t in MENU)
    doc = f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(titre)}</title>
<meta name="description" content="{E(description)}">
<meta name="robots" content="noindex,nofollow">
{alternates}<link rel="stylesheet" href="assets/site.css?v={VERSION_CSS}">
</head>
<body>

<div class="avert"><div class="wrap">
  <b>Plan de travail, pas un site en ligne.</b> Les pages de ville sont des
  gabarits : elles attendent la matiere locale que toi seul as. Tant qu'elle
  manque, elles sont en <code>noindex</code> &mdash;
  <a href="plan.html">pourquoi, et le calcul</a>.
</div></div>

<header class="top"><div class="wrap bar">
  <a class="marque" href="index.html">{E(MARQUE)}</a>
  <nav class="nav">{nav}</nav>
</div></header>

<main>
{corps}
</main>

<footer class="pied"><div class="wrap">
  {E(MARQUE)} &mdash; plan de pages locales. Aucun tarif, aucune reference
  inventee, aucune page publiee.
</div></footer>

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
    "fixes": 4,          # accueil, services, villes, plan
    "regions": len(REGIONS),
}
PROPOSE["total"] = (PROPOSE["villes"] + PROPOSE["services"]
                    + PROPOSE["fixes"] + PROPOSE["regions"])


# ---------------------------------------------------------------------------
def accueil():
    cartes = "".join(f"""<div class="carte"><h3>{s[1]}</h3><p>{E(s[2])}</p>
      <p class="aussi">Aussi cherche : {', '.join(E(a) for a in s[3])}</p></div>"""
                     for s in SERVICES)
    regions = "".join(f"""<a class="carte" href="region-{cle}.html">
      <h3>{nom}</h3><p>{len(liste)} villes</p></a>"""
                      for cle, nom, liste in REGIONS)
    return f"""
<section class="hero"><div class="wrap">
  <h1>Le web, <em>ville par ville</em></h1>
  <p class="lede">Quatre prestations, {n(PROPOSE['villes'])} villes, une page
  par ville. Pas une page par synonyme et par ville : c'est ce qui separe un
  site local d'une ferme de pages, et c'est ce qui decide si le domaine
  survit.</p>
  <div class="chiffres">
    <div class="chiffre"><div class="v">{n(PROPOSE['villes'])}</div>
      <div class="l">Villes</div></div>
    <div class="chiffre"><div class="v">{PROPOSE['regions']}</div>
      <div class="l">Regions</div></div>
    <div class="chiffre"><div class="v">{PROPOSE['services']}</div>
      <div class="l">Prestations</div></div>
    <div class="chiffre"><div class="v">{n(PROPOSE['total'])}</div>
      <div class="l">Pages au total</div></div>
  </div>
  <div class="actions">
    <a class="btn" href="villes.html">Parcourir les villes</a>
    <a class="btn btn-b" href="plan.html">Le calcul, et pourquoi pas 190 500</a>
  </div>
</div></section>

<section class="sec"><div class="wrap">
  <div class="sec-h"><h2>Les quatre regions</h2>
    <a class="plus" href="villes.html">Toutes les villes &rarr;</a></div>
  <div class="grille g4">{regions}</div>
</div></section>

<section class="sec"><div class="wrap">
  <div class="sec-h"><h2>Quatre services, onze facons de les nommer</h2></div>
  <p class="chapeau">Tes onze termes disent quatre choses. Les sept autres sont
  des variantes d'ecriture du meme besoin : elles ont leur place <b>dans</b> la
  page, pas chacune la leur.</p>
  <div class="grille g2" style="margin-top:18px">{cartes}</div>
</div></section>
"""


def services_index():
    lignes = "".join(f"""<a class="carte" href="service-{s[0]}.html">
      <h3>{s[1]}</h3><p>{E(s[2])}</p></a>""" for s in SERVICES)
    tous = "".join(f"<li>{E(t)}</li>" for t in TERMES)
    return f"""
<section class="sec"><div class="wrap">
  <h1 class="titre">Services</h1>
  <p class="chapeau">Une page par service. Chacune nomme les variantes que les
  gens tapent, ce qui couvre le vocabulaire sans multiplier les pages.</p>
  <div class="grille g2" style="margin-top:20px">{lignes}</div>

  <div class="sec-h" style="margin-top:34px"><h2>Tes onze termes</h2></div>
  <ul class="liste2">{tous}</ul>
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
  <nav class="fil"><a href="index.html">Accueil</a> &rsaquo;
    <a href="services.html">Services</a> &rsaquo; {nom}</nav>
  <h1 class="titre">{nom}</h1>
  <p class="chapeau">{E(phrase)}</p>

  <div class="sec-h" style="margin-top:28px"><h2>Aussi appele</h2></div>
  <p>{', '.join(E(v) for v in variantes)}. Ce sont les memes projets ; la
  facon de les nommer change d'un client a l'autre.</p>

  <div class="sec-h" style="margin-top:28px"><h2>Ce que contient la page</h2></div>
  <div class="encadre"><p>{tbd()}<br>
  Ce que fait l'equipe, comment se deroule un projet, et ce qui fait varier un
  devis. Le site de l'agence porte deja ce texte : il sera repris ici plutot
  que reecrit, pour qu'il n'existe qu'a un seul endroit.</p></div>

  <div class="sec-h" style="margin-top:28px"><h2>Ou</h2></div>
  <div class="villes-liens">{regions}</div>
  <div class="villes-liens" style="margin-top:10px">{exemples}</div>
</div></section>
"""


def villes_index():
    blocs = ""
    for cle, nom, liste in REGIONS:
        apercu = "".join(f'<a href="ville-{v[0]}.html">{E(v[1])}</a>'
                         for v in liste[:14])
        blocs += f"""<div class="sec-h" style="margin-top:30px">
            <h2>{nom}</h2>
            <a class="plus" href="region-{cle}.html">Les {len(liste)} villes &rarr;</a></div>
          <div class="villes-liens">{apercu}</div>"""
    return f"""
<section class="sec"><div class="wrap">
  <h1 class="titre">Villes</h1>
  <p class="chapeau">{n(len(TOUTES))} villes, comme tu les as fixees :
  {len(REGIONS[0][2])} pour les Etats-Unis et le Canada,
  {len(REGIONS[1][2])} en Europe, {len(REGIONS[2][2])} au Moyen-Orient et
  {len(REGIONS[3][2])} en Asie. Chaque ville a UNE page, qui couvre les quatre
  prestations.</p>
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
                  f'<span class="note">{len(par_pays[code])} villes</span></div>'
                  f'<div class="grille g4">{cartes}</div>')
    return f"""
<section class="sec"><div class="wrap">
  <nav class="fil"><a href="index.html">Accueil</a> &rsaquo;
    <a href="villes.html">Villes</a> &rsaquo; {nom}</nav>
  <h1 class="titre">{nom}</h1>
  <p class="chapeau">{len(liste)} villes, groupees par pays.</p>
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
        alt = ('<p class="note">Ville multilingue (' +
               ", ".join(LANGUES_NOM.get(l, l) for l in langues) +
               '). Les versions se declarent en <code>hreflang</code> sur une '
               'seule page, pas en dupliquant l\'adresse.</p>')

    return f"""
<section class="sec"><div class="wrap">
  <nav class="fil"><a href="index.html">Accueil</a> &rsaquo;
    <a href="villes.html">Villes</a> &rsaquo;
    <a href="region-{region}.html">{REG_NOM[region]}</a> &rsaquo; {E(nom)}</nav>
  <h1 class="titre">Developpement web a {E(nom)}</h1>
  <p class="chapeau">{E(division)}, {E(pays_nom(pays))} &middot;
    {", ".join(LANGUES_NOM.get(l, l) for l in langues)}</p>
  {alt}

  <div class="sec-h" style="margin-top:26px"><h2>Ce qu'on fait ici</h2></div>
  <div class="grille g2">{services}</div>

  <div class="sec-h" style="margin-top:32px"><h2>Ce qui manque sur cette page</h2></div>
  <div class="encadre encadre--alerte">
    <p><b>C'est le seul endroit qui compte, et il est vide.</b></p>
    <ul>
      <li>Un projet reel livre a {E(nom)} ou dans la region &mdash; {tbd()}</li>
      <li>Le nom d'un client qui accepte d'etre cite &mdash; {tbd()}</li>
      <li>Ce qui differe VRAIMENT ici : langue de travail, secteurs dominants,
          obligations locales &mdash; {tbd()}</li>
    </ul>
    <p class="note">Sans au moins un de ces trois elements, cette page dit la
    meme chose que les {n(len(TOUTES) - 1)} autres, le nom de la ville
    excepte. C'est ce que les moteurs appellent une page satellite, et la
    sanction porte sur le domaine entier.</p>
  </div>

  <div class="sec-h" style="margin-top:32px"><h2>Autres villes &mdash;
    {REG_NOM[region]}</h2>
    <a class="plus" href="region-{region}.html">Toutes &rarr;</a></div>
  <div class="villes-liens">{autres}</div>
</div></section>
"""


def plan():
    g = GRILLE
    return f"""
<section class="sec"><div class="wrap">
  <h1 class="titre">Le plan, et le calcul</h1>
  <p class="chapeau">Le calcul vient de ton fichier
  <code>Websites platform.xlsx</code>, avec tes propres nombres. Le plan, lui,
  est celui que tu as fixe ensuite.</p>

  <div class="sec-h" style="margin-top:28px"><h2>Ce que demandait la grille</h2></div>
  <div class="enroule"><table class="tab">
    <thead><tr><th>Bloc</th><th class="n">Calcul</th><th class="n">Pages</th></tr></thead>
    <tbody>
      <tr><td>Mondial &mdash; {g['modeles_mondiaux']} modeles de mots-cles</td>
        <td class="n">{g['modeles_mondiaux']} &times; {g['pays']} &times;
          {g['villes_par_pays']} &times; {g['langues_par_pays']}</td>
        <td class="n">{n(g['total_mondial'])}</td></tr>
      <tr><td>Canada + Etats-Unis</td>
        <td class="n">{g['termes_na']} &times; {g['villes_na']}</td>
        <td class="n">{n(g['total_na'])}</td></tr>
      <tr><td>Variante francaise (Canada)</td>
        <td class="n">{g['termes_na']} &times; {g['villes_fr_ca']}</td>
        <td class="n">{n(g['total_fr'])}</td></tr>
      <tr class="total"><td><b>Total</b></td><td class="n"></td>
        <td class="n"><b>{n(g['total'])}</b></td></tr>
    </tbody>
  </table></div>

  <div class="sec-h" style="margin-top:32px"><h2>Ce qui est construit</h2></div>
  <div class="enroule"><table class="tab">
    <thead><tr><th>Pages</th><th class="n">Nombre</th></tr></thead>
    <tbody>
      <tr><td>Une page par ville &mdash; 100 USA &amp; Canada, 50 Europe,
        50 Moyen-Orient, 50 Asie</td>
        <td class="n">{n(PROPOSE['villes'])}</td></tr>
      <tr><td>Une page par region</td><td class="n">{PROPOSE['regions']}</td></tr>
      <tr><td>Une page par service</td><td class="n">{PROPOSE['services']}</td></tr>
      <tr><td>Accueil, services, villes, plan</td>
        <td class="n">{PROPOSE['fixes']}</td></tr>
      <tr class="total"><td><b>Total</b></td>
        <td class="n"><b>{n(PROPOSE['total'])}</b></td></tr>
    </tbody>
  </table></div>
  <p class="note" style="margin-top:14px">Soit
  {g['total'] // PROPOSE['total']} fois moins de pages que la grille, et des
  pages qu'on peut reellement remplir.</p>

  <div class="sec-h" style="margin-top:32px"><h2>Pourquoi pas les {n(g['total'])}</h2></div>
  <div class="grille g2">
    <div class="carte"><h3>Il n'y avait pas {n(g['total'])} textes a ecrire</h3>
      <p>Il y en avait un, repete. « Web Development » et « Website
      Development » ne sont pas deux metiers : ce sont deux orthographes. Une
      page par orthographe et par ville, c'est le meme texte
      {g['termes_na']} fois dans chaque ville.</p></div>
    <div class="carte"><h3>Le nom de la chose</h3>
      <p>Les moteurs appellent ca des pages satellites. La sanction ne porte
      pas sur la page, elle porte sur le <b>domaine</b> : le risque n'est pas
      « ces pages ne marcheront pas », c'est « le site entier disparait ».</p></div>
    <div class="carte"><h3>Les meta descriptions</h3>
      <p>Une par page, toutes differentes &mdash; un controle le verifie sur
      les {n(PROPOSE['total'])} pages. Une description dupliquee est remplacee
      par un extrait choisi par le moteur : l'ecrire une fois pour toutes
      revient a ne pas l'ecrire.</p></div>
    <div class="carte"><h3>Ce que je ne peux pas inventer</h3>
      <p>Ce qui differencie une page locale, c'est un client, un projet, un
      chiffre dans cette ville. Ecrire « nous accompagnons les entreprises de
      Calgary depuis 2019 » sans que ce soit vrai n'est pas une optimisation,
      c'est une affirmation fausse sous ton nom.</p></div>
  </div>

  <div class="sec-h" style="margin-top:32px"><h2>Ce dont j'ai besoin de toi</h2></div>
  <div class="encadre"><ol>
    <li>Les villes ou tu as <b>reellement</b> un projet livre, un client ou un
    contact. Trois suffisent pour commencer.</li>
    <li>Pour chacune : ce qui y a ete fait, et si le client accepte d'etre cite.</li>
    <li>Le nom et l'entite de l'agence &mdash; le site porte encore un nom
    provisoire.</li>
  </ol></div>
</div></section>
"""


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    with open(os.path.join(RACINE, "assets", "site.css"), encoding="utf-8") as f:
        css = f.read()
    assert css.count("/*") == css.count("*/"), "site.css : commentaires desequilibres"

    page("index.html", f"{MARQUE} — developpement web, ville par ville",
         f"Developpement web et applications sur mesure dans {len(TOUTES)} "
         "villes : USA, Canada, Europe, Moyen-Orient, Asie. Une page par ville.",
         accueil())
    page("services.html", f"Services — {MARQUE}",
         "Quatre prestations de developpement web, et les onze facons dont "
         "elles sont nommees par les clients.", services_index())
    page("villes.html", f"Villes — {MARQUE}",
         f"Les {len(TOUTES)} villes couvertes : 100 en Amerique du Nord, "
         "50 en Europe, 50 au Moyen-Orient, 50 en Asie.", villes_index())
    page("plan.html", f"Le plan et le calcul — {MARQUE}",
         "Ce que la grille de mots-cles demandait, ce qui est construit a la "
         "place, et pourquoi une page par ville plutot que par synonyme.",
         plan())

    for cle, nom, liste in REGIONS:
        propre = nom.replace("&amp;", "&")
        page(f"region-{cle}.html", f"{propre} — {MARQUE}",
             f"Developpement web dans {len(liste)} villes : {propre}. "
             "Une page par ville, groupees par pays.",
             page_region(cle, nom, liste), actuel="villes.html")

    for s in SERVICES:
        propre = s[1].replace("&amp;", "&")
        page(f"service-{s[0]}.html", f"{propre} — {MARQUE}",
             f"{propre} : {s[2]} Aussi appele {', '.join(s[3])}.",
             page_service(s), actuel="services.html")

    for rang, v in enumerate(TOUTES):
        page(f"ville-{v[0]}.html",
             f"Developpement web a {v[1]} — {MARQUE}",
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
