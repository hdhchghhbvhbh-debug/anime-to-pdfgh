import streamlit as st
from moviepy.editor import VideoFileClip, ImageClip, concatenate_videoclips
import tempfile
import os

st.title("🎬 صانع فيديو اللقطات الثابتة")
st.write("سأقوم بجعل الفيديو يتوقف لمدة ثانية واحدة كل 4 ثوانٍ")

uploaded_video = st.file_uploader("ارفع فيديو الأنمي هنا", type=["mp4", "mkv"])

if uploaded_video:
    # حفظ الفيديو المرفوع مؤقتاً
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tfile:
        tfile.write(uploaded_video.read())
        video_path = tfile.name

    if st.button("بدء معالجة الفيديو"):
        with st.spinner("جاري إنشاء الفيديو الجديد... قد يستغرق ذلك دقيقة"):
            try:
                clip = VideoFileClip(video_path)
                duration = clip.duration
                
                final_parts = []
                for start_t in range(0, int(duration), 4):
                    end_t = min(start_t + 4, duration)
                    # الجزء المتحرك (4 ثوانٍ)
                    sub_clip = clip.subclip(start_t, end_t)
                    final_parts.append(sub_clip)
                    
                    # لقطة التوقف (ثبات لثانية واحدة عند نهاية الجزء)
                    freeze_frame = sub_clip.to_ImageClip(t=sub_clip.duration - 0.1).set_duration(1)
                    final_parts.append(freeze_frame)
                
                # دمج الأجزاء
                final_video = concatenate_videoclips(final_parts)
                out_name = "output_frozen.mp4"
                final_video.write_videofile(out_name, codec="libx264", audio_codec="aac")
                
                st.success("تم الانتهاء!")
                with open(out_name, "rb") as f:
                    st.download_button("📥 تحميل الفيديو المعدل", f, file_name="anime_fixed.mp4")
            except Exception as e:
                st.error(f"حدث خطأ: {e}")
