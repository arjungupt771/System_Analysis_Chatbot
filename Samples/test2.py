import streamlit as st
from pytube import YouTube
from moviepy import VideoFileClip
import os
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from sklearn.metrics.pairwise import cosine_similarity
import openai
from streamlit_player import st_player



# Initialize session state
if "videos" not in st.session_state:
    st.session_state.videos = []
if "messages" not in st.session_state:
    st.session_state.messages = []
    
#client = openai.OpenAI(api_key=ZrEspEMMQ0nMjnuBg7kkuJRFEF1iMS4Rn-VKjG10MEGGvNfRHla9W5pAl7A85Ub51eH5NI2VsYT3BlbkFJFuYmMLciG5ecjeN2aPglNQlY1HTCed2yI9LqkyZsg7HtAwS3nyurQbMkKuttDVdJYgk7cGkqsA)
def process_video(video_path):
    """Extract audio and transcribe using Whisper"""
    audio_path = video_path.split('.')[0] + '.wav'
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)
    
    with open(audio_path, "rb") as audio_file:
        transcript = openai.audio.transcriptions.create("whisper-1", audio_file)
    
    os.remove(audio_path)
    return transcript['text']

def get_youtube_video(url):
    """Download YouTube video and return local path"""
    yt = YouTube(url)
    video = yt.streams.filter(progressive=True, file_extension='mp4').first()
    return video.download()

# Streamlit UI
st.title("Video Analysis Chatbot")
st.sidebar.header("Video Input")

# Video input section
video_url = st.sidebar.text_input("Enter YouTube URL:")
uploaded_file = st.sidebar.file_uploader("Or upload video", type=["mp4", "mov"])

if st.sidebar.button("Add Video"):
    if video_url:
        local_path = get_youtube_video(video_url)
        st.session_state.videos.append({"source": video_url, "path": local_path})
    elif uploaded_file:
        with open(uploaded_file.name, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.session_state.videos.append({"source": uploaded_file.name, "path": uploaded_file.name})

# Display uploaded videos
st.sidebar.subheader("Loaded Videos")
for vid in st.session_state.videos:
    st.sidebar.write(f"📹 {vid['source'][:30]}...")

# Chat interface
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "video" in message:
            if "youtube.com" in message["video"]:
                st_player(message["video"])
            else:
                st.video(message["video"])

if prompt := st.chat_input("Ask about the videos:"):
    # Process question
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Process videos and create embeddings
    transcripts = []
    for vid in st.session_state.videos:
        transcript = process_video(vid["path"])
        transcripts.append(transcript)
    
    # Create vector store
    embeddings = OpenAIEmbeddings()
    docsearch = FAISS.from_texts(transcripts, embeddings)
    
    # Find most relevant video
    query_embedding = embeddings.embed_query(prompt)
    doc_embeddings = docsearch.index.reconstruct_n()
    
    similarities = cosine_similarity([query_embedding], doc_embeddings)[0]
    best_match_idx = similarities.argmax()
    
    # Generate response
    context = transcripts[best_match_idx]
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{
            "role": "user",
            "content": f"Question: {prompt}\nContext: {context}"
        }]
    ).choices[0].message['content']
    
    # Display response
    with st.chat_message("assistant"):
        st.markdown(response)
        if len(st.session_state.videos) > 1:
            st.write(f"**Most relevant video:** {st.session_state.videos[best_match_idx]['source']}")
            if "youtube.com" in st.session_state.videos[best_match_idx]['source']:
                st_player(st.session_state.videos[best_match_idx]['source'])
            else:
                st.video(st.session_state.videos[best_match_idx]['path'])
        
    st.session_state.messages.append({
        "role": "assistant", 
        "content": response,
        "video": st.session_state.videos[best_match_idx]['source']
    })
