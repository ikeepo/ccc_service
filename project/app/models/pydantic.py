from pydantic import BaseModel


class SummaryPayloadSchema(BaseModel):
    url: str


class SummaryResponseSchema(SummaryPayloadSchema):
    id: int


class CategoryPayloadSchema(BaseModel):
    base: str


class CategoryResponseSchema(CategoryPayloadSchema):
    category: str


class DrawcashflowPayloadSchema(BaseModel):
    sender_address: str  # from


class CashflowPayloadSchema(DrawcashflowPayloadSchema):
    block_number: int
    transaction_index: int
    gas: int
    gas_price: int
    nonce: int
    v: int
    value: int
    to: str
    input: str
    type: int


class CashflowResponseSchema(CashflowPayloadSchema):
    id: int
