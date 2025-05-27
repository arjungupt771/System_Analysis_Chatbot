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


# def get_win32_apps():
#     result = subprocess.run([
#         "powershell","-Command",
#         "Get-WmiObject -Class Win32_Product | Select Name, InstallLocation | ConvertTo-Json"
#     ], capture_output=True, text=True)
#     try:
#         return json.loads(result.stdout)
#     except Exception:
#         return[]


        # data= json.loads(result.stdout)
        # if isinstance(data,dict):
        #     data=[data]
        
        
        
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

        
    # if "is_listening" not in st.session_state:
    #     st.session_state.is_listening = False
    
        # if "mic_recognizer" not in st.session_state: # To hold the recognizer and mic instances
    #     st.session_state.mic_recognizer = None
        
    # if "mic_source" not in st.session_state:
    #     st.session_state.mic_source = None
        
    # if "stop_listening_func" not in st.session_state: # For background listening stop
    #     st.session_state.stop_listening_func = None
    
    
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
    
    
            # speak_clicked = "🛑 Stop Listening" if st.session_state.get('is_listening', False) else "🎤 Speak"
        # if st.button(speak_button_label, key="speak_toggle_button_main"): # New key
        #     if not st.session_state.get('is_listening', False):
        #         st.session_state.spoken_text_from_mic = "" # Clear before starting
        #listen_from_mic() # <<< THIS CALL
        #         st.rerun()
        #     else:
        #         stop_listening_manually()
        #         st.rerun()
        
        
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
        
        
                        # st.metric(label="CPU Physical Cores", value=str(hardware_details.get('cpu_physical_cores', 'N/A')))
                # st.metric(label="CPU Logical Cores", value=str(hardware_details.get('cpu_logical_cores', 'N/A')))
                # st.metric(label="CPU Current Usage", value=f"{hardware_details.get('cpu_usage_percent', 'N/A')} %")
                
                
                

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
        
        
                    # else: # Optional: message if no other disks found
                # st.caption("No additional disk partitions found or psutil not available for detailed listing.")
                
                    
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