import streamlit as st
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import sys
import threading
import tempfile
from pygame import mixer
import os

# Initialize recognizer and text-to-speech engine
listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 150)

# Initialize Streamlit page configuration
st.set_page_config(
    page_title="Virtual Assistant",
    page_icon="🤖",
    layout="centered"
)

# Add custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        height: 3rem;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

def text_to_speech(text):
    """Convert text to speech and save as audio file"""
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
        engine.save_to_file(text, fp.name)
        engine.runAndWait()
        return fp.name

def play_audio(file_path):
    """Play audio file using pygame mixer"""
    mixer.init()
    mixer.music.load(file_path)
    mixer.music.play()
    while mixer.music.get_busy():
        continue
    mixer.quit()
    # Clean up the temporary file
    os.remove(file_path)

def engine_talk(text):
    """Converts text to speech"""
    try:
        st.write(f"🗣️ Assistant: {text}")
        audio_file = text_to_speech(text)
        play_audio(audio_file)
    except Exception as e:
        st.error(f"Text-to-speech error: {e}")

def user_commands():
    """Captures voice input and converts it to text"""
    command = ""
    try:
        with sr.Microphone() as source:
            st.info("Listening... Speak now!")
            listener.adjust_for_ambient_noise(source)
            voice = listener.listen(source, timeout=5)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'alexa' in command:
                command = command.replace('alexa', '').strip()
            st.write(f"🎤 You said: {command}")
            return command
    except sr.UnknownValueError:
        st.warning("Sorry, I could not understand that.")
    except sr.RequestError:
        st.error("Could not request results. Check your internet connection.")
    except Exception as e:
        st.error(f"Error: {e}")
    return command

def process_command(command):
    """Processes user commands and performs actions"""
    if not command:
        return

    if 'play' in command:
        song = command.replace('play', '').strip()
        engine_talk(f"Playing {song}")
        pywhatkit.playonyt(song)
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        engine_talk(f"The current time is {time}")
    elif 'who is' in command:
        name = command.replace('who is', '').strip()
        try:
            info = wikipedia.summary(name, sentences=1)
            st.write(info)
            engine_talk(info)
        except wikipedia.exceptions.PageError:
            engine_talk("I couldn't find any information on that.")
    elif 'joke' in command:
        joke = pyjokes.get_joke()
        engine_talk(joke)
    else:
        engine_talk("I could not understand your command. Please try again.")

def main():
    st.title("🤖 Virtual Assistant")
    st.markdown("---")
    
    # Add description
    st.markdown("""
    Welcome to your Virtual Assistant! You can:
    - Ask for the time
    - Play YouTube videos
    - Ask "Who is..." questions
    - Request jokes
    """)
    
    # Add voice command button
    if st.button("🎤 Start Listening"):
        command = user_commands()
        if command:
            process_command(command)
    
    # Add text input alternative
    text_command = st.text_input("Or type your command here:")
    if st.button("Send"):
        if text_command:
            st.write(f"🎤 You typed: {text_command}")
            process_command(text_command.lower())

    # Add footer
    st.markdown("---")
    st.markdown("Made with ❤️ using Streamlit")

if __name__ == "__main__":
    main() 