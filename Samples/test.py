# # # # # # # # # # # import speech_recognition as sr

# # # # # # # # # # # recognizer = sr.Recognizer()
# # # # # # # # # # # mic = sr.Microphone()

# # # # # # # # # # # print("Say something...")

# # # # # # # # # # # with mic as source:
# # # # # # # # # # #     recognizer.adjust_for_ambient_noise(source)
# # # # # # # # # # #     audio = recognizer.listen(source)

# # # # # # # # # # # print("Got audio! Trying to recognize...")

# # # # # # # # # # # try:
# # # # # # # # # # #     text = recognizer.recognize_google(audio)
# # # # # # # # # # #     print("You said:", text)
# # # # # # # # # # # except sr.UnknownValueError:
# # # # # # # # # # #     print("Could not understand the audio.")
# # # # # # # # # # # except sr.RequestError as e:
# # # # # # # # # # #     print("Could not request results; {0}".format(e))

# # # # # # # # # # # import speech_recognition as sr

# # # # # # # # # # # print(sr.Microphone.list_microphone_names())

# # # # # # # # # # # import speech_recognition as sr

# # # # # # # # # # # print(sr.Microphone.list_microphone_names())

# # # # # # # # # # # import speech_recognition as sr

# # # # # # # # # # # for index, name in enumerate(sr.Microphone.list_microphone_names()):
# # # # # # # # # # #     print(f"{index}: {name}")


# # # # # # # # # # # import speech_recognition as sr

# # # # # # # # # # # recognizer = sr.Recognizer()

# # # # # # # # # # # with sr.Microphone() as source:
# # # # # # # # # # #     print("Say something...")
# # # # # # # # # # #     audio = recognizer.listen(source)

# # # # # # # # # # # try:
# # # # # # # # # # #     print("You said: " + recognizer.recognize_google(audio))
# # # # # # # # # # # except sr.UnknownValueError:
# # # # # # # # # # #     print("Could not understand audio")
# # # # # # # # # # # except sr.RequestError as e:
# # # # # # # # # # #     print(f"Could not request results; {e}")


# # # # # # # # # # import streamlit as st
# # # # # # # # # # import requests
# # # # # # # # # # import subprocess
# # # # # # # # # # import os
# # # # # # # # # # import re

# # # # # # # # # # # 1. Map software names to trusted download URLs and installer filenames
# # # # # # # # # # SOFTWARE_CATALOG = {
# # # # # # # # # #     "vlc media player": {
# # # # # # # # # #         "url": "https://get.videolan.org/vlc/3.0.18/win64/vlc-3.0.18-win64.exe",
# # # # # # # # # #         "installer": "vlc_installer.exe",
# # # # # # # # # #         "silent_flag": "/S"
# # # # # # # # # #     },
# # # # # # # # # #         "r":{
# # # # # # # # # #             "url":"https://cran.icts.res.in/",
# # # # # # # # # #             "installer":"r.exe",
            
# # # # # # # # # #         }
# # # # # # # # # #     }
# # # # # # # # # #     # Add more software here as needed


# # # # # # # # # # def parse_software_name(command):
# # # # # # # # # #     # Simple regex to extract software name after 'install'
# # # # # # # # # #     match = re.search(r'install (.+)', command, re.IGNORECASE)
# # # # # # # # # #     if match:
# # # # # # # # # #         return match.group(1).strip().lower()
# # # # # # # # # #     return None

# # # # # # # # # # def download_and_install_software(software_key):
# # # # # # # # # #     info = get_software_info(software_key)
# # # # # # # # # #     if not info:
# # # # # # # # # #         st.error("Software not found in catalog.")
# # # # # # # # # #         return
    
# # # # # # # # # #     url = info["url"]
# # # # # # # # # #     installer = info["installer"]
# # # # # # # # # #     silent_flag = info.get("silent_flag", "")

# # # # # # # # # #     # Download
# # # # # # # # # #     st.info(f"Downloading {software_key.title()}...")
# # # # # # # # # #     try:
# # # # # # # # # #         with requests.get(url, stream=True) as r:
# # # # # # # # # #             r.raise_for_status()
# # # # # # # # # #             with open(installer, 'wb') as f:
# # # # # # # # # #                 for chunk in r.iter_content(chunk_size=8192):
# # # # # # # # # #                     f.write(chunk)
# # # # # # # # # #         st.success("Download complete.")
# # # # # # # # # #     except Exception as e:
# # # # # # # # # #         st.error(f"Download failed: {e}")
# # # # # # # # # #         return

# # # # # # # # # #     # Install
# # # # # # # # # #     st.info("Installing... (this may take a moment)")
# # # # # # # # # #     try:
# # # # # # # # # #         subprocess.run([installer, silent_flag], check=True)
# # # # # # # # # #         st.success(f"{software_key.title()} installed successfully!")
# # # # # # # # # #     except Exception as e:
# # # # # # # # # #         st.error(f"Installation failed: {e}")
# # # # # # # # # #     finally:
# # # # # # # # # #         # Clean up installer file
# # # # # # # # # #         if os.path.exists(installer):
# # # # # # # # # #             os.remove(installer)
# # # # # # # # # #             st.info("Installer removed.")

# # # # # # # # # # # Streamlit UI
# # # # # # # # # # st.title("Software Installer Chatbot")

# # # # # # # # # # user_input = st.text_input("Type your command (e.g., install vlc media player):")

# # # # # # # # # # if user_input:
# # # # # # # # # #     software_name = parse_software_name(user_input)
# # # # # # # # # #     if software_name and software_name in SOFTWARE_CATALOG:
# # # # # # # # # #         download_and_install_software(software_name)
# # # # # # # # # #     elif user_input.lower().startswith("install "):
# # # # # # # # # #         st.warning("Sorry, I don't recognize that software yet.")
# # # # # # # # # #     else:
# # # # # # # # # #         st.write("You said:", user_input)

# # # # # # # # # # import streamlit as st

# # # # # # # # # # # Add vertical space (adjust the range for more/less space)
# # # # # # # # # # for _ in range(10):
# # # # # # # # # #     st.write("")

# # # # # # # # # # # Center horizontally with columns
# # # # # # # # # # col1, col2, col3 = st.columns([1,2,1])
# # # # # # # # # # with col2:
# # # # # # # # # #     user_input = st.text_input("Type your search here")


# # # # # # # # # import streamlit as st
# # # # # # # # # import subprocess
# # # # # # # # # import os
# # # # # # # # # import json

# # # # # # # # # def get_appx_packages():
# # # # # # # # #     result = subprocess.run([
# # # # # # # # #         "powershell", "-Command",
# # # # # # # # #         "Get-AppxPackage -AllUsers | Select Name, InstallLocation | ConvertTo-Json"
# # # # # # # # #     ], capture_output=True, text=True)
# # # # # # # # #     try:
# # # # # # # # #         return json.loads(result.stdout)
# # # # # # # # #     except Exception:
# # # # # # # # #         return []

# # # # # # # # # def get_win32_apps():
# # # # # # # # #     result = subprocess.run([
# # # # # # # # #         "powershell", "-Command",
# # # # # # # # #         "Get-WmiObject -Class Win32_Product | Select Name, InstallLocation | ConvertTo-Json"
# # # # # # # # #     ], capture_output=True, text=True)
# # # # # # # # #     try:
# # # # # # # # #         return json.loads(result.stdout)
# # # # # # # # #     except Exception:
# # # # # # # # #         return []

# # # # # # # # # def get_folder_size(path):
# # # # # # # # #     total_size = 0
# # # # # # # # #     for dirpath, dirnames, filenames in os.walk(path):
# # # # # # # # #         for f in filenames:
# # # # # # # # #             fp = os.path.join(dirpath, f)
# # # # # # # # #             try:
# # # # # # # # #                 if os.path.isfile(fp):
# # # # # # # # #                     total_size += os.path.getsize(fp)
# # # # # # # # #             except Exception:
# # # # # # # # #                 pass
# # # # # # # # #     return total_size

# # # # # # # # # st.title("System vs Downloaded Apps and Storage Usage")

# # # # # # # # # if st.button("Scan My Apps"):
# # # # # # # # #     with st.spinner("Scanning system apps..."):
# # # # # # # # #         system_apps = get_appx_packages()
# # # # # # # # #     with st.spinner("Scanning downloaded apps..."):
# # # # # # # # #         downloaded_apps = get_win32_apps()

# # # # # # # # #     system_total = 0
# # # # # # # # #     downloaded_total = 0
# # # # # # # # #     system_list = []
# # # # # # # # #     downloaded_list = []

# # # # # # # # #     with st.spinner("Calculating storage usage..."):
# # # # # # # # #         for app in system_apps:
# # # # # # # # #             path = app.get("InstallLocation")
# # # # # # # # #             name = app.get("Name")
# # # # # # # # #             if path and os.path.exists(path):
# # # # # # # # #                 size = get_folder_size(path)
# # # # # # # # #                 system_total += size
# # # # # # # # #                 system_list.append({"App": name, "Size (MB)": f"{size/1e6:.2f}"})

# # # # # # # # #         for app in downloaded_apps:
# # # # # # # # #             path = app.get("InstallLocation")
# # # # # # # # #             name = app.get("Name")
# # # # # # # # #             if path and os.path.exists(path):
# # # # # # # # #                 size = get_folder_size(path)
# # # # # # # # #                 downloaded_total += size
# # # # # # # # #                 downloaded_list.append({"App": name, "Size (MB)": f"{size/1e6:.2f}"})

# # # # # # # # #     st.subheader("Summary")
# # # # # # # # #     st.markdown(f"**System Apps:** {len(system_list)} apps, **{system_total/1e9:.2f} GB**")
# # # # # # # # #     st.markdown(f"**Downloaded Apps:** {len(downloaded_list)} apps, **{downloaded_total/1e9:.2f} GB**")

# # # # # # # # #     with st.expander("See details for System Apps"):
# # # # # # # # #         st.table(system_list)
# # # # # # # # #     with st.expander("See details for Downloaded Apps"):
# # # # # # # # #         st.table(downloaded_list)

# # # # # # # # import streamlit as st
# # # # # # # # import tempfile
# # # # # # # # import PyPDF2
# # # # # # # # import speech_recognition as sr
# # # # # # # # import pyttsx3
# # # # # # # # import subprocess

# # # # # # # # # Initialize TTS engine once
# # # # # # # # engine = pyttsx3.init()

# # # # # # # # def call_gemini_api(prompt):
# # # # # # # #     return f"Gemini says: {prompt}"

