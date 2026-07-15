import requests

import cli


def test_cli_exits_cleanly(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _: "7")

    cli.main()

    assert "Goodbye!" in capsys.readouterr().out


def test_cli_fetches_a_product_by_barcode(monkeypatch):
    answers = iter(["5", "3017620422003", "7", "7"])
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
        lambda *args, **kwargs: calls.append(args) or DummyResponse({"id": "1", "name": "Chocolate spread", "quantity": "400 g"}),
    )

    cli.main()

    assert calls == [("GET", "/inventory/product/barcode/3017620422003")]


def test_cli_can_import_search_result(monkeypatch):
    answers = iter(["6", "chocolate", "y", "7"])
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
        or DummyResponse({"id": "1", "name": "Chocolate spread", "quantity": "400 g"}),
    )

    cli.main()

    assert ("POST", "/inventory", {"json": {"id": "1", "name": "Chocolate spread", "quantity": "400 g"}}) in calls


def test_cli_handles_unavailable_api(monkeypatch, capsys):
    answers = iter(["6", "mango", "7"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    monkeypatch.setattr(
        cli.requests,
        "request",
        lambda *args, **kwargs: (_ for _ in ()).throw(requests.ConnectionError("offline")),
    )

    cli.main()

    output = capsys.readouterr().out
    assert "unavailable" in output.lower()
