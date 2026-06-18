![Python](https://img.shields.io/badge/python-3.11-blue?logo=python&logoColor=white)
![Jupyter](https://img.shields.io/badge/jupyter-notebook-F37626?logo=jupyter&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-data%20processing-150458?logo=pandas&logoColor=white)
![Scikit-learn](https://img.shields.io/badge/scikit--learn-ML-F7931E?logo=scikitlearn&logoColor=white)
![Streamlit](https://img.shields.io/badge/streamlit-app-FF4B4B?logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/plotly-data%20viz-3F4F75?logo=plotly&logoColor=white)
![Statut](https://img.shields.io/badge/statut-en%20cours-yellow)
![Projet](https://img.shields.io/badge/projet-académique-blueviolet)
![YNOV](https://img.shields.io/badge/YNOV-Bachelor%203-002B5C)

# Performance sportive aux Jeux Olympiques de Los Angeles 2028

> Projet fil rouge — YNOV Campus Paris, Bachelor 3 Data & IA
> Sujet 3 : *Performances sportives pour les JO 2028 à Los Angeles* — startup fictive **YPerf**

## Sommaire

- [Contexte du projet](#contexte-du-projet)
- [Problématique](#problématique)
- [Public visé](#public-visé)
- [Jeux de données utilisés](#jeux-de-données-utilisés)
- [Préparation et nettoyage des données](#préparation-et-nettoyage-des-données)
- [Analyse exploratoire](#analyse-exploratoire)
- [Analyse des générations montantes](#analyse-des-générations-montantes)
- [Modélisation prédictive](#modélisation-prédictive)
- [Application de data storytelling](#application-de-data-storytelling)
- [Structure du projet](#structure-du-projet)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Livrables](#livrables)
- [Auteur](#auteur)

---

## Contexte du projet

Les Jeux Olympiques constituent l'un des événements sportifs les plus suivis au monde. Les performances des nations y sont souvent interprétées comme des indicateurs de leur puissance sportive, de leurs investissements dans le sport de haut niveau et de leur rayonnement international.

Dans ce contexte, ce projet vise à exploiter les données historiques des Jeux Olympiques afin d'estimer les performances futures des pays lors des Jeux Olympiques de Los Angeles 2028.

---

## Problématique

**Combien de médailles un pays est-il susceptible de remporter dans chaque sport aux Jeux Olympiques de Los Angeles 2028 en se basant sur ses performances lors des éditions précédentes ?**

Dans un second temps, lorsque l'obtention d'une médaille est prédite, nous cherchons également à déterminer le type de médaille susceptible d'être remporté (or, argent ou bronze).

---

## Public visé

Cette étude peut intéresser plusieurs acteurs :

**Comités olympiques nationaux** — Les résultats peuvent aider à identifier les disciplines dans lesquelles un pays possède les meilleures perspectives de réussite.

**Décideurs publics** — Les gouvernements et institutions sportives peuvent utiliser ces analyses pour orienter leurs investissements vers les disciplines les plus prometteuses.

**Sponsors et partenaires** — Les entreprises investissant dans le sport de haut niveau peuvent identifier les pays et disciplines présentant le plus fort potentiel de visibilité lors des Jeux Olympiques 2028.

**Analystes sportifs** — Les modèles développés permettent d'étudier les dynamiques de performance des nations sur plusieurs décennies.

---

## Jeux de données utilisés

### Dataset principal

- Dataset Kaggle – Jeux Olympiques de Paris 2024
- Dataset Kaggle – Jeux Olympiques de Tokyo 2020

Ces deux datasets constituent la base principale de notre étude car ils contiennent les données les plus récentes et les plus pertinentes pour anticiper les performances futures.

### Dataset historique écarté

Nous avions initialement retenu le dataset **120 Years of Olympic History (1896–2016)**. Ce dataset présente l'avantage de couvrir une longue période historique. Toutefois, plusieurs incohérences importantes ont conduit à son abandon comme source principale.

**Problème n°1 : médailles retirées** — Des athlètes ayant été ultérieurement disqualifiés pour dopage ou fraude apparaissent toujours comme médaillés.

**Problème n°2 : sports collectifs** — Les épreuves collectives sont comptabilisées comme si chaque athlète avait remporté une médaille individuelle. Par exemple, une équipe de football composée de 18 joueurs recevant une médaille d'or est comptabilisée comme 18 médailles au lieu d'une seule. Cette erreur entraîne une forte surestimation des résultats de nombreux pays : la Russie apparaît avec plus de 1000 médailles dans ce dataset alors que les statistiques officielles en recensent environ 550.

Compte tenu de ces incohérences structurelles et de l'absence d'indicateur permettant d'identifier facilement les épreuves collectives, ce dataset a été écarté au profit de sources plus fiables.

---

## Préparation et nettoyage des données

### Gestion des pays disparus

Les entités géopolitiques aujourd'hui disparues — URSS, RDA, Tchécoslovaquie, Yougoslavie — ont été conservées dans les analyses descriptives.

**Justification** : ces pays représentent une réalité historique propre. Fusionner leurs résultats avec ceux des États actuels reviendrait à modifier artificiellement l'histoire olympique. Par exemple, les performances de l'URSS ne peuvent être attribuées intégralement à la Russie puisque plusieurs États actuels sont héritiers de cette ancienne nation.

Les pays disparus sont donc **conservés** pour les visualisations, les statistiques historiques et l'analyse des tendances passées. Ils sont en revanche **exclus** de la modélisation prédictive, des calculs de progression et des prévisions pour 2028 — seuls les pays existant actuellement peuvent participer aux Jeux Olympiques de Los Angeles 2028.

### Gestion des athlètes disqualifiés

Afin d'obtenir des données cohérentes avec les résultats officiels actuels, les athlètes ayant perdu leurs médailles à la suite de sanctions (dopage, fraude, infractions au règlement olympique) ont été retirés du dataset. Les informations ont été vérifiées à partir des listes de médailles retirées publiées par le Comité International Olympique et recoupées avec les références disponibles sur Wikipédia. L'objectif est de travailler sur les résultats officiellement reconnus aujourd'hui.

---

## Analyse exploratoire

L'analyse exploratoire vise à identifier les principales tendances historiques :

- répartition des médailles par pays ;
- répartition des médailles par sport ;
- évolution des performances dans le temps ;
- comparaison des spécialisations sportives des pays ;
- identification des pays dominants ;
- identification des disciplines les plus compétitives.

Ces analyses permettent de construire le profil sportif de chaque pays avant la phase de modélisation.

---

## Analyse des générations montantes

Nous avons envisagé d'intégrer l'âge des athlètes afin d'identifier les nouvelles générations susceptibles de performer en 2028. Pour cela, une fusion a été testée avec le dataset Kaggle **120 Years of Olympic History**, qui contient notamment l'âge des athlètes. Cette approche a finalement été abandonnée.

**Première limite** : le dataset s'arrête aux Jeux de Rio 2016. Il ne contient donc aucune information sur Tokyo 2020 ni Paris 2024 — or ces deux éditions sont les plus pertinentes pour anticiper les performances de 2028.

**Deuxième limite** : la fusion entre les datasets produisait de nombreuses erreurs d'association, en raison des homonymes, des différences d'écriture et de l'absence d'identifiant unique partagé. La qualité de la jointure n'était pas suffisamment fiable.

**Solution retenue** : un indicateur indirect basé sur la récence d'apparition des athlètes dans les palmarès olympiques. Cet indicateur permet d'identifier les profils émergents tout en restant cohérent avec les données disponibles.

---

## Modélisation prédictive

L'objectif principal est de prédire le nombre de médailles qu'un pays peut remporter dans chaque discipline lors des Jeux Olympiques de Los Angeles 2028. Cette tâche correspond à un **problème de régression**.

Les modèles étudiés sont :
- Régression Linéaire ;
- Random Forest Regressor ;
- Gradient Boosting Regressor.

Les performances sont évaluées à l'aide des métriques MAE, RMSE et R².

Dans un second temps, une tâche de **classification** est réalisée afin de prédire le type de médaille obtenu (Or, Argent, Bronze), avec les modèles suivants :
- Régression Logistique ;
- Random Forest Classifier.

L'interprétation des variables importantes permet également d'identifier les facteurs ayant le plus d'influence sur les performances olympiques futures.

---

## Application de data storytelling

Une application **Streamlit** interactive permet d'explorer l'ensemble des résultats sans avoir à relancer les notebooks :

| Onglet | Contenu |
|---|---|
|  Carte des médailles | Carte choroplèthe filtrable par période et discipline |
|  Pays & disciplines | Évolution temporelle, heatmap pays × édition, courbes cumulées |
|  Progression | Pays en progression / en déclin sur les 3 dernières éditions |
|  Athlètes | Top 5 par discipline, trajectoire dans le temps, côte des athlètes |
|  Records | Frise chronologique des records olympiques |
|  Prédictions 2028 | Projections par pays/discipline, comparaison des modèles, détail Or/Argent/Bronze |
|  Avis | Avis communautaires sur athlètes, pays ou disciplines |

---

## Structure du projet

```
yperf-jo2028/
├── fil_rouge.ipynb                 # Notebook d'exploration et de nettoyage
├── modelisation_JO2028.ipynb       # Notebook de modélisation prédictive
├── all_olympic_medalists.csv       # Données brutes (médailles)
├── records_olympiques.csv          # Données brutes (records)
├── dataset_final_clean.csv         # Dataset nettoyé (généré par fil_rouge.ipynb)
├── graphiques/                     # Exports graphiques (PNG, HTML)
├── data/
│   └── processed/
│       ├── predictions_2028.csv
│       ├── cotes_athletes.csv
│       ├── comparaison_modeles.csv
│       └── avis_utilisateurs.csv   # Généré à l'usage par l'application
├── app/
│   ├── app.py                      # Application Streamlit
│   └── model.pkl                   # Modèle entraîné (généré par modelisation_JO2028.ipynb)
├── requirements.txt
└── README.md
```

---

## Installation

```bash
# 1. Cloner le dépôt
git clone https://github.com/L-em-hash/PREDICTION-JO-2028-ML.git
cd PREDICTION-JO-2028-ML

# 2. Créer un environnement virtuel (recommandé)
python -m venv venv
source venv/bin/activate        # Windows : venv\Scripts\activate

# 3. Installer les dépendances
pip install -r requirements.txt
```

---

## Utilisation

**Étape 1 — Exploration et nettoyage des données**
Exécuter `fil_rouge.ipynb` de bout en bout (Kernel → Restart & Run All). Ce notebook génère `dataset_final_clean.csv` à la racine du projet.

**Étape 2 — Modélisation prédictive**
Exécuter `modelisation_JO2028.ipynb` de bout en bout. Ce notebook entraîne les modèles et génère `app/model.pkl` ainsi que les fichiers de `data/processed/`.

**Étape 3 — Lancer l'application**
```bash
streamlit run app/app.py
```
L'application s'ouvre automatiquement dans le navigateur à l'adresse `http://localhost:8501`.

---

## Livrables

- [x] Dépôt Git avec code et documentation
- [x] Jupyter Notebook retraçant la démarche et les analyses
- [x] Application de data storytelling déployée localement
- [x] Documentation technique et manuel d'installation (ce README)

---

## Auteur

**LAWSON 6 LARTEGO Emmanuella & DOTSU Olympe** — Bachelor 3 Data & IA, YNOV Campus Paris
Projet réalisé dans le cadre de l'UF Spécialité IA & Data
