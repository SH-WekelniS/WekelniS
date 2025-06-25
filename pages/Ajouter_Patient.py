import streamlit as st
from owlready2 import get_ontology
import base64
import bcrypt

# إعداد الصفحة
st.set_page_config(page_title="Ajouter un patient", layout="wide")

# دالة إعداد الخلفية والتنسيق
def set_background_and_style(image_file):
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

    label, .stTextInput label, .stSelectbox label, .stNumberInput label, .stMultiSelect label {{
        color: black !important;
        font-weight: bold;
    }}

    h1, h2, h3, h4, h5, h6, p {{
        color: black !important;
        font-family: 'Poppins', sans-serif;
    }}

    .stTextInput input, .stNumberInput input, .stSelectbox select, .stMultiSelect select, .stTextArea textarea {{
        background-color: white !important;
        color: black !important;
        border-radius: 8px;
        border: 1px solid #ccc;
        padding: 8px;
        caret-color: black !important;
        animation: blink-caret 1s step-end infinite;
    }}

    div.stButton > button:first-child {{
        display: block;
        margin: auto;
        background-color: #90ee90 !important; 
        color: white !important;
        font-weight: bold;
        font-size: 14px;
        padding: 6px 20px;
        border: none;
        border-radius: 8px;
    }}

    @keyframes blink-caret {{
        from, to {{ caret-color: transparent; }}
        50% {{ caret-color: black; }}
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# تطبيق الخلفية والتنسيق
set_background_and_style("Images/1.jpg")

# محاذاة النموذج في الوسط
left_col, center_col, right_col = st.columns([1, 2, 1])

with center_col:
    # العنوان الرئيسي
    st.markdown("""
        <div style="text-align: center; margin-top: -60px; margin-bottom: 20px;">
            <h1 style="font-size: 58px; font-family: 'Poppins', sans-serif; font-weight: 600;">WekelniS</h1>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("## 🧾Ajouter un nouveau patient")
    st.subheader("🧍 Informations du patient")

    nom = st.text_input("Nom")
    email = st.text_input("Adresse Gmail")
    motdepasse = st.text_input("Mot de passe", type="password")

    sex = st.selectbox("Sexe", options=["Homme", "Femme"])
    age = st.number_input("Âge", min_value=1, step=1)
    poids = st.number_input("Poids (kg)", min_value=00.0, format="%.1f")
    taille = st.number_input("Taille (cm)", min_value=000.0, format="%2.1f", help="Entrez votre taille en centimètres. Exemple: 170")

    maladie = st.multiselect(
        "Maladies chroniques",
        options=["Hypertension", "Heart Disease", "Diabetes", "Chronic Kidney Disease", "Asthma", "Arthritis", "nan"]
    )

    if st.button("S'inscrire"):
        # التحقق من إدخال كافة البيانات
        if nom and email and motdepasse and sex and age > 0 and poids > 0 and taille > 0 and maladie:
            with st.spinner("S'inscrire..."):
                onto = get_ontology("ontology9-singaux4.owl").load()

                Patient = onto.Patient
                MaladieChroniqueC = onto.MaladieChronique

                p_id = len(list(onto.Patient.instances())) + 1
                patient = Patient(f"Patient_{p_id}")

                # ملء بيانات المريض
                patient.Name = nom
                patient.Sex = sex
                patient.aAge = int(age)
                patient.aPoids = poids
                patient.aTaille = taille

                # تشفير كلمة المرور
                salt = bcrypt.gensalt()
                hashed_password = bcrypt.hashpw(motdepasse.encode('utf-8'), salt).decode('utf-8')
                patient.aEmail = email
                patient.aPassword = hashed_password

                # ربط الأمراض
                maladies_objs = []
                for m in maladie:
                    maladie_ind = None
                    for inst in onto.MaladieChronique.instances():
                        if inst.name.lower() == m.lower():
                            maladie_ind = inst
                            break
                    if not maladie_ind:
                        maladie_ind = MaladieChroniqueC(m.replace(" ", "_"))
                    maladies_objs.append(maladie_ind)
                patient.aMaladie = maladies_objs

                # حساب IMC
                imc = poids / ((taille / 100) ** 2)
                patient.aIMC = round(imc, 2)

                # حساب السعرات الحرارية
                if sex == "Homme":
                    calories = 10 * poids + 6.25 * taille - 5 * age + 5
                else:
                    calories = 10 * poids + 6.25 * taille - 5 * age - 161
                patient.CaloriesP = round(calories, 2)

                # حفظ الأنطولوجيا
                onto.save(file="C:/Users/NexTech/Desktop/codeM/ontology9-singaux4.owl")

            st.success("✅ Patient ajouté avec succès !")

            # حفظ بيانات الجلسة
            st.session_state['email'] = email
            st.session_state['password'] = motdepasse

            # الانتقال لصفحة اختيار الوجبات
            st.switch_page("pages/choisir.py")
        else:
            st.error("❌ Veuillez remplir tous les champs avant d'ajouter le patient.")
