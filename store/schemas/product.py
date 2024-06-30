from decimal import Decimal
from typing import Annotated, Optional
from bson import Decimal128
from pydantic import AfterValidator, Field
from datetime import datetime
from store.schemas.base import BaseSchemaMixin, OutSchema

class ProductBase(BaseSchemaMixin):
    name: str = Field(..., description="Product name")
    quantity: int = Field(..., description="Product quantity")
    price: Decimal = Field(..., description="Product price")
    status: bool = Field(..., description="Product status")

class ProductIn(ProductBase, BaseSchemaMixin):
    ...

class ProductOut(ProductIn, OutSchema):
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

def convert_decimal_128(v):
    return Decimal128(str(v))

Decimal_ = Annotated[Decimal, AfterValidator(convert_decimal_128)]

class ProductUpdate(BaseSchemaMixin):
    quantity: Optional[int] = Field(None, description="Product quantity")
    price: Optional[Decimal_] = Field(None, description="Product price")
    status: Optional[bool] = Field(None, description="Product status")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")

class ProductUpdateOut(ProductOut):
    ...
