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
    """
    Build a structured prompt for reviewing a draft.

    Args:
        draft: the user's orginal piece of writing
        input_type: The category of the piece of work returned by the classifier.
    
    Returns:
        A formatted review prompt.

    Raises:
        ValueError: If the draft or input type is empty.
    """

    cleaned_draft = draft.strip()
    cleaned_input_type = input_type.strip()

    if not cleaned_draft:
        raise ValueError("Draft cannot be empty.")
    
    if not cleaned_input_type:
        raise ValueError("Input type cannot be empty.")

    sections = "\n".join(
        f"{index}. {section}"
        for index, section in enumerate(REVIEW_SECTIONS, start=1)
    )

    return (
        "You are IsmailReview, an application-writing reviewer.\n\n"
        f"Input Type: {cleaned_input_type}\n\n"
        "Review the following draft:\n"
        f'"""\n{cleaned_draft}\n"""\n\n'
        "Provide feedback using these sections:\n"
        f"{sections}\n\n"
        "Give specific, constructive feedback. Preserve the writer's "
        "meaning and voice when creating the improved version."
    )

if __name__ == "__main__":
    sample_draft = (
        "I really like working at my college gym because it is fun "
        "and I enjoy helping people."
    )

    prompt = build_review_prompt(sample_draft, "essay")
    print(prompt)