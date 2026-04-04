import streamlit as st
from collections import Counter
import re
import pandas as pd
import json
from lxml import etree

# File handling
import PyPDF2
from docx import Document
import pytesseract
from PIL import Image

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Resume Skill Extractor", layout="centered")

# ------------------ STYLE ------------------
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #f5f5dc, #e8d8c3, #d6c1a3);
    color: #333;
}
h1 { text-align: center; color: #8B7355; font-size: 50px; }
</style>
""", unsafe_allow_html=True)

# ------------------ TITLE ------------------
st.title("📄 Resume Skill Extractor")

# ------------------ FILE UPLOAD ------------------
uploaded_file = st.file_uploader("📂 Upload Resume (PDF, DOCX, Image)", 
                                type=["pdf", "docx", "png", "jpg", "jpeg"])

job_desc = st.text_area("💼 Paste Job Description Here")

# ------------------ TEXT EXTRACTION FUNCTIONS ------------------

def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def extract_text_from_docx(file):
    doc = Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text_from_image(file):
    image = Image.open(file)
    return pytesseract.image_to_string(image)

# ------------------ CONVERT TO JSON ------------------
def text_to_json(text):
    return json.dumps({"resume_text": text}, indent=4)

# ------------------ CONVERT TO XML ------------------
def text_to_xml(text):
    root = etree.Element("resume")
    content = etree.SubElement(root, "text")
    content.text = text
    return etree.tostring(root, pretty_print=True).decode()

# ------------------ SKILLS ------------------
skills_list = [
    "python", "java", "c", "c++", "html", "css", "javascript",
    "sql", "machine learning", "data analysis", "excel",
    "communication", "teamwork", "leadership"
]

# ------------------ PROCESS FILE ------------------
resume_text = ""

if uploaded_file:
    file_type = uploaded_file.type

    if "pdf" in file_type:
        resume_text = extract_text_from_pdf(uploaded_file)

    elif "word" in file_type or "docx" in file_type:
        resume_text = extract_text_from_docx(uploaded_file)

    elif "image" in file_type:
        resume_text = extract_text_from_image(uploaded_file)

    st.success("✅ File processed successfully!")

    # Show extracted text (optional)
    with st.expander("📄 Extracted Text"):
        st.write(resume_text)

    # JSON + XML
    st.subheader("🔄 Converted Formats")

    json_data = text_to_json(resume_text)
    xml_data = text_to_xml(resume_text)

    st.download_button("⬇ Download JSON", json_data, "resume.json")
    st.download_button("⬇ Download XML", xml_data, "resume.xml")

# ------------------ ANALYSIS ------------------
if st.button("🔍 Analyze Resume") and resume_text and job_desc:

    resume = resume_text.lower()
    job = job_desc.lower()

    resume_skills = [s for s in skills_list if s in resume]
    job_skills = [s for s in skills_list if s in job]

    matched = list(set(resume_skills) & set(job_skills))
    missing = list(set(job_skills) - set(resume_skills))

    score = int((len(matched) / len(job_skills)) * 100) if job_skills else 0

    # ------------------ RESULTS ------------------
    st.header("📊 Results")

    st.subheader("✅ Matched Skills")
    st.write(matched if matched else "No matches found")

    st.subheader("❌ Missing Skills")
    st.write(missing if missing else "No missing skills")

    st.subheader("📈 Match Score")
    st.progress(score / 100)
    st.write(f"{score}% match")

    # ------------------ BAR CHART ------------------
    chart_data = pd.DataFrame({
        "Matched": [len(matched)],
        "Missing": [len(missing)]
    })
    st.bar_chart(chart_data)

    # ------------------ WORD FREQUENCY ------------------
    words = re.findall(r'\w+', resume)
    common_words = Counter(words).most_common(5)

    if common_words:
        w, c = zip(*common_words)

        df = pd.DataFrame({
            "Words": w,
            "Count": c
        }).set_index("Words")

        st.bar_chart(df)

    st.success("✅ Analysis Complete!")