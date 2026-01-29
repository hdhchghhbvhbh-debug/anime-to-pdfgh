import streamlit as st
import cv2
import tempfile
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os

st.title("🎬 محول الأنمي - لقطات كل 4 ثوانٍ")

uploaded_video = st.file_uploader("ارفع فيديو الأنمي هنا", type=["mp4", "mkv"])

if uploaded_video:
    # عرض الفيديو في التطبيق لكي تراه
    st.video(uploaded_video)
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tfile:
        tfile.write(uploaded_video.read())
        video_path = tfile.name

    if st.button("صنع ملف PDF مع نصوص"):
        st.info("جاري معالجة المشاهد... يرجى الانتظار")
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        interval = int(fps * 4) 
        
        pdf_path = "anime_with_text.pdf"
        c = canvas.Canvas(pdf_path, pagesize=letter)
        width, height = letter
        
        count = 0
        images_added = 0
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: break
            
            if count % interval == 0:
                img_name = f"frame_{count}.jpg"
                cv2.imwrite(img_name, frame)
                
                # وضع الصورة في النصف العلوي من الصفحة
                c.drawImage(img_name, 50, height - 350, width=500, height=300)
                
                # كتابة النص تحت الصورة
                c.setFont("Helvetica", 12)
                text = f"Scene at: {int(count/fps)} seconds"
                c.drawString(50, height - 380, text) # إحداثيات النص تحت الصورة
                
                c.showPage()
                os.remove(img_name)
                images_added += 1
            count += 1
            
        cap.release()
        c.save()
        
        if images_added > 0:
            st.success(f"تم صنع PDF بنجاح!")
            with open(pdf_path, "rb") as f:
                st.download_button("📥 تحميل ملف الـ PDF", f, file_name="anime_scenes.pdf")
