# Step 156 — D0 owner ordinary identity completion

> 2026-08-10 | T110 | `PASS`

## Independent declarative checker source

<!-- verifier:start -->
```python
import copy, hashlib, json, math, re, subprocess, sys
from pathlib import Path
import yaml
import numpy as np

ROOT=Path.cwd()
OWNER=ROOT/'projects/thesis-fso/coded-decoder-feedback-groundwork/d0-defect-smoke-contract.yaml'
PRE='ca2c8146dec5edec62984cdadf678d808291cb6b2a736fd99059651fc7a50535'
SCI='c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d'
HEAD='715a65884b988ee737f21982f3bbf372860a1da8'
ROOTS={'p_s':'bfc3cef2c8e6fc800b6a40f9da778ab98b666ec57e5e12ae1f0c8b9f25b78864','sigma_e2':'0f37cdf467a04283bbf03792c5654545947ce759c052ed11e98c20c2618401ca','combined':'0cdb5e547e31997cd931a97f97f681ff5eeae28c372810eb12f593f4dca99fdf'}
PROTECTED={
'.sessions/2026-08-09-coded-decoder-feedback-groundwork/R001-d0-canonical-identity-binding.md':'1882c9d51a43a75efd3d56cb708edde2a1d88b06e850ba0dbe63821402095d37',
'.sessions/2026-08-09-coded-decoder-feedback-groundwork/decisions.md':'b20e8ffc5c28a0335ccf5da3791e3e462bbfdd7e1ed49682cc986350497a5bc8',
'.sessions/2026-08-09-coded-decoder-feedback-groundwork/verifications.md':'fb3173c6db7809d44f67d2c03619eb9ad3b3901b44cbd10bb9fea7daadaea67e',
'.sessions/2026-08-09-coded-decoder-feedback-groundwork/topic-index.md':'1e8469aa2f10ad53f57d2d2819b6e58909648b8a74fb01ea022d8f96cf836ef6',
'projects/simulation/explore/coded-decoder-feedback/contract.py':'0df83a86105a9ff5f8c76d2d937b7ac2a99f51f7d97783f7d3f4260c4d5bfc94',
'projects/simulation/tests/test_d0_contract_views.py':'745ccbe5732816c8100ad9187a181d6acf6f2072269795e32e58487b66cce4f6',
'projects/simulation/explore/coded-decoder-feedback/schemas.py':'a42ffa184d2db3cfa68775b9dc0b3aac60195bf34abfdf5e37732f398445e401',
'projects/simulation/tests/test_d0_schemas_statistics.py':'a94731c3c9d44c1f0ba8ef1b27df578cbb9f982f3069f51786f3becc419dd4c9',
'projects/thesis-fso/worker-logs/step-154-d0-owner-identity-typed-loader.md':'0a33ec8011faf929a56956cc6d13b6e9f77f02fc6281f2bd81a923c08a850a7a',
'projects/thesis-fso/worker-logs/step-155-d0-owner-identity-loader-independent-verification.md':'ce5edec6a9e8102bea6840abfff028bf8d36ca73d75e3dd9e6bab8078dfdfde9',
'projects/simulation/explore/cma-fade-divergence/p05_run.log':'7843b048a2a79755c95542a438a5344f8e89e791113f48913926c419fc2a4f11',
'projects/simulation/explore/cma-fade-divergence/p05_run2.log':'735e4650093d297e01a0e6dfe28f0431c149a2931fcbb7c08eecfa28f0aac38b',
'projects/simulation/explore/cma-fade-divergence/p05_run3.log':'c76887c6950aaac2b4c0dced7689517749322c44da868880915786c173b1344d',
'projects/simulation/explore/cma-fade-divergence/p05_run4.log':'95a1d184740a797b6d55d7f817008c898cb3754987ab6e1c1d00376f74a621de'}

n=0; failures=[]
def ck(ok,label,sev='P1'):
 global n
 n+=1
 if not ok: failures.append((sev,label))
 return bool(ok)
def hb(b): return hashlib.sha256(b).hexdigest()
def hf(p): return hb(Path(p).read_bytes())
def enc(o): return json.dumps(o,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def rh(o): return hb(enc(o))

class Strict(yaml.SafeLoader): pass
def mapping(loader,node,deep=False):
 loader.flatten_mapping(node); out={}
 for kn,vn in node.value:
  k=loader.construct_object(kn,deep=deep)
  if k in out: raise ValueError('duplicate:'+repr(k))
  out[k]=loader.construct_object(vn,deep=deep)
 return out
Strict.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,mapping)

raw=OWNER.read_bytes(); start_sha=hb(raw); text=raw.decode('utf-8')
try: doc=yaml.load(text,Loader=Strict); ck(isinstance(doc,dict),'strict_duplicate_yaml','P0')
except Exception as e:
 print(json.dumps({'verdict':'INCOMPLETE_STRICT_PARSE','error':repr(e)},sort_keys=True)); sys.exit(3)
ib=doc['identity_binding_contract']; cb=ib['consumer_bindings']; projections=cb['projections']

def d(name,typ,source=None): return {'name':name,'source':source or 'raw.'+name,'atom_type':typ}
pk={
'S2_off':[d('record_type','str'),d('seed','int'),d('cell_id','str'),d('target_polarization','str'),d('fixture_id','str'),d('jump_present','bool'),d('method_id','str')],
'S2_on':[d('record_type','str'),d('seed','int'),d('cell_id','str'),d('target_polarization','str'),d('fixture_id','str'),d('jump_present','bool'),d('method_id','str')],
'S3':[d('record_type','str'),d('seed','int'),d('cell_id','str'),d('target_polarization','str'),d('fixture_id','str'),d('candidate_id','str')],
'BPS':[d('record_type','str'),d('tuple_id','str'),d('B','int'),d('Nw','int'),d('seed','int'),d('cell_id','str'),d('polarization','str')],
'B2_clean':[d('record_type','str'),d('tuple_id','str'),d('seed','int'),d('cell_id','str'),d('polarization','str')],
'B2_controlled':[d('record_type','str'),d('tuple_id','str'),d('seed','int'),d('cell_id','str'),d('target_polarization','str'),d('fixture_id','str'),d('row_polarization','str')],
'S4':[d('record_type','str'),d('check_id','str')]}
wk={
'S2_off':[d('seed','int'),d('cell_id','str'),d('target_polarization','str'),d('jump_present','bool'),d('method_id','str'),d('canonical_owner_fixture_id','str','literal.B04_K1')],
'S2_on':[d('seed','int'),d('cell_id','str'),d('target_polarization','str'),d('fixture_id','str'),d('jump_present','bool'),d('method_id','str')],
'S3':[d('record_type_as_split','str','raw.record_type'),d('seed','int'),d('cell_id','str'),d('target_polarization','str'),d('fixture_id','str'),d('candidate_id','str')],
'BPS':[d('tuple_id','str'),d('B','int'),d('Nw','int'),d('seed','int'),d('cell_id','str')],
'B2_clean':[d('tuple_id','str'),d('seed','int'),d('cell_id','str')],
'B2_controlled':[d('tuple_id','str'),d('seed','int'),d('cell_id','str'),d('target_polarization','str'),d('fixture_id','str')],
'S4':[d('check_id','str')]}
phase={
'S2_off':{'kind':'literal','value':'S2'},'S2_on':{'kind':'literal','value':'S2'},
'S3':{'kind':'enum_map','source':'raw.record_type','values':{'S3_CANDIDATE_DEV':'S3_DEV','S3_CANDIDATE_TEST':'S3_TEST'}},
'BPS':{'kind':'literal','value':'BPS_DEV'},'B2_clean':{'kind':'literal','value':'B2_DEV'},'B2_controlled':{'kind':'literal','value':'B2_DEV'},'S4':{'kind':'literal','value':'S4'}}
operation={
'S2_off':{'kind':'literal','value':'B1_DECODE'},
'S2_on':{'kind':'enum_map','source':'raw.method_id','values':{'GLOBAL_FOUR_ROTATION_DECODER_SELECTION':'B1_DECODE','OFC17_16QAM_EXTFRAME_V1':'B2_DECODE','TRUTH_BOUNDARY_ROTATION_CORRECTION':'O1_DECODE'}},
'S3':{'kind':'literal','value':'CANDIDATE_DECODE'},'BPS':{'kind':'literal','value':'B1_DECODE'},'B2_clean':{'kind':'literal','value':'B2_DECODE'},'B2_controlled':{'kind':'literal','value':'B2_DECODE'},'S4':{'kind':'literal','value':'OTHER_S4_CHECK'}}
kind={'S2_off':'S2_B1_OFF_CANONICAL_B04','S2_on':'S2_ON_METHOD_DECODE','S3':'S3_CANDIDATE_DECODE','BPS':'BPS_DUAL_POL_SHARED','B2_clean':'B2_CLEAN_DUAL_POL_SHARED','B2_controlled':'B2_CONTROLLED_DUAL_POL_SHARED','S4':'S4_STANDALONE_CHECK'}
hpk=[d('record_type','str'),d('tuple_id','str'),d('p_s_index','int'),d('sigma_e2_index','int'),d('stratum_role','str'),d('cell_id','str'),d('polarization','str'),d('chunk_id','str')]
href={'kind':'COMPUTATION_IDS_MANIFEST_SHA256','raw_field':'computation_ids_manifest_sha256','payload_schema':'coded_decoder_feedback.d0.computation_id_manifest.v1','rule':'exact_typed_chunk_primary_key_equals_group_consumer_primary_key','logical_member_authority':'hmm_authority.logical_computation'}
s4ids=['no_slip_noiseless_B0_B1_O1_identity','all_rotation_boundary_noiseless_O1_zero_error','mapping_rotation_truth_metamorphic_pass','candidate_isolation_and_empty_decoder_state_pass','all_scores_finite_and_deterministic','no_truth_field_reaches_receiver_view','diagnostic_cost_ledger_complete']
coverage_need={'ordinary_and_HMM_binding_targets_are_separate','all_consumer_primary_key_descriptors_exact_typed_and_ordered','all_ordinary_phase_operation_work_key_descriptors_exact','S4_exact_check_id_set_and_order'}
required_need={'ordinary_consumer_identity_rules_and_typed_descriptors_exact','HMM_chunk_manifest_reference_exact_and_not_logical_id_binding','S4_exact_check_id_set_and_order'}
mutation_need={'ordinary_binding_kind_mutation','ordinary_phase_map_mutation','ordinary_operation_map_mutation','ordinary_work_key_kind_mutation','ordinary_same_type_source_swap','ordinary_atom_type_drift','S2_off_B04_literal_mutation','ordinary_consumer_PK_order_mutation','ordinary_consumer_PK_atom_mutation','S4_check_id_order_or_substitution','HMM_reference_kind_mutation','HMM_reference_raw_field_mutation','HMM_reference_payload_schema_mutation'}

def d017_errors(block):
 out=[]
 c=block.get('consumer_bindings',{}); ps=c.get('projections',{})
 if block.get('payload_schemas',{}).get('consumer_binding_manifest',{}).get('exact_binding_kind')!='LOGICAL_COMPUTATION_ID': out.append('global_binding_kind')
 if c.get('rule')!={'ordinary':'each_raw_consumer_exact_typed_primary_key_maps_to_one_declared_logical_computation_id','HMM_chunk':'each_HMM_chunk_exact_typed_primary_key_maps_to_one_computation_ids_manifest_sha256'}: out.append('common_rule')
 for name in pk:
  p=ps.get(name,{})
  if p.get('exact_binding_kind')!='LOGICAL_COMPUTATION_ID': out.append(name+'.binding_kind')
  if p.get('consumer_pk_fields')!=pk[name]: out.append(name+'.consumer_pk_fields')
  if p.get('phase_rule')!=phase[name]: out.append(name+'.phase_rule')
  if p.get('operation_rule')!=operation[name]: out.append(name+'.operation_rule')
  if p.get('work_key_kind')!=kind[name]: out.append(name+'.work_key_kind')
  if p.get('work_key_fields')!=wk[name]: out.append(name+'.work_key_fields')
  if any(list(q)!=['name','source','atom_type'] for q in p.get('consumer_pk_fields',[])+p.get('work_key_fields',[])): out.append(name+'.descriptor_key_order')
  if 'consumer_pk_order' in p and p['consumer_pk_order']!=[q['name'] for q in p.get('consumer_pk_fields',[])]: out.append(name+'.consumer_pk_order_drift')
  if 'work_key_order' in p and p['work_key_order']!=[q['name'] for q in p.get('work_key_fields',[])]: out.append(name+'.work_key_order_drift')
 h=ps.get('HMM_chunk',{})
 if 'exact_binding_kind' in h: out.append('HMM_chunk.binding_kind_present')
 if h.get('consumer_pk_fields')!=hpk: out.append('HMM_chunk.consumer_pk_fields')
 if any(list(q)!=['name','source','atom_type'] for q in h.get('consumer_pk_fields',[])): out.append('HMM_chunk.descriptor_key_order')
 if h.get('consumer_pk_order')!=[q['name'] for q in h.get('consumer_pk_fields',[])]: out.append('HMM_chunk.consumer_pk_order_drift')
 if h.get('reference')!=href: out.append('HMM_chunk.reference')
 if ps.get('S4',{}).get('exact_check_ids')!=s4ids: out.append('S4.exact_check_ids')
 if not coverage_need.issubset(set(c.get('coverage',[]))): out.append('coverage')
 vo=block.get('validator_obligations',{})
 if not required_need.issubset(set(vo.get('required',[]))): out.append('required')
 if not mutation_need.issubset(set(vo.get('reject_mutations',[]))): out.append('reject_mutations')
 return out

shape_errors=d017_errors(ib)
for e in shape_errors: ck(False,'D017_'+e)
ck(list(projections)==['S2_off','S2_on','S3','BPS','B2_clean','B2_controlled','HMM_chunk','S4'],'projection_order')
ck(sum(len(x) for x in wk.values())==32,'work_descriptors_32')
ck(sum(len(x) for x in pk.values())==41,'ordinary_pk_descriptors_41')
ck(sum(len(x) for x in pk.values())+len(hpk)==49,'all_pk_descriptors_49')
ck(len(pk)==7 and len(projections)-len(pk)==1,'ordinary_HMM_7_1')
signatures=set()
for name in pk:
 pv=list(phase[name]['values'].values()) if phase[name]['kind']=='enum_map' else [phase[name]['value']]
 ov=list(operation[name]['values'].values()) if operation[name]['kind']=='enum_map' else [operation[name]['value']]
 signatures.update((p,o) for p in pv for o in ov)
ck(len(signatures)==8,'phase_operation_signatures_8')

# Full 128-literal and three-root check.
eps=[float(x).hex() for x in np.concatenate((np.array([0.],dtype=np.float64),np.logspace(-7,-1,121,endpoint=True,base=10,dtype=np.float64)))]
ess=[float(x).hex() for x in np.array([0.,1e-5,1e-4,1e-3,1e-2,1e-1],dtype=np.float64)]
ga=ib['grid_authority']; po=ga['p_s']['standalone_payload']; so=ga['sigma_e2']['standalone_payload']; literals=0
for name,obj,exp in [('p_s',po,eps),('sigma_e2',so,ess)]:
 for i,(v,h) in enumerate(zip(obj['values'],exp)):
  good=list(v)==['index','float64_hex'] and type(v['index']) is int and v['index']==i and type(v['float64_hex']) is str and v['float64_hex']==h and float.fromhex(h).hex()==h
  if ck(good,f'literal_{name}_{i}'): literals+=1
combo=ga['combined']['payload']; roots=sum([ck(rh(po)==ROOTS['p_s']==ga['p_s']['sha256'],'root_p_s'),ck(rh(so)==ROOTS['sigma_e2']==ga['sigma_e2']['sha256'],'root_sigma'),ck(rh(combo)==ROOTS['combined']==ga['combined']['sha256'],'root_combined')])
ck(combo['p_s']==po and combo['sigma_e2']==so,'combined_deep_equal')

# Independent canonical payload builders and ten old golden checks.
pd=ib['payload_schemas']
def atom(v,t): return {'type':t,'value':v}
def ents(items): return [{'name':k,'atom':atom(v,t)} for k,v,t in items]
def cpk(table,items): return {'schema':pd['consumer_primary_key']['version'],'table':table,'fields':ents(items)}
def work(k,items): return {'schema':pd['typed_work_key']['version'],'kind':k,'fields':ents(items)}
def lid(ph,op,w): return 'd0c1-'+rh({'schema':pd['logical_computation_identity']['version'],'phase':ph,'operation':op,'work_key':w})
def group(tup,role,pol,pilot,cell='snr_10db__linewidth_10000hz'):
 return {'schema':pd['hmm_group_identity']['version'],'kind':'HMM_GRID_CHUNK_GROUP','fields':ents([('tuple_id',tup,'str'),('p_s_index',0,'int'),('p_s_float64_hex','0x0.0p+0','float64_hex'),('sigma_e2_index',0,'int'),('sigma_e2_float64_hex','0x0.0p+0','float64_hex'),('stratum_role',role,'str'),('cell_id',cell,'str'),('polarization',pol,'str'),('pilot_count',pilot,'int')])}
def hw(tup,role,s,cell,pol,target=None,fix=None):
 q=[('tuple_id',tup,'str'),('stratum_role',role,'str'),('seed',s,'int'),('cell_id',cell,'str'),('polarization',pol,'str')]
 if target is not None: q += [('target_polarization',target,'str'),('fixture_id',fix,'str')]
 return work('HMM_TRAJECTORY_FULL_122_BY_6_GRID',q)
fixtures=ib['hmm_authority']['fixture_owner_legal_order']; seeds=list(range(8000,8010)); cell='snr_10db__linewidth_10000hz'
def hmm(tup,role,pol,target=None):
 pilot=ib['hmm_authority']['pilot_count_by_tuple'][tup]; gp=group(tup,role,pol,pilot); ch='hmmg1-'+rh(gp)
 cp=cpk('b2_hmm_grid_chunk',[('record_type','B2_HMM_GRID_CHUNK','str'),('tuple_id',tup,'str'),('p_s_index',0,'int'),('sigma_e2_index',0,'int'),('stratum_role',role,'str'),('cell_id',cell,'str'),('polarization',pol,'str'),('chunk_id',ch,'str')])
 axes=[(s,None) for s in seeds] if role=='CLEAN_INCLUDED' else [(s,f) for s in seeds for f in fixtures]; ms=[]; bs=[]
 for i,(s,f) in enumerate(axes):
  mp=cpk('b2_tuple_clean_dev',[('record_type','B2_TUPLE_CLEAN_DEV','str'),('tuple_id',tup,'str'),('seed',s,'int'),('cell_id',cell,'str'),('polarization',pol,'str')]) if role=='CLEAN_INCLUDED' else cpk('b2_tuple_controlled_dev',[('record_type','B2_TUPLE_CONTROLLED_DEV','str'),('tuple_id',tup,'str'),('seed',s,'int'),('cell_id',cell,'str'),('target_polarization',target,'str'),('fixture_id',f,'str'),('row_polarization',pol,'str')])
  logical=lid('B2_DEV','HMM_GRID_SCORE',hw(tup,role,s,cell,pol,target,f)); status='EXECUTED'; source=None
  if tup=='M3_N100' or role=='CONTROLLED_SENTINEL_EXCLUDED':
   status='CACHE_READ'; st='M2_N100' if tup=='M3_N100' else tup; source=lid('B2_DEV','HMM_GRID_SCORE',hw(st,'CLEAN_INCLUDED',s,cell,pol))
  ms.append({'ordinal':i,'member_primary_key':mp}); bs.append({'schema':pd['hmm_computation_binding']['version'],'ordinal':i,'member_primary_key':mp,'computation_id':logical,'cache_status':status,'source_computation_id':source})
 mm={'schema':pd['hmm_member_key_manifest']['version'],'consumer_primary_key':cp,'members':ms}; cm={'schema':pd['computation_id_manifest']['version'],'group':{'group_identity':gp,'chunk_id':ch,'consumer_primary_key':cp,'pilot_count':pilot},'aggregate':{'algorithm':'CANONICAL_BINARY64_EXACT_RATIONAL_SUM_V1','member_count':len(ms)},'bindings':bs}
 return ch,mm,cm,bs
G=ib['golden_vectors']; golden=0
def gold(ok,label):
 global golden
 if ck(ok,'golden_'+label): golden+=1
gold(rh(po)==G['grid_commitments']['p_s_sha256'],'grid_p_s'); gold(rh(so)==G['grid_commitments']['sigma_e2_sha256'],'grid_sigma'); gold(rh(combo)==G['grid_commitments']['combined_sha256'],'grid_combined')
for args,key in [(('M2_N100','CLEAN_INCLUDED','X',None),'clean10'),(('M2_N100','CONTROLLED_TARGET_INCLUDED','X','X'),'target90'),(('M2_N100','CONTROLLED_SENTINEL_EXCLUDED','Y','X'),'sentinel90_to_clean'),(('M3_N100','CLEAN_INCLUDED','X',None),'M3_N100_direct_to_M2')]:
 ch,mm,cm,bs=hmm(*args); q=G[key]; gold(ch==q['chunk_id'] and rh(mm)==q['member_key_manifest_sha256'] and rh(cm)==q['computation_ids_manifest_sha256'] and bs[0]['computation_id']==q['first_logical_computation_id'] and ('first_source_computation_id' not in q or bs[0]['source_computation_id']==q['first_source_computation_id']),key)
q=G['S2_off_nine_to_one']; z=q['inputs']; sw=work('S2_B1_OFF_CANONICAL_B04',[('seed',z['seed'],'int'),('cell_id',z['cell_id'],'str'),('target_polarization',z['target_polarization'],'str'),('jump_present',False,'bool'),('method_id',z['method_id'],'str'),('canonical_owner_fixture_id',z['projected_owner_fixture_id'],'str')]); sl=lid('S2','B1_DECODE',sw); sb=[{'consumer_primary_key':cpk('s2_method',[('record_type','S2_METHOD','str'),('seed',z['seed'],'int'),('cell_id',z['cell_id'],'str'),('target_polarization',z['target_polarization'],'str'),('fixture_id',f,'str'),('jump_present',False,'bool'),('method_id',z['method_id'],'str')]),'logical_computation_id':sl} for f in fixtures]; sm={'schema':pd['consumer_binding_manifest']['version'],'binding_kind':z['binding_kind'],'bindings':sb}; gold(sl==q['shared_logical_computation_id'] and rh(sm)==q['consumer_binding_manifest_sha256'],'S2')
q=G['BPS_dual_pol_shared']; z=q['inputs']; bw=work('BPS_DUAL_POL_SHARED',[('tuple_id',z['tuple_id'],'str'),('B',z['B'],'int'),('Nw',z['Nw'],'int'),('seed',z['seed'],'int'),('cell_id',z['cell_id'],'str')]); bl=lid('BPS_DEV','B1_DECODE',bw); bb=[{'consumer_primary_key':cpk('bps_dev_score',[('record_type','BPS_DEV_SCORE','str'),('tuple_id',z['tuple_id'],'str'),('B',z['B'],'int'),('Nw',z['Nw'],'int'),('seed',z['seed'],'int'),('cell_id',z['cell_id'],'str'),('polarization',p,'str')]),'logical_computation_id':bl} for p in z['consumer_polarizations']]; bm={'schema':pd['consumer_binding_manifest']['version'],'binding_kind':z['binding_kind'],'bindings':bb}; gold(bl==q['shared_logical_computation_id'] and rh(bm)==q['consumer_binding_manifest_sha256'],'BPS')
q=G['runtime_clean10_synthetic_exact_sum']; z=q['inputs']; rc=[{'ordinal':i,'content_sha256':hb(f'resolved-member-content-v1:{i}'.encode())} for i in range(10)]; rp={'schema':pd['runtime_aggregate_content']['version'],'computation_ids_manifest_sha256':z['computation_ids_manifest_sha256'],'resolved_member_contents':rc,'normalized_nll_exact_sum_numerator_decimal':z['normalized_nll_exact_sum_numerator_decimal'],'normalized_nll_exact_sum_denominator_power2':z['normalized_nll_exact_sum_denominator_power2'],'member_count':z['member_count']}; gold(rh(rp)==q['content_sha256'],'runtime')

# D017 closed-world mutation rejection against the declarative validator.
mutations=[]
def m(label,fn):
 x=copy.deepcopy(ib)
 try: fn(x); mutations.append((label,not d017_errors(x)))
 except (KeyError, IndexError, TypeError, AttributeError): mutations.append((label,True))
m('binding_kind',lambda x:x['consumer_bindings']['projections']['S2_off'].__setitem__('exact_binding_kind','OTHER'))
m('phase_map',lambda x:x['consumer_bindings']['projections']['S3']['phase_rule']['values'].__setitem__('S3_CANDIDATE_DEV','S3_TEST'))
m('operation_map',lambda x:x['consumer_bindings']['projections']['S2_on']['operation_rule']['values'].__setitem__('OFC17_16QAM_EXTFRAME_V1','B1_DECODE'))
m('work_kind',lambda x:x['consumer_bindings']['projections']['B2_clean'].__setitem__('work_key_kind','OTHER'))
m('source_swap',lambda x:x['consumer_bindings']['projections']['S2_on']['work_key_fields'][0].__setitem__('source','raw.cell_id'))
m('work_atom',lambda x:x['consumer_bindings']['projections']['BPS']['work_key_fields'][1].__setitem__('atom_type','str'))
m('B04_literal',lambda x:x['consumer_bindings']['projections']['S2_off']['work_key_fields'][-1].__setitem__('source','literal.B04_K2'))
m('PK_order',lambda x:x['consumer_bindings']['projections']['S3']['consumer_pk_fields'].reverse())
m('PK_atom',lambda x:x['consumer_bindings']['projections']['B2_controlled']['consumer_pk_fields'][1].__setitem__('atom_type','int'))
m('S4_order',lambda x:x['consumer_bindings']['projections']['S4']['exact_check_ids'].reverse())
m('S4_substitution',lambda x:x['consumer_bindings']['projections']['S4']['exact_check_ids'].__setitem__(0,'other'))
m('HMM_kind',lambda x:x['consumer_bindings']['projections']['HMM_chunk']['reference'].__setitem__('kind','OTHER'))
m('HMM_raw',lambda x:x['consumer_bindings']['projections']['HMM_chunk']['reference'].__setitem__('raw_field','other'))
m('HMM_schema',lambda x:x['consumer_bindings']['projections']['HMM_chunk']['reference'].__setitem__('payload_schema','other'))
m('HMM_rule',lambda x:x['consumer_bindings']['projections']['HMM_chunk']['reference'].__setitem__('rule','other'))
m('HMM_authority',lambda x:x['consumer_bindings']['projections']['HMM_chunk']['reference'].__setitem__('logical_member_authority','other'))
m('common_rule',lambda x:x['consumer_bindings']['rule'].__setitem__('ordinary','other'))
m('descriptor_missing',lambda x:x['consumer_bindings']['projections']['B2_clean']['work_key_fields'].pop())
mutation_pass=sum(ck(not accepted,'mutation_'+label) for label,accepted in mutations)

# Cardinality enumeration and frozen accounting.
consumer_counts={'S2':2160,'S3':10800,'BPS':7200,'B2_clean':1200,'B2_controlled':21600,'S4':len(s4ids)}
logical_counts={'S2':1680,'S3':10800,'BPS':3600,'B2_clean':600,'B2_controlled':10800,'S4':len(s4ids)}
ordinary_bindings=sum(consumer_counts.values()); ordinary_logical=sum(logical_counts.values()); hmm_logical=5*10*12*2*(1+9+9); hmm_chunks=5*122*6*3*12*2; ledger=ordinary_logical+hmm_logical
ck(ordinary_bindings==42967,'ordinary_bindings_42967'); ck(ordinary_logical==27487,'ordinary_logical_27487'); ck(hmm_logical==22800,'HMM_logical_22800'); ck(hmm_chunks==263520,'HMM_chunks_263520'); ck(ledger==50287,'ledger_50287')
la=ib['ledger_accounting']; count_values={'chunks':hmm_chunks,'logical_trajectory_rows':hmm_logical,'logical_primitive_scores':hmm_logical*732,'executed_trajectory_rows':4*10*12*2*(1+9),'materialized_primitive_scores':9600*732,'cache_trajectory_rows':hmm_logical-9600}; count_pass=sum(ck(la['formulas'][k]['expected']==v,'count_'+k) for k,v in count_values.items())

# Science/permission/protection/drift checks.
imb=re.search(rb'(?m)^identity_binding_contract:\r?$',raw); stb=re.search(rb'(?m)^strata:\r?$',raw); projected=raw[:imb.start()]+raw[stb.start():]
ck(hb(projected)==SCI,'scientific_raw_projection','P0')
projected_doc=yaml.load(projected.decode('utf-8'),Loader=Strict); without_identity=copy.deepcopy(doc); without_identity.pop('identity_binding_contract'); ck(without_identity==projected_doc,'scientific_parsed_projection','P0')
c=doc['control']; perms=[c['epoch']==12,c['checkpoint']=='CP012',c['action_class']=='D0_TESTBED_IMPLEMENTATION',c['implementation_authorized'] is True,c['unit_test_authorized'] is True,c['engineering_benchmark_authorized'] is True,c['execution_authorized'] is False,c['scientific_experiment_authorized'] is False,doc['statistical_contract_repair']['scientific_threshold_seed_and_gate_change']=='none']
for i,v in enumerate(perms): ck(v,'permission_'+str(i),'P0')
for p,h in PROTECTED.items(): ck((ROOT/p).is_file() and hf(ROOT/p)==h,'protected_'+p,'P0')
ck(subprocess.run(['git','rev-parse','HEAD'],capture_output=True,text=True).stdout.strip()==HEAD,'HEAD','P0')
staged=subprocess.run(['git','diff','--cached','--name-only'],capture_output=True,text=True); ck(staged.returncode==0 and not staged.stdout.strip(),'staging','P0')
dc=subprocess.run(['git','diff','--check'],capture_output=True,text=True); ck(dc.returncode==0 and not dc.stdout.strip(),'diff_check','P0')
census=(sum(1 for p in ROOT.rglob('*.pyc') if p.is_file()),sum(1 for p in ROOT.rglob('__pycache__') if p.is_dir()),sum(1 for p in ROOT.rglob('.pytest_cache') if p.is_dir())); ck(census==(202,41,4),'cache_census_'+repr(census),'P0')
end_sha=hf(OWNER); ck(end_sha==start_sha,'owner_begin_end_stable','P0')

pc={s:sum(1 for q,_ in failures if q==s) for s in ('P0','P1','P2')}
is_red=start_sha==PRE
verdict='MANDATORY_PRE_EDIT_RED' if is_red and shape_errors else 'FAIL' if failures else 'OWNER_ORDINARY_IDENTITY_COMPLETION_READY_FOR_INDEPENDENT_VERIFICATION'
summary={'verdict':verdict,'P0':pc['P0'],'P1':pc['P1'],'P2':pc['P2'],'assertions':n,'D017_shape_errors':shape_errors,'literal_pass':f'{literals}/128','roots':f'{roots}/3','goldens':f'{golden}/10','mutations':f'{mutation_pass}/18','counts':f'{count_pass}/6','ordinary_bindings':ordinary_bindings,'ordinary_logical_ids':ordinary_logical,'HMM_logical_ids':hmm_logical,'HMM_chunks':hmm_chunks,'ledger_total':ledger,'permission_drift':'none' if not any(l.startswith('permission_') for _,l in failures) else 'detected','grid_count_science_drift':'none' if roots==3 and count_pass==6 and hb(projected)==SCI else 'detected','cache_census':list(census),'owner_start_sha256':start_sha,'owner_end_sha256':end_sha,'failures':[{'severity':s,'label':l} for s,l in failures]}
payload=json.dumps(summary,sort_keys=True,separators=(',',':'),ensure_ascii=False); print(payload); print('stdout_payload_sha256='+hb(payload.encode())); sys.exit(23 if verdict=='MANDATORY_PRE_EDIT_RED' else 0 if verdict=='OWNER_ORDINARY_IDENTITY_COMPLETION_READY_FOR_INDEPENDENT_VERIFICATION' else 1)
```
<!-- verifier:end -->

