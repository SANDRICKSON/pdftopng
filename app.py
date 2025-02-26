import streamlit as st
from PIL import Image
from reportlab.pdfgen import canvas
import os

st.set_page_config(page_title="Image to PDF Converter", page_icon="📄")

st.title("🖼️ Image to PDF Converter")
st.write("Upload images and convert them into a PDF file.")

# ატვირთვა
uploaded_files = st.file_uploader("Upload Images", accept_multiple_files=True, type=["png", "jpg", "jpeg"])
pdf_name = st.text_input("Enter PDF Name (default: output.pdf)", "output.pdf")

if st.button("Convert to PDF"):
    if not uploaded_files:
        st.warning("Please upload at least one image.")
    else:
        pdf_path = pdf_name if pdf_name.endswith(".pdf") else pdf_name + ".pdf"
        c = canvas.Canvas(pdf_path, pagesize=(612, 792))

        for uploaded_file in uploaded_files:
            img = Image.open(uploaded_file)
            img_width, img_height = img.size
            scale_factor = min(540 / img_width, 720 / img_height)
            new_width = img_width * scale_factor
            new_height = img_height * scale_factor
            x = (612 - new_width) / 2
            y = (792 - new_height) / 2
            c.drawImage(uploaded_file, x, y, width=new_width, height=new_height)
            c.showPage()

        c.save()
        st.success("✅ PDF Created!")
        st.download_button("📥 Download PDF", data=open(pdf_path, "rb"), file_name=pdf_path, mime="application/pdf")
