from main import classify_input

# Tests whether classify_input correctly identifies a resume bullet input type.
def test_resume_bullet_classification():
    draft = "Helped fix machines and respond to questions."

    result = classify_input(draft)

    assert result == "Resume bullet"


# Tests whether classify_input correctly identifies an activity description input type.
def test_activity_description_classification():
    draft = "Played intramural volleyball."

    result = classify_input(draft)

    assert result == "Activity description"


# Tests whether classify_input correctly identifies a short answer input type.
def test_short_answer_classification():
    draft = "I would like to join this program because it matches my interests."

    result = classify_input(draft)

    assert result == "Short answer"

# Tests whether classify_input correctly identifies an essay paragraph input type.
def test_essay_paragraph_classification():
    draft = (
        "Rock climbing has taught me how to remain calm under pressure, communicate "
        "with others, recover from setbacks, and continue improving even when progress "
        "feels slow. Through training and working with other climbers, I have developed "
        "greater confidence, patience, and responsibility while learning how important "
        "trust and teamwork are in challenging situations."
    )

    result = classify_input(draft)

    assert result == "Essay paragraph"


# Tests whether classify_input correctly identifies unknown input types.
def test_unknown_classification():
    draft = "A bunch of nothing."

    result = classify_input(draft)

    assert result == "Unknown"