## Mandatory pre-edit RED receipt

The checker was extracted from the fenced source above and piped through stdin to
`C:\Users\zzt\scoop\apps\python311\current\python.exe -B -` with
`PYTHONDONTWRITEBYTECODE=1` and `PYTHONHASHSEED=0`. No owner edit had occurred.

- terminal: `MANDATORY_PRE_EDIT_RED`
- process exit code: `23`
- assertions: `248`; P0/P1/P2=`0/57/0`
- D017 shape deficits: `41`
- mutation gate before the missing authority exists: `2/18` (non-acceptance result,
  not a final-gate claim)
- preserved old authority: literals `128/128`, roots `3/3`, goldens `10/10`,
  counts `6/6`
- ordinary/HMM/accounting enumeration:
  `42,967 / 27,487 / 22,800 / 263,520 / 50,287`
- permission/grid/count/science drift: none
- owner begin/end SHA256:
  `ca2c8146dec5edec62984cdadf678d808291cb6b2a736fd99059651fc7a50535`
- canonical stdout payload SHA256:
  `151e2a57299f01870be236da10b4ddad1de03f63dfa83973ba819e1f2436e786`

The RED explicitly reported all required deficit families: seven ordinary typed
consumer/work projections and phase/operation authority; five missing work-key
kinds; the erroneous HMM logical-ID binding plus missing manifest reference; the
missing exact S4 check-ID list; and missing D017 coverage/validator/mutation gates.

