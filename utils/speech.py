import pyttsx3
import streamlit as st        
import speech_recognition as sr

def speak(text):
    try:
        
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 1.0)
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        st.error(f"TTS Error:{e}")

    
def listen_from_mic():
    recognizer = sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
            st.info("🎤 Listening...")
            print(source,"this is source")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=5,phrase_time_limit=10)
            print(audio,"this is audio")
            st.success("Voice Captured, processing...")
            text=recognizer.recognize_google(audio)
            return text
    except sr.UnknownValueError:
        st.error("Please Speak Again.")
    except sr.RequestError as e:
        st.error(f"API error:{e}")
    except Exception as e:
         st.error(f"Error like:{e}")
    return None 