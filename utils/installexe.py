import streamlit as st              
import os
import subprocess
import tempfile
import re
import requests
from Software_Catalog import get_software_info


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