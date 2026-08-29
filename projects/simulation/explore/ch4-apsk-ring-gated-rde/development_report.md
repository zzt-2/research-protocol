# Ch4 gated-RDE bounded development

- Round 2: SKIPPED
- winner: `none`
- provisional grade: `D/STOP_NO_METHOD_SIGNAL`
- runtime: `314.64 s`

- Round-1 stop reasons: `NO_ORACLE_HEADROOM, NO_PREREGISTERED_GATE_SIGNAL`

| cell | B0* | candidate gain | cheap gain | oracle headroom | ring/decision/combined AUROC | candidate vs count-match | cheap vs count-match | underpowered |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| D1 (plain) | 0.0275777 | -6.842% | -5.773% | 0.018% | 0.961/0.786/0.661 | -0.477% | 0.718% | False |
| D2 (plain) | 0.00500488 | -8.333% | -8.232% | -0.152% | N/A/0.921/0.685 | -0.471% | -0.330% | False |
| D3 (plain) | 0.0231501 | -4.251% | -3.559% | -0.055% | 0.973/0.814/0.671 | -0.095% | 0.486% | False |

- Count-matched finding: No apparent gain over B0* existed, so count-matched absorption is not the stopping mechanism.
- Unique next action: stop C4-2 gated-RDE development and return to the master for the preregistered C4-1/C4-0 rotation; do not tune a third gate variant.

Development-only evidence. No confirmation seeds were generated and no final method signal is claimed.
