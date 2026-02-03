"""
Script pour installer les dépendances manquantes
Nécessaire pour l'affichage des métriques
"""

import subprocess
import sys

# Packages à installer
packages = [
    'matplotlib',
    'seaborn',
    'scikit-learn'
]

print("Installation des packages requis pour l'affichage des métriques...")
print("=" * 60)

for package in packages:
    print(f"\n📦 Installation de {package}...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ {package} installé avec succès!")
    except Exception as e:
        print(f"❌ Erreur lors de l'installation de {package}: {e}")

print("\n" + "=" * 60)
print("✅ Installation terminée!")
print("\nVous pouvez maintenant lancer l'application avec:")
print("  streamlit run app_new.py")