# # # # # # # # def extract_text_from_pdf(pdf_file):
# # # # # # # #     pdf_reader = PyPDF2.PdfReader(pdf_file)
# # # # # # # #     text = ""
# # # # # # # #     for page in pdf_reader.pages:
# # # # # # # #         text += page.extract_text() + "\n"
# # # # # # # #     return text

# # # # # # # # def recognize_speech():
# # # # # # # #     recognizer = sr.Recognizer()
# # # # # # # #     with sr.Microphone() as source:
# # # # # # # #         st.info("Listening... Please speak now.")
# # # # # # # #         audio = recognizer.listen(source, phrase_time_limit=5)
# # # # # # # #     try:
# # # # # # # #         text = recognizer.recognize_google(audio)
# # # # # # # #         return text
# # # # # # # #     except:
# # # # # # # #         return None

# # # # # # # # def install_software(exe_path):
# # # # # # # #     try:
# # # # # # # #         subprocess.Popen(exe_path, shell=True)
# # # # # # # #         return "Installation started."
# # # # # # # #     except Exception as e:
# # # # # # # #         return f"Error: {str(e)}"

# # # # # # # # st.title("Chatbot with Auto Listen & Auto Speak")

# # # # # # # # # State to store input text
# # # # # # # # if "user_input" not in st.session_state:
# # # # # # # #     st.session_state.user_input = ""

# # # # # # # # # Auto listen on first load
# # # # # # # # if st.session_state.user_input == "":
# # # # # # # #     spoken_text = recognize_speech()
# # # # # # # #     if spoken_text:
# # # # # # # #         st.session_state.user_input = spoken_text
# # # # # # # #         st.success(f"You said: {spoken_text}")
# # # # # # # #     else:
# # # # # # # #         st.warning("Couldn't understand speech or microphone not available.")

# # # # # # # # # Text input to modify or enter manually
# # # # # # # # user_input = st.text_input("Your message:", st.session_state.user_input)

# # # # # # # # # PDF upload & extraction
# # # # # # # # uploaded_pdf = st.file_uploader("Upload PDF", type=["pdf"])
# # # # # # # # if uploaded_pdf:
# # # # # # # #     with tempfile.NamedTemporaryFile(delete=False) as temp_pdf:
# # # # # # # #         temp_pdf.write(uploaded_pdf.read())
# # # # # # # #         extracted_text = extract_text_from_pdf(temp_pdf.name)
# # # # # # # #     st.text_area("Extracted PDF Text", extracted_text, height=200)

# # # # # # # # # Software installation input
# # # # # # # # exe_file_path = st.text_input("Path to .exe for installation:")

# # # # # # # # if st.button("Install Software"):
# # # # # # # #     if exe_file_path:
# # # # # # # #         install_message = install_software(exe_file_path)
# # # # # # # #         st.info(install_message)
# # # # # # # #     else:
# # # # # # # #         st.error("Please enter .exe path.")

# # # # # # # # # If user input available, get bot response and auto speak it
# # # # # # # # if user_input:
# # # # # # # #     response = call_gemini_api(user_input)
# # # # # # # #     st.markdown(f"**Bot:** {response}")
    
# # # # # # # #     # TTS auto speak
# # # # # # # #     engine.say(response)
# # # # # # # #     engine.runAndWait()
    
# # # # # # # #     # Clear user input after response so next time auto listen triggers again
# # # # # # # #     st.session_state.user_input = ""

# # # # # # # import streamlit as st
# # # # # # # import speech_recognition as sr
# # # # # # # import pyttsx3

# # # # # # # # === Text-to-Speech ===
# # # # # # # def speak(text):
# # # # # # #     try:
# # # # # # #         engine = pyttsx3.init()
# # # # # # #         engine.setProperty('rate', 150)
# # # # # # #         engine.setProperty('volume', 1.0)
# # # # # # #         voices = engine.getProperty('voices')
# # # # # # #         engine.setProperty('voice', voices[0].id)  # You can customize this
# # # # # # #         engine.say(text)
# # # # # # #         engine.runAndWait()
# # # # # # #     except Exception as e:
# # # # # # #         st.error(f"TTS Error: {e}")

# # # # # # # # === Voice Input from Microphone ===
# # # # # # # def listen_from_mic():
# # # # # # #     recognizer = sr.Recognizer()
# # # # # # #     try:
# # # # # # #         with sr.Microphone() as source:
# # # # # # #             st.info("🎤 Listening... Speak now.")
# # # # # # #             recognizer.adjust_for_ambient_noise(source)
# # # # # # #             audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
# # # # # # #             st.success("🎧 Voice captured. Processing...")
# # # # # # #             return recognizer.recognize_google(audio)
# # # # # # #     except sr.WaitTimeoutError:
# # # # # # #         st.warning("Listening timed out.")
# # # # # # #     except sr.UnknownValueError:
# # # # # # #         st.warning("Could not understand your voice.")
# # # # # # #     except sr.RequestError as e:
# # # # # # #         st.error(f"Speech Recognition API error: {e}")
# # # # # # #     except Exception as e:
# # # # # # #         st.error(f"Error capturing mic input: {e}")
# # # # # # #     return None

# # # # # # # # === Dummy Gemini-style Response Generator ===
# # # # # # # def generate_response(prompt):
# # # # # # #     prompt = prompt.lower()
# # # # # # #     if "hello" in prompt:
# # # # # # #         return "Hello! How can I help you today?"
# # # # # # #     elif "your name" in prompt:
# # # # # # #         return "I'm your AI assistant bot."
# # # # # # #     elif "time" in prompt:
# # # # # # #         from datetime import datetime
# # # # # # #         return "The current time is " + datetime.now().strftime("%I:%M %p")
# # # # # # #     else:
# # # # # # #         return "Sorry, I didn't understand that. Try asking something else!"

# # # # # # # # === Streamlit App ===
# # # # # # # st.title("🧠 Voice Command Chatbot")
# # # # # # # st.markdown("Speak and get a response!")

# # # # # # # if st.button("🎙️ Speak Now"):
# # # # # # #     user_text = listen_from_mic()
# # # # # # #     if user_text:
# # # # # # #         st.markdown(f"**You said:** {user_text}")
# # # # # # #         response = generate_response(user_text)
# # # # # # #         st.markdown(f"**Bot:** {response}")
# # # # # # #         speak(response)

# # # # # # import streamlit as st
# # # # # # import os
# # # # # # import tempfile
# # # # # # from typing import List, Dict, Tuple
# # # # # # import numpy as np
# # # # # # from PIL import Image
# # # # # # import cv2
# # # # # # import whisper
# # # # # # from sentence_transformers import SentenceTransformer
# # # # # # #import youtube_dl
# # # # # # import yt_dlp
# # # # # # from datetime import timedelta
# # # # # # import gdown

# # # # # # ydl_opts = {
# # # # # #     'format': 'bestvideo+bestaudio/best',
# # # # # #     'ffmpeg_location': r'C:\ffmpeg\ffmpeg-7.1.1-essentials_build\bin',
# # # # # #     'outtmpl': '%(title)s.%(ext)s',
# # # # # #     'postprocessors': [{
# # # # # #         'key': 'FFmpegVideoConvertor',
# # # # # #         'preferedformat': 'mp4',
# # # # # #     }],
# # # # # # }
# # # # # # def process_video_link(url: str) -> Dict:
# # # # # #     """Process a YouTube or Google Drive video link with timestamps"""
    
# # # # # #     if "youtube.com" in url or "youtu.be" in url:
# # # # # #         # YouTube link
# # # # # #         ydl_opts = {
# # # # # #             'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
# # # # # #             'outtmpl': os.path.join(tempfile.gettempdir(), '%(id)s.%(ext)s'),
# # # # # #             'quiet': True
# # # # # #         }
# # # # # #         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
# # # # # #             info = ydl.extract_info(url, download=True)
# # # # # #             filename = ydl.prepare_filename(info)
# # # # # #     elif "drive.google.com" in url:
# # # # # #         # Google Drive link
# # # # # #         try:
# # # # # #             file_id = None
# # # # # #             if "id=" in url:
# # # # # #                 file_id = re.search(r'id=([^&]+)', url).group(1)
# # # # # #             elif "/d/" in url:
# # # # # #                 file_id = re.search(r'/d/([^/]+)', url).group(1)

# # # # # #             if not file_id:
# # # # # #                 raise ValueError("Could not extract Google Drive file ID.")
            
# # # # # #             filename = os.path.join(tempfile.gettempdir(), f"drive_{file_id}.mp4")
# # # # # #             gdown.download(f"https://drive.google.com/uc?id={file_id}", output=filename, quiet=False)
# # # # # #         except Exception as e:
# # # # # #             raise RuntimeError(f"Failed to download from Google Drive: {e}")
# # # # # #     else:
# # # # # #         raise ValueError("Unsupported link type. Please use a YouTube or Google Drive share link.")
    
# # # # # #     # Process the downloaded file
# # # # # #     video_data = process_video_file(filename)
# # # # # #     video_data['type'] = 'link'
# # # # # #     video_data['source_url'] = url
    
# # # # # #     return video_data
# # # # # # # Initialize models (cache these to avoid reloading)
# # # # # # @st.cache_resource
# # # # # # def load_models():
# # # # # #     # Whisper for speech-to-text with timestamps
# # # # # #     whisper_model = whisper.load_model("base")
# # # # # #     # Sentence Transformer for text similarity
# # # # # #     text_model = SentenceTransformer('all-MiniLM-L6-v2')
# # # # # #     return whisper_model, text_model

# # # # # # whisper_model, text_model = load_models()

# # # # # # def process_video_file(video_path: str) -> Dict:
# # # # # #     """Process an uploaded video file with timestamps"""
# # # # # #     # Extract metadata
# # # # # #     cap = cv2.VideoCapture(video_path)
# # # # # #     fps = cap.get(cv2.CAP_PROP_FPS)
# # # # # #     frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
# # # # # #     duration = frame_count / fps
    
# # # # # #     # Extract key frames (simplified - just getting some frames)
# # # # # #     key_frames = []
# # # # # #     frame_interval = int(frame_count / 5)  # Get 5 frames
# # # # # #     for i in range(0, frame_count, frame_interval):
# # # # # #         cap.set(cv2.CAP_PROP_POS_FRAMES, i)
# # # # # #         ret, frame = cap.read()
# # # # # #         if ret:
# # # # # #             timestamp = i / fps
# # # # # #             key_frames.append({
# # # # # #                 'image': Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)),
# # # # # #                 'timestamp': timestamp
# # # # # #             })
    
