"""
Test des fonctionnalités de métriques
Vérifie que les données et fonctions sont correctement configurées
"""

import json
import os
import sys

print("=" * 70)
print("🧪 TEST DES FONCTIONNALITÉS DE MÉTRIQUES")
print("=" * 70)

# Test 1 : Vérifier les fichiers essentiels
print("\n📁 TEST 1 : Vérification des fichiers...")
print("-" * 70)

required_files = [
    "app_new.py",
    "models/model.h5",
    "reports/metrics/metric.json",
    "requirements.txt"
]

all_exist = True
for file_path in required_files:
    exists = os.path.exists(file_path)
    status = "✅" if exists else "❌"
    print(f"{status} {file_path}")
    if not exists:
        all_exist = False

if all_exist:
    print("\n✅ Tous les fichiers requis existent!")
else:
    print("\n⚠️ Certains fichiers manquent!")

# Test 2 : Charger et valider les données de métriques
print("\n📊 TEST 2 : Validation des données de métriques...")
print("-" * 70)

try:
    with open("reports/metrics/metric.json", "r") as f:
        metrics_data = json.load(f)
    
    if 'model_metric' in metrics_data and len(metrics_data['model_metric']) > 0:
        latest = metrics_data['model_metric'][-1]
        print("✅ Données de métriques chargées avec succès!")
        print(f"   Timestamp: {latest.get('time_stamp', 'N/A')}")
        print(f"   Matrice de confusion: {len(latest.get('confusion_matrix', []))}x{len(latest.get('confusion_matrix', [[]])[0]) if len(latest.get('confusion_matrix', [])) > 0 else 0}")
        print(f"   Précision: {latest.get('precision', [])}")
        print(f"   Rappel: {latest.get('recall', [])}")
        print(f"   F1-Score: {latest.get('f1_score', [])}")
    else:
        print("❌ Format de données invalide!")
except Exception as e:
    print(f"❌ Erreur lors du chargement des métriques: {e}")

# Test 3 : Vérifier les imports Python
print("\n🔧 TEST 3 : Vérification des imports Python...")
print("-" * 70)

required_packages = [
    ('tensorflow', 'TensorFlow'),
    ('numpy', 'NumPy'),
    ('streamlit', 'Streamlit'),
    ('PIL', 'Pillow'),
    ('matplotlib', 'Matplotlib'),
    ('seaborn', 'Seaborn'),
    ('sklearn', 'Scikit-Learn'),
    ('yaml', 'PyYAML'),
]

missing_packages = []

for package, name in required_packages:
    try:
        __import__(package)
        print(f"✅ {name}")
    except ImportError:
        print(f"❌ {name} (manquant)")
        missing_packages.append(name)

if missing_packages:
    print(f"\n⚠️ Packages manquants: {', '.join(missing_packages)}")
    print("Exécutez: python install_dependencies.py")
else:
    print("\n✅ Tous les packages sont installés!")

# Test 4 : Structure du JSON
print("\n🔍 TEST 4 : Validation de la structure JSON...")
print("-" * 70)

try:
    with open("reports/metrics/metric.json", "r") as f:
        data = json.load(f)
    
    if 'model_metric' in data:
        print("✅ Clé 'model_metric' présente")
        
        metric = data['model_metric'][-1]
        required_keys = ['time_stamp', 'confusion_matrix', 'precision', 'recall', 'f1_score']
        
        for key in required_keys:
            if key in metric:
                print(f"✅ Clé '{key}' présente")
            else:
                print(f"❌ Clé '{key}' manquante")
    else:
        print("❌ Clé 'model_metric' manquante")
except Exception as e:
    print(f"❌ Erreur: {e}")

# Test 5 : Vérifier la syntaxe de app_new.py
print("\n📝 TEST 5 : Vérification de la syntaxe Python...")
print("-" * 70)

try:
    with open("app_new.py", "r", encoding='utf-8') as f:
        code = f.read()
    compile(code, "app_new.py", "exec")
    print("✅ Syntaxe valide dans app_new.py")
except SyntaxError as e:
    print(f"❌ Erreur de syntaxe dans app_new.py: {e}")

# Résumé
print("\n" + "=" * 70)
print("✅ TESTS TERMINÉS!")
print("=" * 70)

print("\n📌 Prochaines étapes:")
print("1. Si des packages manquent: python install_dependencies.py")
print("2. Lancer l'application: streamlit run app_new.py")
print("3. Afficher les métriques: python demo_metrics.py")

