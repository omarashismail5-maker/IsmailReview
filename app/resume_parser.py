from pathlib import Path
from pypdf import PdfReader
from docx import Document

def extract_resume_text(uploaded_file):

    extension = Path(uploaded_file.name).suffix.lower()
    uploaded_file.seek(0)

    if extension == ".pdf":

        try:
            reader = PdfReader(uploaded_file)

            text = "\n".join(
                page.extract_text() or ""
                for page in reader.pages
            )

        except Exception as e:
            raise ValueError(
                "This PDF could not be opened. "
                "Please upload a valid PDF file."
            ) from e
            
    elif extension == ".docx":

        try:
            document = Document(uploaded_file)

            paragraphs = [
                paragraph.text
                for paragraph in document.paragraphs
                if paragraph.text.strip()
            ]

            for table in document.tables:
                for row in table.rows:
                    row_text = " | ".join(
                        cell.text.strip()
                        for cell in row.cells
                        if cell.text.strip()
                    )

                    if row_text:
                        paragraphs.append(row_text)

            text = "\n".join(paragraphs)

        except Exception as e:
            raise ValueError(
                "This Word document could not be opened. "
                "Please upload a valid DOCX file."
            ) from e

    else:
        raise ValueError("Unsupported file format.")

    if not text.strip():
        raise ValueError("No readable text found in the resume.")

    return text.strip()