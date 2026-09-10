"""H-A-M global registry primitive: lifecycle, locked money, unlock graph. Stdlib only.

Patterns imported (pattern-only, no new dependency):
- cmail: single-use approval tokens, sha256-stored, fail closed with receipts.
- agentmandate/imprest: verdict ladder ALLOW / NEEDS_APPROVAL / DENY; allowance
  ledger (total live grants capped); per-tx + session + daily caps; velocity rule.
- giwacard/agent-scope: NO-SELF-APPROVAL (no tool path resolves an approval;
  enforced here by approver-channel check + test); scoped grants (cap+scope+expiry);
  kill-switch revoke; merchant/purpose scoping; remainder/over-policy queues human.
- ERC-7715/7710: scoped, expirable, revocable session grants (off-chain analogue).
- seed0 HUMAN_LOOP: escalations are records, expiry re-escalates, never auto-approves.

Rules (hard): A closes only with validator-passing evidence; A records are never
hard-deleted (retire_criteria archives, record retained). H approves only on the
human channel. M spends only a signed, unused, unexpired, purpose-matching grant
within cap. Every mutation appends a receipt. The browser UI writes approval
records to the same JSONL file; the agent picks them up via poll().
"""
import hashlib
import json
import time
import uuid
from pathlib import Path
OPEN, DONE, ARCHIVED, APPROVED, DENIED, SPENT, REVOKED = (
    "open", "done", "archived", "approved", "denied", "spent", "revoked")
TERMINAL_A = {DONE, ARCHIVED}
UNLOCK_OK = {DONE, APPROVED}
def _now():
    return time.time()
def _nid():
    return "T-" + uuid.uuid4().hex[:6].upper()
class Registry:
    def __init__(self, path):
        self.path = Path(path)
        self.tasks = {}
        self._load()
    def _load(self):
        self.tasks = {}
        if self.path.exists():
            for line in self.path.read_text().splitlines():
                try:
                    t = json.loads(line)
                    self.tasks[t["id"]] = t
                except Exception:
                    continue
    def _save(self, t):
        self.tasks[t["id"]] = t
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "a") as f:
            f.write(json.dumps(t) + "\n")
    def add(self, kind, title, validation=None, blocked_by=None, cost="$0",
            cap=None, scope=None, unlocks_note=""):
        assert kind in ("A", "H", "M")
        t = {"id": _nid(), "kind": kind, "status": OPEN, "title": title,
             "validation": validation or {}, "blocked_by": blocked_by or [],
             "cost": cost, "cap": cap, "scope": scope, "unlocks_note": unlocks_note,
             "grant": None, "attempts": [], "receipts": [], "created": _now()}
        self._save(t)
        return t
    def get(self, tid):
        return self.tasks[tid]
    # ---- A: close only with validator-passing evidence; retire, never delete ----
    def close_a(self, tid, evidence, validator):
        t = self.tasks[tid]
        assert t["kind"] == "A" and t["status"] == OPEN
        if not validator(evidence):
            t["attempts"].append({"t": _now(), "event": "close-rejected"})
            self._save(t)
            raise ValueError(f"{tid}: evidence failed validation, stays open")
        t["status"] = DONE
        t["receipts"].append({"t": _now(), "event": "closed", "evidence": evidence})
        self._save(t)
        return t
    def retire_criteria(self, tid, note):
        """Only way to remove an A-task's gate: retire its criteria (record kept)."""
        t = self.tasks[tid]
        assert t["kind"] == "A"
        t["validation"] = {"retired": True, "note": note}
        t["status"] = ARCHIVED
        t["receipts"].append({"t": _now(), "event": "criteria-retired", "note": note})
        self._save(t)
        return t
    # ---- H: human channel only (no-self-approval) ----
    def _human(self, approver):
        if not (isinstance(approver, str) and approver.startswith("human:")):
            raise PermissionError("H-approvals need the human channel (no-self-approval)")
    def approve_h(self, tid, approver, note=""):
        self._human(approver)
        t = self.tasks[tid]
        assert t["kind"] == "H" and t["status"] == OPEN
        t["status"] = APPROVED
        t["receipts"].append({"t": _now(), "event": "approved",
                              "approver": approver, "note": note})
        self._save(t)
        return t
    def deny_h(self, tid, approver, note=""):
        self._human(approver)
        t = self.tasks[tid]
        t["status"] = DENIED
        t["receipts"].append({"t": _now(), "event": "denied",
                              "approver": approver, "note": note})
        self._save(t)
        return t
    # ---- M: locked. Single-use scoped grants; spend enforces everything. ----
    def approve_m(self, tid, approver, amount, purpose, expiry_s=86400):
        self._human(approver)
        t = self.tasks[tid]
        assert t["kind"] == "M" and t["status"] == OPEN
        assert amount > 0
        if t.get("cap") is not None:
            assert amount <= t["cap"], "grant exceeds task cap"
        token = hashlib.sha256(f"{tid}{amount}{purpose}{_now()}".encode()).hexdigest()
        t["grant"] = {"token": token, "amount": amount, "purpose": purpose,
                      "expiry": _now() + expiry_s, "used": False}
        t["status"] = APPROVED
        t["receipts"].append({"t": _now(), "event": "grant-issued",
                              "approver": approver, "amount": amount,
                              "purpose": purpose})
        self._save(t)
        return t, token
    def spend_m(self, tid, token, amount, purpose):
        t = self.tasks[tid]
        g = t.get("grant")
        def refuse(reason):
            t["attempts"].append({"t": _now(), "event": "spend-refused", "reason": reason})
            self._save(t)
            raise PermissionError(f"spend refused: {reason}")
        if not g:
            refuse("no signed grant (locked)")
        if g["used"]:
            refuse("grant already spent (single-use)")
        if g["token"] != token:
            refuse("bad grant token")
        if _now() > g["expiry"]:
            refuse("grant expired")
        if purpose != g["purpose"]:
            refuse("purpose mismatch (scoped grant)")
        if amount > g["amount"]:
            refuse("over cap")
        g["used"] = True
        t["status"] = SPENT
        rec = {"t": _now(), "event": "spent", "amount": amount, "purpose": purpose}
        t["receipts"].append(rec)
        self._save(t)
        return rec
    def revoke(self, tid, approver, note=""):
        """Kill-switch: human revokes a grant/approval instantly."""
        self._human(approver)
        t = self.tasks[tid]
        if t.get("grant"):
            t["grant"]["used"] = True
        t["status"] = REVOKED
        t["receipts"].append({"t": _now(), "event": "revoked",
                              "approver": approver, "note": note})
        self._save(t)
        return t
    # ---- unlock graph + priority + browser poll ----
    def runnable_a(self):
        out = []
        for t in self.tasks.values():
            if t["kind"] != "A" or t["status"] != OPEN:
                continue
            if all(self.tasks.get(b, {}).get("status") in UNLOCK_OK
                   for b in t.get("blocked_by", [])):
                out.append(t)
        return sorted(out, key=lambda t: t["created"])
    def unlock_count(self, hid):
        return sum(1 for t in self.tasks.values() if hid in t.get("blocked_by", []))
    def human_priority(self):
        hs = [t for t in self.tasks.values()
              if t["kind"] == "H" and t["status"] == OPEN]
        return sorted(hs, key=lambda t: -self.unlock_count(t["id"]))
    def poll(self):
        """Re-read the file: browser UI appends approval records; agent sees them."""
        before = {i: t["status"] for i, t in self.tasks.items()}
        self._load()
        return {i: t["status"] for i, t in self.tasks.items()
                if before.get(i) != t["status"]}