# # # # # #     cap.release()
    
# # # # # #     # Transcribe audio with timestamps
# # # # # #     result = whisper_model.transcribe(video_path)
# # # # # #     segments = result["segments"]
    
# # # # # #     return {
# # # # # #         'type': 'file',
# # # # # #         'path': video_path,
# # # # # #         'metadata': {
# # # # # #             'duration': duration,
# # # # # #             'fps': fps,
# # # # # #             'frame_count': frame_count
# # # # # #         },
# # # # # #         'key_frames': key_frames,
# # # # # #         'transcript': segments,
# # # # # #         'full_text': result["text"]
# # # # # #     }

# # # # # # def process_video_link(url: str) -> Dict:
# # # # # #     """Process a video link (YouTube, etc.) with timestamps"""
# # # # # #     # Download video using youtube-dl
# # # # # #     ydl_opts = {
# # # # # #         'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
# # # # # #         'outtmpl': os.path.join(tempfile.gettempdir(), '%(id)s.%(ext)s'),
# # # # # #         'quiet': True
# # # # # #     }
    
# # # # # #     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
# # # # # #         info = ydl.extract_info(url, download=True)
# # # # # #         filename = ydl.prepare_filename(info)
    
# # # # # #     # Process the downloaded file
# # # # # #     video_data = process_video_file(filename)
# # # # # #     video_data['type'] = 'link'
# # # # # #     video_data['source_url'] = url
    
# # # # # #     return video_data

# # # # # # def format_timestamp(seconds: float) -> str:
# # # # # #     """Convert seconds to HH:MM:SS format"""
# # # # # #     return str(timedelta(seconds=seconds))

# # # # # # def find_relevant_segments(segments: List[Dict], question_embedding: np.ndarray, top_n: int = 3) -> List[Dict]:
# # # # # #     """Find the most relevant segments in a video to the question"""
# # # # # #     segment_scores = []
    
# # # # # #     for segment in segments:
# # # # # #         # Embed the segment text
# # # # # #         segment_embedding = text_model.encode(segment['text'])
# # # # # #         # Calculate cosine similarity
# # # # # #         similarity = np.dot(question_embedding, segment_embedding) / (
# # # # # #             np.linalg.norm(question_embedding) * np.linalg.norm(segment_embedding)
# # # # # #         )
# # # # # #         segment_scores.append((segment, similarity))
    
# # # # # #     # Sort by similarity score
# # # # # #     segment_scores.sort(key=lambda x: x[1], reverse=True)
    
# # # # # #     # Return top N segments with timestamps
# # # # # #     return [{
# # # # # #         'text': seg['text'],
# # # # # #         'start': seg['start'],
# # # # # #         'end': seg['end'],
# # # # # #         'score': score
# # # # # #     } for seg, score in segment_scores[:top_n]]

# # # # # # def analyze_videos(video_data: List[Dict], question: str) -> Dict:
# # # # # #     """Analyze multiple videos against a question with temporal references"""
# # # # # #     # Embed the question
# # # # # #     question_embedding = text_model.encode(question)
    
# # # # # #     # Compare against each video's transcript
# # # # # #     video_results = []
# # # # # #     for data in video_data:
# # # # # #         # Find relevant segments in this video
# # # # # #         relevant_segments = find_relevant_segments(data['transcript'], question_embedding)
        
# # # # # #         # Calculate overall video relevance (average of top segments)
# # # # # #         if relevant_segments:
# # # # # #             avg_score = sum(seg['score'] for seg in relevant_segments) / len(relevant_segments)
# # # # # #         else:
# # # # # #             avg_score = 0
        
# # # # # #         video_results.append({
# # # # # #             'video_data': data,
# # # # # #             'relevant_segments': relevant_segments,
# # # # # #             'score': avg_score
# # # # # #         })
    
# # # # # #     # Determine most relevant video
# # # # # #     most_relevant = max(video_results, key=lambda x: x['score'])
    
# # # # # #     return {
# # # # # #         'most_relevant': most_relevant,
# # # # # #         'all_results': video_results,
# # # # # #         'explanation': generate_explanation(most_relevant, question)
# # # # # #     }

# # # # # # def generate_explanation(analysis: Dict, question: str) -> str:
# # # # # #     """Generate explanation with temporal references"""
# # # # # #     video_data = analysis['video_data']
# # # # # #     relevant_segments = analysis['relevant_segments']
    
# # # # # #     explanation = []
    
# # # # # #     if video_data['type'] == 'link':
# # # # # #         explanation.append(f"**Most Relevant Video:** [Video Link]({video_data['source_url']})")
# # # # # #     else:
# # # # # #         explanation.append("**Most Relevant Video:** Uploaded Video")
    
# # # # # #     explanation.append(f"\n**Relevance Score:** {analysis['score']:.2f}")
# # # # # #     explanation.append("\n**Key Moments:**")
    
# # # # # #     for i, segment in enumerate(relevant_segments, 1):
# # # # # #         explanation.append(
# # # # # #             f"{i}. At {format_timestamp(segment['start'])} - {segment['text']}"
# # # # # #         )
    
# # # # # #     explanation.append("\n**Why it's relevant:**")
# # # # # #     explanation.append(f"The video contains {len(relevant_segments)} segments specifically addressing your question about '{question}'")
    
# # # # # #     return "\n".join(explanation)

# # # # # # # Streamlit UI
# # # # # # st.title("Video Analysis Chatbot with Temporal References")

# # # # # # # Initialize session state
# # # # # # if "messages" not in st.session_state:
# # # # # #     st.session_state.messages = []
# # # # # # if "video_data" not in st.session_state:
# # # # # #     st.session_state.video_data = []

# # # # # # # Display chat messages
# # # # # # for message in st.session_state.messages:
# # # # # #     with st.chat_message(message["role"]):
# # # # # #         st.markdown(message["content"])

# # # # # # # Video upload section
# # # # # # with st.expander("Upload Videos or Add Links"):
# # # # # #     uploaded_files = st.file_uploader(
# # # # # #         "Choose video files", 
# # # # # #         type=["mp4", "mov", "avi"],
# # # # # #         accept_multiple_files=True
# # # # # #     )
# # # # # #     video_links = st.text_area(
# # # # # #         "Enter video links (one per line)",
# # # # # #         help="Supported: YouTube, Vimeo, etc."
# # # # # #     )
    
# # # # # #     if st.button("Process Videos"):
# # # # # #         with st.spinner("Processing videos..."):
# # # # # #             # Clear previous data
# # # # # #             st.session_state.video_data = []
            
# # # # # #             # Process uploaded files
# # # # # #             for uploaded_file in uploaded_files:
# # # # # #                 with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
# # # # # #                     tmp_file.write(uploaded_file.read())
# # # # # #                     st.session_state.video_data.append(process_video_file(tmp_file.name))
            
# # # # # #             # Process video links
# # # # # #             if video_links:
# # # # # #                 for link in video_links.split('\n'):
# # # # # #                     if link.strip():
# # # # # #                         try:
# # # # # #                             st.session_state.video_data.append(process_video_link(link.strip()))
# # # # # #                         except Exception as e:
# # # # # #                             st.error(f"Couldn't process {link}: {str(e)}")
            
# # # # # #             st.success(f"Processed {len(st.session_state.video_data)} videos")

# # # # # # # Chat input
# # # # # # if prompt := st.chat_input("Ask a question about the videos"):
# # # # # #     # Add user message to chat history
# # # # # #     st.session_state.messages.append({"role": "user", "content": prompt})
    
# # # # # #     # Display user message
# # # # # #     with st.chat_message("user"):
# # # # # #         st.markdown(prompt)
    
# # # # # #     # Check if we have videos to analyze
# # # # # #     if not st.session_state.video_data:
# # # # # #         response = "Please upload videos or provide video links first."
# # # # # #     else:
# # # # # #         # Analyze videos
# # # # # #         with st.spinner("Analyzing videos..."):
# # # # # #             analysis_result = analyze_videos(st.session_state.video_data, prompt)
            
# # # # # #             # Prepare detailed response with timestamps
# # # # # #             response = analysis_result['explanation']
            
# # # # # #             # Add preview of key frames from most relevant segments
# # # # # #             relevant_video = analysis_result['most_relevant']['video_data']
# # # # # #             relevant_segments = analysis_result['most_relevant']['relevant_segments']
            
# # # # # #             if relevant_segments:
# # # # # #                 response += "\n\n**Preview of Key Moments:**"
                
# # # # # #                 # Get frames closest to segment starts
# # # # # #                 cap = cv2.VideoCapture(relevant_video['path'])
# # # # # #                 fps = cap.get(cv2.CAP_PROP_FPS)
                
# # # # # #                 for seg in relevant_segments[:3]:  # Show up to 3 frames
# # # # # #                     frame_pos = int(seg['start'] * fps)
# # # # # #                     cap.set(cv2.CAP_PROP_POS_FRAMES, frame_pos)
# # # # # #                     ret, frame = cap.read()
# # # # # #                     if ret:
# # # # # #                         st.image(
# # # # # #                             Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)),
# # # # # #                             caption=f"At {format_timestamp(seg['start'])}: {seg['text'][:50]}...",
# # # # # #                             width=300
# # # # # #                         )
# # # # # #                 cap.release()
    
# # # # # #     # Display assistant response
# # # # # #     with st.chat_message("assistant"):
# # # # # #         st.markdown(response)
    
# # # # # #     # Add assistant response to chat history
# # # # # #     st.session_state.messages.append({"role": "assistant", "content": response})


# # # # # import streamlit as st
# # # # # import os
# # # # # import tempfile
# # # # # from typing import List, Dict
# # # # # import numpy as np
# # # # # from PIL import Image
# # # # # import cv2
# # # # # import whisper
# # # # # from sentence_transformers import SentenceTransformer
# # # # # import youtube_dl

# # # # # # Initialize models (cache these to avoid reloading)

# # # # # ydl_opts = {
# # # # #     'format': 'bestvideo+bestaudio/best',
# # # # #     'ffmpeg_location': r'C:\ffmpeg\bin',
# # # # #     'outtmpl': '%(title)s.%(ext)s',
# # # # #     'postprocessors': [{
# # # # #         'key': 'FFmpegVideoConvertor',
# # # # #         'preferedformat': 'mp4',
# # # # #     }],
# # # # #     'verbose': True,  # Add this line for detailed output
# # # # # }

