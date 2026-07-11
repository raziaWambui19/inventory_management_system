import cli


def test_cli_exits_cleanly(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _: "7")

    cli.main()

    assert "Goodbye!" in capsys.readouterr().out


def test_cli_fetches_a_product_by_barcode(monkeypatch):
    answers = iter(["5", "3017620422003", "7"])
    calls = []
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    monkeypatch.setattr("cli.make_request", lambda *args, **kwargs: calls.append(args))

    cli.main()

    assert calls == [("GET", "/inventory/product/barcode/3017620422003")]
