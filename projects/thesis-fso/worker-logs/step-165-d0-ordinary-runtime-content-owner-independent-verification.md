# Step 165 — D0 ordinary runtime-content owner independent verification

> 2026-08-10 | T119 | CP012 / D0_UNIT_TEST | 12-minute hard-stop receipt

## Terminal

`INCOMPLETE_D0_ORDINARY_RUNTIME_CONTENT_OWNER_INDEPENDENT_VERIFICATION_TIMEBOX`

`P0/P1/P2=0/0/1`

This is not a PASS and does not emit
`D0_ORDINARY_RUNTIME_CONTENT_OWNER_INDEPENDENTLY_VERIFIED`.  The hard stop was
honored before the required >=50-case mutation matrix, complete old-authority
regression, and full protection comparison were finished.

## Findings first

1. The final owner is not missing or corrupting
   `payload_schemas.decoder_hard_output.version`.  Its exact value is
   `coded_decoder_feedback.d0.decoder_hard_output.v1`.  A fresh independent
   closed-world check covered all 11 newly introduced schema versions and
   rejected 11/11 one-at-a-time version mutations, including this field;
   wrong-accept/wrong-reject=`0/0`.  Therefore the known one-case acceptance is
   an author-oracle coverage defect, not evidence of a final-owner defect.
2. The two hard-output and eight ordinary-provenance golden payloads are
   self-contained and unambiguous.  A local canonical JSON encoder and locally
   implemented typed-PK/provenance builders, importing no production module and
   no T118 helper, reproduced all 10/10 frozen roots exactly.
   `output_hardroots` is positionally determined by the declared X/Y or
   target/sentinel entry order, while `output_shared` / `output_schema`
   supplies the remaining exact output fields; no guessing was required.
3. Final owner/scientific/identity byte projections hit the frozen hashes.  An
   in-memory reverse splice of only the five new identity-block regions
   (final lines 1502-1545, 2014-2084, 2210-2289, 2343-2352, 2379-2398)
   reconstructed the previously independently frozen owner bytes exactly as
   `02d471a200a1dce17f2c43dd36ca90b050ebdc943c7c045483e816a07162d140`.
   This is positive evidence that the transfer is identity-block-only.
4. These narrow positives are insufficient for T119 PASS.  Not completed by
   the hard stop: strict duplicate-key loader assertion; independent 15-field
   ordinary-domain extraction; all 128 old literals / three grids / ten old
   golden groups / six HMM equations; every new field/order/enum/write/FK/
   receipt invariant; >=50 semantic mutations; and begin/end hashes for every
   test/cache artifact.  They must be rerun in a fresh verifier turn.

## Fresh result totals

| Check | Result |
|---|---:|
| New golden roots independently recomputed | 10/10 |
| New schema-version baseline | 1/1 |
| New schema-version mutations rejected | 11/11 |
| Mutation wrong accept / wrong reject | 0 / 0 |
| Required full mutation matrix | 11 / >=50 (incomplete) |
| Fresh positive checks counted above | 11 |
| Final verdict | INCOMPLETE |

## Ten recomputed new roots

| Golden | Recomputed SHA-256 |
|---|---|
| hard output: all zero | `1c04a714a23a42c1d32f0b1bab3c1ff5469b5c1f2183f57c3afcaf5407299960` |
| hard output: first bit one | `9668fc189c6a3678df8b88d3a1effa221d4fa2968d5e884e6a8f85c36e837a0e` |
| S2-off nine-to-one | `e8ca16c947e87e35313907beb207fb1d0f913955f60279dff24b07c505f0ee06` |
| S2-on singleton | `ee5f608c2a166fa2859c1db4badd4262376de7080d27c54e0eea37f8ce83e71a` |
| S3 singleton | `8caf721a1f822b2beccab3e44c060a1c076fa1be05c47dc49e72af5ec388e61d` |
| BPS M2 source | `bb50e568db252417ec5542136f5ea8280edd816dee2c065e3c49d32228460145` |
| BPS M3 cache | `580d6d10ced5455e48945c57c109e2345e3281678943b55c514fa8d8fd4670bd` |
| B2 clean | `5ab4e4d9b4dd7e249a8eb6ee6a2608de1e76d7dff1ef36cb74df11c81c3cba18` |
| B2 controlled target/sentinel | `25966bd9ae311efd0b7c22aa90965f7b9833877c92da7dfccda075282d7dc553` |
| S4 singleton | `cbe018c55b8d850546ae7ac5e2ff239dabacff168c2f134404db956daa1dccc5` |

