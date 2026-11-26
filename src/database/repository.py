from psycopg.types.json import Jsonb
from psycopg.rows import dict_row

from .connection import connect_to_database
from src.ingestion.schemas import Product


def save_product(
    product: Product,
    source_file: str,
    source_path: str,
    raw_text: str,
    rag_text: str
) -> int:

    with connect_to_database() as connection:
        with connection.cursor() as cursor:

            cursor.execute("""
                INSERT INTO public.products (
                    name,
                    category,
                    description,
                    specifications,
                    source_file,
                    source_path,
                    raw_text,
                    rag_text
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)

                ON CONFLICT (source_path)
                DO UPDATE SET
                    name = EXCLUDED.name,
                    category = EXCLUDED.category,
                    description = EXCLUDED.description,
                    specifications = EXCLUDED.specifications,
                    source_file = EXCLUDED.source_file,
                    raw_text = EXCLUDED.raw_text,
                    rag_text = EXCLUDED.rag_text

                RETURNING id;
            """, (
                product.name,
                product.category,
                product.description,
                Jsonb(product.specifications),
                source_file,
                source_path,
                raw_text,
                rag_text
            ))

            return cursor.fetchone()[0]


def get_product(product_id: int) -> dict | None:

    with connect_to_database() as connection:
        with connection.cursor(row_factory=dict_row) as cursor:

            cursor.execute("""
                SELECT *
                FROM public.products
                WHERE id = %s;
            """, (product_id,))

            return cursor.fetchone()


def get_all_products() -> list[dict]:

    with connect_to_database() as connection:
        with connection.cursor(row_factory=dict_row) as cursor:

            cursor.execute("""
                SELECT *
                FROM public.products
                ORDER BY id;
            """)

            return cursor.fetchall()


def product_exists(source_path: str) -> bool:

    with connect_to_database() as connection:
        with connection.cursor() as cursor:

            cursor.execute("""
                SELECT EXISTS (
                    SELECT 1
                    FROM public.products
                    WHERE source_path = %s
                );
            """, (source_path,))

            return cursor.fetchone()[0]