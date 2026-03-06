import streamlit as st
import random

# වචන මාලාව (Factory + Daily Use)
if 'word_pool' not in st.session_state:
    st.session_state.word_pool = [
        {"it": "Buongiorno", "pr": "බොන්ජෝර්නෝ", "si": "සුබ උදෑසනක්"},
        {"it": "Come stai?", "pr": "කොමේ ස්තායි", "si": "කොහොමද සැප දුක්?"},
        {"it": "Grazie", "pr": "ග්‍රාත්සියේ", "si": "ස්තූතියි"},
        {"it": "Prego", "pr": "ප්‍රේගෝ", "si": "සාදරයෙන් පිළිගනිමි / කමක් නැහැ"},
        {"it": "Dov'è...?", "pr": "දොවේ", "si": "කොහේද...?"},
        {"it": "Quanto costa?", "pr": "ක්වන්තෝ කොස්තා", "si": "ගණන කීයද?"},
        {"it": "Acqua", "pr": "අක්ක්වා", "si": "වතුර"},
        {"it": "Pane", "pr": "පානේ", "si": "පාන්"},
        {"it": "Andiamo", "pr": "අන්ඩියාමෝ", "si": "යමු"},
        {"it": "Ho fame", "pr": "ඕ ෆාමේ", "si": "මට බඩගිනියි"},
        {"it": "Lavoro", "pr": "ලවෝරෝ", "si": "වැඩ"},
        {"it": "Macchina", "pr": "මක්කිනා", "si": "මැෂින් එක"},
        {"it": "Valvola", "pr": "වල්වොලා", "si": "වෑල්ව් එක"},
        {"it": "Pezzi", "pr": "පෙත්සි", "si": "කෑලි"},
        {"it": "Guasto", "pr": "ගුවාස්තෝ", "si": "කැඩිලා"},
        {"it": "Veloce", "pr": "වෙලෝචේ", "si": "වේගයෙන්"},
        {"it": "Piano", "pr": "පියානෝ", "si": "හෙමින්"},
        {"it": "Sinistra", "pr": "සිනිස්ත්‍රා", "si": "වම"},
        {"it": "Destra", "pr": "දෙස්ත්‍රා", "si": "දකුණ"},
        {"it": "Aiuto", "pr": "අයූතෝ", "si": "උදව්"}
    ]

st.set_page_config(page_title="Italy 10-Step Challenge", page_icon="🇮🇹")

# Game State පවත්වා ගැනීම
if 'game_round' not in st.session_state:
    st.session_state.game_round = 1  # වචන 10න් කීවෙනි එකද?
    st.session_state.score = 0
    st.session_state.game_over = False
    # මේ වටයට වචන 10ක් අහඹු ලෙස තෝරාගන්නවා
    st.session_state.current_set = random.sample(st.session_state.word_pool, 10)

def reset_game():
    st.session_state.game_round = 1
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.current_set = random.sample(st.session_state.word_pool, 10)
    st.rerun()

st.title("🇮🇹 Italy 10-Word Challenge")

if not st.session_state.game_over:
    # දැනට තියෙන වචනය
    current_word = st.session_state.current_set[st.session_state.game_round - 1]
    
    # Progress Bar
    st.write(f"ප්‍රශ්නය: {st.session_state.game_round} / 10")
    st.progress(st.session_state.game_round / 10)

    # Display Card
    st.markdown(f"""
    <div style="background-color: #f0f2f6; padding: 25px; border-radius: 15px; text-align: center; border-left: 10px solid #008C45; border-right: 10px solid #CD212A;">
        <h1 style="color: #333; margin:0;">{current_word['it']}</h1>
        <p style="color: #666; font-size: 1.2em;">({current_word['pr']})</p>
    </div>
    """, unsafe_allow_html=True)

    # Options 4ක් සෑදීම
    if 'current_options' not in st.session_state:
        correct = current_word['si']
        others = [w['si'] for w in st.session_state.word_pool if w['si'] != correct]
        wrong_options = random.sample(others, 3)
        all_opts = wrong_options + [correct]
        random.shuffle(all_opts)
        st.session_state.current_options = all_opts

    # Buttons පෙන්වීම
    cols = st.columns(2)
    for i, opt in enumerate(st.session_state.current_options):
        with cols[i % 2]:
            if st.button(opt, use_container_width=True, key=opt):
                if opt == current_word['si']:
                    st.toast("නියමයි! ✅", icon="🎉")
                    st.session_state.score += 1
                else:
                    st.toast(f"වැරදියි! නිවැරදි: {current_word['si']} ❌")
                
                # ඊළඟ වටයට සූදානම් වීම
                if st.session_state.game_round < 10:
                    st.session_state.game_round += 1
                    del st.session_state.current_options
                    st.rerun()
                else:
                    st.session_state.game_over = True
                    st.rerun()

else:
    # Game Over Screen
    st.balloons()
    st.success(f"වැඩේ ඉවරයි! ලකුණු සංඛ්‍යාව: {st.session_state.score} / 10")
    
    if st.session_state.score == 10:
        st.write("🔥ඔක්කොම හරි!")
    elif st.session_state.score > 5:
        st.write("හොඳයි, තව ටිකක් ට්‍රයි කරමු!")
    else:
        st.write("කමක් නැහැ, ආයෙත් කරලා බලමුද?")

    if st.button("අලුත් වටයක් පටන් ගන්න (New Words)"):
        reset_game()