import streamlit as st
import base64
from owlready2 import get_ontology
import bcrypt

# إعداد الصفحة
st.set_page_config(page_title="Patient Dashboard", layout="wide")

# دالة تعيين الخلفية ونمط CSS
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
        .stButton button {{
            font-weight: bold !important;
            font-size: 14px !important;
            padding: 8px 24px !important;
            border-radius: 8px !important;
            border: none !important;
            cursor: pointer !important;
            transition: background-color 0.3s ease !important;
        }}
        .stButton button:nth-of-type(1) {{
            background-color: #007BFF !important;
            color: white !important;
        }}
        .stButton button:nth-of-type(1):hover {{
            background-color: #0056b3 !important;
        }}
        .stButton button:nth-of-type(2) {{
            background-color: #28a745 !important;
            color: white !important;
        }}
        .stButton button:nth-of-type(2):hover {{
            background-color: #19692c !important;
        }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("⚠️ Impossible de charger l’image de fond. Vérifiez le chemin du fichier.")

# تعيين الخلفية
set_background_and_style("Images/3.jpg")

# التحقق من بيانات الجلسة
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

# دالة مساعده لإرجاع أول قيمة أو "N/A"
def get_first_value(prop):
    if isinstance(prop, list) and len(prop) > 0:
        return prop[0]
    return prop if prop else "N/A"

# التحقق من صحة المستخدم
found = False
for patient in onto.Patient.instances():
    if hasattr(patient, "hasEmail") and email_input == get_first_value(patient.hasEmail):
        hashed_password = get_first_value(patient.hasPassword).encode('utf-8')
        if bcrypt.checkpw(password_input.encode('utf-8'), hashed_password):
            found = True

            nom_patient = get_first_value(getattr(patient, "Name", "Inconnu"))
            calories = get_first_value(getattr(patient, "CaloriesP", "N/A"))
            mews = get_first_value(getattr(patient, "aMEWS", "N/A"))

            # عرض البيانات
            st.markdown(f"<h2 style='text-align:center;'>Bienvenue, {nom_patient}</h2>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='text-align:center;'>🔥 Calories : {calories}</h3>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='text-align:center;'>🩺 MEWS : {mews}</h3>", unsafe_allow_html=True)

            # مربع الاختيارات
            st.markdown("""
                <div class="box-container">
                    <h3>Que voulez-vous choisir ?</h3>
                </div>
            """, unsafe_allow_html=True)

            col1, _, col3 = st.columns([1, 6, 1])
            with col1:
                if st.button("LLM", key="btn_llm"):
                    st.success("✅ Vous avez choisi LLM")
            with col3:
                if st.button("Choisir", key="btn_choisir"):
                    st.success("✅ Vous avez choisi 'Choisir'")
                    st.switch_page("pages/choisir_repas.py")  # بدون .py

            # حذف كلمة المرور بعد التحقق
            del st.session_state['password']
            break

# إذا لم يتم العثور على المريض
if not found:
    st.error("❌ Informations de connexion invalides. Veuillez réessayer depuis la page de connexion.")
