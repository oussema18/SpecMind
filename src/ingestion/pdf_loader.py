from pathlib import Path

import pymupdf

from .schemas import CATEGORY_MAPPING, Category

PDF_DIR = Path(__file__).resolve().parents[2] / "data" / "PDFs"


def extract_text(pdf_path: Path) -> str:
    with pymupdf.open(pdf_path) as document:
        text = "\n".join(
            page.get_text(
                "text", sort=True,
                flags=pymupdf.TEXTFLAGS_TEXT | pymupdf.TEXT_INHIBIT_SPACES,
            )
            for page in document
        ).strip()
    if not text:
        raise ValueError(f"No text extracted from {pdf_path.name}")
    return text


def discover_documents(pdf_dir: Path = PDF_DIR) -> list[tuple[Path, Category]]:
    documents = []
    for folder in sorted(pdf_dir.iterdir()):
        if not folder.is_dir():
            continue
        if folder.name not in CATEGORY_MAPPING:
            print(f"Skipping unknown folder: {folder.name}")
            continue
        documents.extend(
            (pdf, CATEGORY_MAPPING[folder.name])
            for pdf in sorted(folder.rglob("*"))
            if pdf.is_file() and pdf.suffix.lower() == ".pdf"
        )
    return documents
