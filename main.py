import streamlit as st
import my_chain as mch
import textwrap
import os

st.set_page_config(page_title=" AI YouTube Assistant", page_icon="static/youtube.svg", layout="centered")

svg_path = os.path.join("static", "youtube.svg")
if os.path.exists(svg_path):
    svg = open(svg_path, "r", encoding="utf-8").read()
    svg = svg.replace(
        "<svg",
        "<svg style='width:1.8em; height:1.8em; vertical-align:middle;'"
    )
    st.markdown(
        f"""
        <div style="display:flex; justify-content:center; margin-bottom: 1rem;">
          <div style="font-size: 1.8rem; display: flex; align-items: center; gap: 0.4em;">
            {svg}
            <span style="line-height: 1;">  YouTube AI Assistant </span>
          </div>
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown("<h1 style='text-align:center;'>YouTube Assistant</h1>")

with st.sidebar:
    st.header("🔍 Ask about a YouTube video")
    with st.form(key='my_form'):
        youtube_url = st.text_area("📺 YouTube video URL", max_chars=200)
        query = st.text_area("💬 Your question", max_chars=200)
        openai_api_key = st.text_input("🔑 OpenAI API Key", type="password")
        st.markdown("[Get an OpenAI API key](https://platform.openai.com/account/api-keys)")
        submit_button = st.form_submit_button("Submit")

if submit_button:
    if not (youtube_url and query and openai_api_key):
        st.warning("⚠️ Please complete all fields.")
        st.stop()
    with st.spinner("⏳ Processing…"):
        db = mch.create_vect_db_from_ytb_url(youtube_url)
        response = mch.response_from_query(db, query)
        st.subheader("🧠 Answer:")
        st.text(textwrap.fill(response, width=85))