## Owner repair receipt

The owner-only additive repair implements D017 without changing the scientific
projection or any pre-existing identity root:

- replaced the scalar binding rule with separate exact ordinary and HMM rules;
- expanded seven ordinary projections to 41 ordered typed consumer-PK
  descriptors and 32 ordered typed work-key descriptors;
- froze all ordinary phase/operation rules and seven work-key kinds;
- preserved all existing `consumer_pk_order`, `work_key_order`, `omitted`,
  `preserved`, `cardinality`, and `binding` declarations;
- removed only `HMM_chunk.exact_binding_kind`, then added its eight ordered typed
  PK descriptors and exact `COMPUTATION_IDS_MANIFEST_SHA256` reference;
- copied the seven owner S4 check IDs in the original order;
- added four coverage requirements, three validator obligations, and thirteen
  explicit D017 mutation categories.

No source, test, schema, session, P05, benchmark, science, MVE, install, staging,
commit, or push action was performed.

## Final author gate receipt

### Terminal

`OWNER_ORDINARY_IDENTITY_COMPLETION_READY_FOR_INDEPENDENT_VERIFICATION / P0/P1/P2=0/0/0`

This terminal is limited to owner-byte readiness for an independent verifier. It
does not refresh the loader seal, close I05, or authorize a benchmark/science run.

