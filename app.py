import streamlit as st
import pandas as pd
import random
import time

# --- වැදගත්: මෙතනට ඔයා Publish කරලා ගත්ත CSV Link එක දාන්න ---
sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQEYl7N7muoi3zY5fgFDBWo8gPrNKJvj8sJQQYmm-nAyF1qE6DMgl2a3cuNsbbrzPMIht-JervgZkMn/pub?output=csv"

@st.cache_data(ttl=600) 
def load_data():
    try:
        # ලින්ක් එකෙන් CSV එක කියවනවා
        df = pd.read_csv(sheet_url)
        # column names වල තියෙන හිස්තැන් අයින් කරනවා
        df.columns = df.columns.str.strip()
        return df.to_dict('records')
    except Exception as e:
        st.error(f"දත්ත ලබාගැනීමේ දෝෂයක්: {e}")
        return []

# දත්ත මුලින්ම ලෝඩ් කරගන්නවා
words = load_data()

st.set_page_config(page_title="Italy Challenge Pro", page_icon="🇮🇹")

# දත්ත නැත්නම් ඇප් එක නවත්වනවා
if not words:
    st.warning("Google Sheet එකෙන් දත්ත ලැබුණේ නැහැ. කරුණාකර 'Publish to Web' කරලා CSV ලින්ක් එක නිවැරදිව දාන්න.")
    st.stop()

if 'word_pool' not in st.session_state:
    st.session_state.word_pool = words

# --- Session States ---
if 'game_round' not in st.session_state:
    st.session_state.game_round = 0
    st.session_state.score = 0
    st.session_state.wrong_list = []
    st.session_state.is_retake_mode = False
    st.session_state.current_set = random.sample(st.session_state.word_pool, min(len(st.session_state.word_pool), 10))
    st.session_state.is_answered = False

# CSS (කලින් තිබුණු එකමයි)
st.markdown("""
    <style>
    div.stButton > button:first-child { height: 3em; font-size: 18px; }
    </style>
""", unsafe_allow_html=True)

st.title("🇮🇹 Italy Master Challenge")

# Main Game Logic
if st.session_state.game_round < len(st.session_state.current_set):
    curr_word = st.session_state.current_set[st.session_state.game_round]
    
    st.write(f"ප්‍රශ්නය: {st.session_state.game_round + 1} / {len(st.session_state.current_set)}")
    
    # Question Card (KeyError නොවෙන්න Check කරලා තියෙන්නේ)
    it_word = curr_word.get('it', 'N/A')
    pr_word = curr_word.get('pr', '')
    si_word = curr_word.get('si', 'N/A')

    st.markdown(f"""
        <div style="background-color: #f8f9fa; padding: 25px; border-radius: 15px; text-align: center; border-left: 10px solid #008C45; border-right: 10px solid #CD212A; margin-bottom: 20px;">
            <h1 style="color: #333; margin:0;">{it_word}</h1>
            <p style="color: #666;">({pr_word})</p>
        </div>
    """, unsafe_allow_html=True)

    # Options සෑදීම
    if 'current_options' not in st.session_state:
        correct_ans = si_word
        wrong_candidates = [w.get('si', 'N/A') for w in st.session_state.word_pool if w.get('si') != correct_ans]
        wrong_options = random.sample(wrong_candidates, min(len(wrong_candidates), 3))
        all_opts = wrong_options + [correct_ans]
        random.shuffle(all_opts)
        st.session_state.current_options = all_opts

    # බටන් පෙන්වීම සහ අනෙක් Logic ටික (ඔයාගේ කලින් කෝඩ් එකමයි)
    cols = st.columns(2)
    for i, opt in enumerate(st.session_state.current_options):
        with cols[i % 2]:
            if st.button(opt, use_container_width=True, key=f"btn_{st.session_state.game_round}_{opt}", disabled=st.session_state.is_answered):
                st.session_state.selected_option = opt
                st.session_state.is_answered = True
                if opt == si_word:
                    st.session_state.score += 1
                else:
                    if curr_word not in st.session_state.wrong_list:
                        st.session_state.wrong_list.append(curr_word)
                st.rerun()

    if st.session_state.is_answered:
        if st.session_state.selected_option == si_word:
            st.success("නිවැරදියි! ✅")
        else:
            st.error(f"වැරදියි! ❌ නිවැරදි පිළිතුර: {si_word}")
        
        time.sleep(1.2)
        st.session_state.game_round += 1
        st.session_state.is_answered = False
        if 'current_options' in st.session_state: del st.session_state.current_options
        st.rerun()

else:
    # Game Over Logic (කලින් තිබුණු එකමයි)
    st.balloons()
    st.success(f"වටය අවසන්! ලකුණු: {st.session_state.score}/{len(st.session_state.current_set)}")
    if st.button("නැවත ආරම්භ කරන්න"):
        st.session_state.game_round = 0
        st.session_state.score = 0
        st.session_state.wrong_list = []
        st.session_state.current_set = random.sample(st.session_state.word_pool, 10)
        st.rerun()