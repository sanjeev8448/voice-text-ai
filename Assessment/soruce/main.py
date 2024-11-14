import os
import sqlite3
import bcrypt
import streamlit as st
import sounddevice as sd
import numpy as np
import speech_recognition as sr
from gtts import gTTS
from googletrans import LANGUAGES, Translator

# Initialize Translator
translator = Translator()

# Database setup
conn = sqlite3.connect("users.db")
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (
             username TEXT PRIMARY KEY,
             password BLOB)''')
conn.commit()

# Utility functions for password hashing
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed)

# Signup function
def signup(username, password):
    hashed_password = hash_password(password)
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

# Login function
def login(username, password):
    c.execute("SELECT password FROM users WHERE username = ?", (username,))
    record = c.fetchone()
    if record and check_password(password, record[0]):
        return True
    return False

# Main translation function
def translator_function(spoken_text, from_language, to_language):
    return translator.translate(spoken_text, src=from_language, dest=to_language)

# Voice playback function
def text_to_voice(text_data, to_language):
    myobj = gTTS(text=text_data, lang=to_language, slow=False)
    myobj.save("cache_file.mp3")
    audio_file = open("cache_file.mp3", "rb")
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format="audio/mp3")
    audio_file.close()
    os.remove("cache_file.mp3")

# Session state for tracking authentication status
if "is_authenticated" not in st.session_state:
    st.session_state["is_authenticated"] = False

# Authentication Page
st.title("Voice-to-Text with Generative AI with User Authentication")

if st.session_state["is_authenticated"]:
    st.sidebar.button("Logout", on_click=lambda: st.session_state.update({"is_authenticated": False}))
    
    # Translator app UI
    st.subheader("Real-Time Language Translator")

    # Dropdowns for selecting languages
    from_language_name = st.selectbox("Select Source Language:", list(LANGUAGES.values()))
    to_language_name = st.selectbox("Select Target Language:", list(LANGUAGES.values()))

    # Convert language names to language codes
    from_language = list(LANGUAGES.keys())[list(LANGUAGES.values()).index(from_language_name)]
    to_language = list(LANGUAGES.keys())[list(LANGUAGES.values()).index(to_language_name)]

    # Real-time transcript placeholders
    st.subheader("Original Transcript")
    original_placeholder = st.empty()

    st.subheader("Translated Transcript")
    translated_placeholder = st.empty()

    # Start listening and translating on button click
    start_button = st.button("Start")

    if start_button:
        rec = sr.Recognizer()

        # Recording parameters
        samplerate = 16000  # Audio sample rate
        duration = 5  # Recording duration per segment

        with sd.InputStream(samplerate=samplerate, channels=1, dtype='int16') as stream:
            while True:
                original_placeholder.text("Listening...")
                audio_data = stream.read(duration * samplerate)[0]  # Read audio data
                audio_data = np.array(audio_data, dtype=np.int16)

                # Convert audio to speech using speech_recognition
                audio = sr.AudioData(audio_data.tobytes(), samplerate, 2)
                try:
                    spoken_text = rec.recognize_google(audio, language=from_language)
                    original_placeholder.text(spoken_text)

                    # Translate the spoken text to the target language
                    translated_text = translator_function(spoken_text, from_language, to_language)
                    translated_placeholder.text(translated_text.text)

                    # Play translated text as speech
                    text_to_voice(translated_text.text, to_language)

                except sr.UnknownValueError:
                    original_placeholder.text("Could not understand audio")
                except sr.RequestError:
                    st.error("API unavailable")
                except Exception as e:
                    st.error(f"Error: {e}")
                
                # Add a stop condition to break out of the loop, such as a stop button in Streamlit.

else:
    # Show Signup and Login forms
    option = st.sidebar.selectbox("Select Option", ["Login", "Signup"])

    if option == "Signup":
        st.subheader("Signup")

        new_username = st.text_input("Username", key="signup_username")
        new_password = st.text_input("Password", type="password", key="signup_password")

        if st.button("Create Account"):
            if signup(new_username, new_password):
                st.success("Account created! Please log in.")
            else:
                st.error("Username already exists.")

    elif option == "Login":
        st.subheader("Login")

        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login"):
            if login(username, password):
                st.success("Login successful!")
                st.session_state["is_authenticated"] = True
            else:
                st.error("Invalid username or password.")
