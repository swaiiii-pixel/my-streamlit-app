import streamlit as st
from collections import Counter
import re
import pandas as pd

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
h2, h3 { color: #A67B5B; }
textarea {
    background-color: #fffaf0 !important;
    color: #333 !important;
    border-radius: 10px !important;
}
button {
    background-color: #d2b48c !important;
    color: black !important;
    border-radius: 12px !important;
    font-size: 18px !important;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ------------------ TITLE ------------------
st.title("📄 Resume Skill Extractor")
st.write("Analyze your resume and match it with job requirements.")

# ------------------ INPUT ------------------
resume_text = st.text_area("📄 Paste Resume Text Here")
job_desc = st.text_area("💼 Paste Job Description Here")

# ------------------ SKILLS ------------------
skills_list = [
    "python", "java", "c", "c++", "html", "css", "javascript",
    "sql", "machine learning", "data analysis", "excel",
    "communication", "teamwork", "leadership"
]

# ------------------ BUTTON ------------------
if st.button("🔍 Analyze Resume"):

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

    # ------------------ SIMPLE VISUAL (NO PLOTLY) ------------------
    st.subheader("📊 Skill Comparison")

    chart_data = pd.DataFrame({
        "Matched": [len(matched)],
        "Missing": [len(missing)]
    })

    st.bar_chart(chart_data)

    # ------------------ WORD FREQUENCY ------------------
    st.subheader("📈 Resume Word Frequency")

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