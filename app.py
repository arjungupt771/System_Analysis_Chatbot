import os
import streamlit as st
from datetime import datetime, timedelta
import pytz
import tempfile
from utils.model import model
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Tuple
from Software_Catalog import SOFTWARE_CATALOG
from chat_db import init_db, load_chat_history, get_all_chat_ids, delete_chat
from utils.pdf import extract_text_from_pdf, clear_uploads_directory
from utils.chats import create_new_chat, select_chat, get_current_chat_data, get_current_gemini_session, add_message_to_current_chat
from utils.installexe import install_exe, parse_software_name, download_and_install_software
from utils.software_details import  scan_apps_and_storage, get_hardware_details
from utils.speech import speak, listen_from_mic
from streamlit.components.v1 import html
try:
    import psutil
except ImportError:
    psutil = None
    print("Warning: psutil library not found. Some system hardware details (RAM, CPU) will be unavailable.")
    print("Install it with: pip install psutil")



st.set_page_config(page_title="ChatMate AI", page_icon="static/robot.png")


def main():
    init_db()  # Ensure the database is set up
    clear_uploads_directory()
    if "all_chats" not in st.session_state:
        st.session_state.all_chats = {}

    if "current_chat_id" not in st.session_state:
        st.session_state.current_chat_id = None
        
    if "gemini_chat_sessions" not in st.session_state:
        st.session_state.gemini_chat_sessions={}
            
    if "spoken_text_from_mic" not in st.session_state:
        st.session_state.spoken_text_from_mic=""

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
            else:
                st.caption("Detailed CPU info requires 'psutil'.")

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

    if not st.session_state.current_chat_id:
        st.info("Select a chat from the sidebar or create a new one to begin.")
        return

if __name__ == "__main__":
    if not os.path.exists("Uploads"):
        os.makedirs("uploads")
    clear_uploads_directory()
    main()