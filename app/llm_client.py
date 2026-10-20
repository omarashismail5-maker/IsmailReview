import os

from openai import (
    OpenAI,
    APIConnectionError,
    AuthenticationError,
    RateLimitError,
    APIStatusError,
)


def generate_ai_review(prompt):

    if not os.getenv("OPENAI_API_KEY"):
        return (
            "IsmailReview could not connect to the AI service because "
            "the OpenAI API key is not set."
        )

    try:
        client = OpenAI()

        response = client.responses.create(
            model="gpt-5.6",
            input=prompt,
            text={
                "format": {
                    "type": "json_schema",
                    "name": "ismail_review",
                    "strict": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "overall_impression": {"type": "string"},
                            "strengths": {
                                "type": "array",
                                "items": {"type": "string"}
                            },
                            "weaknesses": {
                                "type": "array",
                                "items": {"type": "string"}
                            },
                            "why_it_matters": {"type": "string"},
                            "suggested_improvements": {
                                "type": "array",
                                "items": {"type": "string"}
                            },
                            "improved_version": {"type": "string"},
                            "score": {"type": "integer"}
                        },
                        "required": [
                            "overall_impression",
                            "strengths",
                            "weaknesses",
                            "why_it_matters",
                            "suggested_improvements",
                            "improved_version",
                            "score"
                        ],
                        "additionalProperties": False
                    }
                }
            }
        )

        return response.output_text

    except AuthenticationError:
        return (
            "IsmailReview could not authenticate with the OpenAI API. "
            "Please check the API key."
        )

    except RateLimitError:
        return (
            "IsmailReview could not generate a review because the "
            "API rate limit or quota was reached."
        )

    except APIConnectionError:
        return (
            "IsmailReview could not connect to the OpenAI API. "
            "Please check your internet connection and try again."
        )

    except APIStatusError as error:
        return (
            f"IsmailReview received an API error "
            f"(status code {error.status_code})."
        )