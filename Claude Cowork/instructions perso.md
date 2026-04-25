# Instructions personnelles — TP Composant IA à confiance maîtrisée

## Notes et contraintes

- **Code baseline GitHub** : le code baseline fourni dans le GitHub du challenge ne sera peut-être même pas consulté, faute de temps. Ne pas en faire une dépendance.

- **Challenge public vs TP** : bien distinguer le challenge public officiel (Confiance.ai / ETAIA, avec notation, calendrier, prix…) et le TP académique qui s'en inspire mais qui n'est pas censé être aussi abouti. Le niveau d'exigence du TP est inférieur à celui du challenge réel.

- **Dataset** : le dataset d'origine est disponible dans le répertoire `DATA`.

## Pistes techniques envisagées

- **Approche MIL (Multiple Instance Learning)** : à considérer comme option dans l'architecture du composant IA — pertinente pour les cas où les labels sont disponibles au niveau de l'image entière mais pas au niveau des régions (ce qui peut être le cas pour les soudures).

- **Modèle YOLOv5s-C3CA** : à considérer comme backbone ou modèle de détection dans le composant IA — robuste, rapide, adapté à la vision industrielle.

- Approche Backbone Partagé à Deux Têtes avec MIL. Principe:
architecture repose sur un backbone unique freezé qui sert deux têtes de
détection successives, combinée à une approche MIL (Multiple Instance Learning) pour la localisation faiblement supervisée des défauts.

- Considérer la librairie PUNCC pour la quantification d'incertitude

- Considérer la librairie OODeel pour gérer l'ODD et notamment la detection des cas d'OOD (=out of Distribution)

## Organisation du dépot
Le data set récupé se trouve dans le repertoire DATA
l'environnement virtuel est géré par uv

# 2 types de contenus web à considérer:
Les markdowns suivant retranscrivent des pages web indiquées dans l'énoncé du TP et donc prioritaires en cas de conflit avec ce qui est écrit dans "Claude Cowork/etaia_github_io_renault_welding_use_case.md":
- Claude Cowork\etaia_github_io_main_page.md
- Claude Cowork\etaia_github_io_dataset_page.md
- Claude Cowork\etaia_github_io_evaluation_page.md
- Claude Cowork\etaia_github_io_getting_started_page.md
- Claude Cowork\etaia_github_io_FAQ_page.md
Le markdown:
- Claude Cowork/etaia_github_io_renault_welding_use_case.md
retranscrit une page web résumant le welding detection challenge de Renault. Il n'est pas indiqué dans l'énoncé du TP

# Diagrames:
Les diagrammes sont tous à faire avec Mermaid

## to do list:
- a vérifier: Certains markdowns comportent des descriptions d'images et des equations générées par Claude Cowork à partir de screenshotes du site du challenge. --> faire une vérification de cohérence et faire attention à l'utilisation de ces informations (ne pas trop les considérer sans vérifications si une grosse decision statégique repose sur elles)
- analyser le dataset d'origine voir si il faut les corriger avec des outils de la librairie DebiAI
- vérifier / ajuster les diagrammes d'architecture
- définir l'ODD