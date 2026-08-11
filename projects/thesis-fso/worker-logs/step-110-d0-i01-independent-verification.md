# Step 110 — D0 I01 fresh independent verification

> 2026-08-10 | T064 / D011 / V005 / CP012 / epoch 12 | INDEPENDENT VERIFICATION
> Evidence worktree: `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`
> Candidate was not modified. No benchmark/science, commit, push, web, search or download was run.

## 1. Verdict and findings

```text
VERDICT=PASS
P0_P1_P2=0/0/0
TERMINAL=I01_VERIFIED_READY_FOR_I02
```

No actionable finding was found within I01/CV01–CV03. The historical RED
chronology is accepted only at the evidence level stated in section 5; this
report does not promote the executor's self-report into immutable historical
proof.

## 2. Frozen input and protection preflight

All T064 frozen inputs matched byte-for-byte:

```text
contract.py=a782287246a64f584ef88594f671350d0a4036746cf8dec37337194382054775
test_d0_contract_views.py=3d411c35be5ed01e007c92ea6a4488e200eb3053203ef56915cf9eed597ef9e1
step-109=c85d1a2e2fd52750519a3cf8bf48c869fa4e9f5614ea53f546aa46ca0c0d430b
owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
plan=52322d1374a5385f93d6df833aaca7dd2e7431912d2e751449f1c3de1cc9fd7b
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
branch=codex/rdl-method-production-v2
staging_count=0
step110_initial=ABSENT
```

Preflight cache census was `202` `.pyc`, `41` `__pycache__` directories and
`4` `.pytest_cache` directories. Exactly the same ten tracked dirty cache
paths reported by step-109 were present under `tools/litdownload` and
`tools/litsearch`; none was touched. The preflight porcelain status, encoded
as UTF-8 after `Out-String`, had SHA256
`f8190b99641291c96346cc6c47f23189c124b142a4b46d750afd4f30e1d89d61`.

Protected p05 hashes at preflight:

```text
p05_run.log=7843b048a2a79755c95542a438a5344f8e89e791113f48913926c419fc2a4f11
p05_run2.log=735e4650093d297e01a0e6dfe28f0431c149a2931fcbb7c08eecfa28f0aac38b
p05_run3.log=c76887c6950aaac2b4c0dced7689517749322c44da868880915786c173b1344d
p05_run4.log=95a1d184740a797b6d55d7f817008c898cb3754987ab6e1c1d00376f74a621de
```

## 3. Static audit

The reviewer read T064, plan I01, step-106 CV01–CV03, owner control /
population / seed plan, T063, the step-105 contract interface, all 383 lines
of `contract.py`, all three tests and complete step-109.

| Check | Independent result |
|---|---|
| Exact test surface | Exactly three top-level tests exist, with the three T064 names. No skip/xfail/parametrized dilution. |
| Non-tautological oracles | Control identity/permissions, population values/product and eight seed ranges are literal expectations in the test; expected values are not imported or derived from production constants. The frozen owner SHA independently binds the source identity. |
| Duplicate YAML keys | `_StrictLoader` installs the unique-mapping constructor for the default mapping tag, so nested mappings are covered; the OS-temp nested mutation probe rejected a duplicated `control.topic`. |
| Frozen/value semantics | All seven contract value types are `@dataclass(frozen=True, slots=True)`; loader materializes tuples/frozen child values. |
| Population | Owner loads exact Gray-square-16QAM, `2.5e9`, 1024/1536/16/384/6144/20 and the literal 4×3 product. The resulting 12 cell IDs and `(snr, linewidth)` pairs are unique. |
| Seeds | All eight inclusive ranges match the owner, endpoints are exercised, pairwise intersections are empty, and natural first-stage `8100..8119` is a proper subset of `8100..8149`. Wrong membership, out-of-range seed and unknown label fail closed. Construction-time overlap rejection was independently probed. |
| CP012 action gate | Allowlist is finite and explicit. Implementation, unit, engineering benchmark, source audit and static check are the only mapped actions; unknown/scientific/runtime actions are denied by default. Authorization is additionally bound to v3/epoch12/CP012/D011/V005. |
| Numeric boundary | Field-local conversion exists only for the positive finite symbol rate. `nan`, `inf`, zero and negative values reject; owner spelling `2.5e9` becomes exactly `2500000000.0`. |
| Import/I/O boundary | AST scan found no production `sys.path` reference and exactly one path-I/O call: `Path.open` inside explicit `load_contract` at line 265. The only module-level expression call is strict-loader constructor registration; it performs no contract load or repository I/O. Test-local D0-root insertion is the exact T063-authorized import seam. |
| Scope | Production imports only stdlib plus PyYAML; no ReceiverView, runner, science/estimand implementation, benchmark CLI, `__main__` guard or result writer exists. |

