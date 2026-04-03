import streamlit as st
import matplotlib.pyplot as plt
from collections import Counter
import re

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Resume Skill Extractor", layout="centered")

# ------------------ BEIGE BACKGROUND STYLE ------------------
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #f5f5dc, #e8d8c3, #d6c1a3);
    color: #333;
}

[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}

h1 {
    text-align: center;
    color: #8B7355;
    font-size: 50px;
}

h2, h3 {
    color: #A67B5B;
}

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
st.subheader("📥 Input Section")

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
    fig, ax = plt.subplots()
    ax.bar(["Matched", "Missing"], [len(matched), len(missing)])
    ax.set_title("Skill Comparison")
    st.pyplot(fig)

    # ------------------ PIE CHART ------------------
    fig2, ax2 = plt.subplots()
    ax2.pie(
        [len(matched), len(missing)],
        labels=["Matched", "Missing"],
        autopct='%1.1f%%',
        startangle=90,
        colors=["#c2a383", "#8b5e3c"]
    )
    ax2.axis('equal')
    st.pyplot(fig2)

    # ------------------ WORD FREQUENCY ------------------
    st.subheader("📈 Resume Word Frequency")

    words = re.findall(r'\w+', resume)
    common_words = Counter(words).most_common(5)

    if common_words:
        w, c = zip(*common_words)
        fig3, ax3 = plt.subplots()
        ax3.bar(w, c)
        ax3.set_title("Top Words in Resume")
        st.pyplot(fig3)

    st.success("✅ Analysis Complete!")