import os

from llm_client import generate_ai_review


def test_missing_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    result = generate_ai_review("Test prompt")

    assert "API key is not set" in result


import llm_client


def test_rate_limit_error(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")

    class FakeRateLimitError(Exception):
        pass

    class FakeResponses:
        def create(self, model, input, **kwargs):
            raise FakeRateLimitError()

    class FakeOpenAI:
        def __init__(self):
            self.responses = FakeResponses()

    monkeypatch.setattr(llm_client, "RateLimitError", FakeRateLimitError)
    monkeypatch.setattr(llm_client, "OpenAI", FakeOpenAI)

    result = llm_client.generate_ai_review("Test prompt")

    assert "rate limit or quota was reached" in result

def test_api_connection_error(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")

    class FakeConnectionError(Exception):
        pass

    class FakeResponses:
        def create(self, model, input, **kwargs):
            raise FakeConnectionError()

    class FakeOpenAI:
        def __init__(self):
            self.responses = FakeResponses()

    monkeypatch.setattr(
        llm_client,
        "APIConnectionError",
        FakeConnectionError
    )

    monkeypatch.setattr(
        llm_client,
        "OpenAI",
        FakeOpenAI
    )

    result = llm_client.generate_ai_review("Test prompt")

    assert "could not connect to the OpenAI API" in result