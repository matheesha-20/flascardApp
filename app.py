import streamlit as st
import random

# Factory එකේදී ඕන වෙන වචන සෙට් එක
data = [
    {"it": "Lavoro", "en": "Work", "si": "වැඩ"},
    {"it": "Macchina", "en": "Machine", "si": "මැෂින් එක"},
    {"it": "Valvola", "en": "Valve", "si": "වෑල්ව් එක"},
    {"it": "Attrezzi", "en": "Tools", "si": "උපකරණ"},
    {"it": "Pezzi", "en": "Parts", "si": "කෑලි"},
    {"it": "Veloce", "en": "Fast", "si": "වේගයෙන්"},
    {"it": "Piano", "en": "Slow", "si": "හෙමින්"},
    {"it": "Guasto", "en": "Broken", "si": "කැඩිලා"},
    {"it": "Pericolo", "en": "Danger", "si": "අන්තරාය"},
    {"it": "Sicurezza", "en": "Safety", "si": "ආරක්ෂාව"},
    {"it": "Accendere", "en": "Turn on", "si": "පණගන්වන්න"},
    {"it": "Spegnere", "en": "Turn off", "si": "නිවා දමන්න"},
]

st.set_page_config(page_title="Italy Helper", page_icon="🇮🇹")

st.title("🇮🇹 Italy Flashcards")
st.write("වචනය මතකද බලලා තේරුම චෙක් කරන්න.")

# Session state එක පාවිච්චි කරන්නේ වචනය මාරු වුණත් මතක තියාගන්න
if 'index' not in st.session_state:
    st.session_state.index = random.randint(0, len(data)-1)
    st.session_state.show_answer = False

current_word = data[st.session_state.index]

# Display Card
st.markdown(f"""
<div style="background-color: #f0f2f6; padding: 30px; border-radius: 15px; text-align: center; border: 2px solid #008C45;">
    <h2 style="color: #CD212A;">{current_word['it']}</h2>
</div>
""", unsafe_allow_html=True)

if st.button("Show Meaning / තේරුම බලන්න"):
    st.session_state.show_answer = True

if st.session_state.show_answer:
    st.success(f"🇬🇧 English: {current_word['en']}")
    st.info(f"🇱🇰 Sinhala: {current_word['si']}")

if st.button("Next Word / ඊළඟ වචනය"):
    st.session_state.index = random.randint(0, len(data)-1)
    st.session_state.show_answer = False
    st.rerun()