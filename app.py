import streamlit as st
from moviepy.editor import VideoFileClip, ImageClip, concatenate_videoclips
import tempfile
import os

st.title("🎬 صانع فيديو اللقطات الثابتة")
st.write("هذا التطبيق سيجعل الفيديو يتوقف لمدة ثانية واحدة كل 4 ثوانٍ")

uploaded_video = st.file_uploader("ارفع الفيديو هنا", type=["mp4", "mov", "avi"])

if uploaded_video:
    # حفظ الملف المرفوع مؤقتاً
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tfile:
        tfile.write(uploaded_video.read())
        video_path = tfile.name

    if st.button("بدء إنشاء الفيديو الجديد"):
        with st.spinner("جاري معالجة الفيديو... قد يستغرق ذلك وقتاً حسب طول المقطع"):
            clip = VideoFileClip(video_path)
            duration = clip.duration
            
            parts = []
            current_time = 0
            
            # تقسيم الفيديو وعمل "تجميد" كل 4 ثوانٍ
            while current_time < duration:
                # نأخذ 4 ثوانٍ من الفيديو الأصلي
                end_time = min(current_time + 4, duration)
                sub_clip = clip.subclip(current_time, end_time)
                parts.append(sub_clip)
                
                # نأخذ لقطة ثابتة (آخر فريم في الـ 4 ثوانٍ) ونجعلها تتوقف لثانية واحدة
                freeze_frame = sub_clip.to_ImageClip(t=sub_clip.duration).set_duration(1)
                parts.append(freeze_frame)
                
                current_time += 4
            
            # دمج كل الأجزاء في فيديو واحد
            final_video = concatenate_videoclips(parts)
            output_path = "frozen_anime.mp4"
            final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")
            
            st.success("تم تجهيز الفيديو!")
            with open(output_path, "rb") as file:
                st.download_button("📥 تحميل الفيديو الجديد", file, file_name="frozen_anime.mp4")
            
            # تنظيف الملفات
            clip.close()
            final_video.close()
