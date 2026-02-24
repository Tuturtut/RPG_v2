# Tu peux mettre ça dans un fichier constants.py ou data.py
NARRATIVE_DB = {
    "HUNGER_LEVEL_UP": {
        "Stoïque": [
            "{name} resserre sa ceinture d'un cran, le visage impassible.",
            "Un léger tremblement trahit {name}, mais son regard reste fixe."
        ],
        "Instable": [
            "{name} gratte les murs de ses ongles, cherchant une issue à sa faim.",
            "{name} marmonne des paroles incohérentes en fixant la porte."
        ],
        "DEFAULT": ["{name} sent la faim tirailler ses entrailles."]
    },
    "EAT_FOOD": {
        "Stoïque": ["{name} mange sa part avec une dignité presque insultante."],
        "Instable": ["{name} dévore sa ration en jetant des regards paranoïaques."],
        "DEFAULT": ["{name} consomme son maigre repas."]
    },
    "DEATH": {
        "Stoïque": ["Le corps de {name} finit par céder, sans un cri."],
        "Instable": ["{name} s'éteint dans un dernier spasme de terreur."],
        "DEFAULT": ["{name} a rendu son dernier soupir."]
    }
}