from review_engine import build_review_prompt

# Tests whether build_review_prompt correctly handles a resume bullet.
def test_resume_bullet():
    draft = "Helped fix machines and respond to questions."
    input_type = "Resume bullet"

    prompt = build_review_prompt(draft, input_type)

    assert draft in prompt
    assert input_type in prompt
    assert "Overall Impression" in prompt
    assert "Strengths" in prompt
    assert "Weaknesses" in prompt
    assert "Suggested Improvements" in prompt
    assert "Improved Version" in prompt
    assert "Score" in prompt

# Tests whether build_review_prompt correctly handles an activity description.
def test_activity_description():
    draft = "Played intramural volleyball."
    input_type = "Activity description"

    prompt = build_review_prompt(draft, input_type)

    assert draft in prompt
    assert input_type in prompt


# Tests whether build_review_prompt correctly handles a short answer.
def test_short_answer():
    draft = "I would like to join this program because it matches my interests."
    input_type = "Short answer"

    prompt = build_review_prompt(draft, input_type)

    assert draft in prompt
    assert input_type in prompt

# Tests whether build_review_prompt correctly handles an essay paragraph.
def test_essay_paragraph():
    draft = "Rock climbing taught me how to stay calm under pressure, recover from setbacks, and trust the people around me."
    input_type = "Essay paragraph"

    prompt = build_review_prompt(draft, input_type)

    assert draft in prompt
    assert input_type in prompt


# Tests whether build_review_prompt correctly handles unknown input.
def test_unknown():
    draft = "A bunch of nothing."
    input_type = "Unknown"

    prompt = build_review_prompt(draft, input_type)

    assert draft in prompt
    assert input_type in prompt

# Tests to make sure the review prompt stucture is accurate
def test_review_prompt_structure():
    draft = "Sample application writing."
    input_type = "Unknown"

    prompt = build_review_prompt(draft, input_type)

    required_sections = [
        "Overall Impression",
        "Strengths",
        "Weaknesses",
        "Why It Matters",
        "Suggested Improvements",
        "Improved Version",
        "Score"
    ]

    for section in required_sections:
        assert section in prompt

    assert "Preserve the writer's meaning and voice" in prompt