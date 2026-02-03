"""
Démonstration des métriques d'évaluation du modèle
Affiche comment les données de métriques sont structurées et interprétées
"""

import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Charger les métriques depuis le fichier
with open("reports/metrics/metric.json", "r") as f:
    data = json.load(f)

# Prendre les dernières métriques
latest_metrics = data['model_metric'][-1]

print("=" * 70)
print("📊 RAPPORT D'ÉVALUATION DU MODÈLE")
print("=" * 70)

print(f"\n📅 Timestamp: {latest_metrics['time_stamp']}")

# Afficher la matrice de confusion
print("\n📈 MATRICE DE CONFUSION:")
print("-" * 50)
cm = np.array(latest_metrics['confusion_matrix'])
classes = ['Pneumonie Bactérienne', 'Normal', 'Pneumonie Virale']
print(f"{'':25} | {'Bactérienne':12} | {'Normal':12} | {'Virale':12} |")
print("-" * 70)
for i, class_name in enumerate(classes):
    row = cm[i]
    print(f"{class_name:25} | {row[0]:12} | {row[1]:12} | {row[2]:12} |")

# Afficher les métriques
print("\n\n📊 RAPPORT DE CLASSIFICATION:")
print("-" * 70)
precision = latest_metrics['precision']
recall = latest_metrics['recall']
f1 = latest_metrics['f1_score']

print(f"{'Classe':25} | {'Précision':12} | {'Rappel':12} | {'F1-Score':12} |")
print("-" * 70)

for i, class_name in enumerate(classes):
    print(f"{class_name:25} | {precision[i]:12.4f} | {recall[i]:12.4f} | {f1[i]:12.4f} |")

# Statistiques globales
print("\n\n📈 STATISTIQUES GLOBALES:")
print("-" * 50)
print(f"Précision Moyenne:  {np.mean(precision):.4f}")
print(f"Rappel Moyen:       {np.mean(recall):.4f}")
print(f"F1-Score Moyen:     {np.mean(f1):.4f}")

# Interprétation
print("\n\n💡 INTERPRÉTATION:")
print("-" * 50)
for i, class_name in enumerate(classes):
    print(f"\n{class_name}:")
    print(f"  • Précision: {precision[i]:.2%} - {precision[i]*100:.1f}% des prédictions sont correctes")
    print(f"  • Rappel:    {recall[i]:.2%} - {recall[i]*100:.1f}% des vrais cas ont été détectés")
    print(f"  • F1-Score:  {f1[i]:.4f} - Performance globale")

print("\n" + "=" * 70)
