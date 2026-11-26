import time

from .pdf_loader import PDF_DIR, discover_documents, extract_text
from .product_extractor import extract_product, build_rag_text
from src.database.repository import save_product, product_exists


def run_pipeline(force: bool = False):

    documents = discover_documents()

    successful = 0
    skipped = 0
    failed = 0

    start = time.perf_counter()

    print(f"Documents found: {len(documents)}")

    for index, (pdf, category) in enumerate(documents, 1):

        source_path = pdf.relative_to(PDF_DIR).as_posix()

        print(f"\n[{index}/{len(documents)}] {pdf.name}")

        try:

            if not force and product_exists(source_path):
                print("Skipped: Already processed")
                skipped += 1
                continue

            raw_text = extract_text(pdf)

            product = extract_product(raw_text, category)

            rag_text = build_rag_text(product)

            product_id = save_product(
                product=product,
                source_file=pdf.name,
                source_path=source_path,
                raw_text=raw_text,
                rag_text=rag_text
            )

            successful += 1

            print(f"Saved: {product.name} (ID: {product_id})")

        except Exception as error:

            failed += 1

            print(f"Failed: {error}")

    duration = time.perf_counter() - start

    print("\n--- INGESTION SUMMARY ---")
    print(f"Total documents: {len(documents)}")
    print(f"Successfully saved: {successful}")
    print(f"Skipped: {skipped}")
    print(f"Failed: {failed}")
    print(f"Duration: {duration:.2f}s")


if __name__ == "__main__":
    run_pipeline()