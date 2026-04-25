# CLAUDE.md — TP Composant IA à confiance maitrisée

## Contexte du projet

TP CentraleSupelec MS IA de Confiance basé sur le **Welding Quality Detection Challenge** (contexte industriel Renault).

**Objectif** : Concevoir un Composant IA à confiance maitrisée — les grandes lignes des approches choisies sont documentées, certains éléments sont détaillés selon le temps disponible.

**Important** : Le code baseline fourni par le challenge n'est pas directement réutilisable tel quel dans ce TP.

## Approches techniques choisies

| Aspect | Choix |
|---|---|
| Paradigme de classification | MIL (Multiple Instance Learning) |
| Backbone | YOLOv5s-C3CA |
| Uncertainty Quantification | Bibliothèque PUNCC |
| OOD Detection | Bibliothèque OODeel |

### Justification du choix MIL

- Les images sont des photos plein cadre d'assemblages soudés — pas des patches
- Les labels sont uniquement au niveau image (`OK`/`KO`), sans annotation de régions → apprentissage faiblement supervisé
- **Bag = image entière**, instances = patches/régions extraits de cette image, weak label = qualité globale
- Caméras à point de vue fixe par seam → ROI empirique par groupe (seam, resolution) envisageable
- Pas de champ `bbox_coord` dans les métadonnées — localisation du cordon non fournie
- Contexte environnant complexe : pièces métalliques de couleur similaire au cordon, possible deuxième soudure en arrière-plan

### Statistiques dataset original (vérifié sur ds_meta.parquet — sans données synthétiques)

**Effectifs par (seam, labelling_type, class) :**

| Seam | Annotateur | KO | OK | Total |
|---|---|---|---|---|
| c20 | expert | 228 | 4 613 | 4 841 |
| c20 | operator | 0 | 57 | 57 |
| c102 | expert | 138 | 4 728 | 4 866 |
| c102 | operator | 5 | 4 081 | 4 086 |
| c33 | expert | 122 | 4 942 | 5 064 |
| c33 | operator | 1 | 3 838 | 3 839 |

**Résolutions par (seam, labelling_type) :**

| Seam | Annotateur | Résolution(s) | N |
|---|---|---|---|
| c20 | expert | 1920×1080 | 4 841 |
| c20 | operator | 1920×1080 | 57 |
| c102 | expert | 1920×1080 | 4 866 |
| c102 | operator | 1920×1080 | 80 |
| c102 | operator | 960×540 | 4 006 |
| c33 | expert | 1920×1080 | 5 064 |
| c33 | operator | 1920×1080 | 83 |
| c33 | operator | 960×540 | 3 756 |

**Points clés :**
- `c102` et `c33` opérateur ont deux résolutions (1920×1080 et 960×540) → ROI fixe par (seam, resolution) nécessaire
- 960×540 = exactement la moitié de 1920×1080 → probablement un downscale (zoom ou compression) — à vérifier visuellement
- Déséquilibre sévère : ~97.8% OK / ~2.2% KO global
- Colonnes disponibles : `sample_id`, `class`, `timestamp`, `welding-seams`, `labelling_type`, `resolution`, `path`, `sha256`, `storage_type`, `data_origin`, `blur_level`, `blur_class`, `luminosity_level`, `external_path`

## Structure du dépôt

```
tp-composant-ia/
├── packages/          # Packages Python (workspace uv)
├── docs/              # Documentation MkDocs (4 sections : Architecture, Datasets, KPIs, Artefacts)
├── sandbox/           # Notebooks d'exploration
├── Claude Cowork/     # Documents de référence (challenge, cours, instructions perso)
├── DATA/              # Datasets locaux
│   └── Original dataset/welding-detection-challenge-dataset/
├── scripts/           # Hooks MkDocs (docs_hooks.py)
├── pyproject.toml     # Config workspace uv (Python >= 3.12)
└── mkdocs.yml         # Config documentation
```

## Les 4 livrables du TP

1. **Architecture** — Schémas Mermaid pour les phases opération, entraînement et évaluation (`docs/architecture/`)
2. **Datasets** — Constitution et usage des datasets par phase du cycle de vie (`docs/datasets/`)
3. **KPIs** — Métriques et mapping aux phases du cycle de vie (`docs/kpi/`)
4. **Artefacts** — Agrégation des KPIs et visualisation pour les parties prenantes (`docs/artefacts/`)

## Environnement & outils

```bash
uv sync                              # Installer les dépendances
uv pip install <package>             # Ajouter un package dans le venv
mkdocs serve                         # Servir la doc sur http://127.0.0.1:8000
uv run nox -s lint|fmt|type_check    # Qualité de code
```

**Kernel Jupyter** : `tp-composant-ia` (installé via `uv run python -m ipykernel install --user --name tp-composant-ia`)

## Problèmes connus

- **MkDocs watcher inopérant** : Le chemin du projet contient `à` et des espaces, ce qui empêche watchdog de détecter les changements sur Windows. Contournement : `export WATCHDOG_USE_POLLING=1` avant `mkdocs serve`, ou redémarrer le serveur manuellement après chaque modification.
- **Chemins Windows dans les notebooks** : Utiliser le préfixe `r""` ou des slashes `/` pour éviter les erreurs d'échappement Unicode.

## Références clés

- [`Claude Cowork/instructions perso.md`](Claude%20Cowork/instructions%20perso.md) — Instructions personnelles et todo list
- [`Claude Cowork/Synthese_Cours_ComposantIA_ConfianceMaitrisee.md`](Claude%20Cowork/Synthese_Cours_ComposantIA_ConfianceMaitrisee.md) — Synthèse complète du cours
- [`Claude Cowork/etaia_github_io_*.md`](Claude%20Cowork/) — Pages du challenge (dataset, évaluation, FAQ, getting started)
- [`GEMINI.md`](GEMINI.md) — Plan d'exécution du TP par phases (Infrastructure → Architecture → Datasets → KPIs → Artefacts)