### Transport and result

The final checker source above was freshly extracted and piped through stdin to
`C:\Users\zzt\scoop\apps\python311\current\python.exe -B -` with
`PYTHONDONTWRITEBYTECODE=1` and `PYTHONHASHSEED=0`. Process exit code: `0`.

- assertions: `208`; D017 shape errors: `0`
- ordinary/HMM projection classes: `7/1`
- work descriptors: `32`; ordinary/all consumer-PK descriptors: `41/49`
- unique phase-operation signatures: `8`
- literals: `128/128`; grid roots: `3/3`; old goldens: `10/10`
- D017 mutations rejected: `18/18`; wrong accepts/rejects: `0/0`
- accounting formulas: `6/6`
- ordinary bindings/logical IDs: `42,967 / 27,487`
- HMM logical IDs/chunks: `22,800 / 263,520`
- total ledger identities: `50,287`
- scientific raw and parsed projections: exact; permission/grid/count/science
  drift: none
- frozen receipts, P05 four hashes, cache census `202/41/4`, HEAD, empty staging,
  `git diff --check`, and owner begin/end stability: PASS
- final owner SHA256:
  `02d471a200a1dce17f2c43dd36ca90b050ebdc943c7c045483e816a07162d140`
- canonical stdout payload SHA256:
  `ca000c81434f14b1ff6593d8545948b22271c0e2975428d63604959faf23c0de`

### Complete final stdout

```text
{"D017_shape_errors":[],"HMM_chunks":263520,"HMM_logical_ids":22800,"P0":0,"P1":0,"P2":0,"assertions":208,"cache_census":[202,41,4],"counts":"6/6","failures":[],"goldens":"10/10","grid_count_science_drift":"none","ledger_total":50287,"literal_pass":"128/128","mutations":"18/18","ordinary_bindings":42967,"ordinary_logical_ids":27487,"owner_end_sha256":"02d471a200a1dce17f2c43dd36ca90b050ebdc943c7c045483e816a07162d140","owner_start_sha256":"02d471a200a1dce17f2c43dd36ca90b050ebdc943c7c045483e816a07162d140","permission_drift":"none","roots":"3/3","verdict":"OWNER_ORDINARY_IDENTITY_COMPLETION_READY_FOR_INDEPENDENT_VERIFICATION"}
stdout_payload_sha256=ca000c81434f14b1ff6593d8545948b22271c0e2975428d63604959faf23c0de
process_exit_code=0
```