AST audit summary:

```json
{"dataclasses":["ControlContract","CodeLayout","PhysicalCell","PopulationContract","InclusiveSeedRange","SeedRegistry","D0Contract"],"frozen_slots":"7/7","module_contract_construction":0,"path_io_calls":[{"call":"open","line":265}],"prod_sys_path_refs":0,"test_count":3}
```

## 4. Fresh unit verification

Exact candidate command:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; $env:PYTHONHASHSEED='0'
& 'C:\Users\zzt\scoop\apps\python311\current\python.exe' -B -m pytest -p no:cacheprovider 'projects/simulation/tests/test_d0_contract_views.py' -q
```

Result:

```text
exit_code=0
normalized_utf8_lf_stdout_sha256=1d3314562a9345a9f75b1adf32d61168822c00d316f7db85833230bba023e448
...                                                                      [100%]
3 passed in 0.15s
```

The complete file therefore has `passed=3`, `failed/errors=0`, and no skip,
xfail or warning summary (`0/0/0`).

## 5. TDD chronology reconstruction and evidence level

Current test SHA equals both the RED receipt test SHA and the final GREEN
test SHA (`3d411c...fd9e1`). Current production, owner and step-109 SHAs also
match their frozen values. Step-109 is internally chronological: it records
the test before production, a shared first-import `ModuleNotFoundError`, an
unchanged-test parser failure, and then GREEN. Current filesystem metadata is
corroborative: test creation `2026-08-10T06:29:24.4944040Z`, step-109 creation
`06:30:56.0561331Z`, and production creation `06:32:34.2023359Z`; all three
targets remain untracked.

Evidence level is `DOCUMENT_INTERNAL_CONSISTENCY_PLUS_MUTABLE_FILESYSTEM_METADATA`.
There is no separately persisted immutable RED stdout artifact or pre-production
tree snapshot, so historical `contract.py=ABSENT` and the recorded RED stdout
SHA cannot be independently replayed as historical facts. They remain a
self-report supported, but not proved, by the current identical test hash and
creation-order metadata. T064 explicitly requires this limitation to be stated;
it is not counted as an implementation finding.

## 6. OS-temp mutation probes

The following exact probe ran with `PYTHONDONTWRITEBYTECODE=1`,
`PYTHONHASHSEED=0`, Windows Python 3.11.9 and `-B`. It used
`tempfile.TemporaryDirectory`; no probe file was written in the repository.

```powershell
$probe=@'
import importlib.util, json, sys, tempfile
from pathlib import Path
root=Path(r"D:\code\study\research-protocol\.worktrees\rdl-method-production-v2")
source_path=root/"projects/simulation/explore/coded-decoder-feedback/contract.py"
owner_path=root/"projects/thesis-fso/coded-decoder-feedback-groundwork/d0-defect-smoke-contract.yaml"
spec=importlib.util.spec_from_file_location("d0_i01_contract_probe",source_path)
module=importlib.util.module_from_spec(spec); sys.modules[spec.name]=module; spec.loader.exec_module(module)
owner_text=owner_path.read_text(encoding="utf-8"); results=[]
def expect_reject(name,exc_type,operation,contains):
    try: operation()
    except exc_type as exc:
        message=str(exc)
        if contains not in message: raise AssertionError(f"{name}: wrong message {message!r}")
        results.append({"probe":name,"result":"REJECTED","exception":type(exc).__name__,"message":message})
    else: raise AssertionError(f"{name}: unexpectedly accepted")
