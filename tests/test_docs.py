"""Docs-as-code tests (B12): the catalog must match the tree."""

def test_primitives_catalogs_every_root_module():
    import re
    from pathlib import Path
    root = Path(__file__).resolve().parent.parent
    text = (root / "docs" / "PRIMITIVES.md").read_text()
    missing = [f.stem for f in root.glob("*.py")
               if f"`{f.name}`" not in text]
    assert missing == [], f"uncatalogued modules: {missing}"
