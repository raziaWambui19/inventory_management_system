import requests

import cli


def test_cli_exits_cleanly(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _: "7")

    cli.main()

    assert "Goodbye!" in capsys.readouterr().out


<<<<<<< HEAD
def test_cli_fetches_a_product_by_barcode(monkeypatch):
    answers = iter(["5", "3017620422003", "7", "7"])
=======
def test_cli_fetches_a_product_by_barcode_and_saves_it(monkeypatch):
    answers = iter(["5", "3017620422003", "7"])
>>>>>>> 08f3df8 (last commit)
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
<<<<<<< HEAD
        lambda *args, **kwargs: calls.append(args) or DummyResponse({"id": "1", "name": "Chocolate spread", "quantity": "400 g"}),
=======
        lambda method, path, **kwargs: calls.append((method, path, kwargs))
        or DummyResponse({"id": "3017620422003", "name": "Chocolate spread", "quantity": "400 g"}),
>>>>>>> 08f3df8 (last commit)
    )

    cli.main()

<<<<<<< HEAD
    assert calls == [("GET", "/inventory/product/barcode/3017620422003")]


def test_cli_can_import_search_result(monkeypatch):
    answers = iter(["6", "chocolate", "y", "7"])
    calls = []
=======
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
>>>>>>> 08f3df8 (last commit)

    class DummyResponse:
        def __init__(self, payload):
            self._payload = payload
<<<<<<< HEAD
            self.status_code = 200
=======
            self.status_code = 404
>>>>>>> 08f3df8 (last commit)

        def json(self):
            return self._payload

    monkeypatch.setattr("builtins.input", lambda _: next(answers))
<<<<<<< HEAD
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
=======
    monkeypatch.setattr("cli.make_request", lambda method, path, **kwargs: DummyResponse({"error": "Product not found"}))
    monkeypatch.setattr("cli.search_products_by_name", lambda name: [{"id": "1", "name": "Ice cream", "quantity": "500 g"}])

    cli.main()

    assert "Ice cream" in capsys.readouterr().out
>>>>>>> 08f3df8 (last commit)
