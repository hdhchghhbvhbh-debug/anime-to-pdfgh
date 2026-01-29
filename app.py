import streamlit as st
import cv2
import tempfile
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os

st.title("🎬 محول الأنمي الذكي (نسخ ثابتة كل 4 ثوانٍ)")

uploaded_video = st.file_uploader("ارفع فيديو الأنمي", type=["mp4", "mkv"])

if uploaded_video:
    # حفظ الفيديو المرفوع في ملف مؤقت
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_video.read())
    
    if st.button("صنع ملف PDF للمشاهد"):
        st.info("جاري استخراج المشاهد كل 4 ثوانٍ... يرجى الانتظار")
        
        cap = cv2.VideoCapture(tfile.name)
        fps = cap.get(cv2.CAP_PROP_FPS) # الحصول على عدد الفريمات في الثانية
        interval = int(fps * 4) # تحديد الفاصل الزمني (كل 4 ثوانٍ)
        
        frames = []
        count = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            if count % interval == 0:
                # تحويل اللون من BGR إلى RGB ليكون صحيحاً في الـ PDF
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img_path = f"frame_{count}.jpg"
                cv2.imwrite(img_path, cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR))
                frames.append(img_path)
            count += 1
        cap.release()

        # إنشاء ملف الـ PDF
        pdf_path = "anime_scenes.pdf"
        c = canvas.Canvas(pdf_path, pagesize=letter)
        width, height = letter

        for img in frames:
            c.drawImage(img, 50, height - 350, width=500, height=300)
            c.showPage()
            os.remove(img) # حذف الصورة المؤقتة بعد إضافتها للـ PDF
        
        c.save()
        
        if os.path.exists(pdf_path):
            st.success("تم تجهيز ملف الـ PDF بنجاح!")
            with open(pdf_path, "rb") as f:
                st.download_button("تحميل ملف الـ PDF", f, file_name="anime_scenes.pdf")
        else:
            st.error("حدث خطأ أثناء إنشاء ملف الـ PDF.")
