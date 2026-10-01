
import sys
from pathlib import Path

import streamlit as st


# Add project directories to Python path
PROJECT_ROOT = Path(__file__).resolve().parent
SRC_DIR = PROJECT_ROOT / "src"

sys.path.append(str(PROJECT_ROOT))
sys.path.append(str(SRC_DIR))


from resume_parser import extract_text_from_pdf
from job_description import read_job_description
from analyzer import analyze_resume
from scorer import calculate_weighted_match_score


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)


# --------------------------------------------------
# Application Header
# --------------------------------------------------

st.title("📄 AI Resume Analyzer")

st.write(
    "Analyze how well a resume aligns with a target job description "
    "using Generative AI."
)


# --------------------------------------------------
# File Uploaders
# --------------------------------------------------

resume_file = st.file_uploader(
    "Upload Resume",
    type=["pdf"]
)

job_file = st.file_uploader(
    "Upload Job Description",
    type=["docx"]
)


# --------------------------------------------------
# Analyze Button
# --------------------------------------------------

if st.button("🔍 Analyze Resume"):

    if resume_file is None:
        st.warning("Please upload a resume PDF.")

    elif job_file is None:
        st.warning("Please upload a job description DOCX.")

    else:

        with st.spinner("Analyzing resume against job description..."):

            # Save uploaded files temporarily
            import tempfile
            import os

            resume_temp = tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".pdf"
            )

            resume_temp.write(resume_file.getvalue())
            resume_temp.close()

            job_temp = tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".docx"
            )

            job_temp.write(job_file.getvalue())
            job_temp.close()

            try:

                # ------------------------------------------
                # Extract Resume Text
                # ------------------------------------------

                resume_text = extract_text_from_pdf(
                    resume_temp.name
                )

                # ------------------------------------------
                # Extract Job Description
                # ------------------------------------------

                job_description = read_job_description(
                    job_temp.name
                )

                # ------------------------------------------
                # LLM Analysis
                # ------------------------------------------

                analysis = analyze_resume(
                    resume_text,
                    job_description
                )

                # ------------------------------------------
                # Calculate Score
                # ------------------------------------------

                score_result = calculate_weighted_match_score(
                    analysis.requirement_analysis
                )

            finally:

                os.unlink(resume_temp.name)
                os.unlink(job_temp.name)


        # --------------------------------------------------
        # Match Score
        # --------------------------------------------------

        st.subheader("📊 Resume Match Score")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Weighted Match Score",
                f"{score_result['score']}%"
            )

        with col2:
            st.metric(
                "Matched",
                score_result["matched"]
            )

        with col3:
            st.metric(
                "Missing",
                score_result["missing"]
            )


        # --------------------------------------------------
        # Requirement Analysis
        # --------------------------------------------------

        st.subheader("📋 Requirement Analysis")

        for item in analysis.requirement_analysis:

            if item.status == "matched":
                status = "🟢 Matched"

            elif item.status == "partial":
                status = "🟡 Partial"

            else:
                status = "🔴 Missing"

            with st.expander(
                f"{status} — {item.requirement}"
            ):

                st.write(
                    f"**Evidence:** {item.evidence}"
                )


        # --------------------------------------------------
        # Relevant Experience
        # --------------------------------------------------

        st.subheader("💼 Relevant Experience")

        for item in analysis.relevant_experience:
            st.write(f"• {item}")


        # --------------------------------------------------
        # Experience Gaps
        # --------------------------------------------------

        st.subheader("⚠️ Experience Gaps")

        for item in analysis.experience_gaps:
            st.write(f"• {item}")


        # --------------------------------------------------
        # Strengths
        # --------------------------------------------------

        st.subheader("💪 Strengths")

        for item in analysis.strengths:
            st.write(f"• {item}")


        # --------------------------------------------------
        # Gaps
        # --------------------------------------------------

        st.subheader("🔎 Gaps")

        for item in analysis.gaps:
            st.write(f"• {item}")


        # --------------------------------------------------
        # Overall Assessment
        # --------------------------------------------------

        st.subheader("📝 Overall Assessment")

        st.write(
            analysis.overall_assessment
        )