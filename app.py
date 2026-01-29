import streamlit as st
import os
import sys
import subprocess

# أمر إضافي لضمان تثبيت المكتبة على السيرفر
try:
    from moviepy.editor import VideoFileClip, concatenate_videoclips
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "moviepy"])
    from moviepy.editor import VideoFileClip, concatenate_videoclips

import tempfile

st.set_page_config(page_title="صانع فيديو التوقف")
st.title("🎬 إنشاء فيديو يتوقف كل 4 ثوانٍ")

uploaded_file = st.file_uploader("ارفع الفيديو من جهازك", type=["mp4", "mkv"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tfile:
        tfile.write(uploaded_file.read())
        video_path = tfile.name

    if st.button("بدء المعالجة الآن"):
        with st.spinner("جاري إنشاء الفيديو... انتظر قليلاً"):
            try:
                clip = VideoFileClip(video_path)
                duration = clip.duration
                final_clips = []
                
                for start in range(0, int(duration), 4):
                    end = min(start + 4, duration)
                    sub = clip.subclip(start, end)
                    final_clips.append(sub)
                    # لقطة ثابتة لمدة ثانية واحدة
                    freeze = sub.to_ImageClip(t=sub.duration - 0.1).set_duration(1)
                    final_clips.append(freeze)
                
                final_video = concatenate_videoclips(final_clips)
                output_name = "final_video_camon20.mp4"
                final_video.write_videofile(output_name, codec="libx264", audio_codec="aac")
                
                st.success("✅ تم التجهيز بنجاح!")
                with open(output_name, "rb") as f:
                    st.download_button("📥 تحميل الفيديو المعدل", f, file_name="my_anime_video.mp4")
            except Exception as e:
                st.error(f"حدث خطأ: {e}")
