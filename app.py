import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
import numpy as np
import streamlit as st
from PIL import Image
from io import BytesIO

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Configuration de la page
st.set_page_config(
    page_title="Pneumonia Detection",
    page_icon="🫁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé pour un design professionnel
st.markdown("""
<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    .main {
        background: white;
        border-radius: 15px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
    }
    
    .header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 30px;
        border-radius: 15px 15px 0 0;
        text-align: center;
        margin-bottom: 30px;
    }
    
    .header h1 {
        font-size: 2.5em;
        margin-bottom: 10px;
        font-weight: 700;
    }
    
    .header p {
        font-size: 1.1em;
        opacity: 0.9;
    }
    
    .container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
    }
    
    .upload-section {
        background: #f8f9fa;
        padding: 25px;
        border-radius: 10px;
        margin-bottom: 25px;
        border: 2px dashed #667eea;
    }
    
    .result-container {
        padding: 25px;
        border-radius: 10px;
        margin-top: 25px;
    }
    
    .result-normal {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        border-left: 5px solid #27ae60;
    }
    
    .result-pneumonia {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        border-left: 5px solid #e74c3c;
    }
    
    .result-text {
        color: #000;
        font-size: 1.3em;
        font-weight: 600;
        margin-bottom: 10px;
    }
    
    .confidence {
        color: #000;
        font-size: 1.1em;
    }
    
    .image-container {
        display: flex;
        justify-content: center;
        margin: 25px 0;
    }
    
    .image-container img {
        max-width: 500px;
        border-radius: 10px;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    }
    
    .info-box {
        background: #e8f4f8;
        border-left: 4px solid #667eea;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    
    .info-box h4 {
        color: #667eea;
        margin-bottom: 8px;
    }
    
    .loading-text {
        text-align: center;
        font-size: 1.1em;
        color: #667eea;
    }
</style>
""", unsafe_allow_html=True)

# En-tête
st.markdown("""
<div class="header">
    <h1>🫁 Détection de la pneumonie</h1>
    <p>Analysez vos radiographies thoraciques avec KING IA app</p>
</div>
""", unsafe_allow_html=True)

# Chargement du modèle
@st.cache_resource
def load_model():
    """Charge le modèle pré-entraîné depuis models/model.h5"""
    import os
    
    model_path = 'models/model.h5'
    
    # Vérifier que le fichier existe
    if not os.path.exists(model_path):
        st.error(f"❌ Erreur: Le modèle '{model_path}' n'a pas été trouvé!")
        st.stop()
    
    try:
        model = tf.keras.models.load_model(model_path)
        return model
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement du modèle: {str(e)}")
        st.stop()

# Classes de prédiction
classes = ['Pneumonie Bactérienne', 'Normal', 'Pneumonie Virale']
class_colors = {
    0: 'result-pneumonia',  # Bacterial Pneumonia
    1: 'result-normal',     # Normal
    2: 'result-pneumonia'   # Viral Pneumonia
}

with st.spinner('⏳ Chargement du modèle...'):
    model = load_model()

st.success('✅ Modèle chargé avec succès!')

# Fonction pour traiter l'image
def decode_img(image_data):
    """Prépare l'image pour le modèle"""
    img = tf.image.decode_jpeg(image_data, channels=3)
    img = tf.image.resize(img, [224, 224])
    img = img / 255.0  # Normalisation
    return np.expand_dims(img, axis=0)

def decode_pil_image(pil_image):
    """Prépare une image PIL pour le modèle"""
    # Convertir en RGB (3 canaux) si nécessaire
    if pil_image.mode != 'RGB':
        pil_image = pil_image.convert('RGB')
    
    # Redimensionner à 224x224
    img = pil_image.resize((224, 224))
    
    # Convertir en array numpy et normaliser
    img = np.array(img, dtype=np.float32) / 255.0
    
    # Ajouter la dimension du batch (1, 224, 224, 3)
    return np.expand_dims(img, axis=0)

# Section d'upload
st.markdown("""
<div class="upload-section">
    <h3>📤 Importer votre radiographie thoracique</h3>
    <p style="color: #666; margin-top: 10px;">Formats acceptés: JPG, PNG | Taille max: 200MB</p>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Sélectionnez une image",
    type=["jpg", "jpeg", "png"],
    label_visibility="collapsed"
)

if uploaded_file is not None:
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("### 📸 Image téléchargée")
        image = Image.open(uploaded_file)
        st.image(image, use_column_width=True, width=None)
    
    with col2:
        st.markdown("### 🔬 Résultats de l'analyse")
        
        with st.spinner('⏳ Analyse en cours...'):
            # Prédiction
            prediction = model.predict(decode_pil_image(image), verbose=0)
            confidence = np.max(prediction[0])
            predicted_class_idx = np.argmax(prediction[0])
            predicted_class = classes[predicted_class_idx]
            
        # Affichage des résultats avec couleurs
        if predicted_class_idx == 1:  # Normal
            st.markdown(f"""
            <div class="result-container result-normal">
                <div class="result-text">✅ IMAGE NORMALE</div>
                <div class="confidence">Confiance: {confidence*100:.1f}%</div>
                <p style="color: #000; margin-top: 10px;">
                    Aucune pneumonie détectée
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:  # Pneumonia
            st.markdown(f"""
            <div class="result-container result-pneumonia">
                <div class="result-text">⚠️ PNEUMONIE DÉTECTÉE</div>
                <div class="confidence">Type: {predicted_class}</div>
                <div class="confidence">Confiance: {confidence*100:.1f}%</div>
                <p style="color: #000; margin-top: 10px;">
                    Veuillez consulter un professionnel de santé
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        # Probabilités détaillées
        st.markdown("### 📊 Détail des probabilités")
        for i, class_name in enumerate(classes):
            confidence_pct = float(prediction[0][i] * 100)
            color = "#27ae60" if i == 1 else "#e74c3c"
            st.progress(float(confidence_pct) / 100, text=f"{class_name}: {confidence_pct:.1f}%")
    
    # Informations d'utilisation
    st.markdown("""
    <div class="info-box">
        <h4 style="color: #000;">ℹ️ À propos de cette analyse</h4>
        <p style="color: #000;">Cette application utilise un modèle d'apprentissage profond entraîné pour détecter la pneumonie 
        à partir de radiographies thoraciques. Les résultats sont fournis à titre informatif et ne remplacent 
        pas un diagnostic médical professionnel. Consultez toujours un médecin pour une évaluation complète.</p>
    </div>
    """, unsafe_allow_html=True)

else:
    st.info("👆 Commencez par télécharger une radiographie thoracique pour l'analyse")

