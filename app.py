import streamlit as st
import PyPDF2
import matplotlib.pyplot as plt

# -------- Extract text --------
def extract_text_from_pdf(uploaded_file):
    text = ""
    reader = PyPDF2.PdfReader(uploaded_file)

    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()

    return text.lower()


# -------- UI Design --------
st.set_page_config(page_title="AI Resume Analyzer", layout="centered")

st.title("🚀 AI Resume Analyzer")
st.markdown("### Upload your resume and check your job readiness 💼")

uploaded_file = st.file_uploader("📄 Upload Resume (PDF)", type=["pdf"])


# -------- Skills --------
skills = [
    "python", "java", "sql", "excel",
    "communication", "teamwork",
    "cloud", "data analysis"
]

# -------- Load job description --------
job_desc_text = ""
try:
    with open("job_description.txt", "r") as file:
        job_desc_text = file.read().lower()
except:
    st.warning("⚠️ Job description file not found")


# -------- Analyze --------
if uploaded_file is not None:
    if st.button("🔍 Analyze Resume"):

        resume_text = extract_text_from_pdf(uploaded_file)

        found = []
        missing = []

        for skill in skills:
            if skill in resume_text:
                found.append(skill)
            else:
                missing.append(skill)

        # -------- Score --------
        score = len(found)
        total = len(skills)
        percentage = int((score / total) * 100)

        # -------- Display Results --------
        st.subheader("📊 Resume Score")
        st.progress(percentage)
        st.write(f"**Score:** {score}/{total} ({percentage}%)")

        st.subheader("✅ Found Skills")
        st.success(", ".join(found) if found else "None")

        st.subheader("❌ Missing Skills")
        st.error(", ".join(missing) if missing else "None")

        # -------- Job Matching --------
        st.subheader("🎯 Job Match")

        match = 0
        for skill in skills:
            if skill in resume_text and skill in job_desc_text:
                match += 1

        match_percentage = int((match / total) * 100)

        st.progress(match_percentage)
        st.write(f"Match Score: {match}/{total} ({match_percentage}%)")

        # -------- Chart --------
        st.subheader("📈 Skill Distribution")

        labels = ["Found", "Missing"]
        values = [len(found), len(missing)]

        fig, ax = plt.subplots()
        ax.pie(values, labels=labels, autopct='%1.1f%%')
        st.pyplot(fig)

        # -------- Final Feedback --------
        st.subheader("💡 Feedback")

        if percentage >= 75:
            st.success("🔥 Excellent Resume! You're job ready.")
        elif percentage >= 40:
            st.info("👍 Good Resume, but can improve.")
        else:
            st.warning("⚠️ Improve your resume by adding more skills.")