with tempfile.TemporaryDirectory(prefix="d0_i01_verify_") as td:
    temp=Path(td); duplicate_path=temp/"duplicate_nested.yaml"
    needle="  topic: .sessions/2026-08-09-coded-decoder-feedback-groundwork\n"
    if owner_text.count(needle)!=1: raise AssertionError("nested duplicate mutation anchor not unique")
    duplicate_path.write_text(owner_text.replace(needle,needle+"  topic: duplicate_nested\n",1),encoding="utf-8")
    expect_reject("duplicate_nested_key",module.ContractError,lambda:module.load_contract(duplicate_path),"duplicate YAML key: topic")
    expect_reject("overlap_registry_construction",module.ContractError,lambda:module.SeedRegistry(entries=(("natural_occurrence",module.InclusiveSeedRange(8100,8149)),("overlap",module.InclusiveSeedRange(8149,8159))),first_stage_natural=module.InclusiveSeedRange(8100,8119)),"overlapping seed ranges")
    loaded=module.load_contract(owner_path)
    expect_reject("unknown_action",PermissionError,lambda:module.assert_action_authorized("UNKNOWN_ACTION",loaded),"not authorized under CP012")
    rate_anchor="    symbol_rate_baud: 2.5e9\n"
    if owner_text.count(rate_anchor)!=1: raise AssertionError("population symbol-rate mutation anchor not unique")
    for label,token in (("nan","nan"),("inf","inf"),("zero","0"),("negative","-1")):
        mutated_path=temp/f"symbol_rate_{label}.yaml"
        mutated_path.write_text(owner_text.replace(rate_anchor,f"    symbol_rate_baud: {token}\n",1),encoding="utf-8")
        expect_reject(f"symbol_rate_{label}",module.ContractError,lambda p=mutated_path:module.load_contract(p),"positive finite number")
    if loaded.population.symbol_rate_baud!=2500000000.0: raise AssertionError(f"owner symbol rate changed: {loaded.population.symbol_rate_baud!r}")
    results.append({"probe":"owner_symbol_rate_2.5e9","result":"ACCEPTED_EXACT","value":loaded.population.symbol_rate_baud})
for row in results: print(json.dumps(row,sort_keys=True,separators=(",",":")))
print(json.dumps({"summary":"8/8 probes passed","repo_writes":0},sort_keys=True,separators=(",",":")))
'@
& 'C:\Users\zzt\scoop\apps\python311\current\python.exe' -B -c $probe
```

```text
exit_code=0
normalized_utf8_lf_stdout_sha256=a26fe9b92fe74662d557aaaf25897711e4a1121812fdc86f3070727ccb0c2b4e
duplicate_nested_key=REJECTED ContractError duplicate YAML key: topic
overlap_registry_construction=REJECTED ContractError overlapping seed ranges: natural_occurrence and overlap
unknown_action=REJECTED PermissionError action UNKNOWN_ACTION is not authorized under CP012
symbol_rate_nan=REJECTED ContractError
symbol_rate_inf=REJECTED ContractError
symbol_rate_zero=REJECTED ContractError
symbol_rate_negative=REJECTED ContractError
owner_symbol_rate_2.5e9=ACCEPTED_EXACT value=2500000000.0
summary=8/8 probes passed; repo_writes=0
```

## 7. Final protection receipt

The final post-log check found the frozen candidate/test/owner/plan/step-109
hashes unchanged, branch/HEAD unchanged, staging `0`, and the same cache census
`202 / 41 / 4` with the same ten dirty cache paths. Removing the single
`?? projects/thesis-fso/worker-logs/step-110-d0-i01-independent-verification.md`
line from final porcelain status reproduced the preflight status SHA exactly;
therefore this log is the only path added by this verifier.

Protected p05 hashes remained 4/4 exact:

```text
p05_run.log=7843b048a2a79755c95542a438a5344f8e89e791113f48913926c419fc2a4f11
p05_run2.log=735e4650093d297e01a0e6dfe28f0431c149a2931fcbb7c08eecfa28f0aac38b
p05_run3.log=c76887c6950aaac2b4c0dced7689517749322c44da868880915786c173b1344d
p05_run4.log=95a1d184740a797b6d55d7f817008c898cb3754987ab6e1c1d00376f74a621de
```

No candidate, owner, test, governance, p05 or cache file was modified; no
benchmark/scientific runner was invoked; no commit or push occurred.
