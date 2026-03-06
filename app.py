import streamlit as st
import random

# Wachana list eka
if 'word_pool' not in st.session_state:
    st.session_state.word_pool = [
        {"it": "Lavoro", "pr": "ලවෝරෝ", "si": "වැඩ"},
        {"it": "Macchina", "pr": "මක්කිනා", "si": "මැෂින් එක"},
        {"it": "Valvola", "pr": "වල්වොලා", "si": "වෑල්ව් එක"},
        {"it": "Guasto", "pr": "ගුවාස්තෝ", "si": "කැඩිලා"},
        {"it": "Sicurezza", "pr": "සිකුරෙත්සා", "si": "ආරක්ෂාව"},
        {"it": "Veloce", "pr": "වෙලෝචේ", "si": "වේගයෙන්"},
        {"it": "Piano", "pr": "පියානෝ", "si": "හෙමින්"},
        {"it": "Destra", "pr": "දෙස්ත්‍රා", "si": "දකුණ"},
        {"it": "Sinistra", "pr": "සිනිස්ත්‍රා", "si": "වම"},
        {"it": "Aiuto", "pr": "අයූතෝ", "si": "උදව්"},
    ]

# Game state
if 'current_set' not in st.session_state:
    st.session_state.current_set = random.sample(st.session_state.word_pool, 10)
    st.session_state.round = 0
    st.session_state.score = 0
    st.session_state.wrong_attempts = 0 # Thawa chance ekak denna
    st.session_state.answered = False
    st.session_state.result_color = {} # Button colors manage karanna

# UI layout
st.title("🇮🇹 Italy 10-Step Challenge")

if st.session_state.round < 10:
    curr = st.session_state.current_set[st.session_state.round]
    st.subheader(f"Round: {st.session_state.round + 1}/10")
    st.markdown(f"## {curr['it']} ({curr['pr']})")

    # Options hadaganna
    if 'opts' not in st.session_state:
        correct = curr['si']
        others = [w['si'] for w in st.session_state.word_pool if w['si'] != correct]
        st.session_state.opts = random.sample(others, 3) + [correct]
        random.shuffle(st.session_state.opts)

    for opt in st.session_state.opts:
        # Button color logic
        color = st.session_state.result_color.get(opt, "secondary")
        if st.button(opt, type=color, use_container_width=True):
            if opt == curr['si']:
                st.session_state.result_color = {opt: "primary"} # Kola (Primary in streamlit)
                st.session_state.answered = True
                st.session_state.score += 1
            else:
                st.session_state.result_color = {opt: "secondary"} # Waradi button eka disable wage karanna
                st.session_state.wrong_attempts += 1
                if st.session_state.wrong_attempts >= 1: # 2nd chance eka
                    st.error(f"Waradi! Hari uththare: {curr['si']}")
                    st.session_state.answered = True
                else:
                    st.warning("Waradi! Thawa chance ekak thiyanawa.")

    if st.session_state.answered:
        if st.button("Next ➡️"):
            st.session_state.round += 1
            st.session_state.answered = False
            st.session_state.wrong_attempts = 0
            st.session_state.result_color = {}
            del st.session_state.opts
            st.rerun()
else:
    st.success(f"Game Over! Score: {st.session_state.score}/10")
    if st.button("Restart"):
        st.session_state.current_set = random.sample(st.session_state.word_pool, 10)
        st.session_state.round = 0
        st.session_state.score = 0
        st.rerun()