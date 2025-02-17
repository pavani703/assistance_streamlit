import streamlit as st
import pyjokes
import wikipedia
import datetime
import webbrowser
from gtts import gTTS
import tempfile
import os
import pytz

def text_to_speech(text):
    """Convert text to speech and play the audio."""
    tts = gTTS(text=text, lang="en")
    temp_file = os.path.join(tempfile.gettempdir(), "speech.mp3")
    tts.save(temp_file)
    st.audio(temp_file, format="audio/mp3")

def tell_joke():
    joke = pyjokes.get_joke()
    st.write(joke)
    text_to_speech(joke)

def play_music():
    """Provide a clickable link to open YouTube music search."""
    url = "https://www.youtube.com/results?search_query=relaxing+music"
    st.markdown(f"[Click here to play relaxing music 🎵]({url})")

def search_wikipedia():
    query = st.text_input("Enter a topic to search on Wikipedia:")
    if query:
        try:
            summary = wikipedia.summary(query, sentences=2)
            st.write(summary)
            text_to_speech(summary)
        except wikipedia.exceptions.DisambiguationError:
            st.write("Multiple results found. Please be more specific.")
        except wikipedia.exceptions.PageError:
            st.write("No results found.")

def get_time():
    ist = pytz.timezone('Asia/Kolkata')
    current_time = datetime.datetime.now(ist).strftime("%H:%M:%S")
    st.write(f"Current time: {current_time}")
    text_to_speech(f"The time is {current_time}")

def play_video():
    """Provide a clickable link to open YouTube."""
    url = "https://www.youtube.com/"
    st.markdown(f"[Click here to open YouTube ▶]({url})")


# Streamlit UI
st.title("Virtual Assistant ")

options = {
    "Tell a Joke": tell_joke,
    "Play Music": play_music,
    "Search Wikipedia": search_wikipedia,
    "Get Time": get_time,
    "Play a Video": play_video,
}

choice = st.selectbox("Choose an option:", list(options.keys()))
options[choice]()
