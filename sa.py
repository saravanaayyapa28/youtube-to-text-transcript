import streamlit as st
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
import os
import google.generativeai as genai

load_dotenv() ##load all the environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt = """You are Yotube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points
within 250 words. Please provide the summary of the text given here and also advantages and disadvantages of summary: """


## getting the transcript data from yt videos
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript

    except YouTubeTranscriptApi.TranscriptsDisabled:
        st.error("Subtitles are disabled for this video. Cannot retrieve transcript.")
        return None

    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None
    
## getting the summary based on Prompt from Google Gemini Pro
def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + transcript_text)
    return response.text


st.title("YouTube video To Text  Summarizer 🎬")
youtube_link = st.text_input("Enter YouTube Video Link Below:")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Get Detailed Notes"):
    transcript_text = extract_transcript_details(youtube_link)

    if transcript_text:
        summary = generate_gemini_content(transcript_text, prompt)
        st.markdown("## Detailed Notes:")
        st.write(summary)