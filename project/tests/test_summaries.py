import json

# import pytest


def test_create_summary(test_app_with_db):
    response = test_app_with_db.post(
        "/summaries/", data=json.dumps({"url": "https://foo.bar"})
    )

    assert response.status_code == 201
    assert response.json()["url"] == "https://foo.bar"


# def test_create_summaries_invalid_json(test_app):
#     response = test_app.post("/summaries/", data=json.dumps({}))
#     assert response.status_code == 422
#     assert response.json() == {
#         "detail": [
#             {
#                 "input": {},
#                 "loc": ["body", "url"],
#                 "msg": "Field required",
#                 "type": "missing",
#                 "url": "https://errors.pydantic.dev/2.6/v/missing",
#             }
#         ]
#     }


def test_read_all_summaries(test_app_with_db):
    response = test_app_with_db.post(
        "/summaries/", data=json.dumps({"url": "https://foo.bar"})
    )
    summary_id = response.json()["id"]

    response = test_app_with_db.get("/summaries/")
    assert response.status_code == 200

    response_list = response.json()
    assert len(list(filter(lambda d: d["id"] == summary_id, response_list))) == 1

    def test_read_summary(test_app_with_db):
        response = test_app_with_db.post(
            "/summaries/", data=json.dumps({"url": "https://foo.bar"})
        )
        summary_id = response.json()["id"]

        response = test_app_with_db.get(f"/summaries/{summary_id}/")
        assert response.status_code == 200

        response_dict = response.json()
        assert response_dict["id"] == summary_id
        assert response_dict["url"] == "https://foo.bar"
        assert response_dict["summary"]
        assert response_dict["created_at"]
