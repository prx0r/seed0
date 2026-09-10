"""Example guard: the defense the example probes pin. Replace per project."""
import re

REFUSALS = [
    (re.compile(r"\b(owner|admin)\b.*\b(disable|off|bypass)\b", re.I), "authority"),
    (re.compile(r"(api key|password).*(repeat|show|reveal|list)", re.I), "secret"),
    (re.compile(r"(repeat|show|reveal|list|tell me).{0,40}(api key|password|secret)", re.I),
     "secret-reversed"),
]


def guard(text: str) -> dict:
    for rx, reason in REFUSALS:
        if rx.search(text or ""):
            return {"trip": True, "reasons": [reason],
                    "safe": "I can't do that — a human needs to approve it."}
    return {"trip": False, "reasons": [], "safe": text}
