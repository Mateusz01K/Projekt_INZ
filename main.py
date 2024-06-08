import os.path

import pandas as pd
import streamlit as st
import joblib
from auth import register_user, login_user

model = joblib.load(r"C:\Users\mateu\PycharmProjects\ProjektAnalizaEmocji\emotion_detection_model.pkl")

emotions_index = {0: "anger", 2: "happy", 4: "neutral", 3: "joy", 6: "sadness", 1: "fear", 5: "sad", 7: "shame"}
emotions = {0: "😠", 2: "😀", 4: "🙂", 3: "😁", 6: "😢", 1: "😨", 5: "😔", 7: "☹️"}



def predict_emotions(text):
    probabilities = model.predict_proba([text])[0]
    max_prob_index = probabilities.argmax()
    max_prob_emotion = emotions_index[max_prob_index]
    return max_prob_emotion, probabilities[max_prob_index]*100


POST_FILE = 'post.csv'

def load_post():
    if os.path.exists(POST_FILE):
        return pd.read_csv(POST_FILE)
    else:
        return pd.DataFrame(columns=['username', 'text', 'emotion'])

def save_post(username, text, emotion, selected_emotion):
    posts_df = load_post()
    new_post = pd.DataFrame([[username, f"{text} {selected_emotion}", emotion]], columns=['username', 'text', 'emotion'])
    posts_df = pd.concat([posts_df, new_post], ignore_index=True)
    posts_df.to_csv(POST_FILE, index=False)

def delete_post(post_index):
    posts_df = load_post()
    posts_df = posts_df.drop(index=post_index)
    posts_df.to_csv(POST_FILE, index=False)

def show_registration_page():
    st.title("Registration")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        if register_user(username, password):
            st.success("Registration is successful!")
        else:
            st.error("Username just exists!")


def show_login_page():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Sign in"):
        if login_user(username, password):
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.session_state['is_admin'] = (username == "admin")
            st.experimental_rerun()
        else:
            st.error("Invalid username or password!")


def show_main_page():
    st.title("Analyze emotions")
    st.write(f"Logged as: {st.session_state['username']}")

    text_input = st.text_area("Enter text:")
    selected_emotions = st.selectbox("Select emoji: ", list(emotions.values()))

    if st.button("Analyze and Post"):
        if text_input:
            emotion, probabilities = predict_emotions(text_input)
            save_post(st.session_state['username'], text_input, emotion, selected_emotions)
            st.write(f"The most likely emotion: {emotion}")
            st.write(f"Confidence percentage: {probabilities:2f}%")
        else:
            st.write("Enter text before analysis!")

    if st.button("Sign out"):
        st.session_state['logged_in'] = False
        st.experimental_rerun()

    st.write('### All posts')
    posts_df = load_post()
    for index, row in posts_df.iterrows():
        st.write(f"**{row['username']}**: {row['text']} - _{row['emotion']}_")

        st.session_state[f"Delete post {index}"] = False

        if st.session_state.get('is_admin', False):
            if st.button(f"Delete post {index}"):
                delete_post(index)
                st.success("Post has been deleted!")
                st.experimental_rerun()

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if st.session_state['logged_in']:
    show_main_page()
else:
    login_or_register = st.sidebar.selectbox("Login/Registration", ("Sign in", "Registration"))
    if login_or_register == "Sign in":
        show_login_page()
    else:
        show_registration_page()