import streamlit as st
import auth_handler as auth
import chatbot_engine as ai

st.set_page_config(page_title="Universal Tech Chatbot", page_icon="🤖", layout="wide")

# Persistent State Variables
if "user" not in st.session_state:
    st.session_state.user = None

# Custom CSS styling for beautiful cross-device UI
st.markdown("""
<style>
    .main .block-container { padding-top: 2rem; max-width: 900px; }
    [data-testid="stSidebar"] { min-width: 300px; }
</style>
""", unsafe_allow_html=True)

# --- ACCOUNT SELECTION SIDEBAR ---
with st.sidebar:
    st.title("🔐 User Accounts")
    if not st.session_state.user:
        auth_action = st.radio("Access Level", ["Login", "Sign Up"])
        email = st.text_input("Email Adress")
        password = st.text_input("Password", type="password")
        
        if st.button(auth_action, use_container_width=True):
            if auth_action == "Login":
                user, err = auth.login_user(email, password)
                if user:
                    st.session_state.user = user
                    st.rerun()
                else: st.error(err)
            else:
                user, err = auth.register_user(email, password)
                if user: st.success("Account created successfully! Please switch to Login.")
                else: st.error(err)
    else:
        st.success(f"Logged in: {st.session_state.user.email}")
        if st.button("Log Out", use_container_width=True):
            st.session_state.user = None
            st.rerun()

# --- CHAT WRAPPER MAIN PANEL ---
st.title("🤖 Multi-Device Technical AI Chatbot")
st.write("Ask any tech query. The AI automatically builds simplified explanations and adds structural imagery!")

if st.session_state.user:
    uid = st.session_state.user.id
    history = auth.load_chat_history(uid)
    
    # Render prior messaging logs
    for msg in history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            if msg.get("image_url"):
                st.image(msg["image_url"])
                
    # Await real-time interaction inputs
    if user_input := st.chat_input("Ex: Explain quantum computing / How do fiber optic cables work? (Show diagram)"):
        with st.chat_message("user"):
            st.write(user_input)
        auth.save_chat_message(uid, "user", user_input)
        
        # Refresh log arrays to include newly provided string
        current_logs = auth.load_chat_history(uid)
        
        with st.chat_message("assistant"):
            with st.spinner("Analyzing architecture..."):
                reply, img_url = ai.get_ai_response(user_input, current_logs)
                st.write(reply)
                if img_url:
                    st.image(img_url)
                    
        auth.save_chat_message(uid, "assistant", reply, img_url)
else:
    st.info("⚠️ Please sign up or log in via the left sidebar to unlock the chatbot dashboard and track your session history.")
