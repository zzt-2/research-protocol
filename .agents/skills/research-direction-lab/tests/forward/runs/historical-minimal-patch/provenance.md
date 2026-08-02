# Auditable replay provenance

## Skill identities

- RED: immutable Git tree `53085bb5d1b7cc3e759e62af5c55397979402acc`; reproducible bundle is defined in `baseline-manifest.md`.
- GREEN policy owner bundle: `73cc05da288458ad40ca4cb9a41b504da760918c9bdcec85de8b6904021475a3`.
- GREEN policy serialization: SHA256 of UTF-8 lines `<file_sha256><two spaces><relative_path><LF>`, sorted over `SKILL.md`, `references/evidence-and-claims.md`, `references/long-horizon-control.md`, `references/method-production.md`, and `references/thesis-harvest.md`.

## Prompt identities and fresh contexts

Every accepted replay used `fork_turns=none`, a distinct agent task, the same case prompt for RED and GREEN, and a strict evidence allowlist. The raw adjudication records the actual paths read.

| Case | Prompt SHA256 | RED agent/output | GREEN agent/output |
|---|---|---|---|
| 1 | `34976697ff59e2091d4bc852fe9a7a64c7d5f095b2e78480c20c36cdc6f295df` | `/root/audit_red_case1` → `audit-red-case1.md` | `/root/audit_green_case1` → `audit-green-case1.md` |
| 2 | `b16e7dd6ac9b0256fe23cea2dc68a0e9fccd12ec9f884c357fb10a595edaa28e` | `/root/audit_red_case2_clean` → `audit-red-case2.md` | `/root/audit_green_case2` → `audit-green-case2.md` |
| 3 | `46e6148fb7f397cbfe616f7a81be23c52b3bccb9e8a0d742b885a1af214561c6` | `/root/audit_red_case3_clean` → `audit-red-case3.md` | `/root/audit_green_case3` → `audit-green-case3.md` |
| 4 | `072feb294a8b091ebcf616184bde1c9b26a8a7aae9cf0cb5e046239892fc8d60` | `/root/audit_red_case4` → `audit-red-case4.md` | `/root/audit_green_case4` → `audit-green-case4.md` |
| 5 | `d84a13c4bde9914e31671f1b20ef786a8b721c657addc302d718fe17a3b79f31` | `/root/audit_red_case5` → `audit-red-case5.md` | `/root/audit_green_case5` → `audit-green-case5.md` |
| 6 | `3ef9ec2c5b73e7da0a34ffac1083b8297088d792f6b24df21ebd9d099d01bf46` | `/root/audit_red_case6` → `audit-red-case6.md` | `/root/audit_green_case6` → `audit-green-case6.md` |

The discarded `/root/audit_red_case2` and `/root/audit_red_case3` attempts expanded result directories and observed colocated later invalidation markers. They are not saved as accepted replay evidence; clean agents reran those cases from the narrowed per-file prompts.

## Chronological legacy outputs

`red-case*.md`, `green-case*.md`, and `green-case1-refactor.md` are preserved as the chronological modification-before/after record. They predate this provenance scheme and therefore are not the authoritative fresh-context audit replay. In particular:

- `green-case1.md` was superseded first by `green-case1-refactor.md`, then by `audit-green-case1.md`.
- `green-case6.md` incorrectly retained P11 as 9–15 dB material and is superseded by `audit-green-case6.md`, which traces the fixed 20 dB generator path.
- The chronological RED Case 1 contains the observed old-Skill rationalization that motivated the executable scale/action refinement. The strict replay is nondeterministic and reached STOP independently; this does not rewrite the original raw output.
