import streamlit as st
from moviepy.editor import VideoFileClip, ImageClip, concatenate_videoclips
import tempfile
import os

st.set_page_config(page_title="صانع فيديو التوقف", layout="centered")
st.title("🎬 فيديو اللقطات الثابتة (كل 4 ثوانٍ)")

uploaded_file = st.file_uploader("اختر فيديو الأنمي من جهازك", type=["mp4", "mkv", "mov"])

if uploaded_file:
    # عرض الفيديو الأصلي للتأكد
    st.video(uploaded_file)
    
    if st.button("إنتاج فيديو التوقف الآن"):
        with st.spinner("جاري المعالجة... قد يستغرق الأمر دقيقة"):
            # إنشاء ملف مؤقت
            tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
            tfile.write(uploaded_file.read())
            
            try:
                clip = VideoFileClip(tfile.name)
                duration = clip.duration
                
                final_clips = []
                # التكرار كل 4 ثوانٍ
                for start in range(0, int(duration), 4):
                    end = min(start + 4, duration)
                    sub = clip.subclip(start, end)
                    final_clips.append(sub)
                    
                    # صنع لقطة ثابتة لمدة ثانية واحدة من نهاية كل مقطع
                    freeze = sub.to_ImageClip(t=sub.duration - 0.1).set_duration(1)
                    final_clips.append(freeze)
                
                # دمج المقاطع
                final_video = concatenate_videoclips(final_clips)
                output_file = "final_frozen_video.mp4"
                final_video.write_videofile(output_file, codec="libx264", audio_codec="aac")
                
                st.success("✅ تم بنجاح!")
                with open(output_file, "rb") as f:
                    st.download_button("📥 تحميل الفيديو الجديد", f, file_name="frozen_anime.mp4")
            
            except Exception as e:
                st.error(f"حدث خطأ فني: {e}")
            finally:
                # تنظيف الذاكرة
                if 'clip' in locals(): clip.close()
