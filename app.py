import streamlit as st
import random

# Word Pool (Ona tharam wachana add karapan)
if 'word_pool' not in st.session_state:
    st.session_state.word_pool = [
        {"it": "Buongiorno", "pr": "බොන්ජෝර්නෝ", "si": "සුබ උදෑසනක්"},
        {"it": "Grazie", "pr": "ග්‍රාත්සියේ", "si": "ස්තූතියි"},
        {"it": "Prego", "pr": "ප්‍රේගෝ", "si": "කමක් නැහැ"},
        {"it": "Dov'è...?", "pr": "දොවේ", "si": "කොහේද...?"},
        {"it": "Acqua", "pr": "අක්ක්වා", "si": "වතුර"},
        {"it": "Ho fame", "pr": "ඕ ෆාමේ", "si": "බඩගිනියි"},
        {"it": "Lavoro", "pr": "ලවෝරෝ", "si": "වැඩ"},
        {"it": "Guasto", "pr": "ගුවාස්තෝ", "si": "කැඩිලා"},
        {"it": "Veloce", "pr": "වෙලෝචේ", "si": "වේගයෙන්"},
        {"it": "Piano", "pr": "පියානෝ", "si": "හෙමින්"}
    ]

st.set_page_config(page_title="Italy Learning Pro", page_icon="🇮🇹")

# Initialize Session States
if 'game_round' not in st.session_state:
    st.session_state.game_round = 0
    st.session_state.score = 0
    st.session_state.wrong_list = [] # Waraduna wachana methanata enawa
    st.session_state.is_retake_mode = False
    st.session_state.current_set = random.sample(st.session_state.word_pool, 10)
    st.session_state.selected_option = None

def next_question():
    st.session_state.game_round += 1
    st.session_state.selected_option = None
    if 'current_options' in st.session_state:
        del st.session_state.current_options

st.title("🇮🇹 Italy Master Challenge")

# Main Game Logic
if st.session_state.game_round < len(st.session_state.current_set):
    curr_word = st.session_state.current_set[st.session_state.game_round]
    
    st.write(f"Wachana: {st.session_state.game_round + 1} / {len(st.session_state.current_set)}")
    
    # Question Card
    st.markdown(f"""
        <div style="background-color: #f0f2f6; padding: 20px; border-radius: 15px; text-align: center; border-bottom: 5px solid #008C45;">
            <h1 style="margin:0;">{curr_word['it']}</h1>
            <p style="color: gray;">({curr_word['pr']})</p>
        </div>
    """, unsafe_allow_html=True)

    # Options Generation
    if 'current_options' not in st.session_state:
        correct = curr_word['si']
        others = [w['si'] for w in st.session_state.word_pool if w['si'] != correct]
        opts = random.sample(others, 3) + [correct]
        random.shuffle(opts)
        st.session_state.current_options = opts

    st.write("")
    
    # Buttons with Colors
    for opt in st.session_state.current_options:
        btn_type = "secondary"
        if st.session_state.selected_option == opt:
            btn_type = "primary" if opt == curr_word['si'] else "secondary"
            
        # Custom logic for colors using Streamlit buttons (simplest way)
        if st.button(opt, use_container_width=True, key=f"btn_{opt}"):
            st.session_state.selected_option = opt
            if opt == curr_word['si']:
                st.success("Hari! ✅")
                st.session_state.score += 1
                st.button("Mita passe ➡️", on_click=next_question)
            else:
                st.error("Waradiyi! ❌")
                if curr_word not in st.session_state.wrong_list:
                    st.session_state.wrong_list.append(curr_word)
                st.button("Mita passe ➡️", on_click=next_question)

# Game Over / Retake Mode
else:
    if st.session_state.wrong_list:
        st.warning(f"Iwarayi! Umbata 10n {st.session_state.score}k hari. Dan waraduna {len(st.session_state.wrong_list)}ta ayeth try karamu.")
        if st.button("Waraduna ewa ayeth karanna"):
            st.session_state.current_set = list(st.session_state.wrong_list)
            st.session_state.wrong_list = []
            st.session_state.game_round = 0
            st.session_state.score = 0
            st.session_state.is_retake_mode = True # Meeta passe waradunoth uththare pennanawa
            st.rerun()
    else:
        st.balloons()
        st.success("Supiri! Okkoma hari machan. Dan umba ready!")
        if st.button("Aluth watawak (Restart)"):
            del st.session_state.game_round
            st.rerun()