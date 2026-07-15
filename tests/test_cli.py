import requests

import cli


def test_cli_exits_cleanly(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _: "7")

    cli.main()

    assert "Goodbye!" in capsys.readouterr().out


def test_cli_fetches_a_product_by_barcode_and_saves_it(monkeypatch):
    answers = iter(["5", "3017620422003", "7"])
    calls = []

    class DummyResponse:
        def __init__(self, payload):
            self._payload = payload
            self.status_code = 200

        def json(self):
            return self._payload

    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    monkeypatch.setattr(
        "cli.make_request",
        lambda method, path, **kwargs: calls.append((method, path, kwargs))
        or DummyResponse({"id": "3017620422003", "name": "Chocolate spread", "quantity": "400 g"}),
    )

    cli.main()

    assert ("GET", "/inventory/product/barcode/3017620422003", {}) in calls
    assert ("POST", "/inventory", {"json": {"id": "3017620422003", "name": "Chocolate spread", "quantity": "400 g"}}) in calls


def test_cli_reports_non_json_errors(monkeypatch, capsys):
    answers = iter(["5", "apple", "7"])

    class DummyResponse:
        def __init__(self):
            self.status_code = 404
            self.text = "<!doctype html><title>404 Not Found</title>"

        def json(self):
            raise ValueError("not json")

    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    monkeypatch.setattr("cli.make_request", lambda method, path, **kwargs: DummyResponse())

    cli.main()

    assert "404 Not Found" in capsys.readouterr().out


def test_cli_falls_back_to_direct_name_search(monkeypatch, capsys):
    answers = iter(["6", "ice cream", "7"])

    class DummyResponse:
        def __init__(self, payload):
            self._payload = payload
            self.status_code = 404

        def json(self):
            return self._payload

    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    monkeypatch.setattr("cli.make_request", lambda method, path, **kwargs: DummyResponse({"error": "Product not found"}))
    monkeypatch.setattr("cli.search_products_by_name", lambda name: [{"id": "1", "name": "Ice cream", "quantity": "500 g"}])

    cli.main()

    assert "Ice cream" in capsys.readouterr().out
