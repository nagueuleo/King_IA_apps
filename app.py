import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
import numpy as np
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from datetime import datetime
import base64

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Configuration de la page
st.set_page_config(
    page_title="Pneumonia Detection",
    page_icon="🫁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialiser session_state pour l'historique
if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = []

# CSS personnalisé pour un design professionnel avec thème sombre optimisé
st.markdown("""
<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    .header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 40px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
    }
    
    .header h1 {
        font-size: 2.5em;
        margin-bottom: 10px;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .header p {
        font-size: 1.1em;
        opacity: 0.95;
    }
    
    .upload-section {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 30px;
        border-radius: 10px;
        margin-bottom: 25px;
        border: 2px solid #667eea;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.2);
    }
    
    .upload-section h3 {
        color: #fff;
        margin-bottom: 10px;
    }
    
    .upload-section p {
        color: #cbd5e1 !important;
        margin-top: 10px;
    }
    
    .result-container {
        padding: 30px;
        border-radius: 12px;
        margin-top: 25px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4);
    }
    
    .result-normal {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        border-left: 5px solid #34d399;
    }
    
    .result-pneumonia {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        border-left: 5px solid #fca5a5;
    }
    
    .result-text {
        color: #ffffff !important;
        font-size: 1.3em;
        font-weight: 600;
        margin-bottom: 10px;
    }
    
    .confidence {
        color: #f1f5f9 !important;
        font-size: 1.1em;
        margin-top: 8px;
    }
    
    .result-normal p, .result-pneumonia p {
        color: #ffffff !important;
        margin-top: 10px;
    }
    
    .image-container {
        display: flex;
        justify-content: center;
        margin: 25px 0;
    }
    
    .image-container img {
        max-width: 500px;
        border-radius: 10px;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
        border: 2px solid #667eea;
    }
    
    .info-box {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border-left: 4px solid #667eea;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
    }
    
    .info-box h4 {
        color: #667eea;
        margin-bottom: 8px;
    }
    
    .info-box p {
        color: #cbd5e1 !important;
    }
    
    .history-item {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 10px;
        border-left: 3px solid #667eea;
        color: #cbd5e1;
    }
    
    .metric-box {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 15px;
        border-radius: 8px;
        text-align: center;
        border: 1px solid #667eea;
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

with st.spinner('⏳ Chargement du modèle...'):
    model = load_model()

st.success('✅ Modèle chargé avec succès!')

# Fonction pour traiter l'image
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

def create_report_image(image, prediction, confidence, predicted_class_idx):
    """Crée une image de rapport avec les résultats"""
    img_copy = image.copy()
    img_copy = img_copy.resize((400, 400))
    
    # Créer une image de rapport
    report = Image.new('RGB', (800, 600), color='#0f172a')
    
    # Coller l'image
    report.paste(img_copy, (50, 50))
    
    # Ajouter du texte (utiliser PIL pour le texte)
    draw = ImageDraw.Draw(report)
    
    # Texte des résultats
    diagnosis = "NORMAL" if predicted_class_idx == 1 else "PNEUMONIE DÉTECTÉE"
    confidence_text = f"Confiance: {confidence*100:.1f}%"
    
    # Positions approximatives
    draw.text((500, 100), "DIAGNOSTIC", fill=(102, 126, 234))
    draw.text((500, 150), diagnosis, fill=(255, 255, 255))
    draw.text((500, 250), confidence_text, fill=(255, 255, 255))
    
    return report

# Onglets
tab1, tab2, tab3 = st.tabs(["📤 Analyse", "📊 Historique", "ℹ️ Informations"])

with tab1:
    st.markdown("""
    <div class="upload-section">
        <h3>📤 Importer votre radiographie thoracique</h3>
        <p style="color: #cbd5e1; margin-top: 10px;">Formats acceptés: JPG, PNG | Taille max: 200MB</p>
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
            st.image(image, use_column_width=True)
        
        with col2:
            st.markdown("### 🔬 Résultats de l'analyse")
            
            with st.spinner('⏳ Analyse en cours...'):
                # Prédiction
                prediction = model.predict(decode_pil_image(image), verbose=0)
                confidence = np.max(prediction[0])
                predicted_class_idx = np.argmax(prediction[0])
                predicted_class = classes[predicted_class_idx]
                
                # Ajouter à l'historique
                analysis_data = {
                    'timestamp': datetime.now().strftime("%H:%M:%S"),
                    'diagnosis': predicted_class if predicted_class_idx != 1 else 'Normal',
                    'confidence': confidence,
                    'predicted_class_idx': predicted_class_idx,
                    'image': image
                }
                st.session_state.analysis_history.insert(0, analysis_data)
            
            # Affichage des résultats avec couleurs
            if predicted_class_idx == 1:  # Normal
                st.markdown(f"""
                <div class="result-container result-normal">
                    <div class="result-text">✅ IMAGE NORMALE</div>
                    <div class="confidence">Confiance: {confidence*100:.1f}%</div>
                    <p style="color: #fff; margin-top: 10px;">
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
                    <p style="color: #fff; margin-top: 10px;">
                        Veuillez consulter un professionnel de santé
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            # Bouton de téléchargement du rapport
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button("📥 Télécharger le rapport", use_container_width=True):
                    # Créer une image de rapport
                    report = create_report_image(image, prediction, confidence, predicted_class_idx)
                    
                    # Convertir en bytes
                    img_byte_arr = BytesIO()
                    report.save(img_byte_arr, format='PNG')
                    img_byte_arr.seek(0)
                    
                    st.download_button(
                        label="📥 Télécharger PNG",
                        data=img_byte_arr.getvalue(),
                        file_name=f"rapport_pneumonie_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                        mime="image/png"
                    )
        
        # Probabilités détaillées
        st.markdown("### 📊 Détail des probabilités")
        cols = st.columns(len(classes))
        for i, class_name in enumerate(classes):
            with cols[i]:
                confidence_pct = float(prediction[0][i] * 100)
                st.metric(class_name, f"{confidence_pct:.1f}%")

with tab2:
    st.markdown("### 📋 Historique des analyses")
    
    if st.session_state.analysis_history:
        # Statistiques
        total = len(st.session_state.analysis_history)
        normal = sum(1 for x in st.session_state.analysis_history if x['predicted_class_idx'] == 1)
        pneumonia = total - normal
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class="metric-box">
                <h3 style="color: #667eea;">{total}</h3>
                <p style="color: #cbd5e1;">Total d'analyses</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="metric-box">
                <h3 style="color: #10b981;">{normal}</h3>
                <p style="color: #cbd5e1;">Images normales</p>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="metric-box">
                <h3 style="color: #ef4444;">{pneumonia}</h3>
                <p style="color: #cbd5e1;">Pneumonies détectées</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        for idx, item in enumerate(st.session_state.analysis_history):
            status_icon = "✅" if item['predicted_class_idx'] == 1 else "⚠️"
            st.markdown(f"""
            <div class="history-item">
                <strong>{status_icon} {item['timestamp']}</strong><br>
                Diagnostic: <strong>{item['diagnosis']}</strong><br>
                Confiance: <strong>{item['confidence']*100:.1f}%</strong>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("📭 Aucune analyse effectuée pour le moment. Commencez par télécharger une image!")

with tab3:
    st.markdown("""
    <div class="info-box">
        <h4>ℹ️ À propos de cette application</h4>
        <p>
            Cette application utilise un modèle d'apprentissage profond (VGG16) entraîné pour détecter 
            la pneumonie à partir de radiographies thoraciques. Les résultats sont fournis à titre informatif 
            et ne remplacent pas un diagnostic médical professionnel. Consultez toujours un médecin pour 
            une évaluation complète.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <h4>🏥 Classification des résultats</h4>
        <p>
            <strong>✅ Normal:</strong> Aucune pneumonie détectée<br>
            <strong>⚠️ Pneumonie Bactérienne:</strong> Infection bactérienne détectée<br>
            <strong>⚠️ Pneumonie Virale:</strong> Infection virale détectée
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <h4>📚 Modèle utilisé</h4>
        <p>
            <strong>Architecture:</strong> VGG16 (Transfer Learning)<br>
            <strong>Entrée:</strong> Images 224x224 pixels<br>
            <strong>Sortie:</strong> 3 classes (Normal, Pneumonie Bactérienne, Pneumonie Virale)
        </p>
    </div>
    """, unsafe_allow_html=True)
