import streamlit as st
from owlready2 import get_ontology
import subprocess
import json
import base64
import re

# إعداد الصفحة
st.set_page_config(page_title="Générateur de repas personnalisés", layout="centered")

# تعيين خلفية
def set_background(image_file):
    with open(image_file, "rb") as image:
        encoded = base64.b64encode(image.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            color: black;
        }}
        header {{display: none !important;}}
        footer {{visibility: hidden;}}
        [data-testid="stSidebar"] {{display: none !important;}}
        div.stButton > button:first-child {{
            background-color: #90ee90 !important;
            color: black !important;
            font-weight: bold;
            font-size: 16px;
            padding: 10px 24px;
            border-radius: 10px;
            border: none;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_background("images/3.jpg")

# عرض عنوان WekelniS
st.markdown("""
    <div style="text-align: center; margin-bottom: 20px;">
        <h1 style="font-size: 58px; font-family: 'Poppins', sans-serif; font-weight: 600; color: black;">
            WekelniS 💗🩺
        </h1>
    </div>
""", unsafe_allow_html=True)

# تحميل الأنطولوجيا
onto_path = "C:/Users/NexTech/Desktop/codeM/ontology9-singaux4.owl"
onto = get_ontology(onto_path).load()

st.title("🍽️ Générateur de repas personnalisés")

# التأكد من وجود patient_id في الجلسة
if "patient_id" in st.session_state:
    patient_id = st.session_state["patient_id"]

    if hasattr(onto, patient_id):
        patient = getattr(onto, patient_id)

        patient_name = getattr(patient, "aNom", ["Nom inconnu"])
        patient_name = patient_name[0] if isinstance(patient_name, list) else patient_name

        calories_attr = getattr(patient, "CaloriesP", None)
        if isinstance(calories_attr, list) and calories_attr:
            calories_limit = calories_attr[0]
        elif isinstance(calories_attr, (int, float)):
            calories_limit = calories_attr
        else:
            calories_limit = 400

        # ✅ عرض الاسم والسعرات
        st.markdown(f"""
        <div style='font-size: 22px; font-weight: bold; color: black; margin-bottom: 10px;'>
        👤 Nom du patient : <span style='color: #90ee90;'>{patient_name}</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style='font-size: 22px; font-weight: bold; color: black; margin-bottom: 20px;'>
        🔥 Besoin calorique : <span style='color: #90ee90;'>{calories_limit} kcal</span>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🔍 Générer les repas"):
            all_meals = getattr(patient, "aRepasRecommande", [])
            seen = set()
            meal_data = []
            for m in all_meals:
                name = getattr(m, "Nom_Aliment", None)  # ← استبدال هنا
                calories = getattr(m, "Calories", None)
                if name and calories is not None:
                    name_val = name[0] if isinstance(name, list) else name
                    cal_val = calories[0] if isinstance(calories, list) else calories
                    if name_val not in seen:
                        seen.add(name_val)
                        meal_data.append({"Nom": name_val, "Calories": cal_val})

            if meal_data:
                aliments_str = ", ".join([f"{m['Nom']} ({m['Calories']} kcal/100g)" for m in meal_data])
                noms_disponibles = ", ".join([f'"{m["Nom"]}"' for m in meal_data])

                prompt = f"""
Vous êtes un assistant nutritionniste expert en diététique hospitalière.

Voici la liste des aliments disponibles pour ce patient (avec leurs apports caloriques pour 100g) :
{aliments_str}

Le besoin calorique total du patient est de {calories_limit} kcal par jour.

🎯 Générez 4 repas variés, équilibrés et sains, adaptés à un patient hospitalisé.

🧠 Contraintes :
- Chaque repas doit contenir au moins 2 aliments différents.
- Tous les aliments doivent obligatoirement être choisis uniquement depuis cette liste : [{noms_disponibles}]
- Chaque aliment utilisé est en quantité de 100g.
- Chaque repas doit être **distinct et original** (pas de répétition des mêmes aliments dans plusieurs repas).
- Les repas doivent être riches en fibres, en protéines et pauvres en graisses saturées.
- La somme des calories des 4 repas doit être proche de {calories_limit} kcal (±5%).

📌 Format de réponse attendu (en JSON) :
{{
  "Repas_1": [{{"Aliment": "Nom", "Calories": 123}}, ...],
  "Repas_2": [...],
  "Repas_3": [...],
  "Repas_4": [...]
}}

Répondez uniquement avec le contenu JSON valide. Pas d'explication, pas de phrases autour.
"""

                with st.spinner("⏳ Génération des repas en cours..."):
                    try:
                        result = subprocess.run(
                            ["ollama", "run", "gemma:2b"],
                            input=prompt.encode("utf-8"),
                            capture_output=True,
                            timeout=600
                        )
                        if result.returncode == 0:
                            output = result.stdout.decode("utf-8").strip()

                            # تصفية النص لاستخراج JSON فقط
                            json_text_match = re.search(r"\{[\s\S]+\}", output)
                            if json_text_match:
                                json_text = json_text_match.group(0)
                                try:
                                    json_output = json.loads(json_text)
                                    st.markdown("<div style='color: black; font-weight: bold;'>✅ Repas générés avec succès !</div>", unsafe_allow_html=True)

                                    # عرض النتائج
                                    for meal_type, repas in json_output.items():
                                        st.markdown(f"## 🍴 {meal_type.replace('_', ' ').title()}")
                                        for item in repas:
                                            st.markdown(
                                                f"- 🥗 **{item['Aliment']}** — `100g` — `{item['Calories']} kcal`"
                                            )
                                except json.JSONDecodeError:
                                    st.warning("⚠️ Le contenu retourné n'est pas un JSON valide.")
                                    st.text("📝 Résultat brut :")
                                    st.code(output)
                            else:
                                st.warning("⚠️ Aucun contenu JSON détecté.")
                                st.code(output)
                        else:
                            st.error("❌ Erreur lors de l'exécution d'Ollama :")
                            st.code(result.stderr.decode("utf-8"))
                    except Exception as e:
                        st.error(f"❌ Exception : {e}")
            else:
                st.warning("⚠️ Aucun aliment recommandé trouvé pour ce patient.")
    else:
        st.error(f"❌ Patient non trouvé dans l'ontologie : {patient_id}")
else:
    st.error("❌ Aucun identifiant patient trouvé. Veuillez vous connecter d'abord.")
