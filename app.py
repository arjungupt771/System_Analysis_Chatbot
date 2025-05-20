import os
import uuid
import sys
import ctypes
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
import json
import shutil
import platform
from Software_Catalog import SOFTWARE_CATALOG, get_software_info
from chat_db import init_db, save_message, load_chat_history, get_all_chat_ids
from windows_tools.installed_software import get_installed_software
from streamlit.components.v1 import html

try:
    import psutil
except ImportError:
    psutil = None
    print("Warning: psutil library not found. Some system hardware details (RAM, CPU) will be unavailable.")
    print("Install it with: pip install psutil")

st.set_page_config(page_title="ChatMate AI", page_icon="static/robot.png")

api_key='AIzaSyC3N6bbu0b-Gd3c1DIQCeJLwawSwjcH50c'
genai.configure(api_key=api_key)

generation_config = {
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 100,
    "max_output_tokens": 32768,
}

url =f'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=api_key'


model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text

def clear_uploads_directory(upload_dir="uploads/"):
    for filename in os.listdir(upload_dir):
        file_path = os.path.join(upload_dir, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            st.error(f"Error removing {file_path}: {str(e)}")

def install_exe(exe_file):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.exe') as tmp_exe_file:
            tmp_exe_file.write(exe_file.getbuffer())
            tmp_exe_path = tmp_exe_file.name

        st.write(f"Starting the Installation: {tmp_exe_path}")
        subprocess.run([tmp_exe_path], check=True)

        os.remove(tmp_exe_path)
        st.success(f"Installation completed successfully.")

    except Exception as e:
        st.error(f"An error occurred while installing the software: {e}")
        st.error(f"Please try again.")

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
    
    
# def audio_callback(recognizer, audio):
#     try:
#         text = recognizer.recognize_google(audio)
#         st.session_state.spoken_text_from_mic = text
#         st.success(f"Voice captured: \"{text}\"") # Give feedback
#         # Stop listening after successful recognition
#         if st.session_state.stop_listening_func:
#             st.session_state.stop_listening_func(wait_for_stop=False)
#             st.session_state.is_listening = False
#             st.experimental_rerun() # Rerun to update button label and process text
#     except sr.UnknownValueError:
#         st.session_state.spoken_text_from_mic = "" # Clear if not understood
#         st.warning("Could not understand audio. Please try again.")
#         # Optionally, stop listening on UnknownValueError or let it continue
#         if st.session_state.stop_listening_func:
#              st.session_state.stop_listening_func(wait_for_stop=False)
#              st.session_state.is_listening = False
#              st.experimental_rerun()
#     except sr.RequestError as e:
#         st.session_state.spoken_text_from_mic = ""
#         st.error(f"API error from Google Speech Recognition: {e}")
#         if st.session_state.stop_listening_func:
#             st.session_state.stop_listening_func(wait_for_stop=False)
#             st.session_state.is_listening = False
#             st.experimental_rerun()
#     except Exception as e:
#         st.session_state.spoken_text_from_mic = ""
#         st.error(f"An unexpected error occurred during speech recognition: {e}")
#         if st.session_state.stop_listening_func:
#             st.session_state.stop_listening_func(wait_for_stop=False)
#             st.session_state.is_listening = False
#             st.experimental_rerun()
    

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
    # if st.session_state.is_listening: # Should not happen if button logic is correct
    #     return

    # recognizer = sr.Recognizer()
    # microphone = sr.Microphone()

    # try:
    #     with microphone as source:
    #         recognizer.adjust_for_ambient_noise(source, duration=0.5) # shorter duration

    #     # Start listening in the background
    #     # The audio_callback function will be called when speech is detected
    #     stop_func = recognizer.listen_in_background(microphone, audio_callback, phrase_time_limit=10)
    #     st.session_state.stop_listening_func = stop_func
    #     st.session_state.is_listening = True
    #     st.info("🎤 Listening... Press the button again to stop manually if needed.")
    #     # We don't return text here; it's set in session_state by the callback
    # except Exception as e:
    #     st.error(f"Error starting microphone: {e}")
    #     st.session_state.is_listening = False # Ensure state is correct on error

# def stop_listening_manually():
#     """Stops the background listener if it's active."""
#     if st.session_state.is_listening and st.session_state.stop_listening_func:
#         st.session_state.stop_listening_func(wait_for_stop=False) # Don't block here
#         st.session_state.is_listening = False
#         st.session_state.stop_listening_func = None # Clear the stop function
#         st.session_state.spoken_text_from_mic = "" # Clear any partial result
#         st.info("🎤 Listening stopped.")
#     elif not st.session_state.is_listening:
#         st.info("🎤 Not currently listening.")
    

def parse_software_name(command):
    match = re.search(r'install (.+)', command, re.IGNORECASE)
    if match:
        return match.group(1).strip().lower()
    return None

def is_software_installed(path_check):
    return  os.path.exists(path_check) 

def download_and_install_software(software_key):
    
    info = get_software_info(software_key)
    if not info:
        st.error("❌ The Software is not available in the catalohg.")
        return

    # Properly get software name (fallback to software_key if missing)
    software_name = info.get("name", software_key).title()
    exe_name = info.get("exe_name", software_key)  # You can define this in your catalog if needed

    # ✅ Check if software is already installed
    install_path = info.get("install_path")
    if install_path and is_software_installed(install_path):
        st.success(f"{software_name} is already available on this system.")
        return


    url = info["url"]
    installer = info["installer"]
    silent_flag = info.get("silent_flag", "")

    st.info(f"⬇️ Downloading {software_name}...")
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(installer, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        st.success("📥 Download complete.")
    except Exception as e:
        st.error(f"❌ Download failed: {e}")
        return

    st.info("⚙️ Installing... (this may take a moment)")
    try:
        subprocess.run([installer, silent_flag], check=True)
        st.success(f"✅ {software_name} installed successfully!")
    except Exception as e:
        st.error(f"❌ Installation failed: {e}")
    finally:
        if os.path.exists(installer):
            os.remove(installer)
            st.info("🧹 Installer removed after installation.")

def create_new_chat():
    chat_id = str(uuid.uuid4())
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.all_chats[chat_id]={
        "id": chat_id,
        "title": f"Chat - {timestamp}",
        "messages": [],
        "pdf_texts_associated":[],
        "created_at": timestamp
    }
    st.session_state.current_chat_id = chat_id
    st.session_state.gemini_chat_sessions[chat_id] = model.start_chat(history=[])
    st.rerun()
    
def select_chat(chat_id):
    st.session_state.current_chat_id = chat_id
    if chat_id not in st.session_state.gemini_chat_sessions:
        history_for_session = [
            {"role": msg["role"], "parts": msg["parts"]}
            for msg in st.session_state.all_chats[chat_id]["messages"]
        ]
        st.session_state.gemini_chat_sessions[chat_id] = model.start_chat(history = history_for_session)
    st.rerun()
    
def get_current_chat_data():
    if st.session_state.current_chat_id and st.session_state.current_chat_id in st.session_state.all_chats:
        return st.session_state.all_chats[st.session_state.current_chat_id]
    return None

def get_current_gemini_session():
    if st.session_state.current_chat_id and st.session_state.current_chat_id in st.session_state.gemini_chat_sessions:
        return st.session_state.gemini_chat_sessions[st.session_state.current_chat_id]
    return None

def add_message_to_current_chat(role, content):
    current_chat = get_current_chat_data()
    if current_chat:
        current_chat["messages"].append({"role":role, "parts": [content]})
        save_message(current_chat["id"], role, content)
        if role == "user" and len(current_chat["messages"]) == 1 and current_chat["title"].startswith("Chat - "):
            current_chat["title"] = content[:30] + "..."

def get_appx_packages():
    """Get System apps using powerShell"""
    result = subprocess.run([
        "powershell", "-Command","Get-AppxPackage -AllUsers | Select Name, InstallLocation | ConvertTo-Json"
    ], capture_output=True, text=True)
    try:
        return json.loads(result.stdout)
    except Exception:
        return []
    
# def get_win32_apps():
#     result = subprocess.run([
#         "powershell","-Command",
#         "Get-WmiObject -Class Win32_Product | Select Name, InstallLocation | ConvertTo-Json"
#     ], capture_output=True, text=True)
#     try:
#         return json.loads(result.stdout)
#     except Exception:
#         return[]

def get_win32_apps():
    powershell_script = r"""
    $keys = @(
        "HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*",
        "HKLM:\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*",
        "HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*"
    )

    $apps = foreach ($key in $keys) {
        Get-ItemProperty $key -ErrorAction SilentlyContinue | 
        Where-Object { $_.DisplayName } | 
        Select-Object DisplayName, InstallLocation
    }
    $uniqueApps = $apps | Sort-Object DisplayName -Unique 
    $uniqueApps | ConvertTo-Json

   # $apps | ConvertTo-Json
    """

    result = subprocess.run(
        ["powershell", "-Command", powershell_script],
        capture_output=True,
        text=True
    )
    if result.returncode !=0:
        print(f"PowerShell script for get_win32_apps returned an error. Stderr: {result.stderr}")
        return[]
    
    app_list=[]
    try:
        if result.stdout and result.stdout.strip():
            parsed_output = json.loads(result.stdout)
            if parsed_output is None:
                app_list=[]
            elif isinstance(parsed_output,dict):
                app_list=[parsed_output]
            elif isinstance(parsed_output,list):
                app_list=parsed_output
            else:
                print(f"Warning: Unexpected data type from PowerShell JSON in get_win32_apps: {type(parsed_output)}. Output: {result.stdout[:200]}")
        # data= json.loads(result.stdout)
        # if isinstance(data,dict):
        #     data=[data]
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON from get_win32_apps: {e}. PowerShell stdout: '{result.stdout[:200]}...'")
    except Exception as e:
        print(f"An unexpected error occurred in get_win32_apps: {e}" )
    return app_list

    
    
def get_folder_size(path):
    """Recursively calculate folder size in bytes"""
    total_size =0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            try:
                if os.path.isfile(fp):
                    total_size += os.path.getsize(fp)
            except Exception:
                pass
    return total_size

# def get_apps_with_updates():
#     try:
#         result = subprocess.run(["choco", "outdated"], capture_output=True, text=True, check=True)
#         output = result.stdout
#         lines = output.strip().splitlines()
#         app_names = []
#         for line in lines:
#             if not line.lower().startswith("package") and line.strip():
#                 parts = line.split()
#                 if parts:
#                     app_names.append(parts[0].strip().lower())

#         return set(app_names)
#     except Exception as e:
#         st.error(f"Error checking updates: {e}")
#         return set()
        
        
        

def get_last_updated_date(path):
    """Get the last modified timestamp of the install folder"""
    try:
        timestamp = os.path.getmtime(path)
        return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")
    except Exception:
        return "Unknown"


def scan_apps_and_storage():
    """Scanning and classifying apps with their storage details"""
    system_apps = get_appx_packages()
    downloaded_apps = get_win32_apps()
    #updatable_apps = get_apps_with_updates()
    
    system_apps = system_apps if system_apps is not None else []
    downloaded_apps = downloaded_apps if downloaded_apps is not None else []
    
    system_total = 0
    downloaded_total =0
    system_list =[]
    downloaded_list =[]
    
    # system app
    for app in system_apps:
        path = app.get("InstallLocation")
        name = app.get("Name")
        if path and os.path.exists(path):
            size = get_folder_size(path)
            last_updated = get_last_updated_date(path)
            system_total += size
            system_list.append({"App": name, "Size(MB)": f"{size/1e6: .2f}", "Last Updated":last_updated})
            
    # downloaded apps
    for app in downloaded_apps:
        path = app.get("InstallLocation")
        name = app.get("DisplayName")
        if name and path and os.path.exists(path):
            size = get_folder_size(path)
            downloaded_total +=size
            last_updated=get_last_updated_date(path)
            #update_status = "✅" if name and name.lower() in updatable_apps else "❌"
            downloaded_list.append({"App": name, "Size(MB)": f"{size/1e6: .2f}","Last Updated":last_updated})
        else:
            downloaded_list.append({"App":name, "Size(MB)":"N/A","Last Updated":"N/A"})
            
    return system_list, downloaded_list, system_total, downloaded_total
    
# def restart_as_admin():
#     if ctypes.windll.shell32.IsUserAnAdmin():
#         st.success("✅ Already running as Administrator.")
#         return
    
#     script_path = os.path.abspath(sys.argv[0])
#     try:
#         ctypes.windll.shell32.ShellExecuteW(
#             None, "runas", sys.executable, f'"{script_path}"', None, 1
#         )
#         st.info("Attempting to restart with admin privileges...")
#     except Exception as e:
#         st.error(f"Failed to relaunch as admin: {e}")

# ... (your existing imports like subprocess, streamlit as st, os are already there) ...

# ... (your existing functions like extract_text_from_pdf, speak, etc.) ...
# ... (your existing function get_last_updated_date) ...

# def install_with_chocolatey(package_name):
#     try:
#         st.info(f"Installing {package_name} via Chocolatey...")

#         result = subprocess.run(["choco", "install", package_name, "-y", "--force"], capture_output=True, text=True, shell=False) # Added --force for potential reinstall/fixing
#         if result.returncode == 0:
#             st.success(f"{package_name} installed successfully!")
#             st.code(result.stdout) # Show output
#         else:
#             st.error(f"Installation failed for {package_name}:")
#             st.subheader("Choco stdout:")
#             st.code(result.stdout)
#             st.subheader("Choco stderr:")
#             st.code(result.stderr)
#     except FileNotFoundError:
#         st.error("Chocolatey command 'choco' not found. Please ensure Chocolatey is installed and in your system's PATH.")
#         st.info("You might need to add 'C:\\ProgramData\\chocolatey\\bin' to your PATH environment variable, or restart your terminal/IDE after installation.")
#     except Exception as e:
#         st.error(f"An error occurred during Chocolatey installation: {e}")

# def upgrade_with_chocolatey(package_name):
#     try:
#         st.info(f"Checking for updates and upgrading {package_name} via Chocolatey...")
#         # Ensure choco is in PATH (optional)
#         # if r"C:\ProgramData\chocolatey\bin" not in os.environ["PATH"]:
#         #    os.environ["PATH"] += r";C:\ProgramData\chocolatey\bin"

#         result = subprocess.run(["choco", "upgrade", package_name, "-y", "--force"], capture_output=True, text=True, shell=False) # Added --force
#         if result.returncode == 0:
#             if "0 packages upgraded" in result.stdout or "is the latest version available" in result.stdout:
#                 st.success(f"{package_name} is already up to date.")
#             else:
#                 st.success(f"{package_name} updated successfully!")
#             st.code(result.stdout) # Show output
#         else:
#             # Handle cases where the package might not be installed yet for an upgrade attempt
#             if "This package is not installed" in result.stderr or "This package is not installed" in result.stdout:
#                  st.warning(f"{package_name} is not installed. Try installing it first.")
#             else:
#                 st.error(f"Update failed for {package_name}:")
#             st.subheader("Choco stdout:")
#             st.code(result.stdout)
#             st.subheader("Choco stderr:")
#             st.code(result.stderr)
#     except FileNotFoundError:
#         st.error("Chocolatey command 'choco' not found. Please ensure Chocolatey is installed and in your system's PATH.")
#         st.info("You might need to add 'C:\\ProgramData\\chocolatey\\bin' to your PATH environment variable, or restart your terminal/IDE after installation.")
#     except Exception as e:
#         st.error(f"An error occurred during Chocolatey upgrade: {e}")

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# END OF CHOCOLATEY FUNCTIONS
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# ... (your functions like scan_apps_and_storage, restart_as_admin, etc.) ...

def get_hardware_details():
    details={}
    
    details['os_version'] = f"{platform.system()}{platform.release()}(Version:{platform.version()})"
    details['os_architecture'] = platform.machine()  
    try:
        usage_c = shutil.disk_usage("C:\\")
        details['disk_c_total_gb'] = usage_c.total/(1024**3)
        details['disk_c_used_gb']=usage_c.used/(1024**3)
        details['disk_c_free_gb'] = usage_c.free(1024**3)
    except Exception as e:
        print(f"Could not get disk usage for C:: {e}")
        details['disk_c_total_gb'] = 'N/A'
        details['disk_c_used_gb'] = 'N/A'
        details['disk_c_free_gb'] = 'N/A'
    all_disks_info=[]
    total_system_storage_bytes=0
    processed_devices=set()
    if psutil: # psutil provides a more convenient way to list partitions
        try:
            partitions = psutil.disk_partitions(all=False)
            for p in partitions:
                if 'cdrom' in p.opts or p.fstype=='' or 'loop' in p.device.lower() or not p.mountpoint or not os.path.exists(p.mountpoint): 
                    # Check if mountpoint is accessible
                    continue
                try:
                    usage = shutil.disk_usage(p.mountpoint)
                    current_disk_total_gb: usage.total / (1024**3)
                    current_disk_used_gb: usage.used / (1024**3)
                    current_disk_free_gb: usage.free / (1024**3)
                    all_disks_info.append({
                        "mountpoint": p.mountpoint,
                        "device":p.device,
                        "fstype": p.fstype,
                        "total_gb":current_disk_total_gb,
                        "used_gb":current_disk_used_gb,
                        "free_gb":current_disk_free_gb,
                    })
                    if p.device not in processed_devices:
                        total_system_storage_bytes +=usage.total
                        processed_devices.add(p.device)
                    
                    if p.mountpoint.upper() == 'C:\\':
                        details['disk_c_total_gb'] = current_disk_total_gb
                        details['disk_c_used_gb'] = current_disk_used_gb
                        details['disk_c_free_gb'] = current_disk_free_gb
                        
                    
                except OSError as e: # Skip drives that cause errors (e.g. optical drives with no media)
                        pass
                except Exception as e_inner:
                    pass
        except Exception as e:
            print(f"Could not get all disk partitions info: {e}")
    elif 'disk_c_total_gb' in details and details['disk_c_total_gb'] is not None:
        try:
            usage_c_for_total = shutil.disk_usage("C:\\")
        except:
            pass
    details['all_disks'] = all_disks_info
    details['total_system_storage_gb'] = total_system_storage_bytes/(1024**3) if total_system_storage_bytes>0 else None
    
    if 'disk_c_total_gb' not in details or details['disk_c_total_gb'] is None:
        c_drive_info_from_all_disks = next((d for d in all_disks_info if  d['mountpoint'].upper() == 'C:\\'),None)
        if c_drive_info_from_all_disks:
            details['disk_c_total_gb'] = c_drive_info_from_all_disks('total_gb')
            details['disk_c_used_gb'] = c_drive_info_from_all_disks('used_gb')
            details['disk_c_free_gb'] = c_drive_info_from_all_disks('free_gb')
        else:
            if 'disk_c_total_gb' not in details:
                details['disk_c_total_gb'] = None
            if 'disk_c_used_gb' not in details: details['disk_c_used_gb'] = None
            if 'disk_c_free_gb' not in details: details['disk_c_free_gb'] = None


    # RAM Information (using psutil)
    if psutil:
        try:
            svmem = psutil.virtual_memory()
            details['ram_total_gb'] = svmem.total / (1024**3)
            details['ram_available_gb'] = svmem.available / (1024**3)
            details['ram_used_gb'] = svmem.used / (1024**3)
            details['ram_percent_used'] = svmem.percent
        except Exception as e:
            print(f"Could not get RAM info using psutil: {e}")
            details['ram_total_gb'] = 'N/A'
            details['ram_available_gb'] = 'N/A'
    else:
        details['ram_total_gb'] = 'N/A (psutil not found)'
        details['ram_available_gb'] = 'N/A (psutil not found)'

    # CPU Information (using psutil for more detail)
    details['cpu_model'] = platform.processor() # Basic CPU info
    if psutil:
        try:
            details['cpu_physical_cores'] = psutil.cpu_count(logical=False)
            details['cpu_logical_cores'] = psutil.cpu_count(logical=True)
            details['cpu_current_freq_mhz'] = psutil.cpu_freq().current if psutil.cpu_freq() else 'N/A'
            details['cpu_max_freq_mhz'] = psutil.cpu_freq().max if psutil.cpu_freq() else 'N/A'
            details['cpu_usage_percent'] = psutil.cpu_percent(interval=0.1) # Small interval for quick check
        except Exception as e:
            print(f"Could not get detailed CPU info using psutil: {e}")
            # Keep basic platform.processor() if detailed fails

    return details

def main():
    init_db()  # Ensure the database is set up
    clear_uploads_directory()
    if "all_chats" not in st.session_state:
        st.session_state.all_chats = {}

    if "current_chat_id" not in st.session_state:
        st.session_state.current_chat_id = None
        
    if "gemini_chat_sessions" not in st.session_state:
        st.session_state.gemini_chat_sessions={}
        
    # if "is_listening" not in st.session_state:
    #     st.session_state.is_listening = False
    
    if "spoken_text_from_mic" not in st.session_state:
        st.session_state.spoken_text_from_mic=""
    
    # if "mic_recognizer" not in st.session_state: # To hold the recognizer and mic instances
    #     st.session_state.mic_recognizer = None
        
    # if "mic_source" not in st.session_state:
    #     st.session_state.mic_source = None
        
    # if "stop_listening_func" not in st.session_state: # For background listening stop
    #     st.session_state.stop_listening_func = None
    

    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now()
    current_time = now.strftime("%A, %B %d, %Y at %I:%M %p")

    today = datetime.today().strftime("%A, %B %d, %Y")

    st.title("Welcome to Sophos AI...")
    st.markdown(f"**Current Date & Time (IST):** {current_time}")
    st.markdown("Ask, upload, and discover—AI at your service.")
    st.markdown("~ Arjun Gupta", unsafe_allow_html=True)
    


            
    
    clear_uploads_directory()
    global_pdf_text=""
    


        
    st.sidebar.title("ChatMate AI")
    if st.sidebar.button("➕ New Chat", use_container_width=True):
        create_new_chat()
        
    #st.sidebar.button(scan_apps_and_storage)
    st.sidebar.subheader("Chat History")
    
    chat_options = {
        st.session_state.all_chats[cid]["title"]: cid
        for cid in sorted(
            st.session_state.all_chats.keys(),
            key = lambda cid: st.session_state.all_chats[cid]["created_at"],
            reverse=True
        )
    }
    selected_titles = st.sidebar.multiselect("Select chat(s) to delete or open:", list(chat_options.keys()))
    
    if selected_titles:
        if len(selected_titles) == 1:
            if st.sidebar.button("Open Chat"):
                select_chat(chat_options[selected_titles[0]])
                
        if st.sidebar.button("Delete Selected Chat(s)"):
            for title in selected_titles:
                chat_id = chat_options[title]
                delete_chat(chat_id)
                if chat_id in st.session_state.all_chats:
                    del st.session_state.all_chats[chat_id]
            st.sidebar.success(f"Deleted {len(selected_titles)} chat(s).")
            st.rerun()
    # selected_chats=[]
    
    # with st.sidebar.form("delete_chats_forms"):
    #     sorted_chat_ids = sorted(st.session_state.all_chats.keys(), key=lambda cid: st.session_state.all_chats[cid]["created_at"], reverse=True) 
        
    #     for chat_id in sorted_chat_ids:
    #         chat_title = st.session_state.all_chats[chat_id]["title"]
    #         selected = st.checkbox(chat_title, key=f"check_{chat_id}")
    #         if selected:
    #            selected_chats.append(chat_id)

    #     delete_btn = st.form_submit_button("🗑️ Delete Selected Chats")
        
    # if delete_btn and selected_chats:
    #     for chat_id in selected_chats:
    #         st.session_state.all_chats.pop(chat_id,None)
    #         st.session_state.gemini_chat_sessions.pop(chat_id,None)
            
    #         from chat_db import delete_chat
    #         delete_chat(chat_id)
    #     st.success(f"Deleted{len(selected_chats)}chat(s).")
    #     st.rerun()
            
    for chat_id in get_all_chat_ids():
        if chat_id not in st.session_state.all_chats:
           messages = load_chat_history(chat_id)
           st.session_state.all_chats[chat_id] = {
            "id": chat_id,
            "title": messages[0]["parts"][0][:30] + "..." if messages else f"Chat {chat_id}",
            "messages": messages,
            "pdf_texts_associated": [],
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # you could also store this in DB later
        }

    # if st.button("Run as Administrator"):
    #     restart_as_admin()
        
    # st.sidebar.subheader("Delete Chats")
    # all_chat_ids = list(st.session_state.all_chats.keys())
    # if all_chat_ids:
    #     chats_to_delete = st.sidebar.multiselect("Select chats to delete", options=all_chat_ids)
    #     if st.sidebar.button("Delete Selected"):
    #         for cid in chats_to_delete:
    #             delete_chat(cid)
    #             if cid in st.session_state.all_chats:
    #                 del st.session_state.all_chats[cid]
    #         st.success("Selected chats deleted.")
    #         st.rerun()
    # else:
    #     st.sidebar.write("No chats to delete.")


    st.sidebar.header("Upload PDF Documents")
    pdf_files = st.sidebar.file_uploader("Upload PDFs (Max 10MB each)", type=["pdf"], accept_multiple_files=True, key =f"pdf_uploader_{st.session_state.current_chat_id or 'global'}")
    if pdf_files:
       st.write(f"Uploaded PDF: {pdf_files[0].name}")

    st.sidebar.header("Upload Software .exe file")
    exe_file = st.sidebar.file_uploader("Upload .exe File", type=["exe"],key=f"exe_uploader_{st.session_state.current_chat_id or 'global'}")

    pdf_text = ""
    current_chat_data = get_current_chat_data()

    if pdf_files and current_chat_data:
        newly_extracted_texts = []
       # pdf_texts = []
        for pdf_file in pdf_files:
            if pdf_file.size > 10 * 1024 * 1024:
                st.sidebar.error(f"File {pdf_file.name} exceeds 10MB limit. Skipping.")
                continue
            
            if not any(pdf_info["name"] == pdf_file.name for pdf_info in current_chat_data.get("pdf_texts_associated", [])):
                with st.spinner(f"Processing{pdf_file.name} for current chat..."):
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf", dir="uploads") as tmp_pdf:
                        tmp_pdf.write(pdf_file.getbuffer())
                        tmp_pdf_path = tmp_pdf.name
                    extracted_text = extract_text_from_pdf(tmp_pdf_path)
                   # st.write(f"Extracted Text: {extracted_text[:500]}...")
                    newly_extracted_texts.append(extracted_text)
                    current_chat_data["pdf_texts_associated"].append({"name": pdf_file.name,"full_text":extracted_text, "text_summary": extracted_text[:200]}) # Store some info
                    os.remove(tmp_pdf_path) 
            
        if newly_extracted_texts:
            st.sidebar.success(f"Added{len(newly_extracted_texts)} PDF(s) to current chat!")
            st.write(f"Extracted PDF text: {newly_extracted_texts[:500]}")
        
        if current_chat_data:
            all_pdf_texts_for_this_chat = []
            for pdf_info in current_chat_data.get("pdf_texts_associated", []):
                pass

    if exe_file is not None:
        st.sidebar.write(f"Uploaded .exe: {exe_file.name}")
        if st.sidebar.button("Install Software"):
            install_exe(exe_file)

    
    if not st.session_state.current_chat_id:
        st.info("Select a chat from the sidebar or creates a new one to begin.")
        return
    
    current_chat_display = get_current_chat_data()
    if current_chat_display:
        st.subheader(f"Conversation:{current_chat_display['title']}")
        for message in current_chat_display["messages"]:
            with st.chat_message(message["role"]):
                st.markdown(message["parts"][0])
                
    # get the current session for the gemini test
    current_gemini_session = get_current_gemini_session()
    
    col1, col2 = st.columns([1,1])
    with col1:
        speak_clicked = st.button("🎤 Speak", key="speak_btn")
        # speak_clicked = "🛑 Stop Listening" if st.session_state.get('is_listening', False) else "🎤 Speak"
        # if st.button(speak_button_label, key="speak_toggle_button_main"): # New key
        #     if not st.session_state.get('is_listening', False):
        #         st.session_state.spoken_text_from_mic = "" # Clear before starting
        #listen_from_mic() # <<< THIS CALL
        #         st.rerun()
        #     else:
        #         stop_listening_manually()
        #         st.rerun()
    with col2:
        scan_apps_clicked = st.button("🖥️ Scan Apps", key="scan_apps_btn")
    
    
    spoken_text=None


    if speak_clicked:
        spoken_text = listen_from_mic()
        print(spoken_text,"this is spoken text")
        if spoken_text and spoken_text.strip():
            response=current_gemini_session.send_message(spoken_text)
            st.chat_message("user").markdown(spoken_text)
            add_message_to_current_chat("user", spoken_text)
            speak(response.text)
        else:
            st.warning("didn't capture any speech")
        if st.session_state.spoken_text_from_mic and current_gemini_session:
            spoken_text = st.session_state.spoken_text_from_mic
            st.session_state.spoken_text_from_mic=""
            st.chat_message("user").markdown(spoken_text)
            add_message_to_current_chat("user",spoken_text)
        
        # === Voice Command Mapping ===
        if spoken_text and "scan apps" in spoken_text.lower():
            with st.spinner("Scanning installed apps and calculating storage..."):
                system_list, downloaded_list, system_total, downloaded_total = scan_apps_and_storage()

            st.subheader("Summary")
            st.markdown(f"**System Apps:** {len(system_list)} apps, **{system_total/1e9:.2f} GB**")
            st.markdown(f"**Downloaded Apps:** {len(downloaded_list)} apps, **{downloaded_total/1e9:.2f} GB**")

            with st.expander("System Apps Details"):
               st.table(system_list)
            with st.expander("Downloaded Apps Details"):
               st.table(downloaded_list)

            add_message_to_current_chat("assistant", f"Scanned apps:\nSystem: {len(system_list)} ({system_total/1e9:.2f} GB), "
                                                 f"Downloaded: {len(downloaded_list)} ({downloaded_total/1e9:.2f} GB)")
            st.rerun()
            return
        
        elif spoken_text and "install" in spoken_text.lower():
           software_name = parse_software_name(spoken_text)
           if software_name and software_name in SOFTWARE_CATALOG:
               download_and_install_software(software_name)
               return
           else: 
              st.warning("Software not recognized in the catalog.")
        else:
            if current_gemini_session:
               with st.spinner("Getting Gemini response..."):
                response = current_gemini_session.send_message(spoken_text)
                st.chat_message("assistant").markdown(response.text)
                add_message_to_current_chat("assistant", response.text)
                speak(response.text)
                add_message_to_current_chat("content",response.text)

        
        pdf_context_for_prompt = ""
        global_pdf_text=""
        if current_chat_data and "pdf_texts_associated" in current_chat_data:
            temp_texts = []
            for pdf_item in current_chat_data["pdf_texts_associated"]:
                temp_texts.append(pdf_item.get("text_summary",""))
            
            global_pdf_text = "\n\n".join(temp_texts) 
        

        context = f"Based on the documents:\n{global_pdf_text}\n\nUser Question: {spoken_text}" if global_pdf_text else spoken_text
        # if current_gemini_session:
        #     try:
        #         with st.spinner("ChatMate AI is thinking..."):
        #             response = current_gemini_session.send_message(context)
        #         with st.chat_message("assistant"):
        #             add_message_to_current_chat(response.text)
        #         add_message_to_current_chat("assistant",response.text)
                
        #     except Exception as e:
        #         st.error(f"❌ Error processing your request with Gemini: {e}")
        #     st.experimental_rerun()
        # else:
        #     st.warning("No active Gemini session to send the message to.")
                
                
        try:
             response = current_gemini_session.send_message(context)
             st.chat_message("assistant").markdown(response.text)
             add_message_to_current_chat("assistant", response.text)
             speak(response.text)

        except Exception as e:
             st.error(f"❌ Error processing your request: {e}")
             st.rerun()

    
    if scan_apps_clicked:
        with st.spinner("Scanning installed apps and claculating storage..."):
             system_list, downloaded_list, system_total, downloaded_total = scan_apps_and_storage()
             hardware_details = get_hardware_details()
        st.header("📊 System & Software Scan Results") # Overall header

        # Display System Hardware & OS Information First
        st.subheader("💻 System Hardware & OS Information")
        col_hw1, col_hw2 = st.columns(2)

        with col_hw1:
            st.metric(label="Operating System", value=hardware_details.get('os_version', 'N/A'))
            st.metric(label="OS Architecture", value=hardware_details.get('os_architecture', 'N/A'))
            st.metric(label="CPU Model", value=hardware_details.get('cpu_model', 'N/A'))
            total_storage = hardware_details.get('total_system_storage_gb')
            st.metric(
                label ="Total System Storage(ROM)",
                value=f"{total_storage:.2f} GB" if isinstance(total_storage, (int, float)) else "N/A"
            )
            if psutil: # Check if psutil is available
                cpu_physical_cores = hardware_details.get('cpu_physical_cores')
                cpu_logical_cores = hardware_details.get('cpu_logical_cores')
                cpu_usage_percent = hardware_details.get('cpu_usage_percent')
                st.metric(
                    label = "CPU Physical Cores",
                    value=str(cpu_physical_cores) if cpu_physical_cores is not None else "N/A"
                )
                st.metric(
                    label="CPU Logical Cores",
                    value=str(cpu_logical_cores) if cpu_logical_cores is not None else "N/A"
                )
                st.metric(
                    label="CPU Current Usage",
                    # Format as float if it's a number, otherwise display "N/A"
                    value=(f"{cpu_usage_percent:.1f} %" if isinstance(cpu_usage_percent, (int, float)) else "N/A")
                )
                # st.metric(label="CPU Physical Cores", value=str(hardware_details.get('cpu_physical_cores', 'N/A')))
                # st.metric(label="CPU Logical Cores", value=str(hardware_details.get('cpu_logical_cores', 'N/A')))
                # st.metric(label="CPU Current Usage", value=f"{hardware_details.get('cpu_usage_percent', 'N/A')} %")
            else:
                st.caption("Detailed CPU info requires 'psutil'.")


        # with col_hw2:
        #     if psutil: # Check if psutil is available
        #         st.metric(label="Total RAM", value=f"{hardware_details.get('ram_total_gb', 0):.2f} GB")
        #         st.metric(label="Available RAM", value=f"{hardware_details.get('ram_available_gb', 0):.2f} GB")
        #         st.metric(label="Used RAM", value=f"{hardware_details.get('ram_used_gb', 0):.2f} GB ({hardware_details.get('ram_percent_used', 0):.1f}%)")
        #     else:
        #         st.info("RAM details require the 'psutil' library.")

        #     st.metric(label="C: Drive Total Space", value=f"{hardware_details.get('disk_c_total_gb', 0):.2f} GB")
        #     st.metric(label="C: Drive Used Space", value=f"{hardware_details.get('disk_c_used_gb', 0):.2f} GB")
        #     st.metric(label="C: Drive Free Space", value=f"{hardware_details.get('disk_c_free_gb', 0):.2f} GB")
        with col_hw2:
        
    # RAM Metrics - with proper handling for 'N/A' or None
            if psutil:  # Check if psutil is available
              ram_total = hardware_details.get('ram_total_gb') # Get value, could be number, None, or 'N/A'
              ram_available = hardware_details.get('ram_available_gb')
              ram_used = hardware_details.get('ram_used_gb')
              ram_percent = hardware_details.get('ram_percent_used')

              if isinstance(ram_total, (int, float)):
                st.metric(label="Total RAM", value=f"{ram_total:.2f} GB")
              else:
                 st.metric(label="Total RAM", value=str(ram_total if ram_total is not None else "N/A"))

              if isinstance(ram_available, (int, float)):
                 st.metric(label="Available RAM", value=f"{ram_available:.2f} GB")
              else:
                st.metric(label="Available RAM", value=str(ram_available if ram_available is not None else "N/A"))

              if isinstance(ram_used, (int, float)) and isinstance(ram_percent, (int, float)):
                st.metric(label="Used RAM", value=f"{ram_used:.2f} GB ({ram_percent:.1f}%)")
              elif isinstance(ram_used, (int, float)): # Only ram_used is a number
                st.metric(label="Used RAM", value=f"{ram_used:.2f} GB")
              else: # ram_used is not a number
                st.metric(label="Used RAM", value=str(ram_used if ram_used is not None else "N/A"))
              if not isinstance(ram_percent, (int, float)): # If ram_percent is also not a number
                 st.caption(f"Usage %: {str(ram_percent if ram_percent is not None else 'N/A')}")


            else: # psutil is not available
             st.info("RAM details require the 'psutil' library.")
             st.metric(label="Total RAM", value="N/A")
             st.metric(label="Available RAM", value="N/A")
             st.metric(label="Used RAM", value="N/A")


    # Disk C: Metrics - with proper handling for 'N/A' or None
            disk_c_total = hardware_details.get('disk_c_total_gb')
            disk_c_used = hardware_details.get('disk_c_used_gb')
            disk_c_free = hardware_details.get('disk_c_free_gb')

            if isinstance(disk_c_total, (int, float)):
                st.metric(label="C: Drive Total Space", value=f"{disk_c_total:.2f} GB")
            else:
               st.metric(label="C: Drive Total Space", value=str(disk_c_total if disk_c_total is not None else "N/A"))

            if isinstance(disk_c_used, (int, float)):
               st.metric(label="C: Drive Used Space", value=f"{disk_c_used:.2f} GB")
            else:
               st.metric(label="C: Drive Used Space", value=str(disk_c_used if disk_c_used is not None else "N/A"))

            if isinstance(disk_c_free, (int, float)):
               st.metric(label="C: Drive Free Space", value=f"{disk_c_free:.2f} GB")
            else:
               st.metric(label="C: Drive Free Space", value=str(disk_c_free if disk_c_free is not None else "N/A"))

# ... (rest of your hardware display, like the 'All Disks' table, which also needs similar checks) ...

        if hardware_details.get('all_disks'):
            st.markdown("##### All Disk Partitions")
            disk_data_for_table = []
            for disk_item in hardware_details['all_disks']: # Renamed loop variable
                disk_data_for_table.append({
                    "Mount Point": disk_item['mountpoint'],
                    "File System": disk_item['fstype'],
                    "Total GB": f"{disk_item['total_gb']:.2f}",
                    "Used GB": f"{disk_item['used_gb']:.2f}",
                    "Free GB": f"{disk_item['free_gb']:.2f}",
                })
            if disk_data_for_table:
                st.table(disk_data_for_table)
            # else: # Optional: message if no other disks found
                # st.caption("No additional disk partitions found or psutil not available for detailed listing.")


        st.markdown("---") # Visual separator

        st.subheader("Summary")
        st.markdown(f"**System Apps:** {len(system_list)} apps, **{system_total/1e9:.2f} GB**")
        st.markdown(f"**Downloaded Apps:** {len(downloaded_list)} apps, **{downloaded_total/1e9:.2f} GB**")

        with st.expander("System Apps Details"):
           st.table(system_list)
        with st.expander("Downloaded Apps Details"):
           st.table(downloaded_list)          

    prompt = st.chat_input("What is your question?")
    if prompt and current_gemini_session:
        software_name = parse_software_name(prompt)
        if software_name and software_name in SOFTWARE_CATALOG:
            download_and_install_software(software_name)
        elif prompt.lower().startswith("install "):
            st.warning("Sorry, I don't recognize that software yet.")   
        else:
          #  st.write("You said:", prompt)
            st.chat_message("user").markdown(prompt)
            add_message_to_current_chat("user",prompt)
            
            global_pdf_text=""
            
            if current_chat_data and "pdf_texts_associated" in current_chat_data:
                temp_texts = []
                for pdf_item in current_chat_data["pdf_texts_associated"]:
                    temp_texts.append(f"Content from {pdf_item['name']}:\n{pdf_item.get('full_text', '')}")
                global_pdf_text = "\n\n".join(temp_texts)

            context = f"Based on the documents:\n{global_pdf_text}\n\nUser Question: {prompt}" if global_pdf_text else prompt

            try:
                response = current_gemini_session.send_message(context)
                st.chat_message("assistant").markdown(response.text)
                add_message_to_current_chat("assistant",response.text)

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
            st.rerun()
            
    # with st.sidebar.expander("Chocolatey Software Management", expanded = False):
    #     st.warning(
    #         "! **Administrator Privileges Required**!\n"
    #         "For Chocolatey commands to work, this Streamlit application "
    #         "must be launched from a terminal running with **Administrator rights**."
    #     )
    #     try:
    #         choco_check = subprocess.run(["choco","-?"], capture_output=True, text=True, timeout=5)
    #         if choco_check.returncode != 0 and "is not recognized" in choco_check.stderr.lower(): # Basic check
    #              raise FileNotFoundError 
    #         st.caption("Chocolatey seems to be available.")
    #     except FileNotFoundError:
    #         st.error("`choco` command not found. Please ensure Chocolatey is installed and its bin directory (usually `C:\\ProgramData\\chocolatey\\bin`) is in your system's PATH. You may need to restart your terminal or system after installation/PATH modification.")
    #     except subprocess.TimeoutExpired:
    #         st.warning("Checking for 'choco' command timed out. It might be slow or misconfigured.")
    #     except Exception as e:
    #         st.warning(f"Could not verify 'choco' command: {e}")
    #     choco_package_name = st.text_input(
    #        "Enter Chocolatey package name (e.g., notepadplusplus, git):", 
    #         key="choco_package_name_input" # Use a unique key
    #     )
        
    #     col_choco1, col_choco2 = st.columns(2)
    #     with col_choco1:
    #         if st.button("Install with Chocolatey", key="choco_install_button"):
    #             if choco_package_name:
    #                 install_with_chocolatey(choco_package_name.strip().lower())
    #             else:
    #                 st.warning("Please enter a package name to install.")
    #     with col_choco2:
    #         if st.button("Update with Chocolatey", key="choco_update_button"):
    #             if choco_package_name:
    #                 upgrade_with_chocolatey(choco_package_name.strip().lower())
    #             else:
    #                 st.warning("Please enter a package name to update/check.")
        
    #     st.markdown("👉 Find packages at: [community.chocolatey.org/packages](https://community.chocolatey.org/packages)")
    # # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # # END OF CHOCOLATEY UI SECTION
    # # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    if not st.session_state.current_chat_id:
        st.info("Select a chat from the sidebar or create a new one to begin.")
        return

if __name__ == "__main__":
    if not os.path.exists("Uploads"):
        os.makedirs("uploads")
    clear_uploads_directory()
    main()
