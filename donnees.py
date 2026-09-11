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

MARQUE = "JNCORP Studio"

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
     "Sites et applications sur mesure, du premier ecran a la mise en ligne.",
     ["Website Development", "Web Development Services",
      "Website Development Services", "Digital Development"]),
    ("web-design-development", "Web design &amp; development",
     "La conception graphique et le developpement tenus par la meme equipe.",
     ["Web Design and Development"]),
    ("web-application-development", "Web application development",
     "Des outils metier qui tournent dans le navigateur, avec comptes et donnees.",
     ["Web App Development"]),
    ("web-engineering", "Web engineering",
     "Reprise, fiabilisation et mise a l'echelle d'un site existant.",
     ["Web Solutions Development"]),
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
