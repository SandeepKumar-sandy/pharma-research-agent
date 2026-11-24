from pathlib import Path
from docling.document_converter import DocumentConverter


def read_pdf(pdf_path: str):

    path = Path(pdf_path)

    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    converter = DocumentConverter()

    result = converter.convert(str(path))
    document = result.document

    # Extract document content
    markdown_content = document.export_to_markdown()

    # Extract tables
    extracted_tables = []

    for index, table in enumerate(document.tables):

        dataframe = table.export_to_dataframe(doc=document)

        extracted_tables.append({
            "table_id": index + 1,
            "data": dataframe.to_dict(orient="records")
        })

    return {
        "document_name": path.name,
        "content": markdown_content,
        "tables": extracted_tables
    }


if __name__ == "__main__":

    result = read_pdf("data/documents/research.pdf")

    print("Document:", result["document_name"])
    print("\nExtracted content:")
    print(result["content"][:3000])

    print("\nNumber of tables:", len(result["tables"]))