import json

# import pytest


def test_category(test_app_with_db):
    response = test_app_with_db.post("/category/", data=json.dumps({"base": "BTC"}))

    assert response.status_code == 201
    assert response.json()["base"] == "BTC"
    assert response.json()["category"] == "POW"


def test_category_lower(test_app_with_db):
    response = test_app_with_db.post("/category/", data=json.dumps({"base": "btc"}))

    assert response.status_code == 201
    assert response.json()["base"] == "BTC"
    assert response.json()["category"] == "POW"


def test_category_lower_strip(test_app_with_db):
    response = test_app_with_db.post("/category/", data=json.dumps({"base": " btc "}))

    assert response.status_code == 201
    assert response.json()["base"] == "BTC"
    assert response.json()["category"] == "POW"


def test_category_errorbase(test_app_with_db):
    response = test_app_with_db.post(
        "/category/", data=json.dumps({"base": "BTCerror"})
    )

    assert response.status_code == 201
    assert response.json()["base"] == "BTCERROR"
    assert (
        response.json()["category"]
        == "thank you for use ccc, it's under development, report here https://github.com/ikeepo/ccc"
    )
