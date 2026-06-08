# Etat du projet RPG_v2

Ce document resume l'etat actuel du projet, son intention de design, ce qui fonctionne deja, les limites visibles et les axes de progression prioritaires.

## Vision actuelle

Le projet est un prototype de RPG textuel/simulation narrative en Python, construit autour d'un petit monde vivant. Le joueur observe un monde tour par tour dans lequel des personnages non joueurs ont une position, une routine, des objectifs, et peuvent produire des descriptions ou dialogues selon le contexte.

L'idee centrale n'est pas seulement d'afficher du texte, mais de faire emerger des situations a partir de composants simples :

- une horloge de jeu ;
- des lieux ;
- des personnages ;
- des schedules ;
- des objectifs ;
- des deplacements ;
- des tags de contexte ;
- des templates narratifs filtres par ces tags.

Le projet ressemble donc davantage a une base de simulation narrative emergente qu'a un RPG classique deja complet.

## Architecture

Le code suit une approche proche d'un ECS leger.

### Entites

Les entites sont definies dans `entity.py`. Une entite possede :

- un `id` ;
- un `name` ;
- un dictionnaire de composants ;
- un ensemble de tags.

Les entites representent aussi bien des personnages que des lieux ou des objets.

### Monde

Le monde est gere par `world.py`. Il contient :

- toutes les entites ;
- la liste des systemes ;
- un `world_state` partage entre les systemes.

Le `world_state` contient notamment l'horloge, les logs, les chroniques, les flags globaux comme la pluie ou la guerre, et les references au joueur et au moteur du monde.

### Composants

Les composants sont dans `components/`.

Les composants principaux actuellement presents sont :

- `Area` : marque une entite comme lieu ;
- `Position` : indique ou se trouve une entite ;
- `Movement` : demande un deplacement vers une cible ;
- `Schedule` : decrit les actions ou activites d'une entite selon l'heure ;
- `Goal` : objectif courant d'une entite ;
- `GameClock` : horloge du monde ;
- `Health` : points de vie ;
- `Hunger` : faim ;
- `Inventory`, `Item`, `TradeRequest`, `Service` : base economique/inventaire ;
- `Mood`, `Mindset` : base comportementale/narrative.

Tous ces composants ne sont pas encore pleinement utilises dans la boucle principale.

### Systemes

Les systemes sont dans `systems/`. Ils sont appeles dans l'ordre par `World.update()`.

Les systemes actuellement branches dans `main.py` sont :

- `TimeSystem` : fait avancer l'horloge ;
- `GoalResolutionSystem` : transforme certains objectifs en deplacements ou effets ;
- `MovementSystem` : applique les deplacements ;
- `DescriptionSystem` : genere des descriptions d'ambiance ;
- `TalkingSystem` : genere des dialogues contextuels ;
- `ScheduleSystem` : attribue des objectifs selon l'heure ;
- `DeleteSystem` : supprime les entites marquees pour suppression.

Des systemes existent mais ne sont pas encore branches dans la boucle principale :

- `HealthSystem` ;
- `HungerSystem` ;
- `EatingSystem` ;
- `TradeSystem` ;
- `AISystem`.

Certains de ces systemes semblent venir d'une iteration precedente et doivent etre remis en coherence avec les composants actuels avant activation.

## Boucle de jeu actuelle

L'application est lancee depuis `main.py` avec Textual.

L'interface contient :

- une colonne gauche pour l'etat des PNJ ;
- une colonne droite pour les chroniques et logs ;
- une action `space` pour passer au tour suivant ;
- une action `q` pour quitter.

A chaque tour :

1. `world.update()` lance tous les systemes.
2. La vue des PNJ est reconstruite.
3. Les chroniques narratives sont affichees.
4. Les logs techniques ou temporels sont affiches.

Chaque tour avance actuellement l'horloge de 10 minutes.

## Contenu actuel

Le monde cree dans `main.py` contient actuellement :

- un moteur de monde avec `GameClock` ;
- une taverne ;
- une foret ;
- le joueur, appele `Infiltrator` ;
- un tavernier ;
- un chevalier ;
- un ecuyer.

Les routines actuelles :

