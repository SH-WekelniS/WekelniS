import streamlit as st
from owlready2 import *
from rdflib import Graph
from rdflib.plugins.sparql import prepareQuery
import os

# إعداد Java لـ Pellet
JAVA_EXE = "C:\\Program Files\\Common Files\\Oracle\\Java\\javapath\\java.exe"
if os.path.exists(JAVA_EXE):
    owlready2.JAVA_EXE = JAVA_EXE

# تحميل الأنطولوجيا
onto_path.append(".")
onto_file = "C:/Users/NexTech/Desktop/codeM/ontology8_with_final.owl"
onto = get_ontology(onto_file).load()

# --- قواعد SWRL ---
rules = [
    ["Patient(?p) ^ aMaladie(?p, hypertension) ^ CaloriesP(?p, ?calP) ^ Alimentation(?f) ^ Potassium_Content(?f, ?potassium) ^ Calories(?f, ?calF) ^ greaterThan(?potassium, 300) ^ lessThanOrEqual(?calF, ?calP) -> aRepasRecommande(?p, ?f)"],
    ["Patient(?p) ^ aMEWS(?p, ?m) ^ lessThan(?m, 3) ^ CaloriesP(?p, ?calP) ^ Alimentation(?f) ^ Calories(?f, ?calF) ^ lessThanOrEqual(?calF, ?calP) -> aRepasRecommande(?p, ?f)"],
    ["Patient(?p) ^ aMEWS(?p, ?m) ^ greaterThanOrEqual(?m, 3) ^ CaloriesP(?p, ?calP) ^ Alimentation(?f) ^ Calories(?f, ?calF) ^ lessThanOrEqual(?calF, ?calP) -> aRepasRecommande(?p, ?f)"],
    ["Patient(?p) ^ aAge(?p, ?a) ^ greaterThan(?a, 65) ^ CaloriesP(?p, ?calP) ^ Alimentation(?f) ^ Calcium_Content(?f, ?c) ^ Calories(?f, ?calF) ^ greaterThan(?c, 200) ^ lessThanOrEqual(?calF, ?calP) -> aRepasRecommande(?p, ?f)"],
    ["Patient(?p) ^ aMEWS(?p, ?m) ^ greaterThanOrEqual(?m, 3) ^ CaloriesP(?p, ?calP) ^ Alimentation(?f) ^ Calories(?f, ?calF) ^ lessThanOrEqual(?calF, ?calP) ^ aMaladie(?p, diabetes)  -> aRepasRecommande(?p, ?f)"]
]

# ✅ تشغيل الاستدلال وتحديث aRepasRecommande
def run_raisoning(rules_input):
    with onto:
        for rule in rules_input:
            r = Imp()
            r.set_as_rule(rule[0])

        # تشغيل الريزنر
        sync_reasoner_pellet(infer_property_values=True)

        # تحديث التوصيات يدوياً إذا لم تُستنتج
        for patient in onto.Patient.instances():
            if not hasattr(patient, 'aRepasRecommande'):
                patient.aRepasRecommande = []

            if not patient.aRepasRecommande:
                for food in onto.Alimentation.instances():
                    try:
                        if hasattr(food, "isRecommendedFor") and patient in food.isRecommendedFor:
                            patient.aRepasRecommande.append(food)
                    except:
                        continue

    onto.save(file=onto_file, format="rdfxml")

def convertir_ontologie_rdflib():
    onto.save("temp.owl")
    g = Graph()
    g.parse("temp.owl")
    os.remove("temp.owl")
    return g

def executer_requete_sparql(nom_patient):
    g = convertir_ontologie_rdflib()

    ns = {
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "owl": "http://www.w3.org/2002/07/owl#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "xsd": "http://www.w3.org/2001/XMLSchema#",
        "onto": str(onto.base_iri)
    }

    requete = f"""
    PREFIX onto: <{onto.base_iri}>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    SELECT ?nomPatient ?mews ?calories ?aliment
    WHERE {{
      onto:{nom_patient} rdf:type onto:Patient .
      onto:{nom_patient} onto:Name ?nomPatient .
      OPTIONAL {{ onto:{nom_patient} onto:aMEWS ?mews . }}
      OPTIONAL {{ onto:{nom_patient} onto:CaloriesP ?calories . }}
      OPTIONAL {{ onto:{nom_patient} onto:aRepasRecommande ?aliment . }}
    }}
    """
    q = prepareQuery(requete, initNs=ns)
    results = g.query(q)

    nom, mews, cal = None, None, None
    aliments = set()

    for r in results:
        nom = str(r.nomPatient)
        mews = r.mews.toPython() if r.mews else "0"
        cal = r.calories.toPython() if r.calories else "N/A"
        if r.aliment:
            aliments.add(str(r.aliment).split('#')[-1])

    return nom, mews, cal, list(aliments)

def afficher_interface_patient(nom, mews, calories, aliments):
    st.title("🩺 Résultats Patient avec Recommandations")

    st.subheader("🧍 Informations Patient")
    st.markdown(f"**Nom**: {nom}")
    st.markdown(f"**MEWS**: {mews}")
    st.markdown(f"**Calories**: {calories}")

    st.subheader("🥗 Aliments Recommandés")
    if aliments:
        for a in aliments:
            st.write(f"- {a}")
    else:
        st.info("Aucun aliment recommandé pour ce patient.")

def main():
    st.sidebar.title("🔎 Recherche Patient")
    run = st.sidebar.button("Exécuter le raisonnement")

    if run:
        run_raisoning(rules)
        st.success("🧠 Raisonnement terminé. Ontologie mise à jour avec les recommandations.")

    Patient_id = st.text_input("🆔 ID du patient (ex: Patient_):")

    if st.button("Afficher les résultats") and Patient_id:
        nom_correct = Patient_id.strip()
        nom, mews, calories, aliments = executer_requete_sparql(nom_correct)

        if nom:
            afficher_interface_patient(nom, mews, calories, aliments)
        else:
            st.error("❌ Patient introuvable ou pas de données.")

if __name__ == "__main__":
    main()