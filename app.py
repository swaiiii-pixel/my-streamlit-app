import streamlit as st
import matplotlib.pyplot as plt

st.title("📄 Resume Skill Extractor")

resume = st.text_area("Paste Resume")
job = st.text_area("Paste Job Description")

if st.button("Analyze"):

    matched = 3
    missing = 2

    st.write("Matched Skills:", matched)
    st.write("Missing Skills:", missing)

    # Bar Chart
    fig, ax = plt.subplots()
    ax.bar(["Matched", "Missing"], [matched, missing])
    st.pyplot(fig)

    # Pie Chart
    fig2, ax2 = plt.subplots()
    ax2.pie([matched, missing], labels=["Matched", "Missing"], autopct='%1.1f%%')
    st.pyplot(fig2)