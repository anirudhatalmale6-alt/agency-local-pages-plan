# -*- coding: utf-8 -*-
"""
Les donnees du plan de pages locales de l'agence.

Elles viennent de SON fichier « Websites platform.xlsx » : les onze termes de
service sont les siens, recopies tels quels. Les villes sont reelles — ce sont
des noms de lieux, pas des affirmations sur un marche.

CE QUI N'EST PAS ICI, ET NE PEUT PAS Y ETRE : la matiere locale. Un client,
un projet, un chiffre, une reference dans la ville. Je ne l'ai pas, et je ne
l'invente pas : une page de service qui affirme « nous accompagnons les
entreprises de Calgary depuis 2019 » sans que ce soit vrai est un mensonge
commercial, pas une optimisation.
"""

# Le vocabulaire du vide DE CE PRODUIT. Onzieme, distinct des dix autres, et
# il dit exactement ce qui manque plutot que « a definir ».
VIDE = "Needs local input"

# LE NOM. Il l'a donne le 11 septembre : « Modersly / Is the name ».
# Ecrit EXACTEMENT comme il l'a ecrit. Je lui ai demande de confirmer
# l'orthographe une fois : un nom de marque mal ecrit sur 262 pages coute
# plus cher a corriger qu'a verifier.
MARQUE = "Modersly"
BASELINE = "A modern web studio"

# --- SES onze termes, bloc « CANADA & UNITED STATES TOP 100 CITIES » -------
# Recopies mot pour mot depuis son tableur.
TERMES = [
    "Web Development",
    "Website Development",
    "Web Development Services",
    "Website Development Services",
    "Web Design & Development",
    "Web Design and Development",
    "Web Engineering",
    "Web Application Development",
    "Web App Development",
    "Web Solutions Development",
    "Digital Development",
]

# Les six qui portent une intention DIFFERENTE. Les cinq autres sont des
# variantes d'ecriture du meme besoin (« Web » / « Website », « & » / « and »,
# avec ou sans « Services ») : elles meritent d'etre NOMMEES sur la page, pas
# d'avoir chacune la leur.
SERVICES = [
    ("web-development", "Web development",
     "Websites and applications built to order, from the first screen to launch.",
     ["Website Development", "Web Development Services",
      "Website Development Services", "Digital Development"]),
    ("web-design-development", "Web design &amp; development",
     "Design and engineering held by the same team, so nothing is lost between them.",
     ["Web Design and Development"]),
    ("web-application-development", "Web application development",
     "Tools that run in the browser, with accounts, data and permissions.",
     ["Web App Development"]),
    ("web-engineering", "Web engineering",
     "Taking over an existing site, making it reliable, and making it scale.",
     ["Web Solutions Development"]),
]

# --- LE TRAVAIL REEL ------------------------------------------------------
# Ce sont de VRAIS livrables, en ligne, construits pour ce client. Aucun
# projet invente, aucun logo d'une marque qu'on n'a pas servie, aucun
# temoignage fabrique. `controles` est le nombre de controles automatiques
# de chaque suite — un chiffre d'agence qu'on ne peut pas recompter est un
# chiffre invente qui a juste l'air modeste.
TRAVAUX = [
    ("franchise-directory", "Franchise directory",
     "https://anirudhatalmale6-alt.github.io/annuaire-franchises-demo/",
     76,
     "Two hundred brands, twenty categories, twenty-two countries. Cross "
     "filters, a currency per country, comparison and an application form.",
     ["Filters with predictive counters",
      "Ranked on a common reference value, shown in local currency",
      "French and English from a single data set"]),
    ("hotel-franchising", "Hotel franchising",
     "https://anirudhatalmale6-alt.github.io/annuaire-franchises-demo/hotellerie.html",
     62,
     "A separate section, because a hotel is not bought for a sum but per "
     "key. Filter by hotel size, two fee bases, four contract types.",
     ["Project cost computed, never drawn at random",
      "The size filter asks for membership of a range",
      "The trade's vocabulary rather than generic columns"]),
    ("prestige-houses", "Prestige houses",
     "https://anirudhatalmale6-alt.github.io/maisons-de-prestige/",
     109,
     "A black site, five stars. Management contracts, base and incentive "
     "fees on two different bases, group contribution.",
     ["A full dark design system, accessible in contrast",
      "Five distinctions, four operating structures",
      "Owner form and deep-linked detail sheets"]),
]

