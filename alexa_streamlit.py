import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import os
import webbrowser
import pywhatkit
import datetime
import wikipedia
import pyjokes
import tempfile
from pygame import mixer

# Fix for headless server (Deployment Issue)
os.environ["DISPLAY"] = ""  

# Initialize speech recognizer
listener = sr.Recognizer()

# Streamlit Page Configuration
st.set_page_config(
    page_title="Virtual Assistant",
    page_icon="🤖",
    layout="centered"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main { padding: 2rem; }
    .stButton>button { width: 100%; height: 3rem; margin: 1rem 0; }
    </style>
    """, unsafe_allow_html=True)

def text_to_speech(text):
    """Convert text to speech and save as an audio file"""
    try:
        tts = gTTS(text=text, lang='en')
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
            tts.save(fp.name)
            return fp.name
    except Exception as e:
        st.error(f"Text-to-speech error: {e}")
        return None

def play_audio(file_path):
    """Play an audio file"""
    try:
        mixer.init()
        mixer.music.load(file_path)
        mixer.music.play()
        while mixer.music.get_busy():
            continue
        mixer.quit()
        os.remove(file_path)  # Clean up the temporary file
    except Exception as e:
        st.error(f"Audio playback error: {e}")

def engine_talk(text):
    """Convert text to speech and play"""
    try:
        st.write(f"🗣️ Assistant: {text}")
        audio_file = text_to_speech(text)
        if audio_file:
            play_audio(audio_file)
    except Exception as e:
        st.error(f"Text-to-speech error: {e}")

def user_commands():
    """Capture voice input and return as text"""
    command = ""
    try:
        with sr.Microphone() as source:
            st.info("Listening... Speak now!")
            listener.adjust_for_ambient_noise(source)
            voice = listener.listen(source, timeout=5)
            command = listener.recognize_google(voice)
            command = command.lower()
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
    
    elif 'who is' in command or 'what is' in command:
        topic = command.replace('who is', '').replace('what is', '').strip()
        try:
            info = wikipedia.summary(topic, sentences=2)
            st.write(info)
            engine_talk(info)
        except wikipedia.exceptions.PageError:
            engine_talk(f"Sorry, I couldn't find information on {topic}.")
        except wikipedia.exceptions.DisambiguationError:
            engine_talk("There are multiple results. Please be more specific.")
    
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
    - Ask for the time ⏰
    - Play YouTube videos 🎵
    - Ask "Who is..." or "What is..." questions 📖
    - Request jokes 😂
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
