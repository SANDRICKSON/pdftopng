import streamlit as st
from PIL import Image
from reportlab.pdfgen import canvas
import os

# Streamlit გვერდის კონფიგურაცია
st.set_page_config(page_title="Image to PDF Converter", page_icon="📄")

st.title("🖼️ Image to PDF Converter")
st.write("Upload images and convert them into a PDF file.")

# სურათების ატვირთვა
uploaded_files = st.file_uploader("Upload Images", accept_multiple_files=True, type=["png", "jpg", "jpeg"])

# PDF-ის სახელი
pdf_name = st.text_input("Enter PDF Name (default: output.pdf)", "output.pdf")

# PDF კონვერტაციის ღილაკი
if st.button("Convert to PDF"):
    if not uploaded_files:
        st.warning("⚠️ Please upload at least one image.")
    else:
        pdf_path = pdf_name if pdf_name.endswith(".pdf") else pdf_name + ".pdf"
        c = canvas.Canvas(pdf_path, pagesize=(612, 792))

        for uploaded_file in uploaded_files:
            img = Image.open(uploaded_file)

            # გამოსახულების ზომის რეგულირება
            img_width, img_height = img.size
            scale_factor = min(540 / img_width, 720 / img_height)
            new_width = img_width * scale_factor
            new_height = img_height * scale_factor
            x = (612 - new_width) / 2
            y = (792 - new_height) / 2

            # სურათის დროებითი შენახვა
            temp_img_path = "temp_image.jpg"
            img.convert("RGB").save(temp_img_path)

            # PDF-ში ჩასმა
            c.drawImage(temp_img_path, x, y, width=new_width, height=new_height)
            c.showPage()

            # დროებითი ფაილის წაშლა
            os.remove(temp_img_path)

        c.save()

        # PDF-ის ჩამოტვირთვის ღილაკი
        with open(pdf_path, "rb") as f:
            st.download_button("📥 Download PDF", f, file_name=pdf_path, mime="application/pdf")

        # დროებითი PDF ფაილის წაშლა
        os.remove(pdf_path)

        st.success("✅ PDF Created Successfully!")
