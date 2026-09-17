import streamlit as st
from supabase import create_client

# Access secure cloud variables
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def register_user(email, password):
    try:
        res = supabase.auth.sign_up({"email": email, "password": password})
        if res.user:
            return res.user, None
        return None, "Registration failed."
    except Exception as e:
        return None, str(e)

def login_user(email, password):
    try:
        res = supabase.auth.sign_in_with_password({"email": email, "password": password})
        if res.user:
            return res.user, None
        return None, "Invalid login credentials."
    except Exception as e:
        return None, str(e)

def save_chat_message(user_id, role, content, image_url=None):
    try:
        supabase.table("chat_history").insert({
            "user_id": user_id,
            "role": role,
            "content": content,
            "image_url": image_url
        }).execute()
    except Exception as e:
        print(f"Error saving message: {e}")

def load_chat_history(user_id):
    try:
        res = supabase.table("chat_history").select("*").eq("user_id", user_id).order("created_at").execute()
        return res.data
    except Exception as e:
        print(f"Error loading history: {e}")
        return []
