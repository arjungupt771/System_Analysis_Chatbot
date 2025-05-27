import streamlit as st
import os
import tempfile
import torch
from transformers import pipeline
from sentence_transformers import SentenceTransformer, util
import whisper
import subprocess
import wave
import yt_dlp

# Check if audio file is valid
def is_valid_audio(filepath):
    with wave.open(filepath, 'rb') as wf:
        frames = wf.getnframes()
        framerate = wf.getframerate()
        duration = frames / float(framerate)
        return frames > 0 and duration > 1

# Load models only once
@st.cache_resource
def load_models():
    transcriber = whisper.load_model("tiny")
    embedder = SentenceTransformer('all-MiniLM-L6-v2')
    return transcriber, embedder

transcriber, embedder = load_models()

# Extract audio from video using FFmpeg
def extract_audio_ffmpeg(video_path):
    audio_path = video_path + ".wav"
    command = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-ac", "1",
        "-ar", "16000",
        "-f", "wav",
        audio_path
    ]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if not os.path.exists(audio_path) or os.path.getsize(audio_path) == 0:
        raise RuntimeError("❌ Audio extraction failed or resulted in an empty file.")
    return audio_path

# Transcribe audio
def transcribe_video(video_path):
    audio_path = extract_audio_ffmpeg(video_path)
    if os.path.getsize(audio_path) == 0:
        raise RuntimeError("Extracted Audio is Empty!")
    audio_tensor = whisper.load_audio(audio_path)
    if audio_tensor.shape[0] == 0:
        raise RuntimeError("Audio is Silent or Invalid")
    result = transcriber.transcribe(audio_path)
    return result['text']

# Download YouTube video
def download_video(url):
    temp_dir = tempfile.mkdtemp()
    output_template = os.path.join(temp_dir, '%(title)s.%(ext)s')
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': output_template,
        'merge_output_format': 'mp4',
        'quiet': True,
        'cookies': 'cookies.txt'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        video_path = ydl.prepare_filename(info)
    return video_path

# Streamlit App UI
st.title("🎥 Video Analysis Chatbot")

# Initialize session state
session_data = st.session_state.setdefault('video_data', {})

# Upload section
uploaded_videos = st.file_uploader("Upload Video(s)", type=["mp4", "mpe4", "webm"], accept_multiple_files=True)
video_links_input = st.text_area("Paste video links (YouTube) - One per line")

# Process videos (just once)
if st.button("Process Videos"):
    for uploaded_file in uploaded_videos or []:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
            tmp_file.write(uploaded_file.read())
            path = tmp_file.name
            st.text(f"Processing: {uploaded_file.name}")
            if path not in session_data:
                try:
                    transcript = transcribe_video(path)
                    session_data[path] = {'transcript': transcript}
                except Exception as e:
                    st.error(f"❌ Error processing {uploaded_file.name}: {str(e)}")

    for link in video_links_input.strip().split("\n"):
        if link:
            st.text(f"Processing: {link}")
            try:
                path = download_video(link)
                if path not in session_data:
                    transcript = transcribe_video(path)
                    session_data[path] = {'transcript': transcript}
            except Exception as e:
                st.error(f"❌ Error processing {link}: {str(e)}")

# Question + Chat-style interaction
st.header("💬 Chat with the Videos")
chat_question = st.text_input("Ask a question about any uploaded/linked video:")

if chat_question and session_data:
    q_embedding = embedder.encode(chat_question, convert_to_tensor=True)
    responses = []
    for path, data in session_data.items():
        t_embed = embedder.encode(data['transcript'], convert_to_tensor=True)
        sim_score = util.pytorch_cos_sim(q_embedding, t_embed).item()
        responses.append((sim_score, path, data))

    responses.sort(reverse=True)
    best = responses[0]

    st.markdown(f"**Best Match Video:**")
    st.video(best[1])
    st.markdown(f"**Similarity:** {best[0]:.2f}")
    st.markdown("**Transcript:**")
    st.text_area("Full Transcript", best[2]['transcript'], height=400)