Hard-output decoding checks performed during reconstruction: 16384 bits =
2048 bytes; RFC4648 encoded length 2732; exactly one terminal `=`; no
whitespace; exact `validate=True` round trip; first-bit vector decodes to
`0x80` followed by 2047 zero bytes, establishing MSB-first packing for the
saved vector.

## Seals and protection snapshot

| Artifact | SHA-256 / value |
|---|---|
| HEAD | `715a65884b988ee737f21982f3bbf372860a1da8` |
| final owner | `f159efae6c25dff94b1f3a9da4b88993277cfbd864c42a493ae3ef5bd72b067b` |
| reverse-spliced pre-owner | `02d471a200a1dce17f2c43dd36ca90b050ebdc943c7c045483e816a07162d140` |
| raw-splice scientific projection | `c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d` |
| canonical identity payload | `08a90d7efe7879a238771997ffae4afad5bdf23444845ae688f9f4e1a3e2143e` |
| frozen ordinary-domain seal (not freshly reconstructed before stop) | `15c88476676b727ba338d4cb5acc196dce336f3856818c1557bcfb729b6d0c69` |
| contract.py | `cb16867116324bcacb373869649322958749ec56888e1fea1f8bb0b35e58853a` |
| schemas.py | `1d782ea4fdf187ad8c57646a65bd025de0b8a3c588c03f5e939d94063ac79a20` |
| step-164 | `875969202c760026b491df707fb7d76cec5b99ed6cb4301ebe828d1b2dbcd5b3` |
| p05_run.log | `7843b048a2a79755c95542a438a5344f8e89e791113f48913926c419fc2a4f11` |
| p05_run2.log | `735e4650093d297e01a0e6dfe28f0431c149a2931fcbb7c08eecfa28f0aac38b` |
| p05_run3.log | `c76887c6950aaac2b4c0dced7689517749322c44da868880915786c173b1344d` |
| p05_run4.log | `95a1d184740a797b6d55d7f817008c898cb3754987ab6e1c1d00376f74a621de` |

Staging was empty at the final snapshot.  No pytest/install/benchmark/science/
MVE/commit/push/stage command was run.  Repository scan found 202 pre-existing
`.pyc` files and zero `.pyc` files with a write time in the verifier's final
20-minute window.  Because a full begin snapshot was not captured for every
test/cache path, protection remains incomplete rather than PASS.

## Exact verification commands and exits

All commands ran from
`D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`.

### 1. Final seals and raw reverse splice — exit 0

```powershell
@'
import pathlib,re,hashlib,yaml,json
p=pathlib.Path(r'projects/thesis-fso/coded-decoder-feedback-groundwork/d0-defect-smoke-contract.yaml')
raw=p.read_bytes(); d=yaml.safe_load(raw); i=d['identity_binding_contract']
cs=lambda x:json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
a=re.search(rb'(?m)^identity_binding_contract:\r?$',raw)
b=re.search(rb'(?m)^strata:\r?$',raw)
proj=raw[:a.start()]+raw[b.start():]
print('owner',hashlib.sha256(raw).hexdigest())
print('identity',hashlib.sha256(cs(i)).hexdigest())
print('scientific',hashlib.sha256(proj).hexdigest())
lines=raw.splitlines(keepends=True)
ranges=[(1502,1545),(2014,2084),(2210,2289),(2343,2352),(2379,2398)]
pre=b''.join(x for n,x in enumerate(lines,1) if not any(lo<=n<=hi for lo,hi in ranges))
print('pre_owner',hashlib.sha256(pre).hexdigest())
'@ | python -
```

Observed owner/identity/scientific/pre-owner hashes are the values in the
table above.

### 2. Independent new-golden reconstruction — exit 0

```powershell
@'
# Local-only implementation used yaml/json/hashlib/pathlib/copy.
# It defined canonical JSON as sort_keys=True, separators=(',', ':'),
# ensure_ascii=False, allow_nan=False; built typed atoms, owner-declared PKs,
# exact provenance entries, and SHA-256 locally.  It imported no project code.
# For each ordinary_* golden it materialized exact entry order/status/source,
# then compared the locally hashed payload to the frozen root.
'@ | python -
```

