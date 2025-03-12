from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator  # new


class TextSummary(models.Model):
    url = fields.TextField()
    summary = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return self.url


SummarySchema = pydantic_model_creator(TextSummary)  # new


class CashFlow(models.Model):
    block_number = fields.IntField()
    transaction_index = fields.SmallIntField()
    gas = fields.IntField()
    gas_price = fields.BigIntField()
    nonce = fields.BigIntField()
    v = fields.IntField()
    value = fields.BigIntField()
    sender_address = fields.TextField()  # from
    to = fields.TextField()
    input = fields.TextField()
    type = fields.IntField()
    created_at = fields.DatetimeField(auto_now_add=True)


CashFlowSchema = pydantic_model_creator(CashFlow)  # new
