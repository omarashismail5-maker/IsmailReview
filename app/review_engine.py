"""Functions for constructing the IsmailReview feedback reqiests."""

REVIEW_SECTIONS = [
    "Overall Impression",
    "Strengths",
    "Weaknesses",
    "Why It Matters",
    "Suggested Improvements",
    "Improved Version",
    "Score",
]

def build_review_prompt(draft: str, input_type: str) -> str:
    type_guidance = {
        "Resume bullet": """
Focus especially on:
- Strong action verbs
- Specific responsibilities
- Measurable impact or results
- Professional wording
- Conciseness
""",

        "Activity description": """
Focus especially on:
- The writer's role in the activity
- Skills demonstrated
- Leadership or initiative
- Contribution and impact
- Clear, concise wording
""",

        "Short answer": """
Focus especially on:
- Clear motivation
- Specific supporting examples
- Connection between experience and the opportunity
- Avoiding vague claims
- Directly answering the question
""",

        "Essay paragraph": """
Focus especially on:
- Storytelling and reflection
- Specific details
- Personal voice
- Growth or significance
- Sentence flow and clarity
""",

        "Unknown": """
Focus on identifying what context or information is missing before making major revisions.
"""
    }

    guidance = type_guidance.get(
        input_type,
        type_guidance["Unknown"]
    )

    prompt = f"""
You are IsmailReview, an application-writing reviewer.

Input Type: {input_type}

Review this draft:
\"\"\"
{draft}
\"\"\"

{guidance}

Provide feedback using these sections:
1. Overall Impression
2. Strengths
3. Weaknesses
4. Why It Matters
5. Suggested Improvements
6. Improved Version
7. Score

Give specific, constructive feedback.
Preserve the writer's meaning and voice when creating the improved version.
"""

    return prompt
    

if __name__ == "__main__":
    sample_draft = (
        "I really like working at my college gym because it is fun "
        "and I enjoy helping people."
    )

    prompt = build_review_prompt(sample_draft, "Essay paragraph")
    print(prompt)