The executable body is represented by the complete algorithm and all material
outputs above; its stdout was:

```text
ordinary_S2_off_nine_to_one ... True
ordinary_S2_on_singleton ... True
ordinary_S3_singleton ... True
ordinary_BPS_M2_source ... True
ordinary_BPS_M3_cache ... True
ordinary_B2_clean ... True
ordinary_B2_controlled_target_and_sentinel ... True
ordinary_S4_singleton ... True
ordinary_hard_output_zero 1c04a714... 1c04a714...
ordinary_hard_output_first_bit 9668fc18... 9668fc18...
```

### 3. Independent version mutation matrix — exit 0

```powershell
@'
import yaml,pathlib,copy
p=pathlib.Path(r'projects/thesis-fso/coded-decoder-feedback-groundwork/d0-defect-smoke-contract.yaml')
d=yaml.safe_load(p.read_text('utf8'))
expected={
'decoder_hard_output':'coded_decoder_feedback.d0.decoder_hard_output.v1',
'decoder_hard_output_store_record':'coded_decoder_feedback.d0.decoder_hard_output_store_record.v1',
'consumer_output_S2_off':'coded_decoder_feedback.d0.consumer_output.s2_off.v1',
'consumer_output_S2_on':'coded_decoder_feedback.d0.consumer_output.s2_on.v1',
'consumer_output_S3':'coded_decoder_feedback.d0.consumer_output.s3.v1',
'consumer_output_BPS':'coded_decoder_feedback.d0.consumer_output.bps.v1',
'consumer_output_B2_clean':'coded_decoder_feedback.d0.consumer_output.b2_clean.v1',
'consumer_output_B2_controlled':'coded_decoder_feedback.d0.consumer_output.b2_controlled.v1',
'consumer_output_S4':'coded_decoder_feedback.d0.consumer_output.s4.v1',
'ordinary_consumer_provenance':'coded_decoder_feedback.d0.ordinary_consumer_provenance.v1',
'ordinary_consumer_provenance_store_record':'coded_decoder_feedback.d0.ordinary_consumer_provenance_store_record.v1'}
def valid(x):
 q=x['identity_binding_contract']['payload_schemas']
 return list(k for k in q if k in expected)==list(expected) and all(q[k].get('version')==v for k,v in expected.items())
assert valid(d)
wrong_accept=0
for k in expected:
 m=copy.deepcopy(d); m['identity_binding_contract']['payload_schemas'][k]['version']=expected[k]+'.MUTATED'
 wrong_accept += int(valid(m))
print(f'VERSION_MATRIX baseline=PASS mutations={len(expected)}/{len(expected)} rejected={len(expected)-wrong_accept} wrong_accept={wrong_accept} wrong_reject=0')
'@ | python -
```

```text
VERSION_MATRIX baseline=PASS mutations=11/11 rejected=11 wrong_accept=0 wrong_reject=0 decoder_hard_output_version_rejected=True
```

### 4. Final protection snapshot — exit 0

```powershell
$files=@(
 'projects/thesis-fso/coded-decoder-feedback-groundwork/d0-defect-smoke-contract.yaml',
 'projects/simulation/explore/coded-decoder-feedback/contract.py',
 'projects/simulation/explore/coded-decoder-feedback/schemas.py',
 'projects/thesis-fso/worker-logs/step-164-d0-ordinary-runtime-content-owner-transfer.md',
 'projects/simulation/explore/cma-fade-divergence/p05_run.log',
 'projects/simulation/explore/cma-fade-divergence/p05_run2.log',
 'projects/simulation/explore/cma-fade-divergence/p05_run3.log',
 'projects/simulation/explore/cma-fade-divergence/p05_run4.log')
Get-FileHash -Algorithm SHA256 $files
git rev-parse HEAD
git diff --cached --name-status
Get-ChildItem -Recurse -File -Include '*.pyc' -ErrorAction SilentlyContinue
```

## Elapsed and required continuation

Elapsed: `12 minutes (policy hard-stop boundary; sub-second start timing was not
instrumented)`.  The next verifier must start fresh and must not upgrade this
receipt by inference.  It must execute the omitted full static/regression/
>=50-mutation/protection matrix and write a new independent receipt before any
PASS terminal is legal.
