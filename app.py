import streamlit as st
import pandas as pd
import random

sheet_url = "https://docs.google.com/spreadsheets/d/1ztn3fdk38Qv9pNrtgplCaqqqB1uAOYEldEeFpnKS8fw/edit?usp=sharing"

# වචන මාලාව (තව වචන ඕන තරම් මෙතනට ඇඩ් කරපන්)
@st.cache_data # මේකෙන් කරන්නේ හැමතිස්සෙම sheet එක download නොකර data ටික මතක තියාගන්න එක
def load_data():
    df = pd.read_csv(sheet_url)
    # DataFrame එක dictionary list එකකට හරවනවා
    return df.to_dict('records')

# දැන් word_pool එකට ගන්නේ අර sheet එකේ data
if 'word_pool' not in st.session_state:
    st.session_state.word_pool = load_data()

st.set_page_config(page_title="Italy Challenge Pro", page_icon="🇮🇹")

# CSS පාවිච්චි කරලා බටන් වල පාට වෙනස් කරන විදිහ
st.markdown("""
    <style>
    div.stButton > button:first-child {
        height: 3em;
        font-size: 18px;
    }
    /* හරි උත්තරේ කොළ පාටට */
    .correct-btn {
        background-color: #28a745 !important;
        color: white !important;
    }
    /* වැරදි උත්තරේ රතු පාටට */
    .wrong-btn {
        background-color: #dc3545 !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Session States
if 'game_round' not in st.session_state:
    st.session_state.game_round = 0
    st.session_state.score = 0
    st.session_state.wrong_list = []
    st.session_state.is_retake_mode = False
    st.session_state.current_set = random.sample(st.session_state.word_pool, 10)
    st.session_state.selected_option = None
    st.session_state.is_answered = False

st.title("🇮🇹 Italy Master Challenge")

# Main Game
if st.session_state.game_round < len(st.session_state.current_set):
    curr_word = st.session_state.current_set[st.session_state.game_round]
    
    st.write(f"ප්‍රශ්නය: {st.session_state.game_round + 1} / {len(st.session_state.current_set)}")
    
    # Question Card
    st.markdown(f"""
        <div style="background-color: #f8f9fa; padding: 25px; border-radius: 15px; text-align: center; border-left: 10px solid #008C45; border-right: 10px solid #CD212A; margin-bottom: 20px;">
            <h1 style="color: #333; margin:0;">{curr_word['it']}</h1>
            <p style="color: #666;">({curr_word['pr']})</p>
        </div>
    """, unsafe_allow_html=True)

    # Options හදන එක (මෙතන තමයි කලින් වැරැද්ද හැදුවේ)
    if 'current_options' not in st.session_state:
        correct_ans = curr_word['si']
        # හරි එක නැතුව අනිත් ඒවගෙන් 3ක් ගන්නවා
        wrong_candidates = [w['si'] for w in st.session_state.word_pool if w['si'] != correct_ans]
        wrong_options = random.sample(wrong_candidates, 3)
        all_opts = wrong_options + [correct_ans]
        random.shuffle(all_opts)
        st.session_state.current_options = all_opts

    # බටන්ස් පෙන්වීම
    cols = st.columns(2)
    for i, opt in enumerate(st.session_state.current_options):
        with cols[i % 2]:
            # බටන් එකේ පාට තීරණය කිරීම
            button_key = f"btn_{st.session_state.game_round}_{opt}"
            
            if st.button(opt, use_container_width=True, key=button_key, disabled=st.session_state.is_answered):
                st.session_state.selected_option = opt
                st.session_state.is_answered = True
                
                if opt == curr_word['si']:
                    st.session_state.score += 1
                else:
                    if curr_word not in st.session_state.wrong_list:
                        st.session_state.wrong_list.append(curr_word)
                st.rerun()

    # පිළිතුර දුන් පසු Feedback එක පෙන්වීම
    if st.session_state.is_answered:
        if st.session_state.selected_option == curr_word['si']:
            st.success(f"නිවැරදියි! ✅")
        else:
            if st.session_state.is_retake_mode:
                st.error(f"වැරදියි! නිවැරදි පිළිතුර: {curr_word['si']} ❌")
            else:
                st.error(f"වැරදියි! ❌ \t\t නිවැරදි පිළිතුර: {curr_word['si']}")
        
        time.sleep(1.2) # Feedback එක පේන්න පොඩි වෙලාවක් දෙනවා
        
        # ඊළඟ ප්‍රශ්නයට යෑම
        st.session_state.game_round += 1
        st.session_state.is_answered = False
        st.session_state.selected_option = None
        if 'current_options' in st.session_state:
            del st.session_state.current_options
        st.rerun()

# Game Over / Retake Logic
else:
    if st.session_state.wrong_list:
        st.warning(f"වටය අවසන්! ඔබේ ලකුණු: {st.session_state.score}/10. වැරදුණු වචන {len(st.session_state.wrong_list)} නැවත පුහුණු වෙමු.")
        if st.button("වැරදුණු වචන නැවත කරන්න 🔄"):
            st.session_state.current_set = list(st.session_state.wrong_list)
            st.session_state.wrong_list = []
            st.session_state.game_round = 0
            st.session_state.score = 0
            st.session_state.is_retake_mode = True
            st.rerun()
    else:
        st.balloons()
        st.success("සුපිරිම තමයි! ඔබ සියල්ල නිවැරදිව කළා! 🏆")
        if st.button("අලුත් වටයක් පටන් ගන්න"):
            st.session_state.game_round = 0
            st.session_state.score = 0
            st.session_state.wrong_list = []
            st.session_state.is_retake_mode = False
            st.session_state.current_set = random.sample(st.session_state.word_pool, 10)
            st.rerun()