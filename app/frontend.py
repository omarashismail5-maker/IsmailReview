import json
import streamlit as st
import hashlib

from main import classify_input
from review_engine import build_review_prompt, build_full_resume_prompt
from llm_client import generate_ai_review
from resume_parser import extract_resume_text

def clear_draft():
    st.session_state["draft_input"] = ""
    st.session_state["review"] = None
    st.session_state["review_type"] = None
    st.session_state["improved_version_input"] = ""

def clear_writing_review():
    st.session_state["review"] = None
    st.session_state["review_type"] = None
    st.session_state["improved_version_input"] = ""

st.set_page_config(
    page_title="IsmailReview",
    page_icon=None,
    layout="centered"
)

# Store the latest generated review between Streamlit reruns.
if "review" not in st.session_state:
    st.session_state["review"] = None

if "review_type" not in st.session_state:
    st.session_state["review_type"] = None

if "resume_review" not in st.session_state:
    st.session_state["resume_review"] = None

if "resume_file_hash" not in st.session_state:
    st.session_state["resume_file_hash"] = None

with st.sidebar:
    st.header("About IsmailReview")

    st.write(
        "IsmailReview provides AI-powered feedback for "
        "application writing."
    )

    st.subheader("Supported Writing Types")

    st.write(
        "- Resume bullets\n"
        "- Activity descriptions\n"
        "- Short answers\n"
        "- Essay paragraphs"
    )

    st.divider()

    st.caption(
        "Your draft is classified automatically before "
        "receiving type-specific feedback."
    )

st.title("IsmailReview")

st.caption(
    "AI-powered feedback for resumes, activity descriptions, "
    "short answers, and essay paragraphs."
)

st.subheader("Full Resume Review")

uploaded_resume = st.file_uploader(
    "Upload your resume",
    type=["pdf", "docx"],
    key="resume_upload"
)

# Reset the previous review when a different resume is uploaded.
if uploaded_resume is not None:

    current_hash = hashlib.sha256(
        uploaded_resume.getvalue()
    ).hexdigest()

    if current_hash != st.session_state["resume_file_hash"]:
        st.session_state["resume_review"] = None
        st.session_state["resume_file_hash"] = current_hash

else:
    st.session_state["resume_review"] = None
    st.session_state["resume_file_hash"] = None

if uploaded_resume is not None:
    try:
        resume_text = extract_resume_text(uploaded_resume)

        st.success(f"Successfully read: {uploaded_resume.name}")
        st.write(f"Characters extracted: {len(resume_text)}")

        with st.expander("Preview Extracted Resume Text"):
            st.text(resume_text)

        if st.button("Review Full Resume"):
            review_prompt = build_full_resume_prompt(resume_text)

            with st.spinner("Analyzing your resume..."):
                ai_review = generate_ai_review(review_prompt)

            try:
                st.session_state["resume_review"] = json.loads(ai_review)

            except json.JSONDecodeError:
                st.error(ai_review)

        # Display the saved analysis independently of the button.
        if st.session_state["resume_review"] is not None:

            review = st.session_state["resume_review"]

            st.success("Resume analysis completed!")

            st.metric(
                "Overall Resume Score",
                f'{review["score"]}/10'
            )

            st.subheader("Overall Impression")
            st.write(review["overall_impression"])

            st.subheader("Strengths")
            for strength in review["strengths"]:
                st.write(f"- {strength}")

            st.subheader("Weaknesses")
            for weakness in review["weaknesses"]:
                st.write(f"- {weakness}")

            st.subheader("Why It Matters")
            st.write(review["why_it_matters"])

            st.subheader("Suggested Improvements")
            for improvement in review["suggested_improvements"]:
                st.write(f"- {improvement}")

            st.subheader("Example Improved Bullet")
            st.write(review["improved_version"])

    except Exception as e:
        st.error(f"Unable to read resume: {e}")

st.divider()

draft = st.text_area(
    "Enter your draft:",
    height=250,
    placeholder="Paste your application writing here...",
    key="draft_input",
    on_change=clear_writing_review
)


if st.button("Review"):

    if not draft.strip():
        st.warning("Please enter a draft before requesting a review.")

    else:
        # Classify the writing.
        input_type = classify_input(draft)

        # Generate the appropriate prompt.
        review_prompt = build_review_prompt(draft, input_type)

        # Send the prompt to the LLM.
        with st.spinner("Reviewing your writing..."):
            ai_review = generate_ai_review(review_prompt)

        try:
            review = json.loads(ai_review)

            # Save the results in session state.
            st.session_state["review"] = review
            st.session_state["review_type"] = input_type
            st.session_state["improved_version_input"] = review["improved_version"]

        except json.JSONDecodeError:
            st.error(ai_review)


# Display saved feedback independently of the Review button.
if st.session_state["review"] is not None:

    review = st.session_state["review"]
    input_type = st.session_state["review_type"]

    type_col, score_col = st.columns(2)

    with type_col:
        st.metric("Detected Type", input_type)

    with score_col:
        st.metric("Current Score", f'{review["score"]}/10')

    st.subheader("Overall Impression")
    st.write(review["overall_impression"])

    st.subheader("Strengths")
    for strength in review["strengths"]:
        st.write(f"- {strength}")

    st.subheader("Weaknesses")
    for weakness in review["weaknesses"]:
        st.write(f"- {weakness}")

    st.subheader("Why It Matters")
    st.write(review["why_it_matters"])

    st.subheader("Suggested Improvements")
    for improvement in review["suggested_improvements"]:
        st.write(f"- {improvement}")

    st.subheader("Improved Version")

    st.text_area(
        "Copy or edit the improved version:",
        height=180,
        key="improved_version_input"
    )

st.button(
    "Clear Draft",
    on_click=clear_draft
)