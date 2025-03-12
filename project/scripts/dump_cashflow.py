import json
import logging
import os

import pandas as pd
import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)


def test_local():
    url_base = "http://localhost:8004"  # local
    url_base = "https://young-chamber-41337-67dbb5d1ef56.herokuapp.com"
    for i in range(10):
        for j in range(3):
            payload = {
                "block_number": 1000000 + i,
                "transaction_index": 1 + j,
                "gas": 1,
                "gas_price": 1,
                "nonce": 1,
                "v": 1,
                "value": 1,
                "sender_address": f"0x00011{i}",
                "to": f"0x00011{j}",
                "input": "1",
                "type": 1,
            }
            url_cashflow = f"{url_base}/cash_flow/create_transition/"
            res = requests.post(url=url_cashflow, data=json.dumps(payload))
            print(res.status_code)
            print(res.json())


def test_heroku():
    dp = "/Users/d3/private/cc_flow"
    format = {
        "1": {
            "fns": ["19317670_19417670.csv", "19417670_19419034.csv"],
            "cols": [
                "block_number",
                "transaction_index",
                "gas",
                "gas_price",
                "nonce",
                "v",
                "value",
                "from",
                "to",
                "input",
                "type",
            ],
        },
        "2": {
            "fns": [],
            "cols": [
                "block_number",
                "transaction_index",
                "gas",
                "gas_price",
                "nonce",
                "v",
                "value",
                "from",
                "to",
                "type",
            ],
        },
    }

    for fn in [
        "19016586_19116586.csv",
        # "19317670_19417670.csv",
        # "19417670_19419034.csv"
        # "19316586_19416586.csv",    # 正在下载当中, 先不保存
    ]:
        fp = os.path.join(dp, fn)
        if fn in format["1"]["fns"]:
            df = pd.read_csv(fp, names=format["1"]["cols"])
        else:
            df = pd.read_csv(fp, names=format["2"]["cols"])
        eth_transition_dump_heroku(df)


def eth_transition_dump_heroku(df):
    df["hash"] = pd.util.hash_pandas_object(df)
    # 从文件中读取已经保存的所有hash值
    with open("hashes.txt", "r") as f:
        saved_hashes = f.readlines()
    # 每个元素去除尾部的\n
    saved_hashes = [x.strip() for x in saved_hashes]
    url_base = "https://young-chamber-41337-67dbb5d1ef56.herokuapp.com"
    # 逐行便遍历df, 每行转成一个dict, 作为payload
    length = len(df)
    for i, row in df.iterrows():
        # 如果hash已经保存就跳过
        if str(row["hash"]) in saved_hashes:
            continue
        flag = round(i / length, 3)
        if flag in [0.100, 0.200, 0.500, 0.800, 0.900]:
            logging.info(f"{flag} {i}/{length}")
        payload = row.to_dict()
        # 修改其中的 input, from
        payload["input"] = "placeholder"
        payload["sender_address"] = payload["from"]
        payload.pop("from")
        url_cashflow = f"{url_base}/cash_flow/create_transition/"
        res = requests.post(url=url_cashflow, data=json.dumps(payload))
        logging.info(f"{i} {res.status_code}")
        if res.status_code != 201:
            logging.error(f"{i} {payload} {res.json()}")
        else:
            # 对应的hash写入文件
            with open("hashes.txt", "a") as f:
                f.write(f"{payload['hash']}\n")


if __name__ == "__main__":
    # test_local()
    test_heroku()