# # # # # @st.cache_resource
# # # # # def load_models():
# # # # #     # Whisper for speech-to-text
# # # # #     whisper_model = whisper.load_model("base")
# # # # #     # Sentence Transformer for text similarity
# # # # #     text_model = SentenceTransformer('all-MiniLM-L6-v2')
# # # # #     return whisper_model, text_model

# # # # # whisper_model, text_model = load_models()

# # # # # def process_video_file(video_path: str) -> Dict:
# # # # #     """Process an uploaded video file"""
# # # # #     # Extract metadata
# # # # #     cap = cv2.VideoCapture(video_path)
# # # # #     fps = cap.get(cv2.CAP_PROP_FPS)
# # # # #     frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
# # # # #     duration = frame_count / fps
    
# # # # #     # Extract key frames (simplified - just getting some frames)
# # # # #     key_frames = []
# # # # #     frame_interval = int(frame_count / 5)  # Get 5 frames
# # # # #     for i in range(0, frame_count, frame_interval):
# # # # #         cap.set(cv2.CAP_PROP_POS_FRAMES, i)
# # # # #         ret, frame = cap.read()
# # # # #         if ret:
# # # # #             key_frames.append(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
    
# # # # #     cap.release()
    
# # # # #     # Transcribe audio
# # # # #     transcript = whisper_model.transcribe(video_path)["text"]
    
# # # # #     return {
# # # # #         'type': 'file',
# # # # #         'path': video_path,
# # # # #         'metadata': {
# # # # #             'duration': duration,
# # # # #             'fps': fps,
# # # # #             'frame_count': frame_count
# # # # #         },
# # # # #         'key_frames': key_frames,
# # # # #         'transcript': transcript
# # # # #     }

# # # # # def process_video_link(url: str) -> Dict:
# # # # #     """Process a video link (YouTube, etc.)"""
# # # # #     # Download video using youtube-dl
# # # # #     ydl_opts = {
# # # # #         'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
# # # # #         'outtmpl': os.path.join(tempfile.gettempdir(), '%(id)s.%(ext)s'),
# # # # #         'quiet': True
# # # # #     }
    
# # # # #     with youtube_dl.YoutubeDL(ydl_opts) as ydl:
# # # # #         info = ydl.extract_info(url, download=True)
# # # # #         filename = ydl.prepare_filename(info)
    
# # # # #     # Process the downloaded file
# # # # #     video_data = process_video_file(filename)
# # # # #     video_data['type'] = 'link'
# # # # #     video_data['source_url'] = url
    
# # # # #     return video_data

# # # # # def analyze_videos(video_data: List[Dict], question: str) -> Dict:
# # # # #     """Analyze multiple videos against a question"""
# # # # #     # Embed the question
# # # # #     question_embedding = text_model.encode(question)
    
# # # # #     # Compare against each video's transcript
# # # # #     relevance_scores = []
# # # # #     for data in video_data:
# # # # #         # Embed the transcript
# # # # #         transcript_embedding = text_model.encode(data['transcript'])
# # # # #         # Calculate cosine similarity
# # # # #         similarity = np.dot(question_embedding, transcript_embedding) / (
# # # # #             np.linalg.norm(question_embedding) * np.linalg.norm(transcript_embedding)
# # # # #         )
# # # # #         relevance_scores.append(similarity)
    
# # # # #     # Determine most relevant video
# # # # #     most_relevant_idx = np.argmax(relevance_scores)
    
# # # # #     return {
# # # # #         'most_relevant': video_data[most_relevant_idx],
# # # # #         'scores': relevance_scores,
# # # # #         'explanation': generate_explanation(video_data[most_relevant_idx], question)
# # # # #     }

# # # # # def generate_explanation(video_data: Dict, question: str) -> str:
# # # # #     """Generate explanation for why video is relevant"""
# # # # #     explanation = []
    
# # # # #     if video_data['type'] == 'link':
# # # # #         explanation.append(f"The video from {video_data['source_url']} is most relevant because:")
# # # # #     else:
# # # # #         explanation.append("The uploaded video is most relevant because:")
    
# # # # #     explanation.append(f"- The transcript contains concepts related to your question about '{question}'")
# # # # #     explanation.append(f"- Video duration: {video_data['metadata']['duration']:.2f} seconds")
    
# # # # #     return "\n".join(explanation)

# # # # # # Streamlit UI
# # # # # st.title("Video Analysis Chatbot")

# # # # # # Initialize session state for chat history
# # # # # if "messages" not in st.session_state:
# # # # #     st.session_state.messages = []

# # # # # # Display chat messages
# # # # # for message in st.session_state.messages:
# # # # #     with st.chat_message(message["role"]):
# # # # #         st.markdown(message["content"])

# # # # # # Video upload section
# # # # # with st.expander("Upload Videos or Add Links"):
# # # # #     uploaded_files = st.file_uploader(
# # # # #         "Choose video files", 
# # # # #         type=["mp4", "mov", "avi"],
# # # # #         accept_multiple_files=True
# # # # #     )
# # # # #     video_links = st.text_area(
# # # # #         "Enter video links (one per line)",
# # # # #         help="Supported: YouTube, Vimeo, etc."
# # # # #     )

# # # # # # Process videos when submitted
# # # # # video_data = []
# # # # # if uploaded_files or video_links:
# # # # #     with st.spinner("Processing videos..."):
# # # # #         # Process uploaded files
# # # # #         for uploaded_file in uploaded_files:
# # # # #             with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
# # # # #                 tmp_file.write(uploaded_file.read())
# # # # #                 video_data.append(process_video_file(tmp_file.name))
        
# # # # #         # Process video links
# # # # #         if video_links:
# # # # #             for link in video_links.split('\n'):
# # # # #                 if link.strip():
# # # # #                     try:
# # # # #                         video_data.append(process_video_link(link.strip()))
# # # # #                     except Exception as e:
# # # # #                         st.error(f"Couldn't process {link}: {str(e)}")
        
# # # # #         st.session_state.video_data = video_data
# # # # #         st.success(f"Processed {len(video_data)} videos")

# # # # # # Chat input
# # # # # if prompt := st.chat_input("Ask a question about the videos"):
# # # # #     # Add user message to chat history
# # # # #     st.session_state.messages.append({"role": "user", "content": prompt})
    
# # # # #     # Display user message
# # # # #     with st.chat_message("user"):
# # # # #         st.markdown(prompt)
    
# # # # #     # Check if we have videos to analyze
# # # # #     if "video_data" not in st.session_state or not st.session_state.video_data:
# # # # #         response = "Please upload videos or provide video links first."
# # # # #     else:
# # # # #         # Analyze videos
# # # # #         with st.spinner("Analyzing videos..."):
# # # # #             analysis_result = analyze_videos(st.session_state.video_data, prompt)
            
# # # # #             # Prepare response
# # # # #             relevant_video = analysis_result['most_relevant']
# # # # #             if relevant_video['type'] == 'link':
# # # # #                 video_ref = f"[Video Link]({relevant_video['source_url']})"
# # # # #             else:
# # # # #                 video_ref = "Uploaded Video"
            
# # # # #             response = f"""
# # # # #             **Most Relevant Video:** {video_ref}
            
# # # # #             **Explanation:**  
# # # # #             {analysis_result['explanation']}
            
# # # # #             **Relevance Score:** {analysis_result['scores'][np.argmax(analysis_result['scores'])]:.2f}
# # # # #             """
    
# # # # #     # Display assistant response
# # # # #     with st.chat_message("assistant"):
# # # # #         st.markdown(response)
    
# # # # #     # Add assistant response to chat history
# # # # #     st.session_state.messages.append({"role": "assistant", "content": response})



# # # # import streamlit as st
# # # # import google.generativeai as genai
# # # # import os
# # # # import time # For simulating delays
# # # # import uuid # For unique filenames/blobnames
# # # # # from google.cloud import storage # Uncomment for actual GCS
# # # # # import yt_dlp # Uncomment for actual YouTube downloads

# # # # # --- Configuration ---
# # # # GEMINI_API_KEY = st.secrets.get("API_KEY", os.environ.get("API_KEY"))
# # # # # GCS_BUCKET_NAME = st.secrets.get("GCS_BUCKET_NAME", "your-gcs-bucket-for-videos") # REPLACE or use secrets
# # # # # PROJECT_ID = st.secrets.get("GCP_PROJECT_ID") # For GCS client if needed

# # # # # --- Initialize Gemini ---
# # # # if GEMINI_API_KEY:
# # # #     genai.configure(api_key=GEMINI_API_KEY)
# # # # else:
# # # #     st.error("GEMINI_API_KEY not found. Please set it in your environment or Streamlit secrets.")
# # # #     st.stop()

# # # # # --- Helper Functions (Adapted from previous example, with Streamlit feedback) ---

# # # # # Placeholder for GCS upload function
# # # # def upload_to_gcs(local_file_path, bucket_name, destination_blob_name):
# # # #     # st.write(f"Simulating GCS Upload: {local_file_path} to gs://{bucket_name}/{destination_blob_name}")
# # # #     # For testing without actual GCS, return a dummy gs path
# # # #     # In a real app, use google-cloud-storage library
# # # #     # storage_client = storage.Client(project=PROJECT_ID)
# # # #     # bucket = storage_client.bucket(bucket_name)
# # # #     # blob = bucket.blob(destination_blob_name)
# # # #     # blob.upload_from_filename(local_file_path)
# # # #     # st.success(f"Uploaded {os.path.basename(local_file_path)} to GCS.")
# # # #     # return f"gs://{bucket_name}/{destination_blob_name}"
# # # #     st.success(f"Simulated GCS Upload for {os.path.basename(local_file_path)}")
# # # #     return f"gs://{bucket_name}/{destination_blob_name}" # Dummy path

# # # # # Placeholder for video download
# # # # def download_video_from_url(url, output_filename="temp_video.mp4"):
# # # #     st.write(f"Simulating download of: {url}")
# # # #     # Uncomment and implement with yt-dlp and requests for real downloads
# # # #     # if "youtube.com" in url or "youtu.be" in url:
# # # #     #     ydl_opts = {'outtmpl': output_filename, 'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4', 'quiet': True}
# # # #     #     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
# # # #     #         ydl.download([url])
# # # #     # else:
# # # #     #     import requests
# # # #     #     response = requests.get(url, stream=True)
# # # #     #     with open(output_filename, 'wb') as f:
# # # #     #         for chunk in response.iter_content(chunk_size=8192):
# # # #     #             f.write(chunk)
# # # #     # Create a tiny dummy mp4 file if it doesn't exist for the API to have something
# # # #     if not os.path.exists(output_filename):
# # # #         with open(output_filename, 'wb') as f: f.write(b'\x00\x00\x00\x18ftypmp42') # Minimal mp4 header
# # # #     st.success(f"Simulated download of {url} to {output_filename}")
# # # #     return output_filename

