import os
import streamlit as st

from datetime import datetime
from typing import List, Dict, Tuple

from utils.model import model

from Software_Catalog import SOFTWARE_CATALOG, get_software_info

from chat_db import (
    init_db,
    save_message,
    load_chat_history,
    get_all_chat_ids,
    delete_chat,
)

from utils.pdf import (
    extract_text_from_pdf,
    clear_uploads_directory,
)

from utils.chats import (
    create_new_chat,
    select_chat,
    get_current_chat_data,
    get_current_gemini_session,
    add_message_to_current_chat,
)

from utils.installexe import (
    install_exe,
    parse_software_name,
    download_and_install_software,
)

from utils.software_details import (
    scan_apps_and_storage,
    get_hardware_details,
)

from utils.speech import (
    speak,
    listen_from_mic,
)

from streamlit.components.v1 import html


try:
    import psutil
except ImportError:
    psutil = None
    print(
        "Warning: psutil library not found. "
        "Some system hardware details will be unavailable."
    )
    print("Install it with: pip install psutil")



st.set_page_config(page_title="ChatMate AI", page_icon="static/robot.png")





def main():
    # -----------------------------
    # Initialize database
    # -----------------------------
    init_db()

    # -----------------------------
    # Session state
    # -----------------------------
    if "all_chats" not in st.session_state:
        st.session_state.all_chats = {}

    if "current_chat_id" not in st.session_state:
        st.session_state.current_chat_id = None

    if "gemini_chat_sessions" not in st.session_state:
        st.session_state.gemini_chat_sessions = {}

    if "spoken_text_from_mic" not in st.session_state:
        st.session_state.spoken_text_from_mic = ""

    # -----------------------------
    # Current date/time
    # -----------------------------
    ist = pytz.timezone("Asia/Kolkata")
    now = datetime.now(ist)
    current_time = now.strftime("%A, %B %d, %Y at %I:%M %p")

    # -----------------------------
    # Page header
    # -----------------------------
    st.title("Welcome to Sophos AI...")
    st.markdown(f"**Current Date & Time (IST):** {current_time}")
    st.markdown("Ask, upload, and discover—AI at your service.")
    st.markdown("~ Arjun Gupta", unsafe_allow_html=True)

    # -----------------------------
    # Upload directory cleanup
    # -----------------------------
    clear_uploads_directory()

    # -----------------------------
    # Load saved chats
    # -----------------------------
    for chat_id in get_all_chat_ids():
        if chat_id not in st.session_state.all_chats:
            messages = load_chat_history(chat_id)

            st.session_state.all_chats[chat_id] = {
                "id": chat_id,
                "title": (
                    messages[0]["parts"][0][:30] + "..."
                    if messages
                    else f"Chat {chat_id}"
                ),
                "messages": messages,
                "pdf_texts_associated": [],
                "created_at": datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
            }

    # -----------------------------
    # Sidebar - Chat history
    # -----------------------------
    st.sidebar.title("ChatMate AI")

    if st.sidebar.button(
        "➕ New Chat",
        use_container_width=True,
    ):
        create_new_chat()

    st.sidebar.subheader("Chat History")

    chat_options = {
        st.session_state.all_chats[cid]["title"]: cid
        for cid in sorted(
            st.session_state.all_chats.keys(),
            key=lambda cid: st.session_state.all_chats[cid]["created_at"],
            reverse=True,
        )
    }

    selected_titles = st.sidebar.multiselect(
        "Select chat(s) to delete or open:",
        list(chat_options.keys()),
    )

    if selected_titles:

        if len(selected_titles) == 1:
            if st.sidebar.button("Open Chat"):
                select_chat(
                    chat_options[selected_titles[0]]
                )

        if st.sidebar.button("Delete Selected Chat(s)"):
            for title in selected_titles:
                chat_id = chat_options[title]

                delete_chat(chat_id)

                st.session_state.all_chats.pop(
                    chat_id,
                    None,
                )

                st.session_state.gemini_chat_sessions.pop(
                    chat_id,
                    None,
                )

            st.sidebar.success(
                f"Deleted {len(selected_titles)} chat(s)."
            )

            st.rerun()

    # -----------------------------
    # PDF upload
    # -----------------------------
    st.sidebar.header("Upload PDF Documents")

    pdf_files = st.sidebar.file_uploader(
        "Upload PDFs (Max 10MB each)",
        type=["pdf"],
        accept_multiple_files=True,
        key=f"pdf_uploader_{st.session_state.current_chat_id or 'global'}",
    )

    if pdf_files:
        st.write(f"Uploaded PDF: {pdf_files[0].name}")

    # -----------------------------
    # Windows EXE upload
    # -----------------------------
    st.sidebar.header("Upload Software .exe file")

    exe_file = st.sidebar.file_uploader(
        "Upload .exe File",
        type=["exe"],
        key=f"exe_uploader_{st.session_state.current_chat_id or 'global'}",
    )

    # -----------------------------
    # Current chat
    # -----------------------------
    current_chat_data = get_current_chat_data()

    # -----------------------------
    # Process PDF files
    # -----------------------------
    if pdf_files and current_chat_data:

        newly_extracted_texts = []

        for pdf_file in pdf_files:

            if pdf_file.size > 10 * 1024 * 1024:
                st.sidebar.error(
                    f"File {pdf_file.name} exceeds 10MB limit. Skipping."
                )
                continue

            already_uploaded = any(
                pdf_info["name"] == pdf_file.name
                for pdf_info in current_chat_data.get(
                    "pdf_texts_associated",
                    [],
                )
            )

            if already_uploaded:
                continue

            with st.spinner(
                f"Processing {pdf_file.name} for current chat..."
            ):

                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".pdf",
                    dir="uploads",
                ) as tmp_pdf:

                    tmp_pdf.write(
                        pdf_file.getbuffer()
                    )

                    tmp_pdf_path = tmp_pdf.name

                try:
                    extracted_text = extract_text_from_pdf(
                        tmp_pdf_path
                    )

                    newly_extracted_texts.append(
                        extracted_text
                    )

                    current_chat_data[
                        "pdf_texts_associated"
                    ].append(
                        {
                            "name": pdf_file.name,
                            "full_text": extracted_text,
                            "text_summary": extracted_text[:200],
                        }
                    )

                finally:
                    if os.path.exists(tmp_pdf_path):
                        os.remove(tmp_pdf_path)

        if newly_extracted_texts:
            st.sidebar.success(
                f"Added {len(newly_extracted_texts)} PDF(s) to current chat!"
            )

    # -----------------------------
    # Windows EXE installation
    # -----------------------------
    if exe_file is not None:

        st.sidebar.write(
            f"Uploaded .exe: {exe_file.name}"
        )

        if st.sidebar.button(
            "Install Software",
            key="install_uploaded_exe",
        ):
            install_exe(exe_file)

    # -----------------------------
    # Require an active chat
    # -----------------------------
    if not st.session_state.current_chat_id:
        st.info(
            "Select a chat from the sidebar or create a new one to begin."
        )
        return

    # -----------------------------
    # Display chat history
    # -----------------------------
    current_chat_display = get_current_chat_data()

    if current_chat_display:

        st.subheader(
            f"Conversation: {current_chat_display['title']}"
        )

        for message in current_chat_display["messages"]:

            role = message.get("role")

            # Protect Streamlit from unsupported roles
            if role not in ("user", "assistant"):
                continue

            with st.chat_message(role):
                st.markdown(
                    message["parts"][0]
                )

    # -----------------------------
    # Gemini session
    # -----------------------------
    current_gemini_session = get_current_gemini_session()

    # -----------------------------
    # Voice + Scan buttons
    # -----------------------------
    col1, col2 = st.columns(2)

    with col1:
        speak_clicked = st.button(
            "🎤 Speak",
            key="speak_btn",
        )

    with col2:
        scan_apps_clicked = st.button(
            "🖥️ Scan Apps",
            key="scan_apps_btn",
        )

    # -----------------------------
    # Voice interaction
    # -----------------------------
    if speak_clicked:

        spoken_text = listen_from_mic()

        if spoken_text and spoken_text.strip():

            spoken_text = spoken_text.strip()

            # Display user voice input
            st.chat_message("user").markdown(
                spoken_text
            )

            add_message_to_current_chat(
                "user",
                spoken_text,
            )

            spoken_lower = spoken_text.lower()

            # -------------------------
            # Voice command: Scan Apps
            # -------------------------
            if "scan apps" in spoken_lower:

                with st.spinner(
                    "Scanning installed apps and calculating storage..."
                ):

                    (
                        system_list,
                        downloaded_list,
                        system_total,
                        downloaded_total,
                    ) = scan_apps_and_storage()

                st.subheader("Summary")

                st.markdown(
                    f"**System Apps:** "
                    f"{len(system_list)} apps, "
                    f"**{system_total / 1e9:.2f} GB**"
                )

                st.markdown(
                    f"**Downloaded Apps:** "
                    f"{len(downloaded_list)} apps, "
                    f"**{downloaded_total / 1e9:.2f} GB**"
                )

                with st.expander(
                    "System Apps Details"
                ):
                    st.table(system_list)

                with st.expander(
                    "Downloaded Apps Details"
                ):
                    st.table(downloaded_list)

                add_message_to_current_chat(
                    "assistant",
                    (
                        f"Scanned apps:\n"
                        f"System: {len(system_list)} "
                        f"({system_total / 1e9:.2f} GB)\n"
                        f"Downloaded: {len(downloaded_list)} "
                        f"({downloaded_total / 1e9:.2f} GB)"
                    ),
                )

                return

            # -------------------------
            # Voice command: Install
            # -------------------------
            if "install" in spoken_lower:

                software_name = parse_software_name(
                    spoken_text
                )

                if (
                    software_name
                    and software_name in SOFTWARE_CATALOG
                ):

                    download_and_install_software(
                        software_name
                    )

                    return

                st.warning(
                    "Software not recognized in the catalog."
                )

                return

            # -------------------------
            # Normal voice chat
            # -------------------------
            if current_gemini_session:

                try:

                    with st.spinner(
                        "Getting Gemini response..."
                    ):
                        response = (
                            current_gemini_session.send_message(
                                spoken_text
                            )
                        )

                    st.chat_message(
                        "assistant"
                    ).markdown(
                        response.text
                    )

                    add_message_to_current_chat(
                        "assistant",
                        response.text,
                    )

                    speak(response.text)

                except Exception as e:

                    st.error(
                        f"Error processing voice request: {e}"
                    )

            return

        st.warning(
            "Didn't capture any speech."
        )

    # -----------------------------
    # Windows System Scan
    # -----------------------------
    if scan_apps_clicked:

        with st.spinner(
            "Scanning installed apps and calculating storage..."
        ):

            (
                system_list,
                downloaded_list,
                system_total,
                downloaded_total,
            ) = scan_apps_and_storage()

            hardware_details = get_hardware_details()

        st.header(
            "📊 System & Software Scan Results"
        )

        # -----------------------------
        # Hardware information
        # -----------------------------
        st.subheader(
            "💻 System Hardware & OS Information"
        )

        col_hw1, col_hw2 = st.columns(2)

        with col_hw1:

            st.metric(
                label="Operating System",
                value=hardware_details.get(
                    "os_version",
                    "N/A",
                ),
            )

            st.metric(
                label="OS Architecture",
                value=hardware_details.get(
                    "os_architecture",
                    "N/A",
                ),
            )

            st.metric(
                label="CPU Model",
                value=hardware_details.get(
                    "cpu_model",
                    "N/A",
                ),
            )

            total_storage = hardware_details.get(
                "total_system_storage_gb"
            )

            st.metric(
                label="Total System Storage",
                value=(
                    f"{total_storage:.2f} GB"
                    if isinstance(
                        total_storage,
                        (int, float),
                    )
                    else "N/A"
                ),
            )

            if psutil:

                st.metric(
                    label="CPU Physical Cores",
                    value=str(
                        hardware_details.get(
                            "cpu_physical_cores",
                            "N/A",
                        )
                    ),
                )

                st.metric(
                    label="CPU Logical Cores",
                    value=str(
                        hardware_details.get(
                            "cpu_logical_cores",
                            "N/A",
                        )
                    ),
                )

                cpu_usage = hardware_details.get(
                    "cpu_usage_percent"
                )

                st.metric(
                    label="CPU Current Usage",
                    value=(
                        f"{cpu_usage:.1f}%"
                        if isinstance(
                            cpu_usage,
                            (int, float),
                        )
                        else "N/A"
                    ),
                )

            else:
                st.caption(
                    "Detailed CPU information requires psutil."
                )

        with col_hw2:

            ram_total = hardware_details.get(
                "ram_total_gb"
            )

            ram_available = hardware_details.get(
                "ram_available_gb"
            )

            ram_used = hardware_details.get(
                "ram_used_gb"
            )

            ram_percent = hardware_details.get(
                "ram_percent_used"
            )

            st.metric(
                label="Total RAM",
                value=(
                    f"{ram_total:.2f} GB"
                    if isinstance(
                        ram_total,
                        (int, float),
                    )
                    else "N/A"
                ),
            )

            st.metric(
                label="Available RAM",
                value=(
                    f"{ram_available:.2f} GB"
                    if isinstance(
                        ram_available,
                        (int, float),
                    )
                    else "N/A"
                ),
            )

            if (
                isinstance(ram_used, (int, float))
                and isinstance(ram_percent, (int, float))
            ):
                st.metric(
                    label="Used RAM",
                    value=(
                        f"{ram_used:.2f} GB "
                        f"({ram_percent:.1f}%)"
                    ),
                )
            else:
                st.metric(
                    label="Used RAM",
                    value="N/A",
                )

            disk_c_total = hardware_details.get(
                "disk_c_total_gb"
            )

            disk_c_used = hardware_details.get(
                "disk_c_used_gb"
            )

            disk_c_free = hardware_details.get(
                "disk_c_free_gb"
            )

            st.metric(
                label="C: Drive Total Space",
                value=(
                    f"{disk_c_total:.2f} GB"
                    if isinstance(
                        disk_c_total,
                        (int, float),
                    )
                    else "N/A"
                ),
            )

            st.metric(
                label="C: Drive Used Space",
                value=(
                    f"{disk_c_used:.2f} GB"
                    if isinstance(
                        disk_c_used,
                        (int, float),
                    )
                    else "N/A"
                ),
            )

            st.metric(
                label="C: Drive Free Space",
                value=(
                    f"{disk_c_free:.2f} GB"
                    if isinstance(
                        disk_c_free,
                        (int, float),
                    )
                    else "N/A"
                ),
            )

        # -----------------------------
        # All disk partitions
        # -----------------------------
        if hardware_details.get("all_disks"):

            st.markdown(
                "##### All Disk Partitions"
            )

            disk_data_for_table = []

            for disk_item in hardware_details[
                "all_disks"
            ]:

                disk_data_for_table.append(
                    {
                        "Mount Point": disk_item.get(
                            "mountpoint",
                            "N/A",
                        ),
                        "File System": disk_item.get(
                            "fstype",
                            "N/A",
                        ),
                        "Total GB": f"{disk_item.get('total_gb', 0):.2f}",
                        "Used GB": f"{disk_item.get('used_gb', 0):.2f}",
                        "Free GB": f"{disk_item.get('free_gb', 0):.2f}",
                    }
                )

            if disk_data_for_table:
                st.table(
                    disk_data_for_table
                )

        # -----------------------------
        # Software summary
        # -----------------------------
        st.markdown("---")

        st.subheader("Software Summary")

        st.markdown(
            f"**System Apps:** "
            f"{len(system_list)} apps, "
            f"**{system_total / 1e9:.2f} GB**"
        )

        st.markdown(
            f"**Downloaded Apps:** "
            f"{len(downloaded_list)} apps, "
            f"**{downloaded_total / 1e9:.2f} GB**"
        )

        with st.expander(
            "System Apps Details"
        ):
            st.table(system_list)

        with st.expander(
            "Downloaded Apps Details"
        ):
            st.table(downloaded_list)

    # -----------------------------
    # Text Chat
    # -----------------------------
    prompt = st.chat_input(
        "What is your question?"
    )

    if prompt and current_gemini_session:

        software_name = parse_software_name(
            prompt
        )

        # -------------------------
        # Text command: Install
        # -------------------------
        if (
            software_name
            and software_name in SOFTWARE_CATALOG
        ):

            download_and_install_software(
                software_name
            )

        elif prompt.lower().startswith(
            "install "
        ):

            st.warning(
                "Sorry, I don't recognize that software yet."
            )

        # -------------------------
        # Normal AI chat
        # -------------------------
        else:

            st.chat_message(
                "user"
            ).markdown(prompt)

            add_message_to_current_chat(
                "user",
                prompt,
            )

            # Build PDF context
            global_pdf_text = ""

            if (
                current_chat_data
                and "pdf_texts_associated"
                in current_chat_data
            ):

                pdf_contents = []

                for pdf_item in current_chat_data[
                    "pdf_texts_associated"
                ]:

                    pdf_contents.append(
                        f"Content from "
                        f"{pdf_item['name']}:\n"
                        f"{pdf_item.get('full_text', '')}"
                    )

                global_pdf_text = (
                    "\n\n".join(pdf_contents)
                )

            context = (
                f"Based on the documents:\n"
                f"{global_pdf_text}\n\n"
                f"User Question: {prompt}"
                if global_pdf_text
                else prompt
            )

            try:

                with st.spinner(
                    "ChatMate AI is thinking..."
                ):

                    response = (
                        current_gemini_session.send_message(
                            context
                        )
                    )

                st.chat_message(
                    "assistant"
                ).markdown(
                    response.text
                )

                add_message_to_current_chat(
                    "assistant",
                    response.text,
                )

            except Exception as e:

                st.error(
                    f"An error occurred: {str(e)}"
                )

if __name__ == "__main__":
    if not os.path.exists("uploads"):
        os.makedirs("uploads")

    clear_uploads_directory()
    main()

