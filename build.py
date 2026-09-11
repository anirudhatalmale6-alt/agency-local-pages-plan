# -*- coding: utf-8 -*-
"""
Le plan de pages locales de l'agence, genere.

  python3 build.py   -> ecrit les .html a cote de ce fichier

Une page par VILLE et une page par SERVICE. Pas une page par synonyme et par
ville : c'est la difference entre un site local et une ferme de pages.
"""
import html
import os

from donnees import (GRILLE, LANGUES, MARQUE, PROPOSE, SERVICES, TERMES,
                     VIDE, VILLES)

RACINE = os.path.dirname(os.path.abspath(__file__))
VERSION_CSS = 1
E = html.escape
ECRITES = set()


def n(x):
    return f"{x:,}".replace(",", " ")


def tbd():
    return f'<span class="tbd">{VIDE}</span>'


MENU = [("index.html", "Accueil"), ("services.html", "Services"),
        ("villes.html", "Villes"), ("plan.html", "Le plan")]


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


def ville_par_slug(slug):
    return [v for v in VILLES if v[0] == slug][0]


# ---------------------------------------------------------------------------
def accueil():
    cartes = "".join(f"""<div class="carte"><h3>{s[1]}</h3><p>{E(s[2])}</p>
      <p class="aussi">Aussi cherche : {', '.join(E(a) for a in s[3])}</p></div>"""
                     for s in SERVICES)
    return f"""
<section class="hero"><div class="wrap">
  <h1>Des pages locales qui tiennent debout</h1>
  <p class="lede">Ton tableur demande une page par mot-cle, par ville, par
  langue. Calcule sur tes propres chiffres, cela fait
  <b>{n(GRILLE['total'])} pages</b>. Voici la version qui peut etre publiee
  sans risquer le site : <b>{n(PROPOSE['total'])} pages</b>, une par ville et
  une par service.</p>
  <div class="actions">
    <a class="btn" href="plan.html">Voir le calcul</a>
    <a class="btn btn-b" href="villes.html">Voir une page de ville</a>
  </div>
</div></section>

<section class="sec"><div class="wrap">
  <div class="sec-h"><h2>Quatre services, onze facons de les nommer</h2></div>
  <p class="chapeau">Tes onze termes disent quatre choses. Les sept autres
  sont des variantes d'ecriture du meme besoin : elles ont leur place
  <b>dans</b> la page, pas chacune la leur.</p>
  <div class="grille g2">{cartes}</div>
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
    villes = "".join(
        f'<a href="ville-{v[0]}.html">{E(v[1])}</a>' for v in VILLES[:12])
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
  <div class="villes-liens">{villes}</div>
</div></section>
"""


def villes_index():
    par_pays = {}
    for v in VILLES:
        par_pays.setdefault(v[3], []).append(v)
    blocs = ""
    for code, nom in (("CA", "Canada"), ("US", "Etats-Unis")):
        cartes = "".join(f"""<a class="carte" href="ville-{v[0]}.html">
          <h3>{E(v[1])}</h3><p>{E(v[2])}<br>
          <span class="lg">{' / '.join(LANGUES[l] for l in v[4])}</span></p></a>"""
                         for v in par_pays.get(code, []))
        blocs += f'<div class="sec-h" style="margin-top:28px"><h2>{nom}</h2></div>' \
                 f'<div class="grille g4">{cartes}</div>'
    return f"""
<section class="sec"><div class="wrap">
  <h1 class="titre">Villes</h1>
  <p class="chapeau">Vingt villes pour la demonstration. Ta grille en demande
  deux cents ; le nombre n'est pas le probleme, ce qu'on met dans la page l'est.
  Chaque ville a UNE page, qui couvre les quatre services.</p>
  {blocs}
</div></section>
"""


