import streamlit as st
import random

# වචන මාලාව
data = [
    {"it": "Lavoro", "si": "වැඩ"},
    {"it": "Macchina", "si": "මැෂින් එක"},
    {"it": "Valvola", "si": "වෑල්ව් එක"},
    {"it": "Attrezzi", "si": "උපකරණ"},
    {"it": "Pezzi", "si": "කෑලි"},
    {"it": "Veloce", "si": "වේගයෙන්"},
    {"it": "Piano", "si": "හෙමින්"},
    {"it": "Guasto", "si": "කැඩිලා"},
    {"it": "Pericolo", "si": "අන්තරාය"},
    {"it": "Sicurezza", "si": "ආරක්ෂාව"},
    {"it": "Accendere", "si": "පණගන්වන්න"},
    {"it": "Spegnere", "si": "නිවා දමන්න"},
]

st.set_page_config(page_title="Italy Quiz", page_icon="🇮🇹")

st.title("🇮🇹 Italy Word Quiz")

# Session state පවත්වා ගැනීම
if 'index' not in st.session_state or 'options' not in st.session_state:
    st.session_state.index = random.randint(0, len(data)-1)
    
    # හරි උත්තරයයි, තව වැරදි උත්තරයකුයි තෝරගන්නවා
    correct_ans = data[st.session_state.index]['si']
    wrong_ans = random.choice([item['si'] for item in data if item['si'] != correct_ans])
    
    opts = [correct_ans, wrong_ans]
    random.shuffle(opts) # Shuffle කරනවා උත්තර දෙක මාරු වෙන්න
    st.session_state.options = opts
    st.session_state.answered = False

current_word = data[st.session_state.index]

# ඉතාලි වචනය පෙන්වන Card එක
st.markdown(f"""
<div style="background-color: #f0f2f6; padding: 30px; border-radius: 15px; text-align: center; border: 2px solid #008C45; margin-bottom: 20px;">
    <h1 style="color: #CD212A; margin:0;">{current_word['it']}</h1>
    <p style="color: #555;">මේකේ තේරුම මොකක්ද?</p>
</div>
""", unsafe_allow_html=True)

# Options පෙන්වීම
for option in st.session_state.options:
    if st.button(option, use_container_width=True):
        st.session_state.answered = True
        st.session_state.selected = option

# උත්තරය පරීක්ෂා කිරීම
if st.session_state.answered:
    if st.session_state.selected == current_word['si']:
        st.success(f"නියමයි! ' {current_word['it']} ' කියන්නේ '{current_word['si']}' තමයි. ✅")
    else:
        st.error(f"වැරදියි! නිවැරදි තේරුම: {current_word['si']} ❌")
    
    if st.button("ඊළඟ වචනය ➡️"):
        # Reset කරලා අලුත් වචනයක් ගන්නවා
        del st.session_state.index
        del st.session_state.options
        st.rerun()