# # # # # Process a single video with Gemini 1.5 Pro (or simulate)
# # # # def get_video_analysis_gemini_1_5_pro(gcs_uri, original_source_name):
# # # #     st.write(f"🤖 Analyzing video via Gemini: {original_source_name} (URI: {gcs_uri})")
# # # #     # --- Mocking Gemini 1.5 Pro analysis for now ---
# # # #     # In a real scenario, this would make the API call as shown previously
# # # #     # model = genai.GenerativeModel('gemini-1.5-pro-latest')
# # # #     # video_part = genai.types.Part.from_uri(gcs_uri, mime_type="video/mp4") # Adjust mime_type if needed
# # # #     # prompt = "Analyze this video. Provide a concise transcript of its audio (max 200 words), a brief description of its key visual elements (max 100 words), and a comprehensive summary of its overall content (max 150 words). Structure your response clearly."
# # # #     # try:
# # # #     #     response = model.generate_content([prompt, video_part])
# # # #     #     analysis_text = response.text
# # # #     #     # Basic parsing (improve this for robust extraction)
# # # #     #     summary = "Summary: " + analysis_text.split("Summary:")[-1].split("Transcript:")[0].strip() if "Summary:" in analysis_text else "Could not parse summary."
# # # #     #     transcript = "Transcript: " + analysis_text.split("Transcript:")[-1].split("Visual Description:")[0].strip() if "Transcript:" in analysis_text else "Could not parse transcript."
# # # #     #     st.success(f"Analysis complete for {original_source_name}")
# # # #     #     return {"source_name": original_source_name, "gcs_uri": gcs_uri, "summary": summary, "transcript": transcript}
# # # #     # except Exception as e:
# # # #     #     st.error(f"Error analyzing {original_source_name} with Gemini: {e}")
# # # #     #     return {"source_name": original_source_name, "gcs_uri": gcs_uri, "summary": f"Error: {e}", "transcript": ""}

# # # #     # --- MOCK RESPONSE ---
# # # #     time.sleep(2) # Simulate processing time
# # # #     mock_summary = f"This is a mock summary for '{original_source_name}'. It discusses various interesting topics relevant to its title."
# # # #     mock_transcript = f"Mock transcript snippet for '{original_source_name}': Hello and welcome! Today we explore..."
# # # #     if "cat" in original_source_name.lower():
# # # #         mock_summary = "This video appears to be about cats, showing their playful antics and adorable moments."
# # # #         mock_transcript = "Meow, purr, hiss. The cat jumps on the counter."
# # # #     elif "dog" in original_source_name.lower():
# # # #         mock_summary = "A heartwarming video about dogs, their loyalty, and different breeds. It includes scenes of dogs playing fetch."
# # # #         mock_transcript = "Woof woof! Good boy! Fetch the ball!"

# # # #     st.success(f"Mock analysis complete for {original_source_name}")
# # # #     return {"source_name": original_source_name, "gcs_uri": gcs_uri, "summary": mock_summary, "transcript": mock_transcript}


# # # # # Find most relevant video using Gemini (text model like gemini-pro)
# # # # def find_most_relevant_video_gemini_judge(user_question, video_analysis_list):
# # # #     if not video_analysis_list:
# # # #         st.warning("No videos were processed to analyze.")
# # # #         return "No videos provided to analyze.", None

# # # #     model_judge = genai.GenerativeModel('gemini-pro') # Use text model for judging summaries

# # # #     prompt_parts = [
# # # #         "You are an AI assistant. A user has asked a question and provided information from several videos.",
# # # #         "Your task is to determine which video is the most relevant reference for answering the question.",
# # # #         f"\nUser Question: \"{user_question}\"\n",
# # # #         "Available Video Information:"
# # # #     ]

# # # #     for i, analysis_data in enumerate(video_analysis_list):
# # # #         prompt_parts.append(f"\nVideo {i+1} (Source: {analysis_data['source_name']}):")
# # # #         prompt_parts.append(f"Summary: {analysis_data['summary']}")
# # # #         # prompt_parts.append(f"Transcript Snippet: {analysis_data.get('transcript', '')[:150]}...") # Optional

# # # #     prompt_parts.append("\nBased on the user's question and the video information, which video (by its Source identifier) is the most appropriate reference?")
# # # #     prompt_parts.append("Please provide the Source identifier of the best video and explain your reasoning clearly, referencing specific aspects of its content that make it relevant.")
# # # #     prompt_parts.append("If no video is sufficiently relevant, state that clearly.")
# # # #     prompt_parts.append("Output the chosen Source identifier on a line by itself first, like: 'Chosen Video Source: [Source Name]'")

# # # #     full_prompt = "\n".join(prompt_parts)

# # # #     try:
# # # #         st.write("🤖 Asking Gemini to pick the best video...")
# # # #         response = model_judge.generate_content(full_prompt)
# # # #         ai_response_text = response.text

# # # #         chosen_video_source = None
# # # #         for line in ai_response_text.splitlines():
# # # #             if line.startswith("Chosen Video Source:"):
# # # #                 chosen_video_source = line.replace("Chosen Video Source:", "").strip()
# # # #                 break
        
# # # #         st.success("Gemini has made a selection!")
# # # #         return ai_response_text, chosen_video_source
# # # #     except Exception as e:
# # # #         st.error(f"Error during Gemini evaluation: {e}")
# # # #         return f"Error during Gemini evaluation: {e}", None

# # # # # --- Streamlit App UI ---

# # # # st.set_page_config(layout="wide", page_title="Video Analysis Bot")
# # # # st.title("🎬 Video Analysis Bot with Gemini AI")
# # # # st.markdown("""
# # # # Upload video files or provide links. Then, ask a question about their content,
# # # # and the bot will try to identify the most relevant video.
# # # # **(Note: GCS upload, video download, and Gemini 1.5 Pro analysis are currently SIMULATED for this demo)**
# # # # """)

# # # # # Initialize session state
# # # # if 'video_sources_input' not in st.session_state:
# # # #     st.session_state.video_sources_input = []
# # # # if 'processed_videos_data' not in st.session_state:
# # # #     st.session_state.processed_videos_data = []
# # # # if 'analysis_complete' not in st.session_state:
# # # #     st.session_state.analysis_complete = False
# # # # if 'user_question' not in st.session_state:
# # # #     st.session_state.user_question = ""
# # # # if 'final_result' not in st.session_state:
# # # #     st.session_state.final_result = None


# # # # # --- Step 1: Video Input ---
# # # # st.header("Step 1: Provide Videos")

# # # # col1, col2 = st.columns(2)

# # # # with col1:
# # # #     st.subheader("Upload Video Files")
# # # #     uploaded_files = st.file_uploader("Choose video files", type=['mp4', 'mov', 'avi', 'mkv'], accept_multiple_files=True, key="file_uploader")
# # # #     if uploaded_files:
# # # #         for uploaded_file in uploaded_files:
# # # #             # Avoid re-adding if already processed or listed
# # # #             if not any(entry['type'] == 'file' and entry['name'] == uploaded_file.name for entry in st.session_state.video_sources_input):
# # # #                 st.session_state.video_sources_input.append({'type': 'file', 'data': uploaded_file, 'name': uploaded_file.name, 'id': str(uuid.uuid4())})

# # # # with col2:
# # # #     st.subheader("Or Add Video Links")
# # # #     video_link = st.text_input("Enter a video URL (e.g., YouTube, direct .mp4) and press Enter", key="link_input_field")
# # # #     if st.button("Add Link", key="add_link_button") and video_link:
# # # #         if video_link and not any(entry['type'] == 'link' and entry['url'] == video_link for entry in st.session_state.video_sources_input):
# # # #              st.session_state.video_sources_input.append({'type': 'link', 'url': video_link, 'name': video_link, 'id': str(uuid.uuid4())})
# # # #              st.rerun() # Rerun to update list immediately


# # # # st.subheader("Videos to Process:")
# # # # if not st.session_state.video_sources_input:
# # # #     st.info("No videos added yet.")
# # # # else:
# # # #     for i, src_info in enumerate(st.session_state.video_sources_input):
# # # #         item_name = src_info['name']
# # # #         col_name, col_button = st.columns([0.9, 0.1])
# # # #         with col_name:
# # # #             st.write(f"{i+1}. {src_info['type'].capitalize()}: {item_name}")
# # # #         with col_button:
# # # #             if st.button("❌", key=f"remove_{src_info['id']}", help=f"Remove {item_name}"):
# # # #                 st.session_state.video_sources_input.pop(i)
# # # #                 # If this item was already processed, remove it from processed_videos_data as well
# # # #                 st.session_state.processed_videos_data = [
# # # #                     pv for pv in st.session_state.processed_videos_data if pv.get('original_id') != src_info['id']
# # # #                 ]
# # # #                 if not st.session_state.video_sources_input: # if all removed
# # # #                     st.session_state.analysis_complete = False
# # # #                     st.session_state.final_result = None
# # # #                 st.rerun()


# # # # if st.session_state.video_sources_input and st.button("Process Videos", key="process_videos_button", disabled=st.session_state.analysis_complete):
# # # #     st.session_state.analysis_complete = False # Reset if re-processing
# # # #     st.session_state.processed_videos_data = []
# # # #     st.session_state.final_result = None

# # # #     with st.spinner("Processing videos... This may take a while. (Simulating GCS/Downloads/Gemini Analysis)"):
# # # #         temp_dir = "streamlit_temp_videos"
# # # #         if not os.path.exists(temp_dir):
# # # #             os.makedirs(temp_dir)

# # # #         for src_info in st.session_state.video_sources_input:
# # # #             # Skip if already processed for this session (based on ID)
# # # #             if any(pv.get('original_id') == src_info['id'] for pv in st.session_state.processed_videos_data):
# # # #                 st.write(f"Skipping already processed: {src_info['name']}")
# # # #                 continue

# # # #             local_video_path_for_upload = None
# # # #             original_identifier = src_info['name']
# # # #             gcs_uri = None

