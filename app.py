import streamlit as st
import plotly.express as px
import pandas as pd

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Resume Skill Extractor", layout="centered")

# ------------------ BEIGE BACKGROUND STYLE ------------------
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #f5f5dc, #e8d8c3, #d6c1a3);
    color: #333;
}
</style>
""", unsafe_allow_html=True)

# ------------------ TITLE ------------------
st.title("📄 Resume Skill Extractor")
st.write("Analyze your resume and match it with job requirements.")

# ------------------ INPUT ------------------
resume_text = st.text_area("📄 Paste Resume Text Here")
job_desc = st.text_area("💼 Paste Job Description Here")

# ------------------ SKILL LIST ------------------
skills_list = [
    "python", "java", "c", "c++", "html", "css", "javascript",
    "sql", "machine learning", "data analysis", "excel",
    "communication", "teamwork", "leadership"
]

# ------------------ BUTTON ------------------
if st.button("🔍 Analyze Resume"):

    if not resume_text or not job_desc:
        st.warning("⚠️ Please fill both fields")
        st.stop()

    resume = resume_text.lower()
    job = job_desc.lower()

    resume_skills = [s for s in skills_list if s in resume]
    job_skills = [s for s in skills_list if s in job]

    matched = list(set(resume_skills) & set(job_skills))
    missing = list(set(job_skills) - set(resume_skills))

    score = int((len(matched) / len(job_skills)) * 100) if job_skills else 0

    # ------------------ RESULTS ------------------
    st.header("📊 Results")

    st.write("✅ Matched Skills:", matched)
    st.write("❌ Missing Skills:", missing)
    st.write(f"📈 Match Score: {score}%")

    st.progress(score / 100)

    # ------------------ PIE CHART ------------------
    df = pd.DataFrame({
        "Type": ["Matched", "Missing"],
        "Count": [len(matched), len(missing)]
    })

    fig = px.pie(df, names="Type", values="Count", hole=0.4)
    st.plotly_chart(fig)

    st.success("✅ Done!")