def page_ville(v):
    slug, nom, region, pays, langues = v
    services = "".join(f"""<div class="carte"><h3>{s[1]}</h3>
      <p>{E(s[2])}</p>
      <p class="aussi"><a href="service-{s[0]}.html">La page du service &rarr;</a></p>
      </div>""" for s in SERVICES)

    autres = "".join(f'<a href="ville-{o[0]}.html">{E(o[1])}</a>'
                     for o in VILLES if o[0] != slug)

    # Les alternates de langue. Une VILLE, une page ; la langue est une
    # alternative declaree, pas une deuxieme adresse a faire indexer
    # separement sur le meme contenu.
    alt = ""
    if len(langues) > 1:
        alt = ('<p class="note">Cette ville est bilingue. La version '
               + " et ".join(LANGUES[l] for l in langues)
               + ' se declare en <code>hreflang</code> sur une seule page, '
               'pas en dupliquant l\'adresse.</p>')

    return f"""
<section class="sec"><div class="wrap">
  <nav class="fil"><a href="index.html">Accueil</a> &rsaquo;
    <a href="villes.html">Villes</a> &rsaquo; {E(nom)}</nav>
  <h1 class="titre">Developpement web a {E(nom)}</h1>
  <p class="chapeau">{E(region)}, {"Canada" if pays == "CA" else "Etats-Unis"}
   &middot; {' / '.join(LANGUES[l] for l in langues)}</p>
  {alt}

  <div class="sec-h" style="margin-top:26px"><h2>Ce qu'on fait ici</h2></div>
  <div class="grille g2">{services}</div>

  <div class="sec-h" style="margin-top:32px"><h2>Ce qui manque sur cette page</h2></div>
  <div class="encadre encadre--alerte">
    <p><b>C'est le seul endroit qui compte, et il est vide.</b></p>
    <ul>
      <li>Un projet reel livre a {E(nom)} ou dans la region &mdash; {tbd()}</li>
      <li>Le nom d'un client qui accepte d'etre cite &mdash; {tbd()}</li>
      <li>Ce qui differe VRAIMENT ici : langue de travail, secteurs
          dominants, obligations locales &mdash; {tbd()}</li>
    </ul>
    <p class="note">Sans au moins un de ces trois elements, cette page dit
    exactement la meme chose que les dix-neuf autres, le nom de la ville
    excepte. C'est ce que les moteurs appellent une page satellite, et c'est
    ce qui fait tomber un domaine entier &mdash; pas seulement la page.</p>
  </div>

  <div class="sec-h" style="margin-top:32px"><h2>Autres villes</h2></div>
  <div class="villes-liens">{autres}</div>
</div></section>
"""


