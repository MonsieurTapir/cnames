from app import app, db
import os

app.config.from_object(os.environ['APP_SETTINGS'])

words=["uniforme",
"page",
"iris",
"bête",
"tube",
"lit",
"ninja",
"londres",
"courverture",
"menu",
"chemise",
"sol",
"bureau",
"religieuse",
"poêle",
"partie",
"liquide",
"bon",
"fort",
"peste",
"new-york",
"alpes",
"physique",
"avocat",
"bouton",
"bougie",
"mort",
"bûche",
"place",
"mouche",
"araignée",
"aile",
"corde",
"rouge",
"bâton",
"sirène",
"colle",
"filet",
"forêt",
"marin",
"danse",
"police",
"baleine",
"pôle",
"citrouille",
"rat",
"poisson",
"livre",
"laser",
"terre",
"herbe",
"or",
"héros",
"pingouin",
"oiseau",
"tennis",
"géant",
"vie",
"mars",
"esprit",
"courant",
"noir",
"gauche",
"règle",
"hôpital",
"chasse",
"amérique",
"molière",
"maladie",
"trésor",
"kangourou",
"satellite",
"lien",
"point",
"chausson",
"pyramide",
"champagne",
"chine",
"glace",
"ferme",
"coupe",
"timbre",
"sardine",
"remise",
"solution",
"chou",
"couteau",
"toile",
"mousse",
"numéro",
"carton",
"moule",
"sens",
"majeur",
"critique",
"vague",
"bretelle",
"poste",
"lentille",
"asile",
"palais",
"bande",
"guerre",
"voleur",
"cinéma",
"flûte",
"anneau",
"souris",
"vampire",
"canard",
"restaurant",
"temps",
"journal",
"pied",
"zéro",
"centre",
"baguette",
"afrique",
"chat",
"cercle",
"voiture",
"docteur",
"histoire",
"jeu",
"vert",
"plage",
"noël",
"casino",
"princesse",
"bière",
"berlin",
"indien",
"sept",
"aiguille",
"droite",
"coeur",
"reine",
"bouteille",
"hiver",
"échelle",
"opéra",
"génie",
"jungle",
"hôtel",
"soleil",
"bouche",
"ballon",
"soldat",
"table",
"étoile",
"oeil",
"branche",
"verre",
"cochon",
"résistance",
"égypte",
"roi",
"chance",
"sorcière",
"alien",
"argent",
"noeud",
"jour",
"main",
"roulette",
"dinosaure",
"café",
"tête",
"pouce",
"bateau",
"crochet",
"chevalier",
"pigeon",
"angleterre",
"classe",
"trou",
"robot",
"chocolat",
"tour",
"champ",
"pomme",
"banque",
"requin",
"château",
"vent",
"cheval",
"fou",
"nuit",
"coton",
"temple",
"blé",
"code",
"schtroumpf",
"allemagne",
"himalaya",
"paris",
"robe",
"chien",
"boeuf",
"eau",
"nain",
"mode",
"pétrole",
"neige",
"avion",
"magie",
"scène",
"ange",
"serpent",
"miel",
"pirate",
"microscope",
"plume",
"espion",
"tableau",
"appareil",
"dragon",
"amour",
"maîtresse",
"oeuf",
"luxe",
"canada",
"ceinture",
"piano",
"balle",
"parachute",
"visage",
"science",
"français",
"camembert",
"licorne",
"poison",
"atlantique",
"égalité",
"papier",
"lion",
"machine",
"bouchon",
"pilote",
"rose",
"moustache",
"lune",
"jumelles",
"fantôme",
"école",
"millionnaire",
"lait",
"cirque",
"feu",
"chapeau",
"plante",
"marque",
"membre",
"ligne",
"vase",
"droit",
"banc",
"guide",
"couronne",
"carte",
"plat",
"canon",
"gel",
"garde",
"quartier",
"bourse",
"arc",
"cafard",
"louche",
"carreau",
"pensée",
"baie",
"entrée",
"mine",
"fuite",
"formule",
"titre",
"cartouche",
"manche",
"fraise",
"voila",
"ensemble",
"portable",
"carrière",
"étude",
"kiwi",
"court",
"fer",
"meuble",
"figure",
"napoléon",
"australie",
"ronde",
"grain",
"manège",
"mémoire",
"pile",
"espace",
"éponge",
"note",
"volume",
"charme",
"air",
"prise",
"facteur",
"paille",
"charge",
"rame",
"canne",
"passe",
"orange",
"course",
"rome",
"révolution",
"ampoule",
"patron",
"recette",
"siège",
"but",
"radio",
"marche",
"perle",
"bombe",
"plateau",
"chef",
"vol",
"clé",
"somme",
"hollywood",
"europe",
"prêt",
"rayon",
"russie",
"vin",
"cuisine",
"trait",
"corne",
"mineur",
"col",
"ordre",
"cycle",
"farce",
"boulet",
"poire",
"botte",
"chaîne",
"tuile",
"vaisseau",
"balance",
"éclair",
"pêche",
"base",
"cabinet",
"club",
"enceinte",
"grue",
"jet",
"campagne",
"pendule",
"don",
"planche",
"opération",
"queue",
"foyer",
"tambour",
"cellule",
"pompe",
"fin",
"vision",
"pièce",
"lettre",
"marron",
"rouleau",
"front",
"talon",
"commerce",
"feuille",
"gorge",
"espagne",
"coq",
"grèce",
"tokyo",
"brique",
"grenade",
"palme",
"langue",
"sortie",
"lunettes",
"phare",
"banane",
"raie",
"boîte",
"lumière",
"astérix",
"atout",
"barre",
"essence",
"cadre",
"bar",
"plan",
"crabe",
"tapir"]
from models import Word
i=0
for w in words:
    word=Word(i,w)
    db.session.add(word)
    db.session.commit()
    i+=1
