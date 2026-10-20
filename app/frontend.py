import json
import streamlit as st

from main import classify_input
from review_engine import build_review_prompt
from llm_client import generate_ai_review


st.title("IsmailReview")

st.write(
    "AI-powered feedback for resumes, activity descriptions, "
    "short answers, and essay paragraphs."
)

draft = st.text_area(
    "Enter your draft:",
    height=250,
    placeholder="Paste your application writing here..."
)


if st.button("Review"):

    if not draft.strip():
        st.warning("Please enter a draft before requesting a review.")

    else:
        # Determine what kind of writing the user submitted.
        input_type = classify_input(draft)

        st.write(f"**Detected Type:** {input_type}")

        # Build the appropriate type-specific review prompt.
        review_prompt = build_review_prompt(draft, input_type)

        # Send the prompt to the LLM.
        with st.spinner("Reviewing your writing..."):
            ai_review = generate_ai_review(review_prompt)

        try:
            review = json.loads(ai_review)

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
            st.write(review["improved_version"])

            st.subheader("Score")
            st.write(f'{review["score"]}/10')

        except json.JSONDecodeError:
            st.error(ai_review)