DIALOGUES = {

    "Tavern Keeper": {

        "talk": [
            {
                "texts": [
                   "Il n'y a pas grand monde ce matin, hein ?",
                   "Vous cherchez quelque chose en particulier ?" 
                ],
                "required_tags": ["tavern", "morning", "tavern_open"],
                "forbidden_tags": ["tavern_closed"]
            },
            {
                "texts": [
                   "Bienvenue à la taverne !",
                   "Vous voulez boire un verre ?",
                   "Vous avez faim ? J'ai de la bonne viande fraîche !",
                   "Si vous voulez vous reposer, j'ai des chambres à louer."
                ],
                "required_tags": ["tavern", "afternoon", "tavern_open"],
                "forbidden_tags": ["tavern_closed"]
            },
            {
                "texts": [
                    "Bonsoir... Vous cherchez un endroit où passer la nuit ?",
                    "Je peux vous louer une chambre pour la nuit, si vous voulez."
                ],
                "required_tags": ["tavern", "evening", "tavern_open"],
                "forbidden_tags": ["tavern_closed"]
            },
            {
                "required_tags": ["tavern", "night", "tavern_open"],
                "forbidden_tags": ["tavern_closed"],
                "texts": [
                    "Il est tard... Vous devriez trouver un endroit pour dormir.",
                    "Je peux vous louer une chambre pour la nuit, si vous voulez."
                ],
            },
            {
                "required_tags": ["tavern", "tavern_closed"],
                "forbidden_tags": ["tavern_open"],
                "texts": [
                    "Désolé, la taverne est fermée pour le moment.",
                    "Revenez plus tard !",
                    "Je ne peux pas vous servir pour le moment, la taverne est fermée."
                ],
            },
        ],
    },
    "Knight": {
        "talk": [
            {
                "texts": [
                    "Hé, vous là-bas ! Vous avez l'air d'être quelqu'un de bien. Vous voulez m'aider à trouver un trésor caché dans la forêt ?",
                    "Je suis à la recherche d'un trésor légendaire qui serait caché quelque part dans cette forêt. Vous voulez m'aider à le trouver ?"
                ],
                "required_tags": ["forest", "afternoon"],
                "forbidden_tags": ["combat"]
            },
            {
                "texts": [
                    "Je suis désolé, je ne peux pas parler en ce moment. Je dois me concentrer sur ma quête.",
                    "Je suis en mission pour trouver un trésor caché dans cette forêt. Je ne peux pas me permettre de perdre du temps à discuter."
                ],
                "required_tags": ["forest", "combat"],
                "forbidden_tags": []
            },
        ],
    },
}


DESCRIPTIONS = {

    "Taverne": {

        "ambient": [
            {
                "texts": [
                    "La salle sent le bois ciré, la cendre froide et les restes de repas.",
                    "Quelques chaises grincent doucement dans le calme de la taverne."
                ],
                "required_tags": ["tavern", "morning", "tavern_open"],
                "forbidden_tags": ["combat"]
            },
            {
                "texts": [
                    "La taverne bruisse d'une activité tranquille, entre les tables et le comptoir.",
                    "La lumière de l'après-midi découpe les poussières suspendues dans l'air."
                ],
                "required_tags": ["tavern", "afternoon", "tavern_open"],
                "forbidden_tags": ["combat"]
            },
            {
                "texts": [
                    "Les ombres s'allongent entre les tables, et le feu devient le centre de la pièce.",
                    "La taverne prend une couleur chaude, comme si la nuit attendait dehors."
                ],
                "required_tags": ["tavern", "evening", "tavern_open"],
                "forbidden_tags": ["combat"]
            },
            {
                "texts": [
                    "La taverne est presque silencieuse. Seules les braises gardent la salle éveillée.",
                    "Dans la pénombre, les tables vides semblent attendre le matin."
                ],
                "required_tags": ["tavern", "night"],
                "forbidden_tags": ["combat"]
            },
            {
                "texts": [
                    "La porte de la taverne reste close, et le bâtiment paraît retenir son souffle.",
                    "Derrière les volets fermés, rien ne bouge."
                ],
                "required_tags": ["tavern", "tavern_closed"],
                "forbidden_tags": ["tavern_open", "combat"]
            },
        ],
    },

    "Forêt": {

        "ambient": [
            {
                "texts": [
                    "La forêt respire lentement sous une lumière pâle.",
                    "Des branches humides filtrent le jour en éclats verts et gris."
                ],
                "required_tags": ["forest", "morning"],
                "forbidden_tags": ["combat"]
            },
            {
                "texts": [
                    "Les troncs serrés découpent des chemins incertains entre les fougères.",
                    "Le sous-bois est dense, plein de craquements lointains."
                ],
                "required_tags": ["forest", "afternoon"],
                "forbidden_tags": ["combat"]
            },
            {
                "texts": [
                    "La forêt s'assombrit, et chaque sentier semble mener plus loin que prévu.",
                    "Le soir pose une brume fine entre les arbres."
                ],
                "required_tags": ["forest", "evening"],
                "forbidden_tags": ["combat"]
            },
            {
                "texts": [
                    "La nuit rend la forêt plus profonde, presque sans contours.",
                    "Dans l'obscurité, les arbres se confondent avec le silence."
                ],
                "required_tags": ["forest", "night"],
                "forbidden_tags": ["combat"]
            },
            {
                "texts": [
                    "La pluie accroche les feuilles et transforme le sol en boue noire.",
                    "L'odeur de terre mouillée remonte entre les racines."
                ],
                "required_tags": ["forest", "rain"],
                "forbidden_tags": ["combat"]
            },
        ],
    },
}
