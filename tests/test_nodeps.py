"""Zero-dependency proof: every repo-root module imports stdlib only —
except OPTIONAL accelerators guarded by try/except ImportError (currently:
pydantic in telemetry.py, used only for record validation with an identical
stdlib fallback). The AST check below permits exactly that shape.
Adding an UNguarded third-party import breaks this test ON PURPOSE.
"""
import ast
import sys
from pathlib import Path

ALLOWLIST = {"seed0", "tournament", "funnel", "pyeval", "runs", "tasks",
             "telemetry", "budgets", "learn", "trace", "eval_arch", "ham",
             "loop", "hinbox", "hserver", "grants", "hplane", "metrics",
             "policy", "mcp_server", "gitnotes"}
OPTIONAL = {"pydantic"}


def _guarded(tree: ast.AST, mod: str) -> bool:
    """True iff every import of mod sits inside try/except ImportError."""
    parent: dict[ast.AST, ast.AST] = {}
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            parent[child] = node

    def names_of(n):
        if isinstance(n, ast.Import):
            return [a.name.split(".")[0] for a in n.names]
        if isinstance(n, ast.ImportFrom) and not n.level:
            return [(n.module or "").split(".")[0]]
        return []

    def in_importerror_try(n) -> bool:
        p = parent.get(n)
        while p is not None:
            if isinstance(p, ast.Try) and any(
                    h.type is None or "ImportError" in ast.dump(h.type)
                    or "Exception" in ast.dump(h.type)
                    for h in p.handlers):
                return True
            p = parent.get(p)
        return False

    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)) and mod in names_of(node):
            if not in_importerror_try(node):
                return False
    return True


def test_all_imports_stdlib_or_local():
    stdlib = set(sys.stdlib_module_names)
    root = Path(__file__).resolve().parent.parent
    offenders = []
    for f in sorted(root.glob("*.py")):
        tree = ast.parse(f.read_text())
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                mods = [a.name.split(".")[0] for a in node.names]
            elif isinstance(node, ast.ImportFrom):
                if node.level:
                    continue  # relative, local by construction
                mods = [(node.module or "").split(".")[0]]
            else:
                continue
            for m in mods:
                if not m or m in stdlib or m in ALLOWLIST:
                    continue
                if m in OPTIONAL:
                    tree = ast.parse(f.read_text())
                    assert _guarded(tree, m), \
                        f"{f.name}:{m} must live inside try/except ImportError"
                    continue
                offenders.append(f"{f.name}:{m}")
    assert offenders == [], f"third-party imports (add dep or vendor): {offenders}"


def test_allowlist_matches_tree():
    root = Path(__file__).resolve().parent.parent
    actual = {f.stem for f in root.glob("*.py")}
    assert ALLOWLIST <= actual, f"stale allowlist: {ALLOWLIST - actual}"