# Comment on travaille. Quatre etapes, pas un discours.
ETAPES = [
    ("Scope", "What the site has to do, who edits it afterwards, and what "
              "happens when it is wrong. Written down before anything is drawn."),
    ("Build", "One source of truth. Every page is generated, so a correction "
              "lands everywhere at once instead of in the copy nobody opens."),
    ("Prove", "Every project ships with an automatic check suite, run against "
              "the published site &mdash; not against the version on my machine."),
    ("Hand over", "The code, the generator and the checks. Nothing is locked "
                  "to us, and nothing needs us to stay."),
]

# Ce qui fait varier un devis. A la place d'un tarif : les variables.
VARIABLES = [
    "How many pages, and how many of them are genuinely different",
    "How many languages, and whether they share one data set",
    "What you edit yourself after delivery",
    "Which systems it has to talk to",
    "What happens after launch: hosting, backups, corrections",
]

# --- Les villes -----------------------------------------------------------
# Vingt villes reelles du Canada et des Etats-Unis, pour la demonstration.
# Sa grille en demande deux cents ; le point n'est pas le nombre, c'est ce
# qu'on met dedans.
VILLES = [
    ("toronto", "Toronto", "Ontario", "CA", ["en"]),
    ("montreal", "Montreal", "Quebec", "CA", ["fr", "en"]),
    ("vancouver", "Vancouver", "British Columbia", "CA", ["en"]),
    ("calgary", "Calgary", "Alberta", "CA", ["en"]),
    ("ottawa", "Ottawa", "Ontario", "CA", ["en", "fr"]),
    ("edmonton", "Edmonton", "Alberta", "CA", ["en"]),
    ("quebec-city", "Quebec City", "Quebec", "CA", ["fr", "en"]),
    ("winnipeg", "Winnipeg", "Manitoba", "CA", ["en"]),
    ("hamilton", "Hamilton", "Ontario", "CA", ["en"]),
    ("halifax", "Halifax", "Nova Scotia", "CA", ["en"]),
    ("new-york", "New York", "New York", "US", ["en"]),
    ("los-angeles", "Los Angeles", "California", "US", ["en"]),
    ("chicago", "Chicago", "Illinois", "US", ["en"]),
    ("houston", "Houston", "Texas", "US", ["en"]),
    ("phoenix", "Phoenix", "Arizona", "US", ["en"]),
    ("philadelphia", "Philadelphia", "Pennsylvania", "US", ["en"]),
    ("san-antonio", "San Antonio", "Texas", "US", ["en"]),
    ("san-diego", "San Diego", "California", "US", ["en"]),
    ("dallas", "Dallas", "Texas", "US", ["en"]),
    ("seattle", "Seattle", "Washington", "US", ["en"]),
]

LANGUES = {"en": "English", "fr": "Francais"}

# --- L'arithmetique de SA grille, calculee depuis SON fichier --------------
# Elle est affichee telle quelle sur la page « Le plan ». Personne ne decide
# a l'aveugle une fois qu'il a vu le nombre.
GRILLE = {
    "modeles_mondiaux": 16,     # lignes 2 a 17 du tableur
    "pays": 195,
    "villes_par_pays": 20,      # « Top 20 cities »
    "langues_par_pays": 3,      # « Top 3 languages per country »
    "termes_na": 11,            # lignes 30 a 40
    "villes_na": 200,           # « CANADA & UNITED STATES TOP 100 CITIES »
    "villes_fr_ca": 100,        # « French variant for Canada »
}
GRILLE["total_mondial"] = (GRILLE["modeles_mondiaux"] * GRILLE["pays"]
                           * GRILLE["villes_par_pays"] * GRILLE["langues_par_pays"])
GRILLE["total_na"] = GRILLE["termes_na"] * GRILLE["villes_na"]
GRILLE["total_fr"] = GRILLE["termes_na"] * GRILLE["villes_fr_ca"]
GRILLE["total"] = GRILLE["total_mondial"] + GRILLE["total_na"] + GRILLE["total_fr"]

# Ce que produit le plan propose a la place : une page par ville, pas une par
# synonyme et par ville.
PROPOSE = {
    "villes": GRILLE["villes_na"],
    "services": len(SERVICES),
    "pages_ville": GRILLE["villes_na"],
    "pages_service": len(SERVICES),
}
PROPOSE["total"] = PROPOSE["pages_ville"] + PROPOSE["pages_service"] + 3
