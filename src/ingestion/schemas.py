from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

Category = Literal["Palette", "Caisse", "Caisse Palette", "Poubelle", "Scelle", "Accessoire"]

CATEGORY_MAPPING: dict[str, Category] = {
    "Palettes": "Palette",
    "Caisses": "Caisse",
    "Pallox": "Caisse Palette",
    "Poubelles": "Poubelle",
    "Scelle": "Scelle",
    "Accessoires": "Accessoire",
}


class Product(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    name: str = Field(min_length=1, description="Exact product name or identifier")
    category: Category
    description: str | None = Field(description="Original product description in French")
    specifications: dict[str, str] = Field(
        description="All technical specifications with original labels, values and units"
    )
