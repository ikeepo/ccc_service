from typing import List, Union

from tortoise.expressions import Q

from app.models.pydantic import CashflowPayloadSchema, SummaryPayloadSchema
from app.models.tortoise import CashFlow, TextSummary


async def post_cashflow(payload: CashflowPayloadSchema) -> int:
    cashflow = CashFlow(
        block_number=payload.block_number,
        transaction_index=payload.transaction_index,
        gas=payload.gas,
        gas_price=payload.gas_price,
        nonce=payload.nonce,
        v=payload.v,
        value=payload.value,
        sender_address=payload.sender_address,
        to=payload.to,
        input=payload.input,
        type=payload.type,
    )
    await cashflow.save()
    return cashflow.id


async def post(payload: SummaryPayloadSchema) -> int:
    summary = TextSummary(
        url=payload.url,
        summary="dummy summary",
    )
    await summary.save()
    return summary.id


async def get_transitions(sender_address: str) -> Union[List[dict], None]:
    cashflow = (
        await CashFlow.filter(Q(sender_address=sender_address) | Q(to=sender_address))
        .order_by("-block_number", "-transaction_index")
        .all()
        .values()
    )
    if cashflow:
        return cashflow
    return None


async def get(id: int) -> Union[dict, None]:
    summary = await TextSummary.filter(id=id).first().values()
    if summary:
        return summary
    return None


async def get_all_transitions() -> List:
    cash_flow = await CashFlow.all().values()
    return cash_flow


async def get_all() -> List:
    summaries = await TextSummary.all().values()
    return summaries
