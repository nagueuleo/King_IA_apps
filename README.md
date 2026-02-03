# Détection de la pneumonie par apprentissage par transfert

* La pneumonie est une maladie respiratoire infectieuse et potentiellement mortelle causée par des bactéries, des champignons ou un virus qui infectent les alvéoles pulmonaires, les remplissant de liquide ou de pus.

* La radiographie thoracique est la méthode courante de diagnostic de la pneumonie, mais son interprétation requiert l'expertise d'un médecin. Cette méthode de détection complexe peut entraîner des décès dus à des erreurs de diagnostic et de traitement.

* Grâce à la puissance de calcul croissante, le développement d'un système automatisé de détection et de traitement de la pneumonie est désormais possible, notamment dans les zones reculées où l'accès aux soins est limité.

* Dans cette application web, nous avons utilisé le modèle d'apprentissage par transfert VGG16 pour la prédiction.

Cette application web est créée et déployée sur Streamlit.

## 💡 Comment utiliser notre application web

![alt text]("./pn.png")

## 🚀 Installation et Démarrage

### Prérequis
- Python 3.7 ou supérieur
- Git (pour cloner le projet)
- Un gestionnaire de paquets Python (pip)

### Étape 1 : Cloner le projet

```bash
# Cloner le dépôt
git clone https://github.com/nagueuleo/King_IA_apps.git

# Accéder au répertoire du projet
cd King_IA_apps
```

### Étape 2 : Créer un environnement virtuel (optionnel mais recommandé)

```bash
# Sur Windows
python -m venv pneumonia

# Activer l'environnement virtuel
pneumonia\Scripts\activate

# Sur macOS/Linux
python3 -m venv pneumonia
source pneumonia/bin/activate
```

### Étape 3 : Installer les dépendances

```bash
# Installer tous les packages requis
pip install -r requirements.txt
```

### Étape 4 : Lancer l'application

```bash
# Démarrer l'application Streamlit
streamlit run app.py
```

L'application s'ouvrira automatiquement dans votre navigateur par défaut à l'adresse `http://localhost:8501`

### Utilisation de l'application

1. **Télécharger une image** : Cliquez sur la zone de téléchargement pour sélectionner une radiographie thoracique (JPG ou PNG)
2. **Analyse** : L'application analyse automatiquement l'image
3. **Résultats** : Consultez les résultats avec le niveau de confiance
   - 🟢 **IMAGE NORMALE** : Aucune pneumonie détectée
   - 🔴 **PNEUMONIE DÉTECTÉE** : Pneumonie identifiée (bactérienne ou virale)
## ⏳ Données

![Exemples illustratifs de radiographies thoraciques chez des patients atteints de pneumonie](https://i.imgur.com/jZqpV51.png)

La radiographie thoracique normale (panneau de gauche) montre des poumons clairs, sans aucune opacité anormale. La pneumonie bactérienne (au centre) présente généralement une condensation lobaire focale, ici au niveau du lobe supérieur droit (flèches blanches), tandis que la pneumonie virale (à droite) se manifeste par un aspect interstitiel plus diffus dans les deux poumons.

L'ensemble de données utilisé ici est stocké sous forme de fichiers .jpg dans deux dossiers distincts : « Normal », contenant des radiographies thoraciques normales, et « Pneumonie », contenant des radiographies de pneumonie.

Les radiographies thoraciques (incidence antéro-postérieure) ont été sélectionnées à partir de cohortes rétrospectives de patients pédiatriques âgés de **un à cinq ans** du **Centre médical pour femmes et enfants de Guangzhou**. Toutes les radiographies thoraciques ont été réalisées dans le cadre des soins cliniques de routine des patients.

Pour l'analyse des images radiographiques thoraciques, toutes les radiographies ont d'abord fait l'objet d'un contrôle qualité, les clichés de mauvaise qualité ou illisibles étant éliminés. Les diagnostics ont ensuite été évalués par deux médecins experts avant d'être validés pour l'entraînement du système d'IA. Afin de pallier d'éventuelles erreurs d'évaluation, l'ensemble d'évaluation a également été vérifié par un troisième expert.



## � Structure du projet

```
Pneumonia-Detection/
├── app.py                          # Application principale Streamlit
├── params.yaml                     # Paramètres de configuration
├── requirements.txt                # Dépendances Python
├── template.py                     # Template de projet
├── README.md                       # Documentation
│
├── models/
│   └── model.h5                    # Modèle pré-entraîné (VGG16)
│
├── notebooks/                      # Notebooks Jupyter pour l'analyse
│
├── samples/                        # Exemples d'images pour le test
│   ├── train/
│   │   ├── NORMAL/                 # Images normales d'entraînement
│   │   └── PNEUMONIA/              # Images de pneumonie d'entraînement
│   └── test/
│       ├── NORMAL/                 # Images normales de test
│       └── PNEUMONIA/              # Images de pneumonie de test
│
├── stages/                         # Scripts Python pour les différentes étapes
│   ├── data_preprocessing.py       # Prétraitement des données
│   ├── model_training.py           # Entraînement du modèle
│   └── model_evaluation.py         # Évaluation du modèle
│
├── reports/                        # Rapports et résultats
│   ├── data.json                   # Données brutes
│   ├── metrics/                    # Métriques du modèle
│   │   ├── metric.json
│   │   ├── params.json
│   │   └── scores.json
│   └── model_summary/              # Résumés du modèle
│
└── pneumonia/                      # Environnement virtuel Python
    ├── pyvenv.cfg
    ├── Include/
    ├── Lib/
    ├── Scripts/
    └── share/
```

## 📁 Structure du projet

### Fichiers principaux
- **app.py** : Application web Streamlit pour la détection de pneumonie
- **params.yaml** : Configuration des paramètres du projet
- **requirements.txt** : Dépendances Python nécessaires
- **models/model.h5** : Modèle VGG16 pré-entraîné

### Dossiers importants
- **samples/** : Images d'exemples pour entraînement et test
- **stages/** : Scripts pour chaque étape du pipeline ML
- **reports/** : Métriques, scores et résumés du modèle
- **pneumonia/** : Environnement virtuel Python

## 📁 Structure du projet



### Pipelines d'apprentissage automatique à construire

1. Collecte des données - Directement depuis Kaggle

2. Validation des données - Facultatif

3. Prétraitement des données / Ingénierie des caractéristiques - Terminé

4. Entraînement du modèle - Terminé

5. Évaluation du modèle - Terminé

6. Création de l'application web - Terminé

7. Tests - **Non terminé**

### Scripts automatiques à construire

1. Déploiement CI/CD - Non terminé

2. Supervision du modèle - Non terminé

3. Scripts de réentraînement du modèle - Non terminé

### Artefacts du modèle à stocker

#### Pour le modèle d'apprentissage automatique (toutes les expériences)

1. Paramètres du modèle - Terminé

2. Résumé du modèle - Terminé

3. Métriques de performance du modèle - Terminé

4. Emplacement du modèle et bibliothèques utilisées Utilisé - Terminé

#### Données

1. Schéma des données - Facultatif

2. Emplacements de collecte des données (possibilité de plusieurs emplacements) - Site web Kaggle

3. Emplacement de stockage des données - Système local

4. Caractéristiques des données, distributions des caractéristiques, étiquettes des caractéristiques, etc. - Facultatif

## 🖥️ Bibliothèques utilisées

* TensorFlow
* Keras

* Scikit-learn
* Streamlit

## 🧑🏼‍💻 Contributeurs

1. Lionel NAGUEU