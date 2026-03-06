import streamlit as st
import pandas as pd
import random
import time

# Google Sheet Link (CSV)
sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQEYl7N7muoi3zY5fgFDBWo8gPrNKJvj8sJQQYmm-nAyF1qE6DMgl2a3cuNsbbrzPMIht-JervgZkMn/pub?output=csv"

@st.cache_data(ttl=600) 
def load_data():
    try:
        df = pd.read_csv(sheet_url)
        df.columns = df.columns.str.strip()
        return df.to_dict('records')
    except Exception as e:
        st.error(f"දත්ත ලබාගැනීමේ දෝෂයක්: {e}")
        return []

words = load_data()

st.set_page_config(page_title="Italy Challenge Pro", page_icon="🇮🇹")

if not words:
    st.warning("දත්ත ලැබුණේ නැහැ. කරුණාකර Link එක පරීක්ෂා කරන්න.")
    st.stop()

if 'word_pool' not in st.session_state:
    st.session_state.word_pool = words

# --- Session States ---
if 'game_round' not in st.session_state:
    st.session_state.game_round = 0
    st.session_state.score = 0
    st.session_state.current_set = random.sample(st.session_state.word_pool, min(len(st.session_state.word_pool), 10))
    st.session_state.is_answered = False
    st.session_state.show_retry = False # වැරදුණොත් Retry පෙන්වන්න

st.title("🇮🇹 Italy Master Challenge")

if st.session_state.game_round < len(st.session_state.current_set):
    curr_word = st.session_state.current_set[st.session_state.game_round]
    
    st.write(f"ප්‍රශ්නය: {st.session_state.game_round + 1} / 10")
    
    it_word = curr_word.get('it', 'N/A')
    pr_word = curr_word.get('pr', '')
    si_word = curr_word.get('si', 'N/A')

    st.markdown(f"""
        <div style="background-color: #f8f9fa; padding: 25px; border-radius: 15px; text-align: center; border-left: 10px solid #008C45; border-right: 10px solid #CD212A; margin-bottom: 20px;">
            <h1 style="color: #333; margin:0;">{it_word}</h1>
            <p style="color: #666;">({pr_word})</p>
        </div>
    """, unsafe_allow_html=True)

    if 'current_options' not in st.session_state:
        correct_ans = si_word
        wrong_candidates = [w.get('si', 'N/A') for w in st.session_state.word_pool if w.get('si') != correct_ans]
        wrong_options = random.sample(wrong_candidates, 3)
        all_opts = wrong_options + [correct_ans]
        random.shuffle(all_opts)
        st.session_state.current_options = all_opts

    # බටන්ස්
    cols = st.columns(2)
    for i, opt in enumerate(st.session_state.current_options):
        with cols[i % 2]:
            # පිළිතුරක් දීල නම් බටන් ටික Disable කරනවා (Retry වෙලාවේදී ඇරෙන්න)
            is_disabled = st.session_state.is_answered and not st.session_state.show_retry
            
            if st.button(opt, use_container_width=True, key=f"btn_{st.session_state.game_round}_{opt}", disabled=is_disabled):
                if opt == si_word:
                    st.session_state.is_answered = True
                    st.session_state.show_retry = False
                    st.success("නිවැරදියි! ✅")
                    time.sleep(1)
                    st.session_state.score += 1
                    st.session_state.game_round += 1
                    st.session_state.is_answered = False
                    if 'current_options' in st.session_state: del st.session_state.current_options
                    st.rerun()
                else:
                    st.error("වැරදියි! ❌ නැවත උත්සාහ කරන්න.")
                    st.session_state.show_retry = True

else:
    st.balloons()
    st.success(f"වටය අවසන්! ඔබේ ලකුණු: {st.session_state.score}/10")
    if st.button("අලුත් වටයක් ආරම්භ කරන්න"):
        st.session_state.game_round = 0
        st.session_state.score = 0
        st.session_state.current_set = random.sample(st.session_state.word_pool, 10)
        st.rerun()