# # # #             try:
# # # #                 if src_info['type'] == 'file':
# # # #                     uploaded_file = src_info['data']
# # # #                     local_video_path_for_upload = os.path.join(temp_dir, f"{src_info['id']}_{uploaded_file.name}")
# # # #                     with open(local_video_path_for_upload, "wb") as f:
# # # #                         f.write(uploaded_file.getbuffer())
# # # #                     st.write(f"Saved uploaded file: {uploaded_file.name}")
# # # #                     original_identifier = uploaded_file.name
                
# # # #                 elif src_info['type'] == 'link':
# # # #                     video_url = src_info['url']
# # # #                     safe_filename_part = "".join(c if c.isalnum() or c in ('.', '_') else '_' for c in video_url.split('/')[-1])
# # # #                     output_dl_filename = os.path.join(temp_dir, f"{src_info['id']}_{safe_filename_part}.mp4")
# # # #                     local_video_path_for_upload = download_video_from_url(video_url, output_filename=output_dl_filename)
# # # #                     original_identifier = video_url

# # # #                 if local_video_path_for_upload:
# # # #                     # Simulate GCS Upload
# # # #                     # blob_name = f"chatbot_uploads/{src_info['id']}_{os.path.basename(local_video_path_for_upload)}"
# # # #                     # gcs_uri = upload_to_gcs(local_video_path_for_upload, GCS_BUCKET_NAME, blob_name)
# # # #                     gcs_uri = f"gs://simulated-bucket/{src_info['id']}_{os.path.basename(local_video_path_for_upload)}" # Dummy GCS URI for simulation

# # # #                 if gcs_uri:
# # # #                     analysis = get_video_analysis_gemini_1_5_pro(gcs_uri, original_identifier)
# # # #                     if analysis and "Error" not in analysis.get("summary", ""):
# # # #                         analysis['original_id'] = src_info['id'] # Link back to input item
# # # #                         st.session_state.processed_videos_data.append(analysis)
# # # #                     else:
# # # #                         st.error(f"Could not analyze: {original_identifier}")
                
# # # #                 # Clean up local temp file (optional, or do at end of session)
# # # #                 # if local_video_path_for_upload and os.path.exists(local_video_path_for_upload):
# # # #                 # os.remove(local_video_path_for_upload)

# # # #             except Exception as e:
# # # #                 st.error(f"Error processing {original_identifier}: {e}")

# # # #     if st.session_state.processed_videos_data:
# # # #         st.session_state.analysis_complete = True
# # # #         st.success("All videos processed and analyzed (simulated)!")
# # # #         st.balloons()
# # # #     else:
# # # #         st.error("No videos could be processed.")

# # # # # --- Step 2: Ask Question (only if videos are processed) ---
# # # # if st.session_state.analysis_complete:
# # # #     st.header("Step 2: Ask a Question")
# # # #     st.session_state.user_question = st.text_input(
# # # #         "What question do you have about the content of these videos?",
# # # #         value=st.session_state.user_question,
# # # #         key="question_input"
# # # #     )

# # # #     if st.button("Find Most Relevant Video", key="find_relevant_button") and st.session_state.user_question:
# # # #         if not st.session_state.processed_videos_data:
# # # #             st.warning("Please process some videos first!")
# # # #         else:
# # # #             with st.spinner("Gemini is thinking..."):
# # # #                 evaluation_response, chosen_source = find_most_relevant_video_gemini_judge(
# # # #                     st.session_state.user_question,
# # # #                     st.session_state.processed_videos_data
# # # #                 )
# # # #                 st.session_state.final_result = {
# # # #                     "evaluation_response": evaluation_response,
# # # #                     "chosen_source": chosen_source
# # # #                 }

# # # # # --- Step 3: Display Results ---
# # # # if st.session_state.final_result:
# # # #     st.header("Step 3: Results")
# # # #     result = st.session_state.final_result
# # # #     if result["chosen_source"]:
# # # #         st.subheader(f"🏆 Most Relevant Video: {result['chosen_source']}")
# # # #         st.markdown("**Gemini's Reasoning:**")
# # # #         # Display the full response, which should include the reasoning
# # # #         st.info(result["evaluation_response"])

# # # #         # Optionally display summary of the chosen video again
# # # #         chosen_video_data = next((v for v in st.session_state.processed_videos_data if v['source_name'] == result['chosen_source']), None)
# # # #         if chosen_video_data:
# # # #             with st.expander(f"Details for '{result['chosen_source']}'"):
# # # #                 st.markdown(f"**Summary:** {chosen_video_data['summary']}")
# # # #                 st.markdown(f"**Transcript Snippet:** {chosen_video_data.get('transcript', 'N/A')}")
# # # #     else:
# # # #         st.warning("Gemini could not definitively choose a most relevant video based on the query, or no videos were sufficiently relevant.")
# # # #         st.markdown("**Gemini's Full Response:**")
# # # #         st.info(result["evaluation_response"])

# # # # st.sidebar.subheader("Processed Video Summaries")
# # # # if st.session_state.processed_videos_data:
# # # #     for i, data in enumerate(st.session_state.processed_videos_data):
# # # #         with st.sidebar.expander(f"{i+1}. {data['source_name']}"):
# # # #             st.markdown(f"**Summary:** {data['summary']}")
# # # #             st.markdown(f"**GCS URI (Simulated):** `{data['gcs_uri']}`")
# # # #             st.markdown(f"**Transcript Snippet:** {data.get('transcript', 'N/A')}")
# # # # else:
# # # #     st.sidebar.info("No videos processed yet.")

# # # # # --- For Debugging ---
# # # # # st.sidebar.subheader("Debug: Session State")
# # # # # st.sidebar.json(st.session_state)

# # # import streamlit as st
# # # import google.generativeai as genai
# # # import os
# # # import time # For simulating delays
# # # import uuid # For unique filenames/blobnames
# # # # from google.cloud import storage # Uncomment for actual GCS
# # # # import yt_dlp # Uncomment for actual YouTube downloads

# # # # --- Configuration ---
# # # GEMINI_API_KEY = st.secrets.get("API_KEY", os.environ.get("API_KEY"))
# # # # GCS_BUCKET_NAME = st.secrets.get("GCS_BUCKET_NAME", "your-gcs-bucket-for-videos") # REPLACE or use secrets
# # # # PROJECT_ID = st.secrets.get("GCP_PROJECT_ID") # For GCS client if needed

# # # # --- Initialize Gemini ---
# # # if GEMINI_API_KEY:
# # #     genai.configure(api_key=GEMINI_API_KEY)
# # # else:
# # #     st.error("GEMINI_API_KEY not found. Please set it in your environment or Streamlit secrets.")
# # #     st.stop()

# # # # --- Helper Functions (largely the same, with a new one for single video Q&A) ---

# # # def upload_to_gcs(local_file_path, bucket_name, destination_blob_name):
# # #     st.success(f"Simulated GCS Upload for {os.path.basename(local_file_path)}")
# # #     return f"gs://{bucket_name}/{destination_blob_name}"

# # # def download_video_from_url(url, output_filename="temp_video.mp4"):
# # #     st.write(f"Simulating download of: {url}")
# # #     if not os.path.exists(output_filename): # Create dummy if not exists
# # #         with open(output_filename, 'wb') as f: f.write(b'\x00\x00\x00\x18ftypmp42')
# # #     st.success(f"Simulated download of {url} to {output_filename}")
# # #     return output_filename

# # # def get_video_analysis_gemini_1_5_pro(gcs_uri, original_source_name):
# # #     st.write(f"🤖 Analyzing video via Gemini: {original_source_name} (URI: {gcs_uri})")
# # #     time.sleep(1) # Simulate processing time
# # #     mock_summary = f"This is a mock summary for '{original_source_name}'. It covers several key points from the video, including its main purpose and visual highlights."
# # #     mock_transcript = f"Mock transcript for '{original_source_name}': Welcome to the video. We will discuss A, B, and C. Visually, you can see X, Y, and Z."
# # #     if "cat" in original_source_name.lower():
# # #         mock_summary = "This video showcases feline agility and typical cat behaviors. It highlights playful interactions and moments of quiet contemplation."
# # #         mock_transcript = "The cat gracefully leaps onto the bookshelf. Later, it curls up for a nap in a sunbeam. Purring can be heard."
# # #     elif "dog" in original_source_name.lower():
# # #         mock_summary = "A comprehensive look at canine companionship, featuring various breeds and their unique characteristics. The video emphasizes training and outdoor activities."
# # #         mock_transcript = "A golden retriever enthusiastically plays fetch in the park. A trainer demonstrates basic obedience commands. The dog wags its tail."
# # #     elif "setup" in original_source_name.lower():
# # #         mock_summary = "This video tutorial guides viewers through the initial setup process for a new software application, detailing each step clearly."
# # #         mock_transcript = "First, navigate to the settings menu. Then, select 'User Preferences'. Ensure you save your changes before exiting."

# # #     st.success(f"Mock analysis complete for {original_source_name}")
# # #     return {"source_name": original_source_name, "gcs_uri": gcs_uri, "summary": mock_summary, "transcript": mock_transcript}

# # # def find_most_relevant_video_gemini_judge(user_question, video_analysis_list):
# # #     # ... (same as before) ...
# # #     if not video_analysis_list:
# # #         st.warning("No videos were processed to analyze.")
# # #         return "No videos provided to analyze.", None
# # #     model_judge = genai.GenerativeModel('gemini-pro')
# # #     prompt_parts = [
# # #         "You are an AI assistant. A user has asked a question and provided information from several videos.",
# # #         "Your task is to determine which video is the most relevant reference for answering the question.",
# # #         f"\nUser Question: \"{user_question}\"\n", "Available Video Information:"
# # #     ]
# # #     for i, analysis_data in enumerate(video_analysis_list):
# # #         prompt_parts.append(f"\nVideo {i+1} (Source: {analysis_data['source_name']}):")
# # #         prompt_parts.append(f"Summary: {analysis_data['summary']}")
# # #     prompt_parts.append("\nBased on the user's question and the video information, which video (by its Source identifier) is the most appropriate reference?")
# # #     prompt_parts.append("Please provide the Source identifier of the best video and explain your reasoning clearly, referencing specific aspects of its content that make it relevant.")
# # #     prompt_parts.append("If no video is sufficiently relevant, state that clearly.")
# # #     prompt_parts.append("Output the chosen Source identifier on a line by itself first, like: 'Chosen Video Source: [Source Name]'")
# # #     full_prompt = "\n".join(prompt_parts)
# # #     try:
# # #         st.write("🤖 Asking Gemini to pick the best video...")
# # #         response = model_judge.generate_content(full_prompt)
# # #         ai_response_text = response.text
# # #         chosen_video_source = None
# # #         for line in ai_response_text.splitlines():
# # #             if line.startswith("Chosen Video Source:"):
# # #                 chosen_video_source = line.replace("Chosen Video Source:", "").strip()
# # #                 break
# # #         st.success("Gemini has made a selection!")
# # #         return ai_response_text, chosen_video_source
# # #     except Exception as e:
# # #         st.error(f"Error during Gemini evaluation: {e}")
# # #         return f"Error during Gemini evaluation: {e}", None

