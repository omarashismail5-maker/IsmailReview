def classify_input(draft):

    draft_lower = draft.lower()
    word_count = len(draft.split())

    # Resumes typically starts with some kind of verb, here are some common ones, though not exhaustive.
    resume_starters = [
        "helped", "served", "led", "lead", "managed", "created", "developed",
        "organized", "assisted", "improved", "trained", "built", "designed"
    ]

    for starter in resume_starters:
        if draft_lower.startswith(starter):
            return "Resume bullet"

    # Some common key words used when describing an organization or activity.
    activity_keywords = [
        "played", "participated", "club", "team", "volunteer",
        "intramural", "competition", "member", "practice"
    ]

    for keyword in activity_keywords:
        if keyword in draft_lower and word_count <= 25:
            return "Activity description"

    # Short answers are less about experience, and more about why the applicant wants the position.
    short_answer_keywords = [
        "i would like", "i want", "i believe", "because",
        "this program", "this position", "opportunity"
    ]

    for keyword in short_answer_keywords:
        if keyword in draft_lower and word_count <= 80:
            return "Short answer"

    # Essay paragraphs are usually longer, so if we see a long word count, it might be safe to assume it is an essay..
    if word_count > 40:
        return "Essay paragraph"

    # Everything else is something unknown to the model, so we classify all of those under "Unknown"
    return "Unknown"

# Simple rule-based algorithm that finds common writing issues in the user's draft and provides an explanation of what's wrong.
def common_issues(draft):

    draft_lower = draft.lower()
    word_count = len(draft.split())

    issues = []

    vague_words = [
        "things", "stuff", "a lot", "some time", "very", "really",
        "good", "great", "helped", "nice", "many"
    ]

    for word in vague_words:
        if word in draft_lower:
            issues.append(f"The draft may use vague wording: '{word}'.")

        if word_count < 8:
            issues.append("The draft may be too short to show meaningful detail.")

        if "impact" not in draft_lower and "improved" not in draft_lower and "developed" not in draft_lower:
            issues.append("The draft may need a clearer impact, result, or growth statement.")

        if len(issues) == 0:
            issues.append("No major basic issues detected by the rule-based checker.")

        return issues


# Generates a basic review for the user's draft. It doesn't use AI just
# yet, but will use the input type to provide some feedback
def generate_review(draft, input_type):
    if input_type == "Activity description":
        return """
        Overall Feedback:
        This draft mentions an activity, though it requires some more detail to show
        skill, experience, and impact.

        Strengths:
        - Clearly identifies an activity.
        - Activity is clear and concise.

        Weaknesses:
        - The impact the activity had is not emphasized enough.
        - The activity mentioned doesn't explain or identify what you did.
        - It could definitely show more skills, growth, leadership, and impact.

        Why this is important:
        Whoever is reading your application does not just want to know what activities you participated in,
        but they also want to know why that activity is important to you, why you chose to do it, 
        and how your participation in that activity is impactful.

        Suggested Improvements:
        - Describe the activity in more detail, making sure to not make it too lengthy.
        - Clearly explain your role in that activity and how your work mattered.
        - Explain how this activity was impactful in some way.

        Revised Version:
        Participated in intramural volleyball, developing teamwork, communication, and discipline through regular practices and competitive games.

        Current Score:
        4/10

        Revised Version Score:
        9/10
        """

    elif input_type == "Resume bullet":
        return """
        Overall Feedback:
        This draft mentions a resume bullet, however, it needs stronger action and needs to be more specific.

        Strengths:
        - Begins with a verb.
        - Points to contribution.

        Weaknesses:
        - The current wording is too general.
        - Does not completely define or identify the impact of this bullet.
        - Could sound more professional.

        Why this is important:
        When reading resumes, the reader needs to know what you've done, but also why that was important, and how your contributions
        were significant. At the same time, a bullet point should remain as a sentence. Anything longer than that is practically a 
        short answer, which the reader might not want to fully read, causing some information to be lost.

        Suggested Improvements:
        - Use a strong action verb
        - Clarify the task and properly mention how you demonstrated responsibility and initiative.
        - Keep your point clear and concise.

        Revised Version:
        Assisted with equipment maintenance and responded to member questions to support a safe, organized, and welcoming environment.

        Current Score:
        5/10

        Revised Version Score:
        9/10
        """
    elif input_type == "Short answer":
        return """
        Overall Feedback:
        This draft is a short answer and explains the your interest in the position, though it could emphasize your reasons for applying,
        demonstrate knowledge in the field and the company this position is under, and also include some previous experience that may be
        worth mentioning.

        Strengths:
        - Communicates interest in the position.
        - Shows confidence and enthusiasm.

        Weaknesses:
        - Claims are broad.
        - Does not include a specific example.
        - Needs to connect experience to the position.

        Why this is important:
        Short answers need to be specific because application readers want evidence, not just general traits.

        Suggested Improvements:
        - Mention at least one relevant experience.
        - Connect that experience to the position.
        - Replace broad traits with concrete examples.

        Revised Version:
        I would like to join this program because it would allow me to apply my experience in leadership, communication, and problem-solving. Through my previous roles, I have learned how to support others, stay calm under pressure, and contribute to a positive team environment.

        Current Score:
        5/10

        Revised Version Score:
        9/10
        """

    elif input_type == "Essay paragraph":
        return """
        Overall Impression:
        This draft appears to be an essay paragraph with a personal idea or experience, but it may need clearer development.

        Strengths:
        - It gives the reader a personal topic.
        - It has room for reflection and storytelling.

        Weaknesses:
        - The main idea may need to be clearer.
        - Some details may be vague or underdeveloped.
        - The paragraph may need smoother flow.

        Why It Matters:
        Essay paragraphs should help the reader understand the student's personality, growth, values, or experiences.

        Suggested Improvements:
        - Clarify the main idea.
        - Add specific examples.
        - Explain why the experience matters.
        - Improve sentence flow and grammar.

        Improved Version:
        This essay could be improved by focusing on one specific experience, explaining what happened, and reflecting on why it shaped the student.

        Score:
        6/10
        """

    else:
        return """
        Overall Impression:
        The draft does not clearly fit one of the supported IsmailReview input types.

        Strengths:
        - There may be an idea present, but it needs more context.

        Weaknesses:
        - The purpose of the draft is unclear.
        - It does not provide enough information for a focused review.

        Why It Matters:
        IsmailReview works best when the writing has a clear purpose, such as an essay paragraph, activity description, resume bullet, or short answer.

        Suggested Improvements:
        - Clarify what type of application writing this is.
        - Add more context or detail.
        - Make the main point easier to identify.

        Improved Version:
        Please provide more context so this draft can be improved for a specific application purpose.

        Score:
        2/10
        """



def main():
    print("Welcome to IsmailReview.")
    print("Paste a draft below, and IsmailReview will classify it.")
    print()

    draft = input("Draft: ")

    input_type = classify_input(draft)
    issues = common_issues(draft)
    review = generate_review(draft, input_type)

    print()
    print("You submitted:")
    print(draft)
    print()
    print(f"Input Type: {input_type}")
    print()

    print("Detected Issues:")
    for issue in issues:
        print(f"- {issue}")

    print()
    print(review)


if __name__ == "__main__":
    main()