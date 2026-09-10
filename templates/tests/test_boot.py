def test_boot():
    import pathlib
    assert (pathlib.Path(__file__).parent.parent / ".env.example").exists()
