# A4-v2 method card

- Technical action: P1 threshold rule, P2 monotone bins, P3 confidence fallback over DA/NDA.
- Deployable inputs: current/past received power and hard-decision innovation only.
- Comparator set: fixed DA, fixed NDA, state-continuous 16-APSK DD-DPLL, validation B*, B-cond.
- Identity result: DPLL smoke PASS; mechanism identity FAIL.
- Physical finding: after removing TX-truth ambiguity and mixed denominator, DA wins all 9 validation conditions; NDA BER remains 0.0359–0.1230.
- Cheap alternative: always-DA dominates the proposed DA/NDA selectors at the identity gate.
- Claim ceiling: `BLOCKED_IDENTITY`; no method, boundary, or dB claim is admissible.

