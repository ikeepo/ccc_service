# import json
# import logging
from typing import List

import pandas as pd

# import plotly.express as px
from fastapi import APIRouter, HTTPException

# from fastapi.responses import JSONResponse
from graphviz import Digraph

from app.api import crud
from app.models.pydantic import (
    CashflowPayloadSchema,
    CashflowResponseSchema,
    DrawcashflowPayloadSchema,
)
from app.models.tortoise import CashFlowSchema

router = APIRouter()


async def transaction_process(address, df=pd.DataFrame(), iteRound=0, iteEnd=2):
    """一个转账过程
    追寻blockNumberStart之后, 这个address后续的资金转移

    Parameters
    ----------
    address : str
        需要追踪的初始地址
    """
    strIte = f"iteRound({iteRound})"
    print(
        f"{strIte}-start-{address} with df: {df}, iter:{iteRound}, iterend:{iteEnd} >>>"
    )
    # 通过address获取transctions
    transitions = await crud.get_transitions(address)
    # print(address)
    # print(transitions)
    dfFrom = pd.DataFrame(transitions).reset_index(drop=True)
    dfFrom.rename(columns={"sender_address": "from"}, inplace=True)
    # print(f"dfFrom:{dfFrom}")
    # 只看value>0即有转账的
    dfTranValue = dfFrom[dfFrom["value"] > 0]
    # print(f"dfTranValue:{dfTranValue}")
    # 保存结果
    dfTranValueCopy = dfTranValue.copy()
    dfTranValueCopy.rename(columns={"v": "level"}, inplace=True)
    dfTranValueCopy["level"] = iteRound
    dfSave = dfTranValueCopy[["from", "value", "to", "level"]]
    # print(f"dfSave: {dfSave}")
    df = pd.concat([df, dfSave])
    # 通过to循环追踪
    listTo = dfTranValue["to"].to_list()
    listValue = dfTranValue["value"].to_list()
    dictToValue = dict(zip(listTo, listValue))  # NOQA: F841

    iteRound += 1
    if iteRound > iteEnd:
        return df
    # print(f"df: {df}")
    # print(f"listTo:{listTo}")
    for i, to in enumerate(list(set(listTo))):
        # 依据to限定blockNumberStart,只追踪to所在区块之后的，之前的跟此笔交易无关
        # _blockNumberStart = min(dfTranValue[dfTranValue["to"] == to]["block_number"].tolist())
        # print(f"listTo:{list(set(listTo))}")
        # print(f"i:{i}")
        # print(f"to:{to}")
        # print(f"df:{df}")
        # print(f"iteRound:{iteRound}")
        df = await transaction_process(address=to, df=df, iteRound=iteRound)
    # print(f"df:{df}")
    return df


def create_graphviz(df, address):
    shapeList = ["circle", "egg", "rarrow", "star"]
    nameDict = {key: [] for key in range(max(df.level.tolist()) + 2)}
    fn = f"{address}"
    df["value"] = df["value"] / 10**18
    df["fs"] = df["from"].str[0:10]
    df["ts"] = df["to"].str[0:10]
    df.sort_values(by=["level"], inplace=True)
    df.reset_index(drop=True, inplace=True)

    f = Digraph(name=fn, comment="blockchain tracking")
    # level = 0的原数据，得到level0 和 level1的name
    dfL0 = df[df["level"] == 0]
    dfL0.reset_index(drop=True, inplace=True)
    f.attr("node", shape="doublecircle")  # level = 0的name
    for i in dfL0.index:
        if dfL0.at[i, "from"] in nameDict[0]:
            pass
        else:
            nameDict[0].append(dfL0.at[i, "from"])
            f.node(dfL0.at[i, "fs"])
    # 循环添加name
    for i in range(max(df.level.tolist()) + 1):
        dfLi = df[df["level"] == i]
        dfLi.reset_index(drop=True, inplace=True)
        f.attr("node", shape=shapeList[i % 4])  # level = 2的name
        for j in dfLi.index:
            if dfLi.at[j, "to"] in nameDict[i + 1]:
                pass
            else:
                nameDict[i + 1].append(dfLi.at[j, "to"])
                f.node(dfLi.at[j, "ts"])
    # 构建连接线
    for i in df.index:
        f.edge(df.at[i, "fs"], df.at[i, "ts"], label=f"{df.at[i, 'value']}")
    return f.source


@router.post(
    "/draw_flowmap/",
    # response_class=JSONResponse,
    status_code=201,
)
async def draw_flowmap(payload: DrawcashflowPayloadSchema):
    sender_address = payload.sender_address
    # get transitions
    df = await transaction_process(sender_address)
    # create graphviz
    fig_source = create_graphviz(df, sender_address)
    # 生成折线图
    return {"message": fig_source}


@router.post(
    "/create_transition/", response_model=CashflowResponseSchema, status_code=201
)
async def create_transition(payload: CashflowPayloadSchema) -> CashflowResponseSchema:
    cashflow_id = await crud.post_cashflow(payload)

    response_object = {
        "id": cashflow_id,
        "block_number": payload.block_number,
        "transaction_index": payload.transaction_index,
        "gas": payload.gas,
        "gas_price": payload.gas_price,
        "nonce": payload.nonce,
        "v": payload.v,
        "value": payload.value,
        "sender_address": payload.sender_address,
        "to": payload.to,
        "input": payload.input,
        "type": payload.type,
    }
    return response_object


@router.get("/{sender_addr}/", response_model=List[CashFlowSchema])
async def read_transitions(sender_addr: str) -> CashFlowSchema:
    transitions = await crud.get_transitions(sender_addr)
    if not transitions:
        raise HTTPException(status_code=404, detail="transition not found")

    return transitions


@router.get("/", response_model=List[CashFlowSchema])
async def read_all_transitions() -> List[CashFlowSchema]:
    return await crud.get_all_transitions()
