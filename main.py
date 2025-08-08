import streamlit as st
from app.youtube_comments import fetch_comments
from app.predict import analyze_comments

st.set_page_config(page_title="YouTube Sentiment Analyzer", layout="wide")

st.title("🎯 YouTube Sentiment Analyzer")

video_url = st.text_input("Enter YouTube Video URL:")

if st.button("Analyze"):
    if not video_url.strip():
        st.error("Please enter a valid YouTube video URL")
    else:
        if "v=" in video_url:
            video_id = video_url.split("v=")[1].split("&")[0]
        else:
            video_id = video_url.split("/")[-1]

        with st.spinner("Fetching comments..."):
            comments = fetch_comments(video_id)

        if not comments:
            st.warning("No comments found for this video.")
        else:
            with st.spinner("Analyzing sentiments..."):
                analysis = analyze_comments(comments)

            summary = {
                "Negative": sum(1 for res in analysis if res["sentiment"] == "Negative"),
                "Neutral": sum(1 for res in analysis if res["sentiment"] == "Neutral"),
                "Positive": sum(1 for res in analysis if res["sentiment"] == "Positive"),
            }

            st.subheader("📊 Sentiment Summary")
            col1, col2, col3 = st.columns(3)
            col1.metric("Positive", summary["Positive"])
            col2.metric("Negative", summary["Negative"])
            col3.metric("Neutral", summary["Neutral"])

            st.bar_chart(summary)

            st.subheader("💬 Top Comments")
            top_comments = sorted(analysis, key=lambda x: abs(x['rating'] - 5), reverse=True)[:20]
            for comment in top_comments:
                st.markdown(
                    f"**{comment['sentiment']}** ({comment['rating']}/10) - {comment['comment']}"
                )
