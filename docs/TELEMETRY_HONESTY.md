# TELEMETRY HONESTY — what our numbers are and aren't

Every token count we record arrives in a usage block written by the party that
bills us. Current research says to treat those numbers as **claims**:

- Hidden-reasoning inflation is undetectable without TEEs/proofs, up to ~1469%
  in adversarial settings (CoIn; Token Inflation 2605.30040). Even visible text
  allows ~50% over-reporting via tokenization ambiguity.
- Martingale auditors (2510.05181) and predictive estimators (PALACE) detect
  *patterns* of inflation, not individual bills. IMMACULATE-style spot proofs are
  the only direction with teeth, and need provider cooperation.

Our posture, encoded in `telemetry.py`:

1. `usage_source` is always `"reported"` — never "verified".
2. Record verbatim; reconcile spend against provider invoices monthly.
3. Unknown models record tokens with cost null — never guessed prices.
4. Budgets are brakes (refuse the next call past the cap), not ledgers.
5. Blind-review + sealed maps protect *our* judgments from *our* biases; they say
   nothing about provider honesty. Different problem, don't conflate them.