# # # def answer_question_about_single_video(user_question, video_data):
# # #     """Answers a question based on the content of a single video."""
# # #     model = genai.GenerativeModel('gemini-pro') # Or gemini-1.5-pro if you want it to "re-watch" from GCS_URI
    
# # #     # For gemini-pro, provide text context.
# # #     # For gemini-1.5-pro, you could potentially provide the gcs_uri again and let it re-analyze with the question in mind.
# # #     # For simplicity and cost, we'll use the already extracted text (summary + transcript) for gemini-pro.

# # #     prompt = f"""
# # #     You are an AI assistant. You have been provided with the content of a single video.
# # #     Please answer the user's question based SOLELY on the information available in this video's content.
# # #     If the information is not in the video, state that clearly.

# # #     Video Source Name: {video_data['source_name']}
# # #     Video Summary: {video_data['summary']}
# # #     Video Transcript (partial or full): {video_data.get('transcript', 'Transcript not available.')}

# # #     User Question: "{user_question}"

# # #     Your Answer:
# # #     """
# # #     try:
# # #         st.write(f"🤖 Asking Gemini about '{video_data['source_name']}'...")
# # #         response = model.generate_content(prompt)
# # #         st.success("Gemini has answered!")
# # #         return response.text
# # #     except Exception as e:
# # #         st.error(f"Error asking Gemini about single video: {e}")
# # #         return f"Error: {e}"


# # # # --- Streamlit App UI ---
# # # st.set_page_config(layout="wide", page_title="Video Analysis Bot")
# # # st.title("🎬 Video Analysis Bot with Gemini AI")
# # # st.markdown("""
# # # Upload video files or provide links. Then, either ask a question to find the most relevant video OR select a single video to ask specific questions about its content.
# # # **(Note: GCS upload, video download, and Gemini 1.5 Pro analysis are currently SIMULATED for this demo)**
# # # """)

# # # # Initialize session state (added new states)
# # # if 'video_sources_input' not in st.session_state: st.session_state.video_sources_input = []
# # # if 'processed_videos_data' not in st.session_state: st.session_state.processed_videos_data = []
# # # if 'analysis_complete' not in st.session_state: st.session_state.analysis_complete = False
# # # if 'query_mode' not in st.session_state: st.session_state.query_mode = "Compare Videos" # New state
# # # if 'selected_video_for_query' not in st.session_state: st.session_state.selected_video_for_query = None # New state
# # # if 'single_video_question' not in st.session_state: st.session_state.single_video_question = "" # New state
# # # if 'single_video_answer' not in st.session_state: st.session_state.single_video_answer = None # New state
# # # if 'multi_video_question' not in st.session_state: st.session_state.multi_video_question = ""
# # # if 'multi_video_result' not in st.session_state: st.session_state.multi_video_result = None


# # # # --- Step 1: Video Input ---
# # # st.header("Step 1: Provide Videos")
# # # # ... (Video input UI is the same as before) ...
# # # col1, col2 = st.columns(2)
# # # with col1:
# # #     st.subheader("Upload Video Files")
# # #     uploaded_files = st.file_uploader("Choose video files", type=['mp4', 'mov', 'avi', 'mkv'], accept_multiple_files=True, key="file_uploader")
# # #     if uploaded_files:
# # #         for uploaded_file in uploaded_files:
# # #             if not any(entry['type'] == 'file' and entry['name'] == uploaded_file.name for entry in st.session_state.video_sources_input):
# # #                 st.session_state.video_sources_input.append({'type': 'file', 'data': uploaded_file, 'name': uploaded_file.name, 'id': str(uuid.uuid4())})
# # # with col2:
# # #     st.subheader("Or Add Video Links")
# # #     video_link = st.text_input("Enter a video URL (e.g., YouTube, direct .mp4) and press Enter", key="link_input_field")
# # #     if st.button("Add Link", key="add_link_button") and video_link:
# # #         if video_link and not any(entry['type'] == 'link' and entry['url'] == video_link for entry in st.session_state.video_sources_input):
# # #              st.session_state.video_sources_input.append({'type': 'link', 'url': video_link, 'name': video_link, 'id': str(uuid.uuid4())})
# # #              st.rerun()

# # # st.subheader("Videos to Process:")
# # # if not st.session_state.video_sources_input:
# # #     st.info("No videos added yet.")
# # # else:
# # #     for i, src_info in enumerate(st.session_state.video_sources_input):
# # #         item_name = src_info['name']
# # #         col_name_disp, col_button_disp = st.columns([0.9, 0.1])
# # #         with col_name_disp: st.write(f"{i+1}. {src_info['type'].capitalize()}: {item_name}")
# # #         with col_button_disp:
# # #             if st.button("❌", key=f"remove_{src_info['id']}", help=f"Remove {item_name}"):
# # #                 st.session_state.video_sources_input.pop(i)
# # #                 st.session_state.processed_videos_data = [pv for pv in st.session_state.processed_videos_data if pv.get('original_id') != src_info['id']]
# # #                 if not st.session_state.video_sources_input:
# # #                     st.session_state.analysis_complete = False
# # #                     st.session_state.multi_video_result = None
# # #                     st.session_state.single_video_answer = None
# # #                 st.rerun()

# # # if st.session_state.video_sources_input and st.button("Process Videos", key="process_videos_button", disabled=st.session_state.analysis_complete):
# # #     st.session_state.analysis_complete = False
# # #     st.session_state.processed_videos_data = []
# # #     st.session_state.multi_video_result = None
# # #     st.session_state.single_video_answer = None
# # #     with st.spinner("Processing videos... (Simulating GCS/Downloads/Gemini Analysis)"):
# # #         temp_dir = "streamlit_temp_videos"; os.makedirs(temp_dir, exist_ok=True)
# # #         for src_info in st.session_state.video_sources_input:
# # #             if any(pv.get('original_id') == src_info['id'] for pv in st.session_state.processed_videos_data): continue
# # #             local_video_path_for_upload = None; original_identifier = src_info['name']; gcs_uri = None
# # #             try:
# # #                 if src_info['type'] == 'file':
# # #                     uploaded_file = src_info['data']
# # #                     local_video_path_for_upload = os.path.join(temp_dir, f"{src_info['id']}_{uploaded_file.name}")
# # #                     with open(local_video_path_for_upload, "wb") as f: f.write(uploaded_file.getbuffer())
# # #                     original_identifier = uploaded_file.name
# # #                 elif src_info['type'] == 'link':
# # #                     video_url = src_info['url']
# # #                     safe_filename_part = "".join(c if c.isalnum() or c in ('.', '_') else '_' for c in video_url.split('/')[-1])
# # #                     output_dl_filename = os.path.join(temp_dir, f"{src_info['id']}_{safe_filename_part}.mp4")
# # #                     local_video_path_for_upload = download_video_from_url(video_url, output_filename=output_dl_filename)
# # #                     original_identifier = video_url
# # #                 if local_video_path_for_upload:
# # #                     gcs_uri = f"gs://simulated-bucket/{src_info['id']}_{os.path.basename(local_video_path_for_upload)}"
# # #                 if gcs_uri:
# # #                     analysis = get_video_analysis_gemini_1_5_pro(gcs_uri, original_identifier)
# # #                     if analysis and "Error" not in analysis.get("summary", ""):
# # #                         analysis['original_id'] = src_info['id']
# # #                         st.session_state.processed_videos_data.append(analysis)
# # #                     else: st.error(f"Could not analyze: {original_identifier}")
# # #             except Exception as e: st.error(f"Error processing {original_identifier}: {e}")
# # #     if st.session_state.processed_videos_data:
# # #         st.session_state.analysis_complete = True
# # #         st.success("All videos processed and analyzed (simulated)!"); st.balloons()
# # #     else: st.error("No videos could be processed.")


# # # # --- Step 2: Choose Query Mode & Ask Question (only if videos are processed) ---
# # # if st.session_state.analysis_complete:
# # #     st.header("Step 2: Ask Your Question(s)")

# # #     # Query Mode Selection
# # #     if len(st.session_state.processed_videos_data) > 1:
# # #         st.session_state.query_mode = st.radio(
# # #             "What would you like to do?",
# # #             ("Compare Videos (Find most relevant)", "Query a Specific Video"),
# # #             key="query_mode_radio",
# # #             horizontal=True
# # #         )
# # #     elif len(st.session_state.processed_videos_data) == 1:
# # #         st.session_state.query_mode = "Query a Specific Video" # Default if only one video
# # #         st.info("Only one video processed. You can ask questions directly about its content.")
# # #     else: # Should not happen if analysis_complete is True
# # #         st.warning("No videos available for querying.")


# # #     # --- A) Compare Multiple Videos ---
# # #     if st.session_state.query_mode == "Compare Videos (Find most relevant)" and len(st.session_state.processed_videos_data) > 1:
# # #         st.subheader("Find the Most Relevant Video")
# # #         st.session_state.multi_video_question = st.text_input(
# # #             "What general question do you have to compare across videos?",
# # #             value=st.session_state.multi_video_question,
# # #             key="multi_video_question_input"
# # #         )
# # #         if st.button("Find Most Relevant Video", key="find_relevant_button") and st.session_state.multi_video_question:
# # #             with st.spinner("Gemini is comparing videos..."):
# # #                 evaluation_response, chosen_source = find_most_relevant_video_gemini_judge(
# # #                     st.session_state.multi_video_question,
# # #                     st.session_state.processed_videos_data
# # #                 )
# # #                 st.session_state.multi_video_result = {
# # #                     "evaluation_response": evaluation_response,
# # #                     "chosen_source": chosen_source
# # #                 }
# # #                 st.session_state.single_video_answer = None # Clear other result type


# # #     # --- B) Query a Specific Video ---
# # #     elif st.session_state.query_mode == "Query a Specific Video" and st.session_state.processed_videos_data:
# # #         st.subheader("Ask About a Specific Video")
        
