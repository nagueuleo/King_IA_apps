# 🫁 KING IA Apps - Détection de Pneumonie

## ✨ Nouvelles Fonctionnalités

### 📊 Matrice de Confusion et Rapport de Classification

Votre application affiche maintenant automatiquement :

1. **📈 Matrice de Confusion** - Visualisation heatmap montrant :
   - Les vrais positifs (diagonal)
   - Les faux positifs et négatifs
   - Les prédictions correctes et incorrectes par classe

2. **📋 Rapport de Classification** - Tableau avec :
   - **Précision** : Exactitude des prédictions positives
   - **Rappel** : Couverture des vrais cas positifs
   - **F1-Score** : Équilibre entre précision et rappel
   - **Statistiques globales moyennes**

## 🚀 Installation et Lancement

### 1. Installer les dépendances requises

```bash
# Option 1 : Utiliser le script automatique
python install_dependencies.py

# Option 2 : Installation manuelle
pip install -r requirements.txt
```

### 2. Lancer l'application

```bash
streamlit run app_new.py
```

L'application s'ouvrira automatiquement dans votre navigateur à `http://localhost:8501`

## 📖 Comment Utiliser

### Affichage des Métriques

1. Allez dans l'**onglet "Analyse"** 
2. Téléchargez une radiographie thoracique (JPG ou PNG)
3. Le modèle effectue la prédiction
4. **Défilez vers le bas** pour voir la section **"📈 Métriques d'évaluation du modèle"**
5. Vous verrez :
   - Matrice de confusion (graphique)
   - Tableau de classification détaillé
   - Statistiques globales (précision, rappel, F1-score moyens)

### Comprendre les Résultats

**Matrice de Confusion :**
```
                Bactérienne  Normal  Virale
Bactérienne        240        2       0      ← Vraies valeurs
Normal             42        158      34
Virale             56         0      92
                   ↓
           Prédictions du modèle
```

**Métriques :**
- **Précision Élevée (>0.9)** : Peu de faux positifs
- **Rappel Élevé (>0.9)** : Détecte la plupart des vrais cas
- **F1-Score Élevé (>0.8)** : Bon équilibre général

## 📁 Structure du Projet

```
King_IA_apps/
├── app_new.py                 # Application Streamlit principale
├── app.py                     # Version précédente
├── requirements.txt            # Dépendances Python
├── install_dependencies.py    # Script d'installation des deps
├── demo_metrics.py            # Démonstration des métriques
├── METRICS_GUIDE.md          # Guide détaillé des métriques
├── models/
│   └── model.h5              # Modèle VGG16 entraîné
├── reports/
│   └── metrics/
│       └── metric.json       # Données des métriques d'évaluation
├── samples/
│   ├── train/
│   │   ├── NORMAL/
│   │   └── PNEUMONIA/
│   └── test/
│       ├── NORMAL/
│       └── PNEUMONIA/
└── stages/
    ├── data_preprocessing.py
    ├── model_training.py
    └── model_evaluation.py
```

## 🔧 Configuration

Les métriques proviennent du fichier : `reports/metrics/metric.json`

Si vous souhaitez mettre à jour les métriques :

```bash
# Évaluer le modèle avec les données de test
python stages/model_evaluation.py --config params.yaml
```

## 📊 Affichage des Métriques

### Via l'Application Streamlit
```
onglet "Analyse" → Télécharger une image → Défilez vers le bas
```

### Via le Script de Démonstration
```bash
python demo_metrics.py
```

## 💡 Interprétation des Métriques

### Classe : Pneumonie Bactérienne
- **Précision: 0.7101** → 71% des détections bactériennes sont correctes
- **Rappel: 0.9917** → 99% des cas bactériens réels sont détectés
- **F1-Score: 0.8276** → Performance globale bonne

### Classe : Normal
- **Précision: 0.9875** → 98% des détections normales sont correctes
- **Rappel: 0.6752** → 67% des cas réels normaux sont détectés
- **F1-Score: 0.8020** → Performance globale bonne

### Classe : Pneumonie Virale
- **Précision: 0.7302** → 73% des détections virales sont correctes
- **Rappel: 0.6216** → 62% des cas viraux réels sont détectés
- **F1-Score: 0.6715** → Performance modérée

## 📌 Améliorations Possibles

- [ ] Courbes ROC (Receiver Operating Characteristic)
- [ ] AUC (Area Under Curve)
- [ ] Matrice de confusion normalisée (%)
- [ ] Comparaison entre différentes epochs d'entraînement
- [ ] Export des métriques en PDF
- [ ] Comparaison inter-modèles

## ⚠️ Avertissements Importants

Cette application est à **usage pédagogique et informatif**. Les résultats :
- **Ne remplacent pas** un diagnostic médical professionnel
- Doivent être **validés par un médecin**
- Utilisent un modèle **entraîné sur un dataset limité**
- Peuvent avoir des **erreurs de prédiction**

**Consultez toujours un professionnel de santé qualifié !**

## 📚 Documentation Supplémentaire

- [METRICS_GUIDE.md](METRICS_GUIDE.md) - Guide détaillé des métriques
- [params.yaml](params.yaml) - Configuration du modèle
- [README.md](README.md) - Documentation originale

## 📧 Support

Pour toute question ou amélioration :
- Vérifiez les fichiers de configuration dans `params.yaml`
- Consultez les logs d'exécution de Streamlit
- Exécutez `python demo_metrics.py` pour voir les métriques en détail

---

**Dernière mise à jour** : Février 2026
**Version** : 2.0 (Avec métriques d'évaluation)
