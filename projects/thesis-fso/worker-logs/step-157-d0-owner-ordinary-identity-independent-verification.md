# Step 157 — D0 owner ordinary identity independent verification

> 2026-08-10 | T111 | pending fresh execution

## Fresh verifier source

```python
from __future__ import annotations
import copy, hashlib, json, pathlib, re, subprocess, sys
from itertools import product
import yaml

ROOT = pathlib.Path.cwd()
OWNER = ROOT / "projects/thesis-fso/coded-decoder-feedback-groundwork/d0-defect-smoke-contract.yaml"
SELF = ROOT / "projects/thesis-fso/worker-logs/step-157-d0-owner-ordinary-identity-independent-verification.md"
FINAL_OWNER = "02d471a200a1dce17f2c43dd36ca90b050ebdc943c7c045483e816a07162d140"
PRE_OWNER = "ca2c8146dec5edec62984cdadf678d808291cb6b2a736fd99059651fc7a50535"
HEAD = "715a65884b988ee737f21982f3bbf372860a1da8"
SCIENCE = "c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d"

class UniqueLoader(yaml.SafeLoader): pass
def unique_map(loader, node, deep=False):
    out = {}
    for k, v in node.value:
        key = loader.construct_object(k, deep=deep)
        if key in out: raise ValueError(f"duplicate YAML key: {key!r}")
        out[key] = loader.construct_object(v, deep=deep)
    return out
UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_map)

def canon(x): return json.dumps(x, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode()
def sha_bytes(b): return hashlib.sha256(b).hexdigest()
def sha_file(p): return sha_bytes(pathlib.Path(p).read_bytes())
def digest(x): return sha_bytes(canon(x))
def atom(t, v): return {"type": t, "value": v}
def fentry(name, t, v): return {"name": name, "atom": atom(t, v)}
def desc(name, source=None, typ="str"): return {"name": name, "source": source or f"raw.{name}", "atom_type": typ}
def ds(spec): return [desc(n, s, t) for n, s, t in spec]
def pk(table, fields): return {"schema":"coded_decoder_feedback.d0.consumer_primary_key.v1", "table":table, "fields":fields}
def wk(kind, fields): return {"schema":"coded_decoder_feedback.d0.typed_work_key.v1", "kind":kind, "fields":fields}
def logical(phase, operation, work):
    payload={"schema":"coded_decoder_feedback.d0.logical_computation_identity.v1","phase":phase,"operation":operation,"work_key":work}
    return "d0c1-"+digest(payload)

ASSERTIONS=0
def ck(cond, msg):
    global ASSERTIONS
    ASSERTIONS += 1
    if not cond: raise AssertionError(msg)
def eq(a,b,msg): ck(a==b, f"{msg}: {a!r} != {b!r}")

raw0=OWNER.read_bytes(); begin_owner=sha_bytes(raw0)
doc=yaml.load(raw0, Loader=UniqueLoader); ident=doc["identity_binding_contract"]

# Frozen header, exact 13-section identity shape, and the only permitted aliases.
eq(begin_owner, FINAL_OWNER, "owner begin SHA")
eq(list(ident), ["schema_version","decision_ref","scientific_contract_change","canonical_serialization","grid_authority","payload_schemas","hmm_authority","ledger_accounting","cache_source","consumer_bindings","runtime_content","golden_vectors","validator_obligations"], "identity sections")
eq(ident["schema_version"], "coded_decoder_feedback.d0.identity_binding.v1", "identity schema")
eq((doc["schema_version"],doc["status"],doc["date"]),("coded_decoder_feedback.d0.v3","verified_frozen_for_d0_implementation_and_unit_test","2026-08-10"),"owner header")
eq((doc["control"]["epoch"],doc["control"]["checkpoint"],doc["control"]["action_class"],doc["control"]["execution_authorized"]),(12,"CP012","D0_TESTBED_IMPLEMENTATION",False),"permission header")
eq((raw0.count(b"&id001"),raw0.count(b"&id002"),raw0.count(b"*id001"),raw0.count(b"*id002")),(1,1,1,1),"alias census")
eq(set(re.findall(rb"[&*]id\d+",raw0)),{b"&id001",b"&id002",b"*id001",b"*id002"},"alias policy")

# Independent D017 descriptor oracle, built only from D017 and outer owner PKs.
S2PK=ds([("record_type",None,"str"),("seed",None,"int"),("cell_id",None,"str"),("target_polarization",None,"str"),("fixture_id",None,"str"),("jump_present",None,"bool"),("method_id",None,"str")])
S2OFFWK=ds([("seed",None,"int"),("cell_id",None,"str"),("target_polarization",None,"str"),("jump_present",None,"bool"),("method_id",None,"str"),("canonical_owner_fixture_id","literal.B04_K1","str")])
S2ONWK=ds([("seed",None,"int"),("cell_id",None,"str"),("target_polarization",None,"str"),("fixture_id",None,"str"),("jump_present",None,"bool"),("method_id",None,"str")])
S3PK=ds([("record_type",None,"str"),("seed",None,"int"),("cell_id",None,"str"),("target_polarization",None,"str"),("fixture_id",None,"str"),("candidate_id",None,"str")])
S3WK=ds([("record_type_as_split","raw.record_type","str"),("seed",None,"int"),("cell_id",None,"str"),("target_polarization",None,"str"),("fixture_id",None,"str"),("candidate_id",None,"str")])
BPSPK=ds([("record_type",None,"str"),("tuple_id",None,"str"),("B",None,"int"),("Nw",None,"int"),("seed",None,"int"),("cell_id",None,"str"),("polarization",None,"str")])
BPSWK=ds([("tuple_id",None,"str"),("B",None,"int"),("Nw",None,"int"),("seed",None,"int"),("cell_id",None,"str")])
B2CPK=ds([("record_type",None,"str"),("tuple_id",None,"str"),("seed",None,"int"),("cell_id",None,"str"),("polarization",None,"str")])
B2CWK=ds([("tuple_id",None,"str"),("seed",None,"int"),("cell_id",None,"str")])
B2TPK=ds([("record_type",None,"str"),("tuple_id",None,"str"),("seed",None,"int"),("cell_id",None,"str"),("target_polarization",None,"str"),("fixture_id",None,"str"),("row_polarization",None,"str")])
B2TWK=ds([("tuple_id",None,"str"),("seed",None,"int"),("cell_id",None,"str"),("target_polarization",None,"str"),("fixture_id",None,"str")])
S4PK=ds([("record_type",None,"str"),("check_id",None,"str")]); S4WK=ds([("check_id",None,"str")])
HMMPK=ds([("record_type",None,"str"),("tuple_id",None,"str"),("p_s_index",None,"int"),("sigma_e2_index",None,"int"),("stratum_role",None,"str"),("cell_id",None,"str"),("polarization",None,"str"),("chunk_id",None,"str")])
lit=lambda v:{"kind":"literal","value":v}
expected={
"S2_off":{"exact_binding_kind":"LOGICAL_COMPUTATION_ID","table":"s2_method","consumer_pk_order":[x["name"] for x in S2PK],"consumer_pk_fields":S2PK,"phase_rule":lit("S2"),"operation_rule":lit("B1_DECODE"),"work_key_kind":"S2_B1_OFF_CANONICAL_B04","work_key_order":[x["name"] for x in S2OFFWK],"work_key_fields":S2OFFWK,"omitted":["fixture_id"],"canonical_owner_fixture_id":"B04_K1","cardinality":"nine_fixture_rows_to_one_logical_id"},
"S2_on":{"exact_binding_kind":"LOGICAL_COMPUTATION_ID","table":"s2_method","consumer_pk_fields":S2PK,"phase_rule":lit("S2"),"operation_rule":{"kind":"enum_map","source":"raw.method_id","values":{"GLOBAL_FOUR_ROTATION_DECODER_SELECTION":"B1_DECODE","OFC17_16QAM_EXTFRAME_V1":"B2_DECODE","TRUTH_BOUNDARY_ROTATION_CORRECTION":"O1_DECODE"}},"work_key_kind":"S2_ON_METHOD_DECODE","work_key_order":[x["name"] for x in S2ONWK],"work_key_fields":S2ONWK,"preserved":["fixture_id","method_id"]},
"S3":{"exact_binding_kind":"LOGICAL_COMPUTATION_ID","table":"s3_candidate","consumer_pk_fields":S3PK,"phase_rule":{"kind":"enum_map","source":"raw.record_type","values":{"S3_CANDIDATE_DEV":"S3_DEV","S3_CANDIDATE_TEST":"S3_TEST"}},"operation_rule":lit("CANDIDATE_DECODE"),"work_key_kind":"S3_CANDIDATE_DECODE","work_key_order":[x["name"] for x in S3WK],"work_key_fields":S3WK,"preserved":["split","seed","cell_id","target_polarization","fixture_id","candidate_id"]},
"BPS":{"exact_binding_kind":"LOGICAL_COMPUTATION_ID","table":"bps_dev_score","consumer_pk_fields":BPSPK,"phase_rule":lit("BPS_DEV"),"operation_rule":lit("B1_DECODE"),"work_key_kind":"BPS_DUAL_POL_SHARED","work_key_order":[x["name"] for x in BPSWK],"work_key_fields":BPSWK,"omitted":["polarization"]},
"B2_clean":{"exact_binding_kind":"LOGICAL_COMPUTATION_ID","table":"b2_tuple_clean_dev","consumer_pk_fields":B2CPK,"phase_rule":lit("B2_DEV"),"operation_rule":lit("B2_DECODE"),"work_key_kind":"B2_CLEAN_DUAL_POL_SHARED","work_key_order":[x["name"] for x in B2CWK],"work_key_fields":B2CWK,"omitted":["polarization"]},
"B2_controlled":{"exact_binding_kind":"LOGICAL_COMPUTATION_ID","table":"b2_tuple_controlled_dev","consumer_pk_fields":B2TPK,"phase_rule":lit("B2_DEV"),"operation_rule":lit("B2_DECODE"),"work_key_kind":"B2_CONTROLLED_DUAL_POL_SHARED","work_key_order":[x["name"] for x in B2TWK],"work_key_fields":B2TWK,"omitted":["row_polarization"]},
"HMM_chunk":{"table":"b2_hmm_grid_chunk","consumer_pk_order":[x["name"] for x in HMMPK],"consumer_pk_fields":HMMPK,"binding":"exact_typed_chunk_primary_key_to_computation_ids_manifest_sha256","reference":{"kind":"COMPUTATION_IDS_MANIFEST_SHA256","raw_field":"computation_ids_manifest_sha256","payload_schema":"coded_decoder_feedback.d0.computation_id_manifest.v1","rule":"exact_typed_chunk_primary_key_equals_group_consumer_primary_key","logical_member_authority":"hmm_authority.logical_computation"}},
"S4":{"exact_binding_kind":"LOGICAL_COMPUTATION_ID","table":"s4_check","consumer_pk_fields":S4PK,"phase_rule":lit("S4"),"operation_rule":lit("OTHER_S4_CHECK"),"work_key_kind":"S4_STANDALONE_CHECK","work_key_fields":S4WK,"exact_check_ids":["no_slip_noiseless_B0_B1_O1_identity","all_rotation_boundary_noiseless_O1_zero_error","mapping_rotation_truth_metamorphic_pass","candidate_isolation_and_empty_decoder_state_pass","all_scores_finite_and_deterministic","no_truth_field_reaches_receiver_view","diagnostic_cost_ledger_complete"],"binding":"explicit_standalone_plan_per_exact_check_primary_key","implicit_or_prefixed_plan":"forbidden"}}
projs=ident["consumer_bindings"]["projections"]
eq(list(projs),list(expected),"projection order")
for n,e in expected.items():
    eq(set(projs[n]),set(e),f"{n} exact keys")
    for k,v in e.items(): eq(projs[n][k],v,f"{n}.{k}")
    for key in ("consumer_pk_fields","work_key_fields"):
        for d in projs[n].get(key,[]): eq(list(d),["name","source","atom_type"],f"{n}.{key} descriptor key order")
eq(ident["consumer_bindings"]["rule"],{"ordinary":"each_raw_consumer_exact_typed_primary_key_maps_to_one_declared_logical_computation_id","HMM_chunk":"each_HMM_chunk_exact_typed_primary_key_maps_to_one_computation_ids_manifest_sha256"},"binding rule")
ck("exact_binding_kind" not in projs["HMM_chunk"],"HMM must not instantiate logical binding manifest")

# Outer-owner PK and enum cross-check, including source and atom types.
tables={**doc["statistical_contract_repair"]["tables"],**doc["statistical_contract_repair"]["dev_freeze_artifact_contract"]["tables"]}
for n,e in expected.items():
    table=e["table"]; names=[x["name"] for x in e["consumer_pk_fields"]]
    eq(names,tables[table]["primary_key"],f"{n} outer PK")
    for d in e["consumer_pk_fields"]:
        raw_type=(tables[table].get("record_type",{}) if d["name"]=="record_type" else tables[table]["fields"][d["name"]])["type"]
        eq({"string":"str","int64":"int","boolean":"bool"}[raw_type],d["atom_type"],f"{n}.{d['name']} outer atom")
eq(expected["S4"]["exact_check_ids"],doc["statistical_contract_repair"]["enums"]["s4_check_id"],"S4 enum owner order")
ordinary=["S2_off","S2_on","S3","BPS","B2_clean","B2_controlled","S4"]
eq((len(ordinary),len(expected)-len(ordinary)),(7,1),"ordinary/HMM projections")
eq(sum(len(expected[n]["work_key_fields"]) for n in ordinary),32,"work descriptors")
eq(sum(len(expected[n]["consumer_pk_fields"]) for n in ordinary),41,"ordinary PK descriptors")
eq(sum(len(expected[n]["consumer_pk_fields"]) for n in expected),49,"all PK descriptors")
eq(len({("S2","B1_DECODE"),("S2","B2_DECODE"),("S2","O1_DECODE"),("S3_DEV","CANDIDATE_DECODE"),("S3_TEST","CANDIDATE_DECODE"),("BPS_DEV","B1_DECODE"),("B2_DEV","B2_DECODE"),("S4","OTHER_S4_CHECK")}),8,"phase-operation signatures")
eq(len({expected[n]["work_key_kind"] for n in ordinary}),7,"unique work kinds")

# Independent cardinality arithmetic from owner axes (no production helpers).
s2_bind=10*3*2*9*(1+3); s2_ids=10*3*2*(1+9*3)
s3_bind=2*10*3*2*9*10; s3_ids=s3_bind
bps_bind=5*6*10*12*2; bps_ids=bps_bind//2
b2c_bind=5*10*12*2; b2c_ids=b2c_bind//2
b2t_bind=5*10*12*2*9*2; b2t_ids=b2t_bind//2
s4_bind=s4_ids=7
ordinary_bind=sum((s2_bind,s3_bind,bps_bind,b2c_bind,b2t_bind,s4_bind)); ordinary_ids=sum((s2_ids,s3_ids,bps_ids,b2c_ids,b2t_ids,s4_ids))
hmm_ids=5*10*12*2*(1+9+9); chunks=5*122*6*3*12*2; ledger=ordinary_ids+hmm_ids
eq((ordinary_bind,ordinary_ids,hmm_ids,chunks,ledger),(42967,27487,22800,263520,50287),"identity counts")

# Literal authority and three grid roots.
ga=ident["grid_authority"]
for name,count in (("p_s",122),("sigma_e2",6)):
    vals=ga[name]["standalone_payload"]["values"]; eq(len(vals),count,f"{name} count")
    prior=-1.0
    for j,x in enumerate(vals):
        eq(list(x),["index","float64_hex"],f"{name}[{j}] shape"); eq(type(x["index"]),int,f"{name}[{j}] index type"); eq(x["index"],j,f"{name}[{j}] index")
        v=float.fromhex(x["float64_hex"]); eq(v.hex(),x["float64_hex"],f"{name}[{j}] canonical hex"); ck(v>=0 and (j==0 or v>prior),f"{name}[{j}] monotone"); prior=v
    eq(digest(ga[name]["standalone_payload"]),ga[name]["sha256"],f"{name} root")
eq(ga["combined"]["payload"]["p_s"],ga["p_s"]["standalone_payload"],"combined p_s deep equal")
eq(ga["combined"]["payload"]["sigma_e2"],ga["sigma_e2"]["standalone_payload"],"combined sigma deep equal")
eq(digest(ga["combined"]["payload"]),ga["combined"]["sha256"],"combined root")

# Ten independent golden groups: grid trio, four HMM groups, S2, BPS, runtime.
fixtures=ident["hmm_authority"]["fixture_owner_legal_order"]
cell="snr_10db__linewidth_10000hz"
def typed_fields(items): return [fentry(n,t,v) for n,t,v in items]
def member_pk(tuple_id,role,seed,pol,fixture=None,target=None):
    if role=="CLEAN_INCLUDED": return pk("b2_tuple_clean_dev",typed_fields([("record_type","str","B2_TUPLE_CLEAN_DEV"),("tuple_id","str",tuple_id),("seed","int",seed),("cell_id","str",cell),("polarization","str",pol)]))
    return pk("b2_tuple_controlled_dev",typed_fields([("record_type","str","B2_TUPLE_CONTROLLED_DEV"),("tuple_id","str",tuple_id),("seed","int",seed),("cell_id","str",cell),("target_polarization","str",target),("fixture_id","str",fixture),("row_polarization","str",pol)]))
def hmm_lid(tuple_id,role,seed,pol,fixture=None,target=None):
    items=[("tuple_id","str",tuple_id),("stratum_role","str",role),("seed","int",seed),("cell_id","str",cell),("polarization","str",pol)]
    if role!="CLEAN_INCLUDED": items += [("target_polarization","str",target),("fixture_id","str",fixture)]
    return logical("B2_DEV","HMM_GRID_SCORE",wk("HMM_TRAJECTORY_FULL_122_BY_6_GRID",typed_fields(items)))
def hmm_group(tuple_id,role,pol,pilot,target=None):
    ps=ga["p_s"]["standalone_payload"]["values"][0]["float64_hex"]; sg=ga["sigma_e2"]["standalone_payload"]["values"][0]["float64_hex"]
    gi={"schema":"coded_decoder_feedback.d0.hmm_group_identity.v1","kind":"HMM_GRID_CHUNK_GROUP","fields":typed_fields([("tuple_id","str",tuple_id),("p_s_index","int",0),("p_s_float64_hex","float64_hex",ps),("sigma_e2_index","int",0),("sigma_e2_float64_hex","float64_hex",sg),("stratum_role","str",role),("cell_id","str",cell),("polarization","str",pol),("pilot_count","int",pilot)])}
    chunk="hmmg1-"+digest(gi)
    cpk=pk("b2_hmm_grid_chunk",typed_fields([("record_type","str","B2_HMM_GRID_CHUNK"),("tuple_id","str",tuple_id),("p_s_index","int",0),("sigma_e2_index","int",0),("stratum_role","str",role),("cell_id","str",cell),("polarization","str",pol),("chunk_id","str",chunk)]))
    raw=[]
    if role=="CLEAN_INCLUDED": raw=[(s,None,None) for s in range(8000,8010)]
    else: raw=[(s,fx,target) for s in range(8000,8010) for fx in fixtures]
    members=[]; bindings=[]
    for ordinal,(seed,fixture,target_pol) in enumerate(raw):
        mp=member_pk(tuple_id,role,seed,pol,fixture,target_pol); lid=hmm_lid(tuple_id,role,seed,pol,fixture,target_pol)
        cache="EXECUTED"; source=None
        if role=="CONTROLLED_SENTINEL_EXCLUDED" or tuple_id=="M3_N100":
            cache="CACHE_READ"; src_tuple="M2_N100" if tuple_id=="M3_N100" else tuple_id
            src_role="CLEAN_INCLUDED" if role=="CONTROLLED_SENTINEL_EXCLUDED" else role
            source=hmm_lid(src_tuple,src_role,seed,pol,fixture if src_role!="CLEAN_INCLUDED" else None,target_pol if src_role!="CLEAN_INCLUDED" else None)
        members.append({"ordinal":ordinal,"member_primary_key":mp})
        bindings.append({"schema":"coded_decoder_feedback.d0.hmm_computation_binding.v1","ordinal":ordinal,"member_primary_key":mp,"computation_id":lid,"cache_status":cache,"source_computation_id":source})
    mm={"schema":"coded_decoder_feedback.d0.hmm_member_key_manifest.v1","consumer_primary_key":cpk,"members":members}
    cm={"schema":"coded_decoder_feedback.d0.computation_id_manifest.v1","group":{"group_identity":gi,"chunk_id":chunk,"consumer_primary_key":cpk,"pilot_count":pilot},"aggregate":{"algorithm":"CANONICAL_BINARY64_EXACT_RATIONAL_SUM_V1","member_count":len(members)},"bindings":bindings}
    return chunk,digest(mm),digest(cm),bindings[0]["computation_id"],bindings[0]["source_computation_id"]
gv=ident["golden_vectors"]
eq((ga["p_s"]["sha256"],ga["sigma_e2"]["sha256"],ga["combined"]["sha256"]),(gv["grid_commitments"]["p_s_sha256"],gv["grid_commitments"]["sigma_e2_sha256"],gv["grid_commitments"]["combined_sha256"]),"golden grid trio")
for name,args in [("clean10",("M2_N100","CLEAN_INCLUDED","X",64,None)),("target90",("M2_N100","CONTROLLED_TARGET_INCLUDED","X",64,"X")),("sentinel90_to_clean",("M2_N100","CONTROLLED_SENTINEL_EXCLUDED","Y",64,"X")),("M3_N100_direct_to_M2",("M3_N100","CLEAN_INCLUDED","X",64,None))]:
    got=hmm_group(*args); g=gv[name]; want=[g["chunk_id"],g["member_key_manifest_sha256"],g["computation_ids_manifest_sha256"],g["first_logical_computation_id"]]
    if "first_source_computation_id" in g: want.append(g["first_source_computation_id"])
    eq(list(got[:len(want)]),want,f"golden {name}")
def s2_golden():
    fields=typed_fields([("seed","int",8150),("cell_id","str","hard"),("target_polarization","str","X"),("jump_present","bool",False),("method_id","str","GLOBAL_FOUR_ROTATION_DECODER_SELECTION"),("canonical_owner_fixture_id","str","B04_K1")])
    lid=logical("S2","B1_DECODE",wk("S2_B1_OFF_CANONICAL_B04",fields)); binds=[]
    for fx in fixtures:
        cp=pk("s2_method",typed_fields([("record_type","str","S2_METHOD"),("seed","int",8150),("cell_id","str","hard"),("target_polarization","str","X"),("fixture_id","str",fx),("jump_present","bool",False),("method_id","str","GLOBAL_FOUR_ROTATION_DECODER_SELECTION")]))
        binds.append({"consumer_primary_key":cp,"logical_computation_id":lid})
    payload={"schema":"coded_decoder_feedback.d0.consumer_binding_manifest.v1","binding_kind":"LOGICAL_COMPUTATION_ID","bindings":binds}
    return lid,digest(payload)
eq(s2_golden(),(gv["S2_off_nine_to_one"]["shared_logical_computation_id"],gv["S2_off_nine_to_one"]["consumer_binding_manifest_sha256"]),"golden S2")
def bps_golden():
    lid=logical("BPS_DEV","B1_DECODE",wk("BPS_DUAL_POL_SHARED",typed_fields([("tuple_id","str","M2_N100"),("B","int",32),("Nw","int",31),("seed","int",8000),("cell_id","str",cell)])))
    binds=[]
    for pol in ["X","Y"]:
        cp=pk("bps_dev_score",typed_fields([("record_type","str","BPS_DEV_SCORE"),("tuple_id","str","M2_N100"),("B","int",32),("Nw","int",31),("seed","int",8000),("cell_id","str",cell),("polarization","str",pol)]))
        binds.append({"consumer_primary_key":cp,"logical_computation_id":lid})
    return lid,digest({"schema":"coded_decoder_feedback.d0.consumer_binding_manifest.v1","binding_kind":"LOGICAL_COMPUTATION_ID","bindings":binds})
eq(bps_golden(),(gv["BPS_dual_pol_shared"]["shared_logical_computation_id"],gv["BPS_dual_pol_shared"]["consumer_binding_manifest_sha256"]),"golden BPS")
r=gv["runtime_clean10_synthetic_exact_sum"]; resolved=[{"ordinal":j,"content_sha256":sha_bytes(f"resolved-member-content-v1:{j}".encode())} for j in range(10)]
rp={"schema":"coded_decoder_feedback.d0.hmm_runtime_aggregate_content.v1","computation_ids_manifest_sha256":r["inputs"]["computation_ids_manifest_sha256"],"resolved_member_contents":resolved,"normalized_nll_exact_sum_numerator_decimal":"123456789","normalized_nll_exact_sum_denominator_power2":42,"member_count":10}
eq((resolved[0]["content_sha256"],resolved[-1]["content_sha256"],digest(rp)),(r["first_resolved_content_sha256"],r["last_resolved_content_sha256"],r["content_sha256"]),"golden runtime")
GOLDENS=10

# Six accounting formulas independently evaluated.
forms=ident["ledger_accounting"]["formulas"]
values=(chunks,hmm_ids,hmm_ids*732,4*10*12*2*(1+9),9600*732,hmm_ids-9600)
for (name,node),v in zip(forms.items(),values): eq(node["expected"],v,f"accounting {name}")
COUNTS=6

# Fail-closed D017 mutations. Expected projection/reference values are never derived from owner.
def focused_ok(d):
    try:
        ii=d["identity_binding_contract"]; pp=ii["consumer_bindings"]["projections"]
        return list(pp)==list(expected) and all(pp[n]==expected[n] for n in expected) and ii["consumer_bindings"]["rule"]==ident["consumer_bindings"]["rule"] and ii["consumer_bindings"]["coverage"]==ident["consumer_bindings"]["coverage"] and ii["validator_obligations"]==ident["validator_obligations"]
    except Exception: return False
mut=[]
def add(name,fn):
    x=copy.deepcopy(doc); fn(x["identity_binding_contract"]["consumer_bindings"]["projections"]); mut.append((name,x))
for n in ordinary:
    add(n+".kind",lambda p,n=n:p[n].__setitem__("work_key_kind","BAD_KIND"))
    add(n+".phase",lambda p,n=n:p[n].__setitem__("phase_rule",lit("BAD_PHASE")))
    add(n+".op",lambda p,n=n:p[n].__setitem__("operation_rule",lit("BAD_OP")))
    add(n+".source",lambda p,n=n:p[n]["work_key_fields"][0].__setitem__("source","raw.bad"))
    add(n+".atom",lambda p,n=n:p[n]["consumer_pk_fields"][0].__setitem__("atom_type","int"))
    add(n+".order",lambda p,n=n:p[n]["consumer_pk_fields"].reverse())
add("S2.method_swap",lambda p:p["S2_on"]["operation_rule"]["values"].__setitem__("OFC17_16QAM_EXTFRAME_V1","O1_DECODE"))
add("S3.phase_swap",lambda p:p["S3"]["phase_rule"]["values"].__setitem__("S3_CANDIDATE_DEV","S3_TEST"))
add("B2.clean_kind_swap",lambda p:p["B2_clean"].__setitem__("work_key_kind","B2_CONTROLLED_DUAL_POL_SHARED"))
add("B2.controlled_kind_swap",lambda p:p["B2_controlled"].__setitem__("work_key_kind","B2_CLEAN_DUAL_POL_SHARED"))
add("B04.literal",lambda p:p["S2_off"].__setitem__("canonical_owner_fixture_id","B04_K2"))
for name,fn in [("S4.missing",lambda a:a.pop()),("S4.duplicate",lambda a:a.append(a[0])),("S4.order",lambda a:a.reverse()),("S4.substitute",lambda a:a.__setitem__(0,"bad"))]: add(name,lambda p,fn=fn:fn(p["S4"]["exact_check_ids"]))
for key in ["kind","raw_field","payload_schema","rule","logical_member_authority"]: add("HMM.ref."+key,lambda p,key=key:p["HMM_chunk"]["reference"].__setitem__(key,"BAD"))
add("HMM.logical_kind",lambda p:p["HMM_chunk"].__setitem__("exact_binding_kind","LOGICAL_COMPUTATION_ID"))
add("HMM.pk_swap",lambda p:p["HMM_chunk"]["consumer_pk_fields"].__setitem__(4,copy.deepcopy(p["HMM_chunk"]["consumer_pk_fields"][5])))
wrong_accept=sum(1 for _,x in mut if focused_ok(x)); eq(wrong_accept,0,"mutation wrong accept")
MUTATIONS=len(mut); ck(MUTATIONS>=24,"mutation count")

# Structural inverse of exactly T110 additions. Reapplying final expected is deep-equal current;
# deleting the whole identity block independently preserves the frozen raw scientific projection.
inverse=copy.deepcopy(doc); ii=inverse["identity_binding_contract"]; cc=ii["consumer_bindings"]
cc["rule"]="each_raw_consumer_exact_typed_primary_key_maps_to_one_declared_logical_computation_id"
for n in ordinary:
    q=cc["projections"][n]
    for k in ["consumer_pk_fields","phase_rule","operation_rule","work_key_fields"]: q.pop(k)
for n in ["S2_on","S3","B2_clean","B2_controlled","S4"]: cc["projections"][n].pop("work_key_kind")
h=cc["projections"]["HMM_chunk"]; h.pop("consumer_pk_fields"); h.pop("reference"); h["exact_binding_kind"]="LOGICAL_COMPUTATION_ID"
cc["projections"]["S4"].pop("exact_check_ids")
cov_add=["ordinary_and_HMM_binding_targets_are_separate","all_consumer_primary_key_descriptors_exact_typed_and_ordered","all_ordinary_phase_operation_work_key_descriptors_exact","S4_exact_check_id_set_and_order"]
req_add=["ordinary_consumer_identity_rules_and_typed_descriptors_exact","HMM_chunk_manifest_reference_exact_and_not_logical_id_binding","S4_exact_check_id_set_and_order"]
rej_add=["ordinary_binding_kind_mutation","ordinary_phase_map_mutation","ordinary_operation_map_mutation","ordinary_work_key_kind_mutation","ordinary_same_type_source_swap","ordinary_atom_type_drift","S2_off_B04_literal_mutation","ordinary_consumer_PK_order_mutation","ordinary_consumer_PK_atom_mutation","S4_check_id_order_or_substitution","HMM_reference_kind_mutation","HMM_reference_raw_field_mutation","HMM_reference_payload_schema_mutation"]
for v in cov_add: cc["coverage"].remove(v)
for v in req_add: ii["validator_obligations"]["required"].remove(v)
for v in rej_add: ii["validator_obligations"]["reject_mutations"].remove(v)
reapplied=copy.deepcopy(inverse); ri=reapplied["identity_binding_contract"]; ri["consumer_bindings"]=copy.deepcopy(ident["consumer_bindings"]); ri["validator_obligations"]=copy.deepcopy(ident["validator_obligations"])
eq(reapplied,doc,"inverse/reapply deep equality")
inverse_identity_sha=digest(ii)
science=copy.deepcopy(doc); science.pop("identity_binding_contract")
identity_start=raw0.index(b"\nidentity_binding_contract:\n")+1
strata_start=raw0.index(b"\nstrata:\n",identity_start)+1
science_sha=sha_bytes(raw0[:identity_start]+raw0[strata_start:])
eq(science_sha,SCIENCE,"raw scientific projection")

# Frozen receipts, P05, cache census, HEAD/staging, and no run-time write outside this log.
frozen={
"projects/simulation/explore/coded-decoder-feedback/contract.py":"0df83a86105a9ff5f8c76d2d937b7ac2a99f51f7d97783f7d3f4260c4d5bfc94",
"projects/simulation/tests/test_d0_contract_views.py":"745ccbe5732816c8100ad9187a181d6acf6f2072269795e32e58487b66cce4f6",
"projects/simulation/explore/coded-decoder-feedback/schemas.py":"a42ffa184d2db3cfa68775b9dc0b3aac60195bf34abfdf5e37732f398445e401",
"projects/simulation/tests/test_d0_schemas_statistics.py":"a94731c3c9d44c1f0ba8ef1b27df578cbb9f982f3069f51786f3becc419dd4c9",
".sessions/2026-08-09-coded-decoder-feedback-groundwork/R001-d0-canonical-identity-binding.md":"1882c9d51a43a75efd3d56cb708edde2a1d88b06e850ba0dbe63821402095d37",
".sessions/2026-08-09-coded-decoder-feedback-groundwork/decisions.md":"b20e8ffc5c28a0335ccf5da3791e3e462bbfdd7e1ed49682cc986350497a5bc8",
".sessions/2026-08-09-coded-decoder-feedback-groundwork/verifications.md":"fb3173c6db7809d44f67d2c03619eb9ad3b3901b44cbd10bb9fea7daadaea67e",
"projects/thesis-fso/worker-logs/step-155-d0-owner-identity-loader-independent-verification.md":"ce5edec6a9e8102bea6840abfff028bf8d36ca73d75e3dd9e6bab8078dfdfde9",
"projects/thesis-fso/worker-logs/step-156-d0-owner-ordinary-identity-completion.md":"387e3840bdf7ba0acaf839515070e5da1cc931e1a42392eb91440974ca613419"}
for p,h in frozen.items(): eq(sha_file(ROOT/p),h,"frozen "+p)
p05=["7843b048a2a79755c95542a438a5344f8e89e791113f48913926c419fc2a4f11","735e4650093d297e01a0e6dfe28f0431c149a2931fcbb7c08eecfa28f0aac38b","c76887c6950aaac2b4c0dced7689517749322c44da868880915786c173b1344d","95a1d184740a797b6d55d7f817008c898cb3754987ab6e1c1d00376f74a621de"]
for j,h in enumerate(p05): eq(sha_file(ROOT/f"projects/simulation/explore/cma-fade-divergence/p05_run{'' if j==0 else j+1}.log"),h,f"P05 {j+1}")
def git(*args): return subprocess.run(["git",*args],cwd=ROOT,text=True,capture_output=True,check=False)
eq(git("rev-parse","HEAD").stdout.strip(),HEAD,"HEAD")
eq(git("diff","--cached","--name-only").stdout.strip(),"","staging")
eq(git("diff","--check").returncode,0,"diff check")
cache_lines=[x for x in git("status","--short","-uall").stdout.splitlines() if "__pycache__" in x]
eq((len(cache_lines),sum(".pyc" in x for x in cache_lines)),(10,10),"tracked cache census")
eq(sha_bytes(OWNER.read_bytes()),begin_owner,"owner end SHA")
ck(ASSERTIONS>=250,"assertion floor")
print(f"OWNER_ORDINARY_IDENTITY_COMPLETION_INDEPENDENTLY_VERIFIED assertions={ASSERTIONS} descriptors=32/41/49 goldens={GOLDENS}/10 mutations={MUTATIONS}/{MUTATIONS} wrong_accept={wrong_accept} wrong_reject=0 counts={COUNTS}/6 mismatch=0")
print(f"IDENTITIES ordinary_bindings={ordinary_bind} ordinary_logical={ordinary_ids} hmm_logical={hmm_ids} hmm_chunks={chunks} ledger={ledger}")
print(f"DRIFT owner={begin_owner} science={science_sha} inverse_identity={inverse_identity_sha} permission=none grid=none count=none golden=none")
print(f"PROTECTION head={HEAD} staging=0 p05=4/4 cache={len(cache_lines)}/{sum('.pyc' in x for x in cache_lines)} diff_check=0 P0/P1/P2=0/0/0")
```

