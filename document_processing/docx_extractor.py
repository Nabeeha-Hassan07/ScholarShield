
from io import BytesIO

from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P


def extract_docx_text(uploaded_file):
    """
    Extract text from an uploaded DOCX document.

    Preserves the order of body paragraphs and tables.
    Empty paragraphs and empty table cells are ignored.

    Raises:
        ValueError: If the file is empty or cannot be read.
    """
    if hasattr(uploaded_file, "getvalue"):
        docx_bytes = uploaded_file.getvalue()
    else:
        docx_bytes = uploaded_file.read()

    if not docx_bytes:
        raise ValueError("The uploaded Word document is empty.")

    try:
        document = Document(BytesIO(docx_bytes))
        extracted_blocks = []

        # Process paragraphs and tables in their document order.
        for element in document.element.body.iterchildren():

            if isinstance(element, CT_P):
                paragraph = Paragraph(element, document)
                text = paragraph.text.strip()

                if text:
                    extracted_blocks.append(text)

            elif isinstance(element, CT_Tbl):
                table = Table(element, document)

                for row in table.rows:
                    cell_texts = []

                    for cell in row.cells:
                        text = " ".join(
                            paragraph.text.strip()
                            for paragraph in cell.paragraphs
                            if paragraph.text.strip()
                        )

                        if text:
                            cell_texts.append(text)

                    if cell_texts:
                        extracted_blocks.append(" | ".join(cell_texts))

    except Exception as exc:
        raise ValueError(
            "Unable to read this Word document. "
            "Please upload a valid DOCX file."
        ) from exc

    return "\n".join(extracted_blocks)