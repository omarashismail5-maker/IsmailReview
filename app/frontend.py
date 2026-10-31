import json
import streamlit as st

from main import classify_input
from review_engine import build_review_prompt
from llm_client import generate_ai_review

def clear_draft():
    st.session_state["draft_input"] = ""

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

draft = st.text_area(
    "Enter your draft:",
    height=250,
    placeholder="Paste your application writing here...",
    key="draft_input"
)


if st.button("Review"):

    if not draft.strip():
        st.warning("Please enter a draft before requesting a review.")

    else:
        # Determine what kind of writing the user submitted.
        input_type = classify_input(draft)

        # Build the appropriate type-specific review prompt.
        review_prompt = build_review_prompt(draft, input_type)

        # Send the prompt to the LLM.
        with st.spinner("Reviewing your writing..."):
            ai_review = generate_ai_review(review_prompt)

        try:
            review = json.loads(ai_review)
            # Save the review so it remains available after reruns.
            st.session_state["review"] = review
            st.session_state["review_type"] = input_type
            st.session_state["improved_version_input"] = review["improved_version"]
            type_col, score_col = st.columns(2)

            with type_col:
                st.metric(
                    label="Detected Type",
                    value=input_type
                )

            with score_col:
                st.metric(
                    label="Current Score",
                    value=f'{review["score"]}/10'
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

            st.subheader("Improved Version")

            st.text_area(
                "Copy or edit the improved version:",
                value=review["improved_version"],
                height=180
            )

        except json.JSONDecodeError:
            st.error(ai_review)

st.button(
    "Clear Draft",
    on_click=clear_draft
)