## Fresh execution

Command（从上方 fenced source 提取后经 stdin fresh 执行；未创建临时源码文件）：

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; $env:PYTHONHASHSEED='0'
$raw=Get-Content -Raw projects/thesis-fso/worker-logs/step-157-d0-owner-ordinary-identity-independent-verification.md
$m=[regex]::Match($raw,'(?s)```python\r?\n(.*?)\r?\n```')
$m.Groups[1].Value | C:\Users\zzt\scoop\apps\python311\current\python.exe -B -
```

Final stdout：

```text
OWNER_ORDINARY_IDENTITY_COMPLETION_INDEPENDENTLY_VERIFIED assertions=920 descriptors=32/41/49 goldens=10/10 mutations=58/58 wrong_accept=0 wrong_reject=0 counts=6/6 mismatch=0
IDENTITIES ordinary_bindings=42967 ordinary_logical=27487 hmm_logical=22800 hmm_chunks=263520 ledger=50287
DRIFT owner=02d471a200a1dce17f2c43dd36ca90b050ebdc943c7c045483e816a07162d140 science=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d inverse_identity=6b2b5949d84eb279be49d6b5a0757f556173a62a2c68d48c9339b10cf0da646f permission=none grid=none count=none golden=none
PROTECTION head=715a65884b988ee737f21982f3bbf372860a1da8 staging=0 p05=4/4 cache=10/10 diff_check=0 P0/P1/P2=0/0/0
```

- final exit=`0`
- final stdout SHA-256=`94be18cde72f6268d67bda800d68c6bb67e08214bd55261bba68a88b2393ca33`
- 两次 verifier-only 路径定位失误（B2 table 嵌套路径）均在 owner 断言前 `KeyError`，exit=`1`，stdout SHA=`8c2b845bf24994fca7c614297ffc3005c8830c922a6b34fe8e6c9ead369bdddf`；一次 raw-vs-parsed scientific projection 口径失误在前序 245+ 断言后退出，exit=`1`，stdout SHA=`5b4a24e25439900e53635c04806656e25223a48863de568e1819d11976f66dda`。三者均只修 verifier，不改 owner/source/tests/session/P05。

## Findings / terminal

- D017 final owner exact descriptor、outer PK/type、HMM manifest-reference 分离与 S4 exact IDs 全部命中；HMM 无 `exact_binding_kind`。
- 128 literals、3 roots、10 golden groups、6 accounting counts全部 fresh 复算命中；S2/BPS IDs+roots及四组 HMM roots无漂移。
- 58/58 预标 mutation 均 fail closed；wrong accept/reject=`0/0`。
- T110 additions 结构化删除后再应用 final authority，deep-equal 当前 parsed owner；raw scientific projection仍为冻结 `c61c88e...`。该逆投影摘要 SHA 为 `6b2b5949...`，不是新的 owner seal。
- begin/end owner、HEAD、staging、Frozen bytes、P05、cache census、`git diff --check`全部通过；唯一写入为本 step-157。
- `P0/P1/P2=0/0/0`。

Terminal：`OWNER_ORDINARY_IDENTITY_COMPLETION_INDEPENDENTLY_VERIFIED`。

该 PASS 只接收 D017 owner bytes；不等于 typed-loader seal刷新、I05完成、benchmark或science授权。
