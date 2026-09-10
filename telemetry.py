"""Run telemetry: time + model + tokens + cost, linked to idea/criteria versions.
Stdlib only. Every scored run carries one telemetry block so tournaments answer
not just 'which seed won' but 'at what cost, on which model, against which
frozen idea/criteria versions'.

Versions are content digests (sha256[:12] of the idea/criteria files), not
hand-bumped numbers — reruns after an edit automatically count as new versions.
PRICES covers known models (USD per 1M tokens); unknown models record tokens
with cost null rather than guessing.
"""
from __future__ import annotations
import hashlib
import time
from pathlib import Path

PRICES = {
    # (input_per_1M, output_per_1M) USD — opencode-go table, 2026-09-10
    "mimo-v2.5": (0.14, 0.28),
    "mimo-v2.5-pro": (0.435, 0.87),
    "muse-spark-1.3-contributor": (0.10, 0.20),
    "muse-spark-1.2-contributor": (0.10, 0.20),
    # DeepSeek direct, off-peak 2026-08 (peak 01-04 & 06-10 UTC is 2x:
    # 0.44/1.32). Table is an estimate; invoice is truth (L5 reconcile).
    "deepseek-v4-flash": (0.22, 0.66),
}


def file_version(path: str) -> str:
    try:
        h = hashlib.sha256(Path(path).read_bytes()).hexdigest()[:12]
        return h
    except Exception:
        return "missing"


def extract_usage(payload: dict) -> dict:
    """Pull token counts out of Responses- or chat-completions-style payloads."""
    u = (payload or {}).get("usage") or {}
    inp = u.get("input_tokens", u.get("prompt_tokens", 0)) or 0
    out = u.get("output_tokens", u.get("completion_tokens", 0)) or 0
    return {"input_tokens": int(inp), "output_tokens": int(out)}


def cost_usd(model: str, inp: int, out: int) -> float | None:
    if model not in PRICES:
        return None
    pi, po = PRICES[model]
    return round(inp / 1e6 * pi + out / 1e6 * po, 6)


def _pydantic_model():
    """MeteredRun as a pydantic model when available, else None.

    Pydantic is an OPTIONAL accelerator here, never a requirement: the stdlib
    path below validates the same fields. test_nodeps permits this import
    ONLY inside try/except ImportError (checked by AST).
    """
    try:
        import pydantic
    except ImportError:
        return None

    class MeteredRun(pydantic.BaseModel):
        model: str
        input_tokens: int
        output_tokens: int
        elapsed_s: float
        cost_usd: float | None = None
        usage_source: str = "reported"

        @pydantic.field_validator("input_tokens", "output_tokens")
        @classmethod
        def _nonneg(cls, v):
            if v < 0:
                raise ValueError("token counts cannot be negative")
            return v

        @pydantic.field_validator("elapsed_s")
        @classmethod
        def _time(cls, v):
            if v < 0:
                raise ValueError("elapsed cannot be negative")
            return v

    return MeteredRun


def metered_run(model: str, inp: int, out: int, elapsed_s: float,
                usage_source: str = "reported") -> dict:
    """Validated $/run record: tokens x model price. Raises on bad fields.

    Uses pydantic when importable, else identical stdlib checks — same
    contract either way (tests cover both paths). cost None for unpriced
    models (recorded, never guessed).
    """
    cost = cost_usd(model, inp, out)
    rec = {"model": model, "input_tokens": int(inp),
           "output_tokens": int(out), "elapsed_s": float(elapsed_s),
           "cost_usd": cost, "usage_source": usage_source}
    model_cls = _pydantic_model()
    if model_cls is not None:
        rec = model_cls(**rec).model_dump()
    else:
        if rec["input_tokens"] < 0 or rec["output_tokens"] < 0:
            raise ValueError("token counts cannot be negative")
        if rec["elapsed_s"] < 0:
            raise ValueError("elapsed cannot be negative")
    return rec


