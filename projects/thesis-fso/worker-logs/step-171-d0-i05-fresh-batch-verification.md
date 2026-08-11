# Step 171 — D0 I05 fresh batch verification

> 2026-08-11 | T125 | independent final-byte verifier | `D0_I05_FRESH_BATCH_VERIFIED`

## Boundary and terminal

- Terminal: `D0_I05_FRESH_BATCH_VERIFIED`.
- Scope: CP012 I05 implementation/unit only. D0 science remains `NOT_RUN`; this result does not authorize benchmark, MVE, or science.
- Verifier did not modify production, owner, tests, session, P05 logs, cache, staging, or git history. The only verifier write is this receipt.

## Frozen-byte and protection checks

Pre/post checks used `git rev-parse HEAD`, `git diff --cached --name-only`, `Get-FileHash -Algorithm SHA256`, and cache-filtered `git status --short`.

| Artifact | SHA-256 | Result |
|---|---|---|
| HEAD | `715a65884b988ee737f21982f3bbf372860a1da8` | exact |
| owner YAML | `f159efae6c25dff94b1f3a9da4b88993277cfbd864c42a493ae3ef5bd72b067b` | exact |
| `contract.py` | `f6e000dcddd8661d2b52ea08de6c2a137cf7fd8f661d2ca415e9b56227ff1aaa` | exact |
| `schemas.py` | `d5bb1bbc8e8bfeba1f057ea87f57b2fb4713fdd1f852bbe40df0a531f6cc29db` | exact |
| `codec.py` | `5c45cf1765a3a9f295105da7fba284d4509de053c414739a2e4a86232b9f4331` | exact |
| contract / ordinary / codec / statistics / waveform tests | `8fa721a984f83b89c410dad93a6e061d381562268a2a72f57f42b20d5035ac8f` / `ef0b2b7e7b70d1add0fc0e45180455a857cf5d38f9eb58b7ce06d4ea4d04d234` / `28401d747ff13143ca828753cf910aac88974f52e0d672edc96d2916767a6d6e` / `ad8065661452fd1f130c191404e9495f4d9d990a2f66286a5fb977925f278510` / `f14cac811b0c68458eb62bbd37578d5dcf592c97cbd4c2ae92765d2e897e01e1` | all exact |
| step-170 | `6a6a7c247ea57bd0a38102d2bec4dde7573feaca4410e0101317da5538435491` | exact |
| P05 logs 1–4 | `7843b048a2a79755c95542a438a5344f8e89e791113f48913926c419fc2a4f11` / `735e4650093d297e01a0e6dfe28f0431c149a2931fcbb7c08eecfa28f0aac38b` / `c76887c6950aaac2b4c0dced7689517749322c44da868880915786c173b1344d` / `95a1d184740a797b6d55d7f817008c898cb3754987ab6e1c1d00376f74a621de` | all exact |

Staging was `0` before and after. No new simulation `__pycache__`, `.pyc`, or `.pytest_cache` appeared.

## Independent spot oracle

An inline Python oracle read the frozen owner YAML directly and used only `yaml`, `json`, `base64`, and `hashlib`; it did not import production or test helpers.

- Hard output: both payloads decode to exactly 2048 bytes = 16 x 1024 binary bits; zero has no nonzero byte; first-bit has byte 0 = `0x80` and all remaining bytes zero, independently confirming CW-major/MSB-first and strict RFC4648 decode. Recanonicalized roots exactly match `1c04a714a23a42c1d32f0b1bab3c1ff5469b5c1f2183f57c3afcaf5407299960` and `9668fc189c6a3678df8b88d3a1effa221d4fa2968d5e884e6a8f85c36e837a0e`.
- Ordinary: records/entries/executed/cache = `27487/42967/30247/12720`; cache edges = `480/1440/10800`; groups = `12427/60/15000`; aggregate executed/cache = `26767/720`; non-S4 hard-output FKs = `42960`. The executed public matrix also matched all 8 owner provenance goldens and direct-source/leaf plus hard-store-FK gates.
- HMM: trajectories/chunks/executed/cache = `22800/263520/9600/13200`; exact-rational check yielded numerator `123456789`, denominator power `42`, content root `9cf9e195032aea53840d164ac36c7c455cfcf997202867c0e6d38864a5b1a0c2`. Four owner roots matched: `d6efb6...c1c7`, `4721d0...79e9`, `25aaaa...dd7`, `0e204f...9eef` (full values are asserted by the executed frozen test).
- FULL: exact ledger `27487 + 22800 = 50287`; authority `6616784457eb4ae1fc3d1324ed12320aeb9a3cceb946f220c29615bc87b73484`.

## Actual five-file regression

Environment: `PYTHONDONTWRITEBYTECODE=1`, `PYTHONHASHSEED=0`.

```powershell
C:\Users\zzt\scoop\apps\python311\current\python.exe -B -m pytest -p no:cacheprovider -q -s projects/simulation/tests/test_d0_contract_views.py projects/simulation/tests/test_d0_ordinary_identity.py projects/simulation/tests/test_d0_receiver_codec_methods.py projects/simulation/tests/test_d0_schemas_statistics.py projects/simulation/tests/test_d0_waveform_channel.py
```

- Exit: `0`; `71 passed in 686.12s`; wrapper wall `689.024s`; fail/skip = `0/0`.
- FULL positive completed: incremental `17.895242s`; ordinary deep-recompile calls `0`; authority exact; 10/10 FULL deep/clone mutations rejected.
- Captured stdout SHA-256 (UTF-8 PowerShell `Out-String`): `e82887374c8bfb9e5d92ee6ba1ec8248565098d1b20475c0cad3836fe26392f1`.

Executed I05 negative/mutation matrix totals `118`: loader `42`; hard-output opaque/factory/store `16`; ordinary output/runtime `18`; ordinary identity `24`; domain/seal `8`; FULL clone/deep/count/owner/content/status/store `10`. Wrong accepts/rejects = `0/0`. This covers unissued clone, entry/output/root, ledger content/status, hard store, count, and owner mismatch fail-closed cases.

## Findings

- P0: `0`
- P1: `0`
- P2: `0`

I05 implementation/unit is independently accepted on the frozen bytes above. Science signal remains `NONE` because no science run occurred.