# # #         video_options = {data['source_name']: data['original_id'] for data in st.session_state.processed_videos_data}
        
# # #         # Get the current index for the selectbox if a video was previously selected
# # #         current_selection_name = st.session_state.selected_video_for_query
# # #         current_index = 0
# # #         if current_selection_name:
# # #             try:
# # #                 current_index = list(video_options.keys()).index(current_selection_name)
# # #             except ValueError: # If previously selected video is no longer in options
# # #                 current_index = 0
# # #                 st.session_state.selected_video_for_query = None


# # #         selected_video_name = st.selectbox(
# # #             "Select a video to query:",
# # #             options=list(video_options.keys()),
# # #             index=current_index,
# # #             key="select_single_video_dropdown"
# # #         )
# # #         st.session_state.selected_video_for_query = selected_video_name # Store the name

# # #         if st.session_state.selected_video_for_query:
# # #             st.session_state.single_video_question = st.text_input(
# # #                 f"Ask a question about '{st.session_state.selected_video_for_query}':",
# # #                 value=st.session_state.single_video_question,
# # #                 key="single_video_question_input"
# # #             )
# # #             if st.button("Get Answer", key="get_single_answer_button") and st.session_state.single_video_question:
# # #                 selected_video_id = video_options[st.session_state.selected_video_for_query]
# # #                 video_to_query = next((data for data in st.session_state.processed_videos_data if data['original_id'] == selected_video_id), None)
                
# # #                 if video_to_query:
# # #                     with st.spinner(f"Gemini is thinking about '{video_to_query['source_name']}'..."):
# # #                         answer = answer_question_about_single_video(
# # #                             st.session_state.single_video_question,
# # #                             video_to_query
# # #                         )
# # #                         st.session_state.single_video_answer = answer
# # #                         st.session_state.multi_video_result = None # Clear other result type
# # #                 else:
# # #                     st.error("Selected video data not found. This shouldn't happen.")


# # # # --- Step 3: Display Results ---
# # # st.header("Step 3: Results")

# # # # Display Multi-Video Comparison Result
# # # if st.session_state.multi_video_result:
# # #     st.subheader("Comparison Result")
# # #     result = st.session_state.multi_video_result
# # #     if result["chosen_source"]:
# # #         st.success(f"🏆 Most Relevant Video: **{result['chosen_source']}**")
# # #         st.markdown("**Gemini's Reasoning:**")
# # #         st.info(result["evaluation_response"])
# # #         chosen_video_data = next((v for v in st.session_state.processed_videos_data if v['source_name'] == result['chosen_source']), None)
# # #         if chosen_video_data:
# # #             with st.expander(f"Details for '{result['chosen_source']}'"):
# # #                 st.markdown(f"**Summary:** {chosen_video_data['summary']}")
# # #                 st.markdown(f"**Transcript Snippet:** {chosen_video_data.get('transcript', 'N/A')}")
# # #     else:
# # #         st.warning("Gemini could not definitively choose a most relevant video or none were sufficiently relevant.")
# # #         st.markdown("**Gemini's Full Response:**")
# # #         st.info(result["evaluation_response"])

# # # # Display Single Video Q&A Result
# # # if st.session_state.single_video_answer:
# # #     st.subheader(f"Answer for '{st.session_state.selected_video_for_query}'")
# # #     st.markdown(f"**Your Question:** *{st.session_state.single_video_question}*")
# # #     st.success("**Gemini's Answer:**")
# # #     st.info(st.session_state.single_video_answer)


# # # # Sidebar for Processed Video Summaries
# # # st.sidebar.subheader("Processed Video Summaries")
# # # if st.session_state.processed_videos_data:
# # #     for i, data in enumerate(st.session_state.processed_videos_data):
# # #         with st.sidebar.expander(f"{i+1}. {data['source_name']}"):
# # #             st.markdown(f"**Summary:** {data['summary']}")
# # #             # st.markdown(f"**GCS URI (Simulated):** `{data['gcs_uri']}`") # Optional
# # #             st.markdown(f"**Transcript Snippet:** {data.get('transcript', 'N/A')}")
# # # else:
# # #     st.sidebar.info("No videos processed yet.")

# # # # --- For Debugging ---
# # # # st.sidebar.subheader("Debug: Session State")
# # # # st.sidebar.json(st.session_state)

# # import streamlit as st
# # from pytube import YouTube
# # import os
# # import tempfile
# # import torch
# # from transformers import pipeline
# # from sentence_transformers import SentenceTransformer, util
# # import moviepy.editor as mp
# # import whisper

# # print(mp.__version__)
# # # Initialize models
# # @st.cache_resource
# # def load_models():
# #     transcriber = whisper.load_model("base")
# #     embedder = SentenceTransformer('all-MiniLM-L6-v2')
# #     return transcriber, embedder

# # transcriber, embedder = load_models()

# # # Transcribe audio from video
# # def transcribe_video(video_path):
# #     video = mp.VideoFileClip(video_path)
# #     audio_path = video_path + ".mp3"
# #     video.audio.write_audiofile(audio_path, verbose=False, logger=None)
# #     result = transcriber.transcribe(audio_path)
# #     return result['text']

# # # Download and save video from URL
# # def download_video(url):
# #     yt = YouTube(url)
# #     stream = yt.streams.filter(file_extension='mp4').get_highest_resolution()
# #     temp_dir = tempfile.mkdtemp()
# #     video_path = stream.download(output_path=temp_dir)
# #     return video_path

# # # UI Start
# # st.title("🎥 Video Analysis Chatbot")

# # uploaded_videos = st.file_uploader("Upload Video(s)", type=["mp4"], accept_multiple_files=True)
# # video_links_input = st.text_area("Paste video links (YouTube) - One per line")
# # question = st.text_input("Ask a question related to the video(s)")

# # video_texts = []
# # video_paths = []

# # if st.button("Analyze") and question:
# #     # Process uploaded videos
# #     if uploaded_videos:
# #         for uploaded_file in uploaded_videos:
# #             with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
# #                 tmp_file.write(uploaded_file.read())
# #                 path = tmp_file.name
# #                 st.text(f"Transcribing: {uploaded_file.name}")
# #                 transcript = transcribe_video(path)
# #                 video_texts.append((transcript, path))

# #     # Process linked videos
# #     if video_links_input:
# #         for link in video_links_input.strip().split("\n"):
# #             st.text(f"Downloading and transcribing: {link}")
# #             try:
# #                 path = download_video(link)
# #                 transcript = transcribe_video(path)
# #                 video_texts.append((transcript, path))
# #             except Exception as e:
# #                 st.error(f"Error processing {link}: {str(e)}")

# #     # Semantic similarity
# #     question_embedding = embedder.encode(question, convert_to_tensor=True)
# #     scores = []
# #     for transcript, path in video_texts:
# #         transcript_embedding = embedder.encode(transcript, convert_to_tensor=True)
# #         similarity = util.pytorch_cos_sim(question_embedding, transcript_embedding)
# #         scores.append((similarity.item(), path, transcript))

# #     scores.sort(reverse=True)

# #     if scores:
# #         best_score, best_path, best_transcript = scores[0]
# #         st.subheader("📌 Most Relevant Video")
# #         st.video(best_path)
# #         st.markdown(f"**Similarity Score:** {best_score:.2f}")
# #         st.markdown("**Transcript Summary:**")
# #         st.markdown(best_transcript[:500] + "...")
# #     else:
# #         st.warning("No relevant videos found.")



# import streamlit as st
# from pytube import YouTube
# import os
# import tempfile
# import torch
# from transformers import pipeline
# from sentence_transformers import SentenceTransformer, util
# import whisper
# from moviepy import VideoFileClip

# # Initialize models
# @st.cache_resource
# def load_models():
#     transcriber = whisper.load_model("base")
#     embedder = SentenceTransformer('all-MiniLM-L6-v2')
#     return transcriber, embedder

# transcriber, embedder = load_models()

# # Extract and transcribe audio using moviepy
# def transcribe_video(video_path):
#     audio_path = video_path + ".wav"
#     video = VideoFileClip(video_path)
#     video.audio.write_audiofile(audio_path, fps=16000, nbytes=2, bitrate="128k")
#     result = transcriber.transcribe(audio_path)
#     return result['text']

# # Download and save video from URL
# def download_video(url):
#     yt = YouTube(url)
#     stream = yt.streams.filter(file_extension='mp4').get_highest_resolution()
#     temp_dir = tempfile.mkdtemp()
#     video_path = stream.download(output_path=temp_dir)
#     return video_path

# # UI Start
# st.title("🎥 Video Analysis Chatbot")

# uploaded_videos = st.file_uploader("Upload Video(s)", type=["mp4"], accept_multiple_files=True)
# video_links_input = st.text_area("Paste video links (YouTube) - One per line")
# question = st.text_input("Ask a question related to the video(s)")

# video_texts = []
# video_paths = []

# if st.button("Analyze") and question:
#     # Process uploaded videos
#     if uploaded_videos:
#         for uploaded_file in uploaded_videos:
#             with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
#                 tmp_file.write(uploaded_file.read())
#                 path = tmp_file.name
#                 st.text(f"Transcribing: {uploaded_file.name}")
#                 transcript = transcribe_video(path)
#                 video_texts.append((transcript, path))

#     # Process linked videos
#     if video_links_input:
#         for link in video_links_input.strip().split("\n"):
#             st.text(f"Downloading and transcribing: {link}")
#             try:
#                 path = download_video(link)
#                 transcript = transcribe_video(path)
#                 video_texts.append((transcript, path))
#             except Exception as e:
#                 st.error(f"Error processing {link}: {str(e)}")

#     # Semantic similarity
#     question_embedding = embedder.encode(question, convert_to_tensor=True)
#     scores = []
#     for transcript, path in video_texts:
#         transcript_embedding = embedder.encode(transcript, convert_to_tensor=True)
#         similarity = util.pytorch_cos_sim(question_embedding, transcript_embedding)
#         scores.append((similarity.item(), path, transcript))

#     scores.sort(reverse=True)

#     if scores:
#         best_score, best_path, best_transcript = scores[0]
#         st.subheader("📌 Most Relevant Video")
#         st.video(best_path)
#         st.markdown(f"**Similarity Score:** {best_score:.2f}")
#         st.markdown("**Transcript Summary:**")
#         st.markdown(best_transcript[:500] + "...")
#     else:
#         st.warning("No relevant videos found.")
