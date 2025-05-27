
# # import tkinter as tk
# # import speech_recognition as sr
# # import pyttsx3

# # # Initialize speech and TTS
# # recognizer = sr.Recognizer()
# # tts_engine = pyttsx3.init()
# # tts_engine.setProperty('rate', 150)
# # tts_engine.setProperty('volume', 1)

# # def speak(text):
# #     tts_engine.say(text)
# #     tts_engine.runAndWait()

# # def listen():
# #     with sr.Microphone() as source:
# #         print("Listening...")
# #         recognizer.adjust_for_ambient_noise(source)
# #         audio = recognizer.listen(source)
# #         try:
# #             command = recognizer.recognize_google(audio)
# #             print(f"You said: {command}")
# #             return command.lower()
# #         except sr.UnknownValueError:
# #             print("Sorry, I did not understand that.")
# #         except sr.RequestError:
# #             print("Speech service is unavailable.")
# #     return ""

# # def speech():
# #     command = listen()
# #     if command:
# #         speak(f"You said: {command}")
# #         input_field.delete(0, tk.END)
# #         input_field.insert(0, command)

# # # UI setup
# # root = tk.Tk()
# # root.title("Voice Assistant")

# # input_field = tk.Entry(root, width=50)
# # input_field.pack(padx=10, pady=10)

# # voice_button = tk.Button(root, text="🎤 Speak", command=speech)
# # voice_button.pack(padx=10, pady=5)

# # # Greeting
# # speak("Voice Assistant at your service. What is your command?")
# # root.mainloop()




# # import tkinter as tk
# # import speech_recognition as sr
# # import pyttsx3

# # # Initialize speech and TTS
# # recognizer = sr.Recognizer()
# # tts_engine = pyttsx3.init()
# # tts_engine.setProperty('rate', 150)
# # tts_engine.setProperty('volume', 1)

# # def speak(text):
# #     tts_engine.say(text)
# #     tts_engine.runAndWait()

# # def listen():
# #     with sr.Microphone() as source:
# #         print("Listening...")
# #         recognizer.adjust_for_ambient_noise(source)
# #         audio = recognizer.listen(source)
# #         try:
# #             command = recognizer.recognize_google(audio)
# #             print(f"You said: {command}")
# #             return command.lower()
# #         except sr.UnknownValueError:
# #             print("Sorry, I did not understand that.")
# #             speak("Sorry, I did not understand that.")
# #         except sr.RequestError:
# #             print("Speech service is unavailable.")
# #             speak("Sorry, the speech service is unavailable.")
# #     return ""

# # def speech():
# #     command = listen()
# #     if command:
# #         speak(f"You said: {command}")
# #         input_field.delete(0, tk.END)
# #         input_field.insert(0, command)

# # # UI setup
# # root = tk.Tk()
# # root.title("Voice Assistant")

# # input_field = tk.Entry(root, width=50)
# # input_field.pack(padx=10, pady=10)

# # voice_button = tk.Button(root, text="🎤 Speak", command=speech)
# # voice_button.pack(padx=10, pady=5)

# # # Greeting
# # speak("Voice Assistant at your service. What is your command?")
# # root.mainloop()

# import tkinter as tk
# import pyttsx3
# import speech_recognition as sr
# import threading

# # Initialize speech and TTS
# recognizer = sr.Recognizer()
# tts_engine = pyttsx3.init()
# tts_engine.setProperty('rate', 150)
# tts_engine.setProperty('volume', 100)
# mic_index=1

# def speak(text):
#     tts_engine.say(text)
#     tts_engine.runAndWait()

# def listen():
#     recognizer = sr.Recognizer()
    
#     try:
#         with sr.Microphone(device_index=mic_index) as source:
#             print("Listening...")
            
#             recognizer.adjust_for_ambient_noise(source, duration=1)
#             audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
#             print("Got audio, Processing...")
            
#         try:
#             command = recognizer.recognize_google(audio)
#             print(f"You said: {command}")
#             return command
#         except sr.UnknownValueError:
#             print("Sorry, I didn't understand that.")
#         except sr.RequestError as e:
#             print(f"Request error from google:{e}")
        
        
#     except Exception as e:
#         print(f"Microphone or audio input error:{e}")
        
#     return ""
    

# def speech():
#     # Use a separate thread to prevent blocking the UI
#     voice_button.config(state="disabled")
#     def run_speech():
#         command = listen()
#         if command:
#             speak(f"You said: {command}")
#             input_field.delete(0, tk.END)
#             input_field.insert(0, command)
#         voice_button.config(state="normal")

#     # Start the speech recognition in a new thread
#     threading.Thread(target=run_speech, daemon=True).start()

# # UI setup
# root = tk.Tk()
# root.title("Voice Assistant")

# input_field = tk.Entry(root, width=50)
# input_field.pack(padx=10, pady=10)

# voice_button = tk.Button(root, text="🎤 Speak", command=speech)
# voice_button.pack(padx=10, pady=5)

# # Greeting
# speak("Voice Assistant at your service. What is your command?")

# root.mainloop()


