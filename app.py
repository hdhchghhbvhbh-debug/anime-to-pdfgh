import streamlit as st
import os
import subprocess
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader

st.title("🎬 محول الأنمي الذكي")
uploaded_video = st.file_uploader("ارفع فيديو الأنمي", type=["mp4", "mkv"])

if uploaded_video:
    if st.button("صنع ملف PDF"):
        st.write("جاري المعالجة... انتظر قليلاً")
        with open("vid.mp4", "wb") as f:
            f.write(uploaded_video.read())
        os.makedirs("pics", exist_ok=True)
        subprocess.run("ffmpeg -i vid.mp4 -vf fps=1/10 pics/out%03d.jpg", shell=True)
        c = canvas.Canvas("anime.pdf", pagesize=letter)
        for img in sorted(os.listdir("pics")):
            c.drawImage(ImageReader(f"pics/{img}"), 50, 400, width=500, height=300)
            c.showPage()
        c.save()
        st.success("تم!")
        st.download_button("تحميل الـ PDF", open("anime.pdf", "rb"), "anime.pdf")
