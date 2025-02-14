import streamlit as st
import pyjokes
import wikipedia
import datetime
import webbrowser
from gtts import gTTS
import os

def speak(text):
    from gtts import gTTS
    tts = gTTS(text=text, lang="en")
    
    # Save the file in a writable directory
    file_path = os.path.join(os.getcwd(), "temp_output.mp3")
    tts.save(file_path)

    # Play the audio
    os.system(f"start {file_path}")  # Windows


st.title("Virtual Assistant")

option = st.selectbox("Choose an option:", ["Tell a Joke", "Play Music", "Search Wikipedia", "Get Time", "Play a Video"])

if option == "Tell a Joke":
    joke = pyjokes.get_joke()
    st.write(joke)
    speak(joke)

elif option == "Play Music":
    st.write("Opening a music video...")
    webbrowser.open("https://www.youtube.com/results?search_query=relaxing+music")

elif option == "Search Wikipedia":
    query = st.text_input("Enter a topic to search on Wikipedia:")
    if query:
        try:
            summary = wikipedia.summary(query, sentences=2)
            st.write(summary)
            speak(summary)
        except wikipedia.exceptions.DisambiguationError as e:
            st.write("Multiple results found. Please be more specific.")
        except wikipedia.exceptions.PageError:
            st.write("No results found.")

elif option == "Get Time":
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    st.write(f"Current time: {current_time}")
    speak(f"The time is {current_time}")

elif option == "Play a Video":
    st.write("Opening YouTube...")
    webbrowser.open("https://www.youtube.com/")
    import tempfile

def speak(text):
    from gtts import gTTS
    import os

    tts = gTTS(text=text, lang="en")

    # Save in a temp directory
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, "output.mp3")
    tts.save(file_path)

    # Play the audio
    os.system(f"start {file_path}")  # Windows
    import tempfile

def speak(text):
    from gtts import gTTS
    import os

    tts = gTTS(text=text, lang="en")

    # Save in a temp directory
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, "output.mp3")
    tts.save(file_path)

    # Play the audio
    os.system(f"start {file_path}")  # Windows