def plan():
    g = GRILLE
    return f"""
<section class="sec"><div class="wrap">
  <h1 class="titre">Le plan, et le calcul</h1>
  <p class="chapeau">Tout ce qui suit est calcule depuis ton fichier
  <code>Websites platform.xlsx</code>, avec tes propres nombres.</p>

  <div class="sec-h" style="margin-top:28px"><h2>Ce que demande la grille</h2></div>
  <div class="enroule"><table class="tab">
    <thead><tr><th>Bloc</th><th class="n">Calcul</th><th class="n">Pages</th></tr></thead>
    <tbody>
      <tr><td>Mondial &mdash; {g['modeles_mondiaux']} modeles de mots-cles</td>
        <td class="n">{g['modeles_mondiaux']} &times; {g['pays']} pays &times;
          {g['villes_par_pays']} villes &times; {g['langues_par_pays']} langues</td>
        <td class="n">{n(g['total_mondial'])}</td></tr>
      <tr><td>Canada + Etats-Unis</td>
        <td class="n">{g['termes_na']} termes &times; {g['villes_na']} villes</td>
        <td class="n">{n(g['total_na'])}</td></tr>
      <tr><td>Variante francaise (Canada)</td>
        <td class="n">{g['termes_na']} &times; {g['villes_fr_ca']}</td>
        <td class="n">{n(g['total_fr'])}</td></tr>
      <tr class="total"><td><b>Total</b></td><td class="n"></td>
        <td class="n"><b>{n(g['total'])}</b></td></tr>
    </tbody>
  </table></div>

  <div class="sec-h" style="margin-top:32px"><h2>Pourquoi je ne les construis pas</h2></div>
  <div class="grille g2">
    <div class="carte"><h3>Il n'y a pas {n(g['total'])} textes a ecrire</h3>
      <p>Il y en a un, repete. « Web Development » et « Website Development »
      ne sont pas deux metiers : ce sont deux orthographes. Une page par
      orthographe et par ville, c'est le meme texte {n(g['termes_na'])} fois
      dans chaque ville.</p></div>
    <div class="carte"><h3>Le nom de la chose</h3>
      <p>Les moteurs appellent ca des pages satellites : des pages creees pour
      une requete, qui menent toutes au meme endroit. La sanction ne porte pas
      sur la page, elle porte sur le <b>domaine</b>. Le risque n'est donc pas
      « ces pages ne marcheront pas », c'est « le site entier disparait ».</p></div>
    <div class="carte"><h3>Ce que je ne peux pas inventer</h3>
      <p>Ce qui differencie une page locale, c'est un client, un projet, un
      chiffre dans cette ville. Je ne les ai pas. Ecrire « nous accompagnons
      les entreprises de Calgary depuis 2019 » sans que ce soit vrai n'est pas
      une optimisation, c'est une affirmation fausse sous ton nom.</p></div>
    <div class="carte"><h3>Trois langues par pays</h3>
      <p>Traduire la meme page en trois langues est legitime &mdash; mais avec
      <code>hreflang</code>, comme trois versions d'UNE page, pas comme trois
      pages qui se font concurrence entre elles.</p></div>
  </div>

  <div class="sec-h" style="margin-top:32px"><h2>Ce que je propose</h2></div>
  <div class="enroule"><table class="tab">
    <thead><tr><th>Pages</th><th class="n">Nombre</th></tr></thead>
    <tbody>
      <tr><td>Une page par ville, couvrant les quatre services</td>
        <td class="n">{n(PROPOSE['pages_ville'])}</td></tr>
      <tr><td>Une page par service, listant les villes</td>
        <td class="n">{n(PROPOSE['pages_service'])}</td></tr>
      <tr><td>Accueil, methode, contact</td><td class="n">3</td></tr>
      <tr class="total"><td><b>Total</b></td>
        <td class="n"><b>{n(PROPOSE['total'])}</b></td></tr>
    </tbody>
  </table></div>
  <p class="note" style="margin-top:14px">Soit
  {g['total'] // PROPOSE['total']} fois moins de pages &mdash; et des pages
  qu'on peut reellement remplir. Le travail se deplace de la generation vers
  la matiere : une ville ouverte quand il y a quelque chose de vrai a y
  ecrire.</p>

  <div class="sec-h" style="margin-top:32px"><h2>Ce dont j'ai besoin de toi</h2></div>
  <div class="encadre"><ol>
    <li>Les villes ou tu as <b>reellement</b> un projet livre, un client ou un
    contact. Meme trois suffisent pour commencer.</li>
    <li>Pour chacune : ce qu'on y a fait, et si le client accepte d'etre cite.</li>
    <li>Le nom et l'entite de l'agence &mdash; le site de demonstration porte
    encore un nom provisoire.</li>
  </ol></div>
</div></section>
"""


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    with open(os.path.join(RACINE, "assets", "site.css"), encoding="utf-8") as f:
        css = f.read()
    assert css.count("/*") == css.count("*/"), "site.css : commentaires desequilibres"

    page("index.html", f"{MARQUE} — plan de pages locales",
         "Le plan de pages locales de l'agence, et le calcul de la grille.",
         accueil())
    page("services.html", f"Services — {MARQUE}",
         "Quatre services, et les onze facons de les nommer.", services_index())
    page("villes.html", f"Villes — {MARQUE}",
         "Les villes couvertes par le plan.", villes_index())
    page("plan.html", f"Le plan et le calcul — {MARQUE}",
         "Ce que la grille demande, ce que ca produit, et ce que je propose.",
         plan())
    for s in SERVICES:
        page(f"service-{s[0]}.html", f"{s[1]} — {MARQUE}", s[2],
             page_service(s), actuel="services.html")
    for v in VILLES:
        page(f"ville-{v[0]}.html",
             f"Developpement web a {v[1]} — {MARQUE}",
             f"Developpement web a {v[1]}, {v[2]}.",
             page_ville(v), actuel="villes.html")

    perimees = sorted(f for f in os.listdir(RACINE)
                      if f.endswith(".html") and f not in ECRITES)
    for f in perimees:
        os.remove(os.path.join(RACINE, f))
    if perimees:
        print("  perimees supprimees :", ", ".join(perimees[:5]))

    print(f"{len(ECRITES)} pages ecrites")
    print(f"  sa grille : {n(GRILLE['total'])} pages"
          f" | proposees : {n(PROPOSE['total'])}")