- le tavernier ouvre la taverne a 8h, la gere jusqu'a 22h, puis la ferme ;
- le chevalier marche dans la foret, mange, puis se repose ;
- l'ecuyer s'entraine le matin et l'apres-midi, avec une pause repas.

Les descriptions et dialogues sont definis dans `templates/narrative_templates.py`.

## Ce qui fonctionne deja bien

### Separation claire des responsabilites

Le projet est lisible. Les entites, composants, systemes et templates narratifs sont separes. C'est une bonne base pour agrandir le jeu sans tout melanger dans un seul fichier.

### Narration contextuelle

Le point le plus fort du projet est le systeme de tags contextuels.

`ContextTagBuilder` construit des tags a partir :

- de l'entite ;
- du lieu ;
- de l'heure ;
- de la meteo ;
- de l'etat global du monde ;
- de la faim ;
- de la sante ;
- de l'objectif courant ;
- du deplacement en cours.

Les dialogues et descriptions peuvent ensuite demander des tags obligatoires et interdire d'autres tags. Cela permet d'ajouter beaucoup de contenu narratif sans modifier les systemes.

### Direction recente tres pertinente : perception du joueur

Les modifications recentes ajoutent une notion importante : le joueur ne doit voir ou entendre que ce qui se passe autour de lui.

`DescriptionSystem` et `TalkingSystem` filtrent maintenant selon la position actuelle du joueur. C'est une excellente evolution, car elle transforme le monde en simulation observable plutot qu'en simple flux global d'evenements.

## Limites et fragilites actuelles

### Plusieurs systemes ne sont pas synchronises avec les composants

Certains systemes utilisent encore d'anciens noms de champs.

Exemples :

- `Health` possede `current`, mais `HealthSystem` utilise `current_health` ;
- `Movement` possede `target_entity_id`, mais le rendu essaie parfois de lire `mov.direction.name` ;
- `AISystem` parle de `Routine`, `pos.at_entity`, `world.add_entity`, qui ne correspondent pas a l'API actuelle.

Ces divergences ne bloquent pas toujours le lancement, car les systemes concernes ne sont pas tous branches. Mais elles deviennent dangereuses si on les reactive.

### Certains objectifs ne peuvent pas se resoudre

Dans `GoalResolutionSystem`, l'objectif `train` cible `training_ground`, mais ce lieu n'est pas cree dans `main.py`.

Resultat probable : l'ecuyer peut recevoir l'objectif `train`, mais cet objectif reste bloque ou sans effet.

### L'ordre des systemes cree de la latence

Actuellement, `ScheduleSystem` est appele apres `GoalResolutionSystem` et `MovementSystem`.

Cela signifie qu'un objectif donne par le schedule est souvent resolu au tour suivant, pas immediatement. Ce n'est pas forcement mauvais, mais il faut que ce soit volontaire.

Un ordre plus naturel pourrait etre :

1. temps ;
2. schedule ;
3. besoins/IA ;
4. resolution d'objectifs ;
5. deplacement/action ;
6. narration ;
7. suppression.

### Le joueur observe plus qu'il n'agit

Le joueur existe dans le monde, mais il n'a pas encore une boucle d'action riche.

Il faudrait ajouter des commandes pour :

- se deplacer ;
- inspecter un lieu ;
- parler a un PNJ ;
- attendre ;
- prendre ou utiliser un objet.

Sans cela, le projet reste surtout une simulation visualisee.

### Le contenu est encore minimal

Le monde est actuellement petit : deux lieux, quelques personnages, peu d'objets, peu de dialogues, pas encore de quete jouable.

Ce n'est pas un probleme pour un prototype, mais le prochain cap sera de transformer la base technique en experience de jeu.

### `requirements.txt` est trop large

Le fichier `requirements.txt` contient beaucoup de dependances qui semblent sans rapport direct avec ce projet Textual.

Cela rend l'installation plus lourde et moins claire. Il faudrait isoler les dependances reelles du RPG, probablement au minimum `textual` et ses dependances.

## Axes de progression prioritaires

### 1. Consolider les contrats entre composants et systemes

Objectif : faire en sorte que tous les systemes parlent le meme langage.

Actions conseillees :

