import streamlit as st
import base64

# إعداد الصفحة
st.set_page_config(page_title="WekelniS", layout="wide", initial_sidebar_state="collapsed")

# إخفاء عناصر Streamlit الافتراضية
hide_streamlit_style = """
    <style>
    #MainMenu, header, footer {visibility: hidden;}
    section[data-testid="stSidebar"] { display: none !important; }
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# دالة لتعيين الخلفية وتنسيقات CSS
def set_background_and_style(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
        encoded = base64.b64encode(data).decode()
    css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700&display=swap');

    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        font-family: 'Poppins', sans-serif;
    }}

    .overlay-text {{
        background-color: rgba(255, 255, 255, 0.92);
        padding: 50px 30px;
        border-radius: 20px;
        margin-top: -50px; /* تحريك الشريط إلى الأعلى */
        text-align: center;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
        width: 85%;
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
        font-weight: bold;  /* جعل الكتابة غامقة */
    }}

    .title {{
        font-size: 56px;
        font-weight: 700;
        color: black; /* جعل كلمة WekelniS باللون الأسود */
        margin-bottom: 15px;
    }}

    .subtitle {{
        font-size: 24px;
        color: #333;
        margin-bottom: 35px;
        font-weight: bold;  /* جعل الكتابة غامقة */
    }}

    .stButton > button {{
        display: block;
        margin: auto;
        background-color: #90ee90 !important; /* أخضر فاتح */
        color: black !important; /* لون الكتابة في الأزرار */
        font-weight: bold;
        font-size: 14px;
        padding: 6px 20px;
        border: none;
        border-radius: 8px;
        width: 100%;
        transition: background-color 0.3s ease;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin-bottom: 15px;
    }}

    .stButton > button:hover {{
        background-color: #7cd97c !important;
    }}

    .fixed-footer {{
        position: fixed;
        bottom: 12px; /* تعديل المسافة من الأسفل */
        left: 50%;
        transform: translateX(-50%);
        background-color: rgba(255, 255, 255, 0.85); /* خلفية شفافة */
        padding: 6px 16px; /* تقليل الحشو */
        font-size: 14px; /* حجم الخط */
        text-align: center;
        border-radius: 12px; /* زوايا مدورة */
        font-weight: bold;  /* جعل الكتابة غامقة في الفوتر */
        color: #222;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1); /* ظل مثل الزر */
        direction: rtl; /* جعل النص من اليمين إلى اليسار */
    }}

    .email-green {{
        color: #4CAF50;
        text-decoration: none;
        font-weight: 600;
    }}

    .heart-beat {{
        display: inline-block;
        animation: heartbeat 1.5s infinite;
    }}
    @keyframes heartbeat {{
        0% {{ transform: scale(1); }}
        25% {{ transform: scale(1.2); }}
        40% {{ transform: scale(1); }}
        60% {{ transform: scale(1.2); }}
        100% {{ transform: scale(1); }}
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# تطبيق التنسيق
set_background_and_style("Images/1.jpg")

# --- المحتوى الرئيسي ---
st.markdown("""
    <div class='overlay-text'>
        <div class='title'>
            WekelniS <span class='heart-beat'>💗🩺</span>
        </div>
        <div class='subtitle'>Système intelligent de nutrition pour les patients chroniques</div>
    </div>
""", unsafe_allow_html=True)

# --- أزرار التسجيل والدخول ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("###")
    if st.button("📝 Créer un nouveau compte"):
        st.switch_page("pages/Ajouter_Patient.py")
    if st.button("🔐 Se connecter"):
        st.switch_page("pages/connecter.py")

# --- الفوتر الاحترافي ---
st.markdown("""
    <div class="fixed-footer">
        📧 Contact: <a href="mailto:wekelni.contact@gmail.com" style="color:#4CAF50; text-decoration: none;">wekelni.contact@gmail.com</a>
        &nbsp;|&nbsp;
        📞 +213 661 23 45 67
    </div>
""", unsafe_allow_html=True)