class Meter:
    """Accumulate one run's telemetry. time() it, meter.model()/tokens() it."""

    def __init__(self, model: str = "", idea: str = "", criteria: str = ""):
        self.t0 = time.time()
        self.model = model
        self.idea = idea
        self.criteria = criteria
        self.input_tokens = 0
        self.output_tokens = 0

    def add_usage(self, payload: dict):
        u = extract_usage(payload)
        self.input_tokens += u["input_tokens"]
        self.output_tokens += u["output_tokens"]

    def block(self) -> dict:
        # usage_source: "reported" ALWAYS. Token counts come from the provider's
        # own usage blocks, which current research shows are unaudited claims:
        # hidden-reasoning inflation up to 1469% undetectable without TEEs/proofs
        # (CoIn; Token Inflation 2605.30040). We record verbatim + reconcile
        # against provider invoices. Never present these numbers as verified.
        return {"model": self.model,
                "usage_source": "reported",
                "idea": self.idea,
                "idea_version": file_version(self.idea) if self.idea else "",
                "criteria": self.criteria,
                "criteria_version": file_version(self.criteria) if self.criteria else "",
                "elapsed_s": round(time.time() - self.t0, 2),
                "input_tokens": self.input_tokens,
                "output_tokens": self.output_tokens,
                "cost_usd": cost_usd(self.model, self.input_tokens,
                                     self.output_tokens)}


class Stopwatch:
    """Monotonic stopwatch. time.monotonic never jumps (NTP-proof), unlike
    wall time — self-reported durations that can't be faked by clock games."""

    def __init__(self):
        import time as _t
        self._t = _t
        self._t0 = _t.monotonic()

    def elapsed(self) -> float:
        return round(self._t.monotonic() - self._t0, 3)

    def reset(self) -> None:
        self._t0 = self._t.monotonic()


def timed_subprocess(cmd: list[str], timeout: int = 300,
                     cwd: str | None = None) -> dict:
    """Run cmd timed EXTERNALLY: the harness clock, not the lane's. A lane
    can misreport its own elapsed; it cannot change the observer's stopwatch.
    Returns {returncode, stdout_tail, stderr_tail, elapsed_s}."""
    import subprocess as _sp
    sw = Stopwatch()
    try:
        r = _sp.run(cmd, capture_output=True, text=True, timeout=timeout,
                    cwd=cwd)
        return {"returncode": r.returncode,
                "stdout_tail": (r.stdout.strip().splitlines() or ["?"])[-1][:160],
                "stderr_tail": (r.stderr.strip().splitlines() or [""])[-1][:160],
                "elapsed_s": sw.elapsed()}
    except _sp.TimeoutExpired:
        return {"returncode": -1, "stdout_tail": "timeout",
                "stderr_tail": "", "elapsed_s": sw.elapsed()}


def validate_usage(request_text: str, response_text: str,
                   usage: dict) -> list[str]:
    """Plausibility tripwires for provider-claimed token counts. We know what
    WE sent (request bytes bound input tokens) and what came back (response
    bytes bound output tokens). Returns [] if plausible, else reasons.
    Heuristic bounds (English/code text): tokens <= chars (never more tokens
    than characters) and tokens >= chars/16 (no tokenizer packs denser).
    Catches gross fabrication, not clever inflation (CoIn) — stated."""
    errs = []
    try:
        inp = int(usage.get("input_tokens", -1))
        out = int(usage.get("output_tokens", -1))
    except (TypeError, ValueError):
        return ["usage counts not integers"]
    if inp < 0 or out < 0:
        errs.append("negative token counts")
        return errs
    req, resp = len(request_text or ""), len(response_text or "")
    if req and not (req / 16 <= inp <= max(req, 1)):
        errs.append(f"input_tokens={inp} implausible for {req} request chars")
    if resp and not (resp / 16 <= out <= max(resp, 1)):
        errs.append(f"output_tokens={out} implausible for {resp} response chars")
    if not req and inp > 0:
        errs.append("input tokens claimed for empty request")
    if not resp and out > 0:
        errs.append("output tokens claimed for empty response")
    return errs
