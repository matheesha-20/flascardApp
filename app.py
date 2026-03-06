import streamlit as st
import random
import time

# වචන මාලාව
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

st.set_page_config(page_title="ඉතාලි ඉගෙනගමු", page_icon="🇮🇹")

# Session States Initialize කිරීම
if 'game_round' not in st.session_state:
    st.session_state.game_round = 0
    st.session_state.score = 0
    st.session_state.wrong_list = []
    st.session_state.is_retake_mode = False
    st.session_state.current_set = random.sample(st.session_state.word_pool, 10)
    st.session_state.answered = False
    st.session_state.feedback = None

st.title("🇮🇹 ඉතාලි භාෂා අභියෝගය")

# ප්‍රශ්න පෙන්වීමේ Logic එක
if st.session_state.game_round < len(st.session_state.current_set):
    curr_word = st.session_state.current_set[st.session_state.game_round]
    
    st.subheader(f"ප්‍රශ්න: {st.session_state.game_round + 1} / {len(st.session_state.current_set)}")
    
    # වචනය පෙන්වන Card එක
    st.markdown(f"""
        <div style="background-color: #f0f2f6; padding: 30px; border-radius: 15px; text-align: center; border-bottom: 5px solid #008C45;">
            <h1 style="margin:0; color: #333;">{curr_word['it']}</h1>
            <p style="color: #666; font-size: 1.2em;">({curr_word['pr']})</p>
        </div>
    """, unsafe_allow_html=True)

    # Options හදන එක
    if 'current_options' not in st.session_state:
        correct = curr_word['si']
        others = [w['si'] for w in st.session_state.word_pool if w['si'] != correct]
        opts = random.sample(others, 3) + [correct]
        random.shuffle(opts)
        st.session_state.current_options = opts

    st.write("")

    # බටන්ස් පෙන්වීම
    for opt in st.session_state.current_options:
        if st.button(opt, use_container_width=True, key=f"{st.session_state.game_round}_{opt}"):
            if opt == curr_word['si']:
                st.session_state.feedback = "success"
                st.session_state.score += 1
            else:
                st.session_state.feedback = "error"
                if curr_word not in st.session_state.wrong_list:
                    st.session_state.wrong_list.append(curr_word)
            
            st.session_state.answered = True
            st.rerun()

    # හරි/වැරදි Feedback එක පෙන්වීම
    if st.session_state.answered:
        if st.session_state.feedback == "success":
            st.success("නිවැරදියි! ✅")
        else:
            if st.session_state.is_retake_mode:
                st.error(f"වැරදියි! නිවැරදි පිළිතුර: {curr_word['si']} ❌")
            else:
                st.error("වැරදියි! ❌")
        
        time.sleep(1) # තත්පරයක් ඉන්නවා feedback එක බලන්න
        st.session_state.game_round += 1
        st.session_state.answered = False
        if 'current_options' in st.session_state:
            del st.session_state.current_options
        st.rerun()

# ක්‍රීඩාව අවසානය
else:
    if st.session_state.wrong_list:
        st.warning(f"අවසන්! ඔබ 10න් {st.session_state.score}ක් නිවැරදිව කළා. දැන් වැරදුණු {len(st.session_state.wrong_list)} නැවත උත්සාහ කරමු.")
        if st.button("වැරදුණු වචන නැවත කරන්න"):
            st.session_state.current_set = list(st.session_state.wrong_list)
            st.session_state.wrong_list = []
            st.session_state.game_round = 0
            st.session_state.score = 0
            st.session_state.is_retake_mode = True
            st.rerun()
    else:
        st.balloons()
        st.success("සුපිරි! ඔබ සියල්ල නිවැරදිව සම්පූර්ණ කළා! 🏆")
        if st.button("මුල සිට ආරම්භ කරන්න"):
            st.session_state.game_round = 0
            st.session_state.score = 0
            st.session_state.wrong_list = []
            st.session_state.is_retake_mode = False
            st.session_state.current_set = random.sample(st.session_state.word_pool, 10)
            st.rerun()