
from io import BytesIO

import pytest
from docx import Document

import resume_parser
from resume_parser import extract_resume_text


def test_docx_extraction():
    # Create a sample Word resume in memory.
    document = Document()
    document.add_paragraph("Jane Doe")
    document.add_paragraph("Software Engineering Intern")

    table = document.add_table(rows=1, cols=2)
    table.cell(0, 0).text = "Python"
    table.cell(0, 1).text = "SQL"

    uploaded_file = BytesIO()
    document.save(uploaded_file)
    uploaded_file.name = "resume.docx"

    # Verify that paragraphs and tables are extracted.
    text = extract_resume_text(uploaded_file)

    assert "Jane Doe" in text
    assert "Software Engineering Intern" in text
    assert "Python" in text
    assert "SQL" in text


def test_pdf_extraction(monkeypatch):
    # Simulate a two-page PDF without needing a real file.
    class FakePage:
        def __init__(self, text):
            self.text = text

        def extract_text(self):
            return self.text

    class FakeReader:
        def __init__(self, uploaded_file):
            self.pages = [
                FakePage("Jane Doe"),
                FakePage("Developed Python applications")
            ]

    monkeypatch.setattr(resume_parser, "PdfReader", FakeReader)

    uploaded_file = BytesIO(b"sample pdf")
    uploaded_file.name = "resume.pdf"

    text = extract_resume_text(uploaded_file)

    assert "Jane Doe" in text
    assert "Developed Python applications" in text


def test_empty_resume():
    # An empty Word document should raise an error.
    document = Document()
    uploaded_file = BytesIO()
    document.save(uploaded_file)
    uploaded_file.name = "empty.docx"

    with pytest.raises(ValueError, match="No readable text"):
        extract_resume_text(uploaded_file)


def test_unsupported_file():
    # Unsupported file formats should be rejected.
    uploaded_file = BytesIO(b"Sample resume")
    uploaded_file.name = "resume.txt"

    with pytest.raises(ValueError, match="Unsupported file format"):
        extract_resume_text(uploaded_file)