import os
import uuid
import subprocess
import google.generativeai as genai
import PyPDF2
import streamlit as st
from datetime import datetime
import pyttsx3
import speech_recognition as sr
import pytz
import requests
import tempfile
import re
import shutil
import winreg
import psutil
from Software_Catalog import SOFTWARE_CATALOG, get_software_info
from chat_db import init_db, save_message, load_chat_history, get_all_chat_ids

# Initialize Streamlit
st.set_page_config(page_title="ChatMate AI", page_icon="static/robot.png")

# Configure Gemini
api_key = 'AIzaSyC3N6bbu0b-Gd3c1DIQCeJLwawSwjcH50c'
genai.configure(api_key=api_key)

generation_config = {
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 100,
    "max_output_tokens": 32768,
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# ==================== NEW STORAGE FUNCTIONS ====================
def get_installed_programs_with_sizes():
    """Returns detailed list with storage usage per program"""
    system_programs = []
    downloaded_programs = []
    
    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall") as key:
        for i in range(0, winreg.QueryInfoKey(key)[0]):
            try:
                subkey_name = winreg.EnumKey(key, i)
                with winreg.OpenKey(key, subkey_name) as subkey:
                    try:
                        name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                        path = winreg.QueryValueEx(subkey, "InstallLocation")[0] or ""
                        publisher = winreg.QueryValueEx(subkey, "Publisher")[0] if winreg.QueryValueEx(subkey, "Publisher") else ""
                        
                        size_gb = calculate_program_size(path)
                        
                        entry = {
                            "name": name,
                            "size_gb": round(size_gb, 2),
                            "path": path
                        }
                        
                        if "Microsoft" in publisher or "Windows" in name:
                            system_programs.append(entry)
                        else:
                            downloaded_programs.append(entry)
                    except WindowsError:
                        continue
            except WindowsError:
                continue
    
    return system_programs, downloaded_programs

def calculate_program_size(path):
    """Calculates storage usage for a single program"""
    if not path or not os.path.exists(path):
        return 0.0
    
    try:
        total_bytes = sum(
            os.path.getsize(os.path.join(root, f))
            for root, _, files in os.walk(path)
            for f in files
        )
        return total_bytes / (1024 ** 3)  # Convert to GB
    except:
        return 0.0

def generate_storage_report():
    """Generates both summary and detailed program list"""
    try:
        system_progs, user_progs = get_installed_programs_with_sizes()
        
        # Sort by size (descending)
        system_progs.sort(key=lambda x: x['size_gb'], reverse=True)
        user_progs.sort(key=lambda x: x['size_gb'], reverse=True)
        
        # Generate formatted lists (top 10 largest)
        sys_list = "\n".join(f"- {p['name']} ({p['size_gb']} GB)" for p in system_progs[:10])
        user_list = "\n".join(f"- {p['name']} ({p['size_gb']} GB)" for p in user_progs[:10])
        
        total_system = sum(p['size_gb'] for p in system_progs)
        total_user = sum(p['size_gb'] for p in user_progs)
        
        report = (
            f"📋 Comprehensive Storage Report\n\n"
            f"🖥️ SYSTEM INSTALLED ({total_system:.2f} GB, {len(system_progs)} programs)\n"
            f"--------------------------------\n"
            f"{sys_list}\n"
            f"... [showing top 10 of {len(system_progs)} total]\n\n"
            f"⬇️ USER INSTALLED ({total_user:.2f} GB, {len(user_progs)} programs)\n"
            f"-----------------------------\n"
            f"{user_list}\n"
            f"... [showing top 10 of {len(user_progs)} total]\n\n"
            f"💾 TOTAL STORAGE USED: {total_system + total_user:.2f} GB"
        )
        
        return report
    except Exception as e:
        return f"❌ Error generating report: {str(e)}"

# ==================== EXISTING FUNCTIONS ==================== 
# [Keep all your existing functions like extract_text_from_pdf, install_exe, speak, 
# listen_from_mic, parse_software_name, is_software_installed, 
# download_and_install_software, create_new_chat, etc.]
# ...

def main():
    init_db()
    clear_uploads_directory()

    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now()
    current_time = now.strftime("%A, %B %d, %Y at %I:%M %p")

    st.title("Welcome to ChatMate AI...")
    st.markdown(f"**Current Date & Time (IST):** {current_time}")
    st.markdown("""
    **New Commands:**
    - `storage report` - Shows program storage usage
    - `list programs` - Displays installed apps
    """)
    
    # [Keep all your existing session state initialization code]
    
    # ==================== MODIFIED PROMPT HANDLER ====================
    if prompt and current_gemini_session:
        # New storage commands
        if prompt.lower() in ["storage report", "list programs", "show installed apps"]:
            report = generate_storage_report()
            st.chat_message("assistant").markdown(report)
            add_message_to_current_chat("assistant", report)
            st.rerun()
            
        # Existing software installation handler
        elif parse_software_name(prompt) and parse_software_name(prompt) in SOFTWARE_CATALOG:
            download_and_install_software(parse_software_name(prompt))
            
        # [Rest of your existing prompt handling code]
        # ...

if __name__ == "__main__":
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    clear_uploads_directory()
    main()