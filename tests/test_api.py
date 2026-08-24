from __future__ import annotations

import json

MASK_URL = "/api/mask/"


def post_json(client, payload):
    return client.post(MASK_URL, data=json.dumps(payload), content_type="application/json")


class TestMaskApi:
    def test_returns_expected_shape(self, client):
        response = post_json(client, {"text": "hello"})
        assert response.status_code == 200
        body = response.json()
        assert set(body) == {"masked", "detections", "summary", "total"}

    def test_empty_text(self, client):
        assert post_json(client, {"text": ""}).json()["masked"] == ""

    def test_rules_filter(self, client):
        response = post_json(client, {"text": "hello", "rules": ["email"]})
        assert response.status_code == 200

    def test_unknown_rule_rejected(self, client):
        response = post_json(client, {"text": "hello", "rules": ["nope"]})
        assert response.status_code == 400

    def test_invalid_json_rejected(self, client):
        response = client.post(MASK_URL, data="ไม่ใช่ json", content_type="application/json")
        assert response.status_code == 400

    def test_wrong_text_type_rejected(self, client):
        assert post_json(client, {"text": 123}).status_code == 400

    def test_get_not_allowed(self, client):
        assert client.get(MASK_URL).status_code == 405


class TestOtherEndpoints:
    def test_rules_endpoint_lists_five_rules(self, client):
        assert len(client.get("/api/rules/").json()["rules"]) == 5

    def test_health(self, client):
        assert client.get("/api/health/").json() == {"status": "ok"}


class TestPages:
    def test_index_renders(self, client):
        response = client.get("/")
        assert response.status_code == 200
        assert b"PDPA" in response.content

    def test_index_has_github_link(self, client):
        assert b"github.com" in client.get("/").content

    def test_htmx_partial_returns_html_fragment(self, client):
        response = client.post("/mask/", {"text": "hello"}, HTTP_HX_REQUEST="true")
        assert response.status_code == 200
        assert b"<html" not in response.content
