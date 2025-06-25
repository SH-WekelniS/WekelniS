import streamlit as st
from owlready2 import get_ontology
import base64
import bcrypt

# إعداد الصفحة
st.set_page_config(page_title="Se connecter", layout="wide")

# إعداد الخلفية ونمط الخط
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

    h1, h2, h3, h4, h5, h6, p, label {{
        color: black !important;
        font-family: 'Poppins', sans-serif;
    }}

    div.stButton > button:first-child {{
        display: block;
        margin: auto;
        background-color: #90ee90 !important; /* أخضر فاتح */
        color: white !important;
        font-weight: bold;
        font-size: 14px;
        padding: 6px 20px;
        border: none;
        border-radius: 8px;
    }}

    input, .stTextInput input {{
        color: black !important;
        background-color: white !important;
    }}

    input:focus, .stTextInput input:focus {{
        caret-color: black !important;
        animation: blink-caret 1s step-end infinite;
    }}

    @keyframes blink-caret {{
        from, to {{ caret-color: transparent; }}
        50% {{ caret-color: black; }}
    }}

    label {{
        color: black !important;
    }}

    .stMarkdown h2 {{
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
        width: 260px;
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

    .forgot-password {{
        text-align: right;
        margin-top: -10px;
        margin-bottom: 20px;
        font-size: 13px;
    }}
    .forgot-password button {{
        background: none;
        border: none;
        color: #4CAF50;
        cursor: pointer;
        font-weight: 600;
        text-decoration: underline;
        padding: 0;
        font-family: 'Poppins', sans-serif;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# تعيين الخلفية
set_background_and_style("Images/1.jpg")

# واجهة التصميم
left_col, center_col, right_col = st.columns([1, 2, 1])

with center_col:
    st.markdown("""
        <div style="text-align: center; margin-top: -60px; margin-bottom: 20px;">
            <h1 style="font-size: 58px; font-family: 'Poppins', sans-serif; font-weight: 600;">WekelniS 💗🩺</h1>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<h2 style='color: black;'>Se connecter</h2>", unsafe_allow_html=True)

    email_input = st.text_input("Adresse Gmail")
    password_input = st.text_input("Mot de passe", type="password")

    if st.button("Mot de passe oublié?", key="forgot_pw_button"):
        st.session_state["show_reset"] = True

    if st.session_state.get("show_reset", False):
        st.info("Entrez votre adresse email pour recevoir un lien de réinitialisation.")
        reset_email = st.text_input("Adresse Gmail pour réinitialisation")
        if st.button("Envoyer le lien de réinitialisation"):
            if reset_email:
                st.success(f"Un lien de réinitialisation a été envoyé à {reset_email} (fonctionnalité à implémenter).")
            else:
                st.error("Veuillez entrer une adresse email valide.")

    if not st.session_state.get("show_reset", False):
        if st.button("Se connecter"):
            if email_input and password_input:
                with st.spinner("Vérification..."):
                    onto = get_ontology("C:/UsersNexTech/OneDrive/WekelniS/ontology9-singaux4.owl").load()
                    found = False

                    for patient in onto.Patient.instances():
                        email_val = getattr(patient, "aEmail", None)
                        pass_val = getattr(patient, "aPassword", None)

                        if email_val and pass_val and email_input == email_val:
                            hashed_password = pass_val.encode('utf-8')
                            if bcrypt.checkpw(password_input.encode('utf-8'), hashed_password):
                                st.success("✅ Connexion réussie !")

                                nom = patient.Name if hasattr(patient, "Name") else "Inconnu"
                                if isinstance(nom, list):
                                    nom = nom[0] if nom else "Inconnu"

                                val = getattr(patient, "CaloriesP", None)
                                if isinstance(val, (list, tuple)) and len(val) > 0:
                                    calories = round(val[0], 2)
                                elif isinstance(val, (float, int)):
                                    calories = round(val, 2)
                                else:
                                    calories = "N/A"

                                val = getattr(patient, "aMEWS", None)
                                if isinstance(val, (list, tuple)) and len(val) > 0:
                                    mews = round(val[0], 2)
                                elif isinstance(val, (float, int)):
                                    mews = round(val, 2)
                                else:
                                    mews = "N/A"

                                st.session_state["nom"] = nom
                                st.session_state["calories"] = calories
                                st.session_state["mews"] = mews
                                st.session_state['email'] = email_input
                                st.session_state['password'] = password_input

                                right_info = f"""
                                <div class="right-box">
                                    <h4>👤 Bienvenue, {nom}</h4>
                                    <p style="font-weight:600; font-size:15px; margin: 8px 0;">📧 Email: <span style="color:#4CAF50;">{email_input}</span></p>
                                    <p style="font-weight:600; font-size:15px; margin: 8px 0;">🔥 Calories journalières: <span style="color:#4CAF50;">{calories}</span> kcal</p>
                                    <p style="font-weight:600; font-size:15px; margin: 8px 0;">📊 MEWS: <span style="color:#4CAF50;">{mews}</span></p>
                                    <hr style="border:none; border-top:1px solid #ddd; margin:10px 0;">
                                    <p style="font-size:14px;">Redirection vers la page de sélection des repas en cours...</p>
                                </div>
                                """
                                st.markdown(right_info, unsafe_allow_html=True)

                                st.switch_page("pages/choisir.py")
                            else:
                                st.error("❌ Mot de passe incorrect.")
                            found = True
                            break

                    if not found:
                        st.error("❌ Utilisateur introuvable.")
            else:
                st.warning("⚠️ Veuillez remplir tous les champs.")

# === معلومات التواصل في الأسفل (مركزية) ===
st.markdown("""
    <div style='
        position: fixed;
        bottom: 12px;
        left: 50%;
        transform: translateX(-50%);
        color: black;
        font-size: 13px;
        font-family: "Poppins", sans-serif;
        background-color: rgba(255, 255, 255, 0.85);
        padding: 6px 16px;
        border-radius: 12px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
        z-index: 999;
    '>
        📧 Contact: <a href="mailto:wekelni.contact@gmail.com" style="color:#4CAF50; text-decoration: none;">wekelni.contact@gmail.com</a>
        &nbsp;|&nbsp;
        📞 +213 661 23 45 67
    </div>
""", unsafe_allow_html=True)
