# Historical minimal-patch behavior comparison

> The chronological raw outputs below are preserved unchanged. Their old ad-hoc bundle hash was `91f306ef72b54dc883b52a9683629b4dff54a0f6ce985d22bd34c33e3822f1ab`; the independently reproducible RED identity is `fbd44ac762114e54f2f6fae90226487ff0748a43c1fa6e8ba57ff9b521274a87` as defined by `baseline-manifest.md`.
> `provenance.md` and `audit-{red,green}-case*.md` are the authoritative same-prompt, fresh-context audit replay. Legacy `green-case1.md` and `green-case6.md` are explicitly superseded there.

| Case | RED old Skill | GREEN patched Skill | Result |
|---|---|---|---|
| 1 scale/action | Blocked immediate scaling but called the implementation boundary “basically reasonable” and left a direct path to `METHOD_SIGNAL` without scale/evaluator decomposition. | Blocks scaling and signal freeze until executable semantic evidence exists; records `NONE`/`SUPPORTING_MATERIAL`. Refactor adds invariant downstream evaluation for normalization actions. | PASS; real RED failure changed. |
| 2 hidden truth | Already traced the indirect hidden-truth call path and returned `EXECUTION_INVALID`. | Repeats the recursive caller-to-callee finding and explicitly requires the metamorphic gate. | PASS; no fabricated RED failure. |
| 3 cost/action | Already discovered full execution followed by an under-reported counter and the symmetry-domain comparator gap. | Uses `real_action_and_cost` explicitly and rejects additional statistics as a repair. | PASS; no fabricated RED failure. |
| 4 evidence coverage | Already refused to close the campaign from the local development probe. | Also fails the unbound executor receipt and keeps closure unestablished. | PASS; local Probe is not a package/campaign closure. |
| 5 parameter injection | Already traced the missing parameter and fixed default, and rejected pooled multi-condition evidence. | Names `parameter_injection` FAIL, requires a sentinel, and keeps the asset diagnostic. | PASS; no fabricated RED failure. |
| 6 packaging | Already kept negative/partial/invalid items out of main methods and declined another count-driven package. | The authoritative audit emits the exact three tiers, admits real engineering components, keeps active carriers empty, traces P11 to fixed 20 dB, reports strategic shortage, and declines P12. | PASS; clearer contract without suppressing engineering value. |

The contribution-tier patch is supported by the chronological Case 1 mis-promotion language and the historical packaging drift; strict replay also shows that old behavior was partly nondeterministic rather than six-for-six broken. Case 6 demonstrates that the patch preserves engineering value while excluding invalidated evidence. The persistence patch is supported by the real topic expansion documented in the closeout audit, not by inventing a behavioral failure in these read-only tasks.
