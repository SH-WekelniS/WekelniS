import streamlit as st
from owlready2 import get_ontology
import base64

st.set_page_config(page_title="Choisir repas", layout="wide")

# الخلفية والتنسيق

def set_background_and_style(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: black;
    }}
    header {{ display: none !important; }}
    footer {{ visibility: hidden; }}
    section[data-testid="stSidebar"] {{ display: none !important; }}
    h1, h2, h3, h4, h5, h6, p, label {{
        color: black !important;
    }}
    .right-box {{
        position: fixed;
        top: 50%;
        right: 3%;
        transform: translateY(-50%);
        background-color: rgba(255,255,255,0.92);
        padding: 15px 20px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        width: 250px;
        max-height: 70vh;
        overflow-y: auto;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 14px;
        color: #333333;
    }}
    .right-box h4 {{
        margin-bottom: 10px;
        font-weight: 600;
        border-bottom: 2px solid #4CAF50;
        padding-bottom: 8px;
        color: #2E7D32;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

set_background_and_style("Images/image22.jpg")

st.markdown("""
    <div style="text-align: center; margin-top: -60px; margin-bottom: 20px;">
        <h1 style="font-size: 58px; font-family: 'Poppins', sans-serif; font-weight: 600;">WekelniS 💗🩺</h1>
    </div>
""", unsafe_allow_html=True)

onto = get_ontology("ontology9-singaux4.owl").load()

def get_first_value(prop):
    if isinstance(prop, list) and len(prop) > 0:
        return prop[0]
    return prop if prop else "N/A"

if 'email' not in st.session_state:
    st.warning("🔒 Veuillez vous connecter d'abord.")
    st.stop()

email_input = st.session_state['email']
patient = None

for p in onto.Patient.instances():
    if hasattr(p, 'aEmail') and get_first_value(p.aEmail) == email_input:
        patient = p
        break

if not patient:
    st.error("❌ Patient introuvable.")
    st.stop()

nom = get_first_value(patient.aNom)
mews = get_first_value(getattr(patient, "aMEWS", "N/A"))
calories_max = float(get_first_value(getattr(patient, "CaloriesP", 2000.0)))

calories_limits = {
    "Petit déjeuner": round(0.20 * calories_max),
    "Déjeuner": round(0.35 * calories_max),
    "Collation": round(0.15 * calories_max),
    "Dîner": round(0.30 * calories_max)
}

st.markdown("<h3>🍽️ Choisissez le type de repas</h3>", unsafe_allow_html=True)
selected_type = st.radio("Type de repas", list(calories_limits.keys()))
st.markdown(f"<p><b>Calories maximales pour {selected_type}:</b> {calories_limits[selected_type]} kcal</p>", unsafe_allow_html=True)

repas_disponibles = []
if hasattr(patient, 'aRepasRecommande'):
    for repas in patient.aRepasRecommande:
        nom_repas = get_first_value(getattr(repas, "Nom_Aliment", "Sans nom"))
        cal_repas = float(get_first_value(getattr(repas, "Calories", 0.0)))
        repas_disponibles.append((repas, nom_repas, cal_repas))

choix_repas = []
total_calories_selected = 0
st.write("### 🥗 Sélectionnez les repas pour le type choisi:")
for i, (repas, nom_r, cal_r) in enumerate(repas_disponibles):
    if total_calories_selected + cal_r <= calories_limits[selected_type]:
        checked = st.checkbox(f"{nom_r} - {cal_r} kcal", key=f"repas_{i}_{selected_type}")
        if checked:
            choix_repas.append((nom_r, cal_r))
            total_calories_selected += cal_r

st.markdown(f"""
<div class="right-box">
    <h4>🍽️ Type: {selected_type}</h4>
    <h4>✅ Total sélectionné: {total_calories_selected} / {calories_limits[selected_type]} kcal</h4>
    <hr style="border:none; border-top:1px solid #ddd; margin:10px 0;">
    <p style="font-weight:600; font-size:15px; margin: 8px 0;">👤 Nom: <span style="color:#4CAF50;">{nom}</span></p>
    <p style="font-weight:600; font-size:15px; margin: 8px 0;">🔥 Calories journalières permises: <span style="color:#4CAF50;">{calories_max:.1f}</span></p>
</div>
""", unsafe_allow_html=True)

# أزرار حقيقية مع وظائف باستخدام st.button
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("✅ Valider mes choix", key="valider_btn"):
        st.session_state["submit_button"] = True
        st.session_state["repas_valides"] = choix_repas

with col2:
    if st.button("🔄 Recommencer", key="recommencer_btn"):
        st.session_state["submit_button"] = False
        st.session_state["repas_valides"] = []
        st.rerun()

with col3:
    if st.button("🔒 Se déconnecter", key="logout_btn"):
        st.session_state.pop("email", None)
        st.switch_page("pages/connecter.py")

# تخصيص ألوان الأزرار
st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #4CAF50 !important;
        color: white !important;
        font-weight: bold;
        border-radius: 8px;
        padding: 12px 24px;
    }
    div.stButton > button:nth-child(2) {
        background-color: #9E9E9E !important;
        color: white !important;
        font-weight: bold;
        border-radius: 8px;
        padding: 12px 24px;
    }
    div.stButton > button:nth-child(3) {
        background-color: #f44336 !important;
        color: white !important;
        font-weight: bold;
        border-radius: 8px;
        padding: 12px 24px;
    }
    </style>
""", unsafe_allow_html=True)

# Affichage popup repas choisis
if st.session_state.get("submit_button") and "repas_valides" in st.session_state:
    repas_html = "".join(
        f"<p style='margin: 8px 0; font-size:16px;'>🍴 <b>{nom_r}</b> - {cal_r} kcal</p>"
        for nom_r, cal_r in st.session_state["repas_valides"]
    )
    popup_html = f"""
        <div style='position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%);
        background-color: rgba(255,255,255,0.95); padding: 30px; border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3); z-index: 9999; width: 400px; text-align: center;'>
            <h3 style='color: #2E7D32;'>✅ Vos repas sélectionnés :</h3>
            {repas_html}
            <hr style='margin:15px 0;'>
            <p style='color:#555; font-size:14px;'>Merci pour votre sélection.</p>
        </div>
    """
    st.markdown(popup_html, unsafe_allow_html=True)
