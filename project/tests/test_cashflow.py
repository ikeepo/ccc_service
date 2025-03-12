import json

# import pytest


def test_create_cashflow(test_app_with_db):
    response = test_app_with_db.post(
        "/cash_flow/create_transition/",
        data=json.dumps(
            {
                "block_number": 100000,
                "transaction_index": 1,
                "gas": 1,
                "gas_price": 1,
                "nonce": 1,
                "v": 1,
                "value": "1",
                "sender_address": "0x000111",
                "to": "0x000111",
                "input": "1",
                "type": 1,
            }
        ),
    )

    assert response.status_code == 201
    assert response.json()["sender_address"] == "0x000111"


def test_create_cashflow_invalid_json(test_app_with_db):
    response = test_app_with_db.post(
        "/cash_flow/create_transition/", data=json.dumps({})
    )
    assert response.status_code == 422


def test_read_all_transitions(test_app_with_db):
    response = test_app_with_db.post(
        "/cash_flow/create_transition/",
        data=json.dumps(
            {
                "block_number": 100000,
                "transaction_index": 1,
                "gas": 1,
                "gas_price": 1,
                "nonce": 1,
                "v": 1,
                "value": "1",
                "sender_address": "0x000111",
                "to": "0x000111",
                "input": "1",
                "type": 1,
            }
        ),
    )
    transition_id = response.json()["id"]

    response = test_app_with_db.get("/cash_flow/")
    assert response.status_code == 200

    response_list = response.json()
    assert len(list(filter(lambda d: d["id"] == transition_id, response_list))) == 1
