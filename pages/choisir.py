import streamlit as st
import base64
import pandas as pd
from owlready2 import get_ontology
import bcrypt

# إعداد الصفحة
st.set_page_config(page_title="Patient Dashboard", layout="wide")

# تعيين الخلفية ونمط CSS
def set_background_and_style(image_file):
    try:
        with open(image_file, "rb") as f:
            data = f.read()
        encoded = base64.b64encode(data).decode()
        css = f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600&display=swap');
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            font-family: 'Poppins', sans-serif;
        }}
        header {{ display: none !important; }}
        footer {{ visibility: hidden; }}
        section[data-testid="stSidebar"] {{ display: none !important; }}
        h1, h2, h3, h4, h5, h6, p, label {{
            color: black !important;
            font-family: 'Poppins', sans-serif;
        }}
        .box-container {{
            background-color: white;
            border-radius: 16px;
            padding: 30px;
            box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
            text-align: center;
            margin-top: 40px;
        }}
        .stButton > button {{
            font-weight: bold;
            font-size: 16px;
            padding: 12px 40px;
            border-radius: 10px;
            width: 100%;
            margin: 10px 0;
            background-color: #0056b3;
            color: white;
        }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("⚠️ Impossible de charger l’image de fond. Vérifiez le chemin du fichier.")

set_background_and_style("Images/3.jpg")

st.markdown("""
    <div style="text-align: center; margin-top: -60px; margin-bottom: 20px;">
        <h1 style="font-size: 58px; font-family: 'Poppins', sans-serif; font-weight: 600;">WekelniS 💗🩺</h1>
    </div>
""", unsafe_allow_html=True)

# تحقق من وجود بيانات الجلسة
if 'email' not in st.session_state or 'password' not in st.session_state:
    st.warning("🔐 Veuillez d'abord vous connecter depuis la page principale.")
    st.stop()

email_input = st.session_state['email']
password_input = st.session_state['password']

# تحميل الأنطولوجيا
try:
    onto = get_ontology("ontology9-singaux4.owl").load()
except Exception as e:
    st.error(f"❌ Erreur lors du chargement de l'ontologie : {e}")
    st.stop()

def get_first_value(prop):
    if prop is None:
        return "N/A"
    if isinstance(prop, (list, tuple)):
        return prop[0] if len(prop) > 0 else "N/A"
    return prop

# التحقق من المريض
found = False
for patient in onto.Patient.instances():
    if hasattr(patient, "aEmail") and patient.aEmail:
        patient_email = patient.aEmail[0] if isinstance(patient.aEmail, (list, tuple)) else patient.aEmail

        if email_input == patient_email:
            if hasattr(patient, "aPassword") and patient.aPassword:
                patient_password = patient.aPassword[0] if isinstance(patient.aPassword, (list, tuple)) else patient.aPassword

                if bcrypt.checkpw(password_input.encode('utf-8'), patient_password.encode('utf-8')):
                    found = True

                    nom_patient = get_first_value(patient.Name) if hasattr(patient, "Name") else "Inconnu"
                    calories = get_first_value(patient.CaloriesP) if hasattr(patient, "CaloriesP") else "N/A"
                    mews = get_first_value(patient.aMEWS) if hasattr(patient, "aMEWS") else "N/A"

                    st.markdown(f"<h2 style='text-align:center;'>Bienvenue sur votre espace santé, {nom_patient}</h2>", unsafe_allow_html=True)
                    st.markdown(f"<h3 style='text-align:center;'>🔥 Calories : {calories}</h3>", unsafe_allow_html=True)

                    try:
                        mews_value = float(mews)
                        if mews_value <= 2:
                            st.success("🟢 État stable et normal")
                        elif 3 <= mews_value <= 4:
                            st.warning("🟡 Surveillance nécessaire, signes vitaux anormaux")
                        elif mews_value >= 5:
                            st.error("🔴 État critique, hospitalisation immédiate recommandée")
                    except:
                        st.warning("⚠️ Le score MEWS n'est pas correctement défini.")
                        mews_value = None

                    # زر لعرض القيم الحيوية
                    show_vitals = st.button("🔍 Afficher les Signes Vitaux")

                    if show_vitals:
                        try:
                            df_vitals = pd.read_csv("signaux_vitaux_patients2.csv")
                            row = df_vitals[df_vitals["aEmail"] == email_input]

                            if not row.empty:
                                vitals_data = row.iloc[0]
                                st.markdown("<h3 style='text-align:center;'>📊 Signes Vitaux</h3>", unsafe_allow_html=True)

                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.info(f"❤️ Fréquence cardiaque : {vitals_data['HeartRate']} bpm")
                                    st.info(f"🌡️ Température : {vitals_data['Temperateur']} °C")
                                with col2:
                                    st.info(f"🫁 Fréquence respiratoire : {vitals_data['RespiratoryR']} rpm")
                                    st.info(f"🧪 Glycémie : {vitals_data['Glycemia']} mg/dL")
                                with col3:
                                    st.info(f"🩸 Tension artérielle : {vitals_data['BloodPressure']} mmHg")
                                    st.info(f"🧬 Saturation O2 : {vitals_data['OxygenSaturation']} %")
                            else:
                                st.warning("⚠️ Les signes vitaux ne sont pas disponibles pour ce patient.")
                        except FileNotFoundError:
                            st.error("❌ Fichier signaux_vitaux_patients.csv introuvable.")
                        except Exception as e:
                            st.error(f"❌ Erreur lors de la lecture des signes vitaux : {e}")

                    # اختيار الطريقة
                    with st.container():
                        st.markdown("""
                        <div class="box-container">
                            <h3>🥗 Veuillez choisir la méthode que vous souhaitez utiliser pour recevoir vos recommandations alimentaires :</h3>
                            <p style="font-size:16px; margin-top:10px;">
                            👉 Soit vous sélectionnez vous-même vos repas (Choisir),<br>
                            👉 Soit vous laissez notre système intelligent (LLM) le faire pour vous.
                            </p>
                        </div>
                        """, unsafe_allow_html=True)

                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("🤖 Recommandation Automatique", key="btn_llm"):
                                if mews_value is not None and mews_value >= 5:
                                    st.error("🔴 Votre état est critique. Vous ne pouvez pas choisir un repas à ce moment-là.")
                                else:
                                    st.success("✅ Vous avez choisi LLM")
                                    st.session_state["patient_id"] = patient.name
                                    st.switch_page("pages/LLM.py")

                        with col2:
                            if st.button("📝 Choix Manuel", key="btn_choisir"):
                                if mews_value is not None and mews_value >= 5:
                                    st.error("🔴 Votre état est critique. Vous ne pouvez pas choisir un repas à ce moment-là.")
                                else:
                                    st.success("✅ Vous avez choisi 'Choisir'")
                                    st.session_state["patient_id"] = patient.name
                                    st.switch_page("pages/choisir_repas.py")

                    break

if not found:
    st.error("❌ Informations de connexion invalides. Veuillez réessayer depuis la page de connexion.")