- uniformiser `Health.current` / `Health.max_val` ;
- uniformiser `Movement.target_entity_id` ;
- corriger ou retirer les references a `Routine`, `direction`, `at_entity`, `add_entity` ;
- verifier tous les systemes non branches avant activation.

C'est le chantier le plus important pour stabiliser le projet.

### 2. Reordonner la boucle de simulation

Objectif : rendre le comportement du monde plus previsible.

Ordre conseille :

1. `TimeSystem`
2. `ScheduleSystem`
3. `HungerSystem` / besoins
4. `GoalResolutionSystem`
5. `MovementSystem`
6. systemes d'action comme manger, commerce, dialogue force
7. `DescriptionSystem`
8. `TalkingSystem`
9. `DeleteSystem`

L'ordre exact peut changer, mais il doit etre explicite et documente.

### 3. Donner des actions au joueur

Objectif : passer d'une simulation observee a un vrai jeu.

Premiere version possible :

- `m` : changer de lieu ;
- `i` : inspecter le lieu ;
- `t` : parler a un PNJ present ;
- `w` : attendre ;
- `g` : ramasser un objet.

Meme avec peu de contenu, cela rendrait le prototype beaucoup plus jouable.

### 4. Externaliser la creation du monde

Objectif : sortir progressivement le contenu de `main.py`.

Approches possibles :

- une factory Python pour creer le monde initial ;
- des fichiers JSON/YAML pour lieux, PNJ, schedules et templates ;
- une combinaison des deux.

Cela rendrait l'ajout de contenu plus simple et eviterait que `main.py` devienne un fichier trop central.

### 5. Enrichir les relations entre PNJ

Objectif : rendre la narration plus personnelle.

Idees :

- relations d'amitie/rivalite ;
- memoire des conversations recentes ;
- reputation du joueur ;
- humeur influencee par les evenements ;
- reactions aux actions du joueur.

Le systeme de tags actuel peut deja supporter une grande partie de cela.

### 6. Ajouter des tests courts

Objectif : eviter les regressions pendant que le moteur change vite.

Tests prioritaires :

- `Schedule.get_actions_for_time` ;
- `Schedule.get_current_activity` ;
- `ContextTagBuilder.tags_match` ;
- `GoalResolutionSystem` ;
- `TalkingSystem.find_valid_dialogues` ;
- `DescriptionSystem.find_valid_descriptions`.

Quelques tests simples suffiraient deja a securiser le coeur du projet.

## Roadmap courte proposee

### Etape 1 : stabilisation

- Corriger les divergences entre composants et systemes.
- Ajouter le lieu `training_ground` ou retirer temporairement l'objectif `train`.
- Reordonner les systemes.
- Nettoyer les imports inutilises.

### Etape 2 : boucle joueur

- Ajouter un systeme de commandes joueur.
- Permettre au joueur de changer de lieu.
- Permettre une interaction volontaire avec les PNJ.
- Differencier les logs systeme des textes narratifs.

### Etape 3 : contenu jouable

- Ajouter une mini-quete avec le chevalier.
- Ajouter quelques objets.
- Ajouter une consequence simple aux choix du joueur.
- Ajouter des dialogues/reponses selon l'etat de la quete.

### Etape 4 : simulation plus profonde

- Reactiver faim/sante/nourriture apres correction.
- Ajouter commerce ou services de taverne.
- Ajouter relations, humeur, reputation.
- Ajouter evenements globaux aleatoires ou scriptes.

## Conclusion

Le projet est encore au stade prototype, mais il possede une tres bonne colonne vertebrale : une simulation ECS simple, un monde tour par tour, et surtout une narration pilotee par des tags contextuels.

Le potentiel est clairement du cote RPG narratif emergent : des PNJ qui vivent selon leurs routines, un joueur qui observe seulement ce qu'il peut percevoir, et des textes qui changent selon le lieu, l'heure, l'etat du monde et les personnages.

Le prochain objectif ne devrait pas etre d'ajouter beaucoup de features. Il faudrait d'abord stabiliser les contrats internes, puis ajouter une vraie boucle d'action joueur. Une fois ces deux points faits, le projet pourra grandir beaucoup plus proprement.
