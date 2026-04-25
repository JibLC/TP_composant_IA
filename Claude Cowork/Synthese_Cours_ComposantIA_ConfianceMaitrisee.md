# Composants IA à Confiance Maîtrisée
**Mastère Spécialisé IA de Confiance — Confiance.ai / IRT SystemX, 2025**  
*Intervenant : Loïc CANTAT*

---

## Plan du cours

1. [Qu'est-ce qu'une IA de confiance ?](#1-quest-ce-quune-ia-de-confiance)
2. [Composant IA vs Modèle ML](#2-composant-ia-vs-modèle-ml)
3. [Méthodologie End-to-End](#3-méthodologie-end-to-end)
4. [Cycle de vie du composant IA](#4-cycle-de-vie-du-composant-ia)
5. [La méthodologie (D)RUM](#5-la-méthodologie-drum)
   - [Robustesse](#robustesse)
   - [Uncertainty Quantification (UQ)](#uncertainty-quantification-uq)
   - [Monitoring](#monitoring)
6. [Explainability](#6-explainability)
7. [Embeddability](#7-embeddability)
8. [Water Marking](#8-water-marking)
9. [Des métriques aux artefacts](#9-des-métriques-aux-artefacts)
10. [TP : Proposer un composant IA](#10-tp--proposer-un-composant-ia)

---

## 1. Qu'est-ce qu'une IA de confiance ?

La confiance dans un système IA ne se résume pas à sa précision. Des cadres réglementaires définissent des exigences multidimensionnelles :

### Exemple EASA (aviation)
La confiance repose sur trois piliers :
- **Caractérisation de l'application IA** : fonction, concept d'opération, analyse fonctionnelle, classification
- **Évaluation de la sécurité ML** : évaluation système, sécurité de l'information
- **Évaluation éthique** : supervision humaine, robustesse technique, vie privée, transparence, équité, redevabilité

### Exemple ALTAI (Union Européenne)
Sept axes de confiance :
- Human Agency and Autonomy
- Technical robustness and safety
- Privacy and data governance
- Transparency
- Diversity, non-discrimination and fairness
- Societal and environmental well-being
- Accountability

### Vision Confiance.ai (2025)
Une approche End-to-End structurée en 3 blocs :

```
Trustworthy Characteristics  →  AI Component Trust Assessment  →  AI Trustworthiness Assessment
  (identification des             (métriques & KPIs,                 (agrégation, assurance case,
   attributs de confiance)         évaluation des attributs)          justification qualité ODD)
```

> **Idée clé** : la confiance émerge de *trade-offs multidimensionnels* contextualisant les différentes étapes du cycle de vie. Elle ne peut pas se réduire à un score unique global.

---

## 2. Composant IA vs Modèle ML

### Un composant logiciel classique
```
Exigence système → [Langage + Code source + Compilateur + Hardware] → Binaire → Composant
```

### Un composant IA (AIC)
> **"Data make algorithms"**

Un composant IA n'est **pas** seulement un modèle ML. C'est un ensemble :

| Élément | Description |
|---------|-------------|
| **Un ou plusieurs modèles ML** | Modèle principal + modèles auxiliaires |
| **Données** | Datasets d'entraînement, validation, test (multiples) |
| **Règles de décision et calibrations** | Seuils, post-traitements |
| **Logiciels de pré/post-traitement** | Pipeline complet |

**Sorties du composant IA :**
- En opération : la **sortie fonctionnelle attendue** (ex : "OK" / "NOK")
- Des **métriques complémentaires** pour surveiller le comportement du composant

### Atomicité (AICs)
> Modifier *un seul constituant* (ajouter des données, changer une calibration…) **invalide généralement la majorité des démonstrations de confiance** effectuées sur la version précédente.

### Architecture complète du composant IA

```
[AIC Design Calibration]
        ↓
[Preprocessor] → [Backbone] → [Latent Space] → [Predictor]      → Functional Output
                                              → [UQ Quantifier]  → Trust Artefacts
                                              → [OOD Detector]   → Prediction Status
                              → [Online Monitoring]
```

---

## 3. Méthodologie End-to-End

Le développement suit un **cycle en V étendu** avec 4 niveaux imbriqués :

```
OPÉRATIONNEL ──────────────────────────────────────────────── Opérationnel
  SYSTÈME ──────────────────────────────────────── Système
    ML ──────────────────────────────── ML
      LOGICIEL ──────────────── Logiciel
               ↓ DATA ENGINEERING (tout au long) ↑
```

### Les 4 scopes

| Scope | Acteur | Objectif | Domaine de conception | Données |
|-------|--------|----------|----------------------|---------|
| **Opérationnel** | Ingénieur opérationnel | Objectif d'automatisation | ODD (Operational Design Domain) | Observations empiriques |
| **Système** | Ingénieur système | Architecture du composant IA | System design domain | Données collectées à qualifier |
| **ML** | Data scientist | Combinaison de fonctions mathématiques | Task-relevant modeling space | Sous-espace du domaine de modélisation |
| **Logiciel** | Dev / ML Engineer | Composant IA intégré | Couverture fonctionnelle logicielle | API & Data-flow |

---

## 4. Cycle de vie du composant IA

```
Phase DESIGN                              Phase OPÉRATION
┌─────────────────────────────┐           ┌──────────────────────────────────┐
│ Collecter, nettoyer,        │           │ Surveiller le comportement        │
│ structurer les données  ──► │ ──────►   │ avec des données live             │
│                             │  CALIB    │ et des insights humains           │
│ Entraîner, optimiser,       │ ◄──────   │                                   │
│ valider le modèle           │           │ → via les mêmes métriques et      │
└─────────────────────────────┘           │   artefacts qu'en phase design    │
                                          └──────────────────────────────────┘
                                                          ↓ DÉCISION
```

> **Trade-offs Lifecycle-Aware** : la confiance (*trustworthiness*) est multidimensionnelle et doit être évaluée de manière contextuelle à chaque étape du cycle de vie.

---

## 5. La méthodologie (D)RUM

Le cœur technique du cours. Trois propriétés **indissociables**, représentées comme un nœud borroméen :

```
        Robustness (R)
           🔴
          / \
         /   \
    🔵 ─────── 🟢
   UQ (U)   Monitoring (M)
        [RUM]
```

> Si vous retirez l'un des trois anneaux, les deux autres se séparent. C'est l'interdépendance.

---

### Robustesse

> **Définition** : capacité d'un modèle ML à maintenir ses performances face à des **variations ou perturbations** des données d'entrée ou du modèle lui-même.

**Question clé** : *"How resilient is the model's performance when faced with different conditions or perturbations?"*

**Techniques** :
- Regularization methods
- Data augmentation
- Adversarial training (ex : DANN — Domain-Adversarial Neural Network, Ganin et al. 2016)
- Model architecture design

**Exemple concret** : un modèle entraîné de jour et testé de nuit → les détections s'emballent (faux positifs).

**Rôle de la robustesse pour M & UQ** :
- Les modèles robustes gèrent mieux les incertitudes dans les données
- Les mesures de robustesse contribuent à de meilleurs modules UQ et de meilleurs outils de monitoring

---

### Uncertainty Quantification (UQ)

> **Définition** : évaluer la confiance ou l'incertitude associée aux prédictions d'un modèle ML.

**Deux types d'incertitude** :
- **Aléatoire** (*aleatoric*) : inhérente aux données, irréductible (bruit naturel)
- **Épistémique** (*epistemic*) : due au manque de connaissance du modèle, réductible avec plus de données

**Question clé** : *"How well does the model know what it doesn't know?"*

**Techniques** :
- Méthodes bayésiennes
- Dropout à l'inférence (Monte Carlo Dropout)
- Ensembles de modèles
- **Conformal Prediction** ← approche phare du cours

#### Conformal Prediction

Méthodes **distribution-free**, **model-agnostic**, **non-asymptotiques** :
- Applicable à tout modèle black-box, faible coût en post-traitement
- Garantit une **validité marginale** si les données sont i.i.d. (ou échangeables)
- La couverture conditionnelle dépend du modèle et de la mesure de non-conformité

**Exemple** : intervalles de prédiction à 90% sur une série temporelle de gaz.

#### Bibliothèque PUNCC
```python
from deel.puncc.regression import SplitCP

alpha = .1  # couverture cible = 90%
split_cp = SplitCP(regr)
split_cp.fit(X_fit, y_fit, X_calib, y_calib)
y_pred, y_pred_lower, y_pred_upper = split_cp.predict(X_test, alpha=alpha)
```

**Rôle de l'UQ pour R & M** :
- Comprendre l'incertitude guide le développement de modèles plus robustes
- Des intervalles bien calibrés fournissent des outils de monitoring précieux
- Sans UQ : *"supervisors will overlook when models don't know what they do not know"*

---

### Monitoring

> **Définition** : suivi et évaluation continus des performances et du comportement d'un modèle ML dans le temps.

**Question clé** : *"Is the model behaving as expected, and is its performance consistent with the intended objectives?"*

**Techniques** :
- Suivi de métriques de performance
- Détection de concept drift
- Détection d'anomalies
- Méthodes d'explicabilité

#### Monitoring Multi-Timescale

```
         t_x (maintenant)
─────────────┬──────────────►
             │
  ◄──────────┤──────────►
  Near-Past  │ Near-Future
  (NPM = ∫)  │ (NFM = ∂)
             △ PTM
```

| Moniteur | Symbole | Ce qu'il détecte |
|----------|---------|-----------------|
| **Near-Past Monitoring** (NPM) | ∫ | Dérives progressives (intégrale) |
| **Present-Time Monitoring** (PTM) | Δ | Anomalies instantanées |
| **Near-Future Monitoring** (NFM) | ∂ | Tendances préoccupantes (dérivée) |

**Principe 1 — Completeness-by-design** : la fonction de monitoring doit démontrer une complétude dans la détection des anomalies. Les trois moniteurs ensemble couvrent tous les types d'anomalies temporelles.

#### ODD et Out-of-ODD (OODD)

Le monitoring permet de définir et surveiller l'**ODD** (Operational Design Domain) :

```
        Specified ODD       ∩        Model ODD
┌──────────────────────────────────────────────┐
│  Need of domain    │  In-Distribution        │
│  adaptation        │  ┌─────────────────┐    │
│  (SODD-targeted)   │  │ Adversarial Rob.│    │
│                    │  │ Common OOD Rob. │    │
│  Known lack of     │  └─────────────────┘    │
│  generalisation    │                         │
└──────────────────────────────────────────────┘
```

**Rôle du Monitoring pour R & UQ** :
- Sans monitoring : feedback temps-réel absent, calibration imprécise, anomalies non détectées
- Le monitoring connecte la robustesse et l'UQ aux données opérationnelles réelles

---

## 6. Explainability

Rendre les décisions du modèle **compréhensibles** pour les humains.

**Usage dans le cas concret (soudures)** : permettre à l'opérateur de comprendre *pourquoi* le modèle classe une soudure comme NOK, pour gagner du temps lors de l'inspection et valider la décision.

---

## 7. Embeddability

Capacité à intégrer le composant IA dans un système plus large, avec les contraintes hardware/software associées.

---

## 8. Water Marking

> **Définition** : un *watermark* de modèle est un changement inhabituel dans les **paramètres ou le comportement** du modèle, connu uniquement du propriétaire et indétectable pour les autres.

**Objectif** : protéger la propriété intellectuelle des réseaux de neurones profonds.

### Exigences d'un bon watermark
- Ne pas trop dégrader les performances du réseau
- Être robuste aux modifications du réseau (fine-tuning, pruning...)
- Être clairement associé à l'identité du propriétaire

### Trois types de watermarks (Zhang et al., 2018)

| Type | Contenu | Exemple |
|------|---------|---------|
| **WM Content** | Contenu significatif intégré dans les données d'entraînement | Logo "TEST" sur l'image |
| **WM Noise** | Bruit pré-spécifié généré par une clé secrète | Pixels colorés aléatoires selon clé secrète |
| **WM Unrelated** | Images non liées à la tâche, labelisées spécifiquement | Image d'avion → classe "voiture" |

**Méthode** : intégration lors de l'entraînement (*backdooring*). Le propriétaire peut vérifier l'ownership en testant si le modèle répond correctement au trigger set.

---

## 9. Des métriques aux artefacts

### Architecture complète du composant (récapitulatif)

```
Phase OPÉRATION :
[Sample] → [Preprocessor] → [Backbone] → [Latent Space] → [Predictor]
                                                          → [UQ Quantifier]   → Metrics Assembly
                                                          → [OOD Detector]    → Functional Output
                              → [Online Monitoring]                            → Trust Artefacts

Phase DÉVELOPPEMENT :
[Historical Data] → split → [Preprocessor] → [Backbone (Freeze)] → [Latent Sp. (Finetune)] → [Predictor (Train)]
                                                                                               → [UQ & OOD Calibration]
                                                                                               → [Off/On-line Monitoring Calibration]
```

### Agrégation des métriques

Les métriques individuelles (performance, UQ, robustesse, OOD...) sont **agrégées** en artefacts synthétiques.

**Opérateurs d'agrégation** — fonctions mathématiques vérifiant des propriétés formelles :
- Conditions aux limites : Aggreg(0,...,0)=0 et Aggreg(1,...,1)=1
- Monotonicité non décroissante
- Continuité, associativité, symétrie
- Idempotence, compensation, contre-balancement...

**Représentations visuelles** :
- Radar Chart (multi-critères)
- VDE (Visual representation) : tableau de bord avec indicateurs colorés par critère (Transparency, Accountability, Privacy, Fairness, Reliability...)

> **Important** : l'agrégation reste très complexe et biaisée. Il n'existe pas de solution universelle — la méthode doit être spécialisée par **classe d'usage**.

### Classes d'usage

Chaque classe d'usage (Industrie 4.0, Défense, etc.) partage :
- Le type de données manipulées
- La fonction réalisée
- L'interaction utilisateur
- La paramétrisation de la performance opérationnelle
- Le pattern de mise à jour

→ Un **AI Blueprint** est conçu pour chaque classe.

---

## 10. TP : Proposer un composant IA

### Contexte : Challenge Confiance — Détection de qualité de soudures Renault

**Problème** : classification d'images de soudures industrielles en 3 classes :
- ✅ **OK** — soudure conforme
- ❌ **NOK** (RETOUCHE) — soudure à retoucher
- ❓ **Unknown** — hors ODD

**Dataset** : Renault Welding (open source) — ~1500 images, Cordon C19, 80.3% OK / 19.7% RETOUCHE.

**Ressources** :
- https://github.com/etaia/Welding-Quality-Detection-Challenge
- https://etaia.github.io/Welding-Quality-Detection-Challenge/
- https://github.com/etaia/reference-environment

### Critères d'évaluation du composant soumis

| Critère | Description |
|---------|-------------|
| **Operational cost metrics** | Matrice de confusion + matrice de coût non-symétrique (contraintes opérationnelles) |
| **Uncertainty metrics** | Capacité à utiliser l'incertitude pour améliorer la fiabilité |
| **Robustness metrics** | Invariance aux perturbations empiriques (flou, luminosité, rotation, translation) |
| **Monitoring metrics** | Capacité à détecter si l'entrée est dans l'ODD |
| **Explainability metrics** | Capacité à fournir une explication pour aider l'opérateur |

### Contenu du TP

Le TP comporte **4 livrables** :

#### Livrable 1 — Architecture du composant IA

**Ce qu'on attend** :
- Le/les modèles ML envisagés
- Les composants logiciels à ajouter (UQ, OOD, monitoring...)
- Une définition précise des entrées/sorties

**Schémas à produire** :
- ① Architecture du composant en **opération**
- ② Architecture du composant en **entraînement**
- ③ Architecture du composant en **évaluation**
- Un bloc markdown de description pour chaque constituant
- Le code Python définissant l'interface (boîte noire retournant du random)

#### Livrable 2 — Datasets

**Ce qu'on attend** :
- Une description de comment constituer chaque dataset (avec paramètres)
  - *Exemple* : dataset de flou (blur level 0 à 10)
  - *Exemple* : dataset de luminosité (brightness level 0 à 200)
- Identification des métadonnées associées aux échantillons
- Le code Python de l'interface qui génère/altère/sélectionne des échantillons

**Format** :
- Un bloc MD pour décrire comment constituer chaque dataset
- Un bloc MD pour décrire l'usage prévu de chaque dataset
- Un bloc de code pour l'interface de création

#### Livrable 3 — KPIs

**Ce qu'on attend** :
- Description du KPI construit (ex : robustesse du modèle au flash éblouissant)
- Identification des métadonnées associées au KPI
- Objectif du KPI dans la démonstration de confiance
- Dans quelle(s) phase(s) ce KPI sera utilisé (dataset construction / entraînement / évaluation / opération)
- Échantillon du KPI attendu

**Format** :
- Un bloc MD pour décrire comment constituer chaque KPI
- Un bloc MD pour décrire l'usage prévu de chaque KPI
- Un bloc de code pour l'interface de calcul

#### Livrable 4 — Artefacts

**Ce qu'on attend** :
- L'agrégation/filtrage/représentation des KPIs utilisés
  - *Exemple* : robustesse du modèle au flash par type de soudure → bar graph
- Identification de la méthode d'agrégation/contextualisation
- À qui est destiné l'artefact, pour quel objectif
- Dans quelle(s) phase(s) cet artefact est utilisé

**Format** :
- Un bloc MD pour décrire comment constituer chaque artefact
- Un bloc MD pour décrire l'usage prévu de chaque artefact
- Une représentation visuelle envisagée

### Forme du TP

**Rendu** : un **repository Git** avec historique des commits (travail en binôme)

```
repository/
├── Docs/
│   ├── Architecture/
│   │   ├── operation.md       ← schéma en opération
│   │   ├── training.md        ← schéma en entraînement
│   │   └── evaluation.md      ← schéma en évaluation
│   ├── Datasets/
│   │   └── dataset_*.md       ← un fichier par dataset
│   ├── KPI/
│   │   └── kpi_*.md           ← un fichier par KPI
│   └── Artefacts/
│       └── artefact_*.md      ← un fichier par artefact
└── Interfaces/
    └── *.py                   ← code Python des interfaces
```

**Outils recommandés** :
- `mkdocs` ou `vitepress` pour générer un site de documentation
- `mermaid` pour les schémas intégrés dans les markdown
- `drawio` pour la simplicité de partage via git

### Critères d'évaluation du TP

| Critère | Ce qui est évalué |
|---------|------------------|
| **Cohérence avec le cas d'usage** | Le composant répond bien au problème de soudures Renault |
| **Cohérence entre les étapes** | Architecture, datasets, KPIs et artefacts sont alignés |
| **Description des constituants** | Chaque module est clairement décrit |
| **Validité des entrées/sorties** | Les interfaces sont logiques et cohérentes |
| **Originalité** | Approche innovante ou créative |

---

## Annexe — Références et ressources

| Ressource | Description |
|-----------|-------------|
| **PUNCC library** | `pip install puncc` — Conformal Prediction open-source |
| **NeuralDE library** | Adaptation d'images test-time (DeSnow, Derain, Deblur...) |
| **Confiance.ai taxonomy** | Taxonomie des attributs de confiance (Batch 2, 2022) |
| **White paper Confiance.ai** | Vision globale de l'IA de confiance |
| **Zhang et al. 2018** | Watermarking des réseaux de neurones par backdooring |
| **Ganin et al. JMLR'16** | DANN — Domain-Adversarial Training |

---

*Document généré à partir du cours MS_ComposantIA_ConfianceMaitrisé_2026.pdf*  
*Confiance.ai© — Toute communication, reproduction, publication, même partielle, est interdite sauf autorisation écrite.*
