# Step 151 — D0 owner canonical identity independent verification retry

> 2026-08-10 | T105 | `FAIL`

## Verifier source

<!-- verifier:start -->
```python
import copy, hashlib, json, math, re, subprocess, sys
from pathlib import Path
import yaml
import numpy as np

ROOT=Path.cwd()
OWNER=ROOT/'projects/thesis-fso/coded-decoder-feedback-groundwork/d0-defect-smoke-contract.yaml'
OLD='c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d'
FINAL='9f12cd11d210aef10c08848ccf42f39183f1ebf5f061d7203d3879335278990d'
HEAD='715a65884b988ee737f21982f3bbf372860a1da8'
ROOTS={'p_s':'bfc3cef2c8e6fc800b6a40f9da778ab98b666ec57e5e12ae1f0c8b9f25b78864','sigma_e2':'0f37cdf467a04283bbf03792c5654545947ce759c052ed11e98c20c2618401ca','combined':'0cdb5e547e31997cd931a97f97f681ff5eeae28c372810eb12f593f4dca99fdf'}
PROTECTED={
'.sessions/2026-08-09-coded-decoder-feedback-groundwork/R001-d0-canonical-identity-binding.md':'679e437b052f5b664f2aae1a42f7268482612c396d9a613d6ea6c18e1d285a4d',
'.sessions/2026-08-09-coded-decoder-feedback-groundwork/decisions.md':'376c3e740a6e4987734bcb64ebf96ffe417d5566ce4342a01e2f20ca2f5674b0',
'.sessions/2026-08-09-coded-decoder-feedback-groundwork/verifications.md':'16957db808e656f5c13bb982aa3c4477846f6264af2668abbe6ad85207d6d56f',
'projects/thesis-fso/worker-logs/step-147-d0-i05-fresh-authority-graph-reverification.md':'a08213733ba451cca0e66da4a5582b455aed071b296abb448d05dd760821041f',
'projects/thesis-fso/worker-logs/step-148-d0-owner-canonical-identity-contract.md':'c089a52190988b7695e6df66a153984ef1bf06f8ade98132a63145490eea31af',
'projects/thesis-fso/worker-logs/step-149-d0-owner-canonical-identity-contract-retry.md':'c69e974e860b5948f44307e51077f7b94ad783a07b4b103db1416af858ab70a8',
'projects/thesis-fso/worker-logs/step-150-d0-owner-canonical-identity-independent-verification.md':'e54d130d7cc080dddc33616e159e2263324850278489d0ee871896120c458fe7',
'projects/simulation/explore/coded-decoder-feedback/schemas.py':'a42ffa184d2db3cfa68775b9dc0b3aac60195bf34abfdf5e37732f398445e401',
'projects/simulation/tests/test_d0_schemas_statistics.py':'a94731c3c9d44c1f0ba8ef1b27df578cbb9f982f3069f51786f3becc419dd4c9',
'projects/simulation/explore/cma-fade-divergence/p05_run.log':'7843b048a2a79755c95542a438a5344f8e89e791113f48913926c419fc2a4f11',
'projects/simulation/explore/cma-fade-divergence/p05_run2.log':'735e4650093d297e01a0e6dfe28f0431c149a2931fcbb7c08eecfa28f0aac38b',
'projects/simulation/explore/cma-fade-divergence/p05_run3.log':'c76887c6950aaac2b4c0dced7689517749322c44da868880915786c173b1344d',
'projects/simulation/explore/cma-fade-divergence/p05_run4.log':'95a1d184740a797b6d55d7f817008c898cb3754987ab6e1c1d00376f74a621de'}

n=0; fails=[]
def ck(x,label,sev='P1'):
 global n
 n+=1
 if not x: fails.append((sev,label))
 return bool(x)
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
ck(start_sha==FINAL,'owner_start','P0')
try: doc=yaml.load(text,Loader=Strict); ck(isinstance(doc,dict),'strict_parse','P0')
except Exception as e:
 print(json.dumps({'verdict':'INCOMPLETE_STRICT_PARSE','error':repr(e)},sort_keys=True)); sys.exit(3)

# Exact authority-approved aliases: two definitions plus two uses, nowhere else.
tokens=list(yaml.scan(text))
anchor_tokens=[t.value for t in tokens if isinstance(t,yaml.tokens.AnchorToken)]
alias_tokens=[t.value for t in tokens if isinstance(t,yaml.tokens.AliasToken)]
ck(anchor_tokens==['id001','id002'] and alias_tokens==['id001','id002'],'exact_2anchors_2aliases','P0')
ck(len(re.findall(r'(?m)^      standalone_payload: &id001$',text))==1,'anchor_id001_path','P0')
ck(len(re.findall(r'(?m)^      standalone_payload: &id002$',text))==1,'anchor_id002_path','P0')
ck(len(re.findall(r'(?m)^        p_s: \*id001$',text))==1,'alias_id001_path','P0')
ck(len(re.findall(r'(?m)^        sigma_e2: \*id002$',text))==1,'alias_id002_path','P0')
events=list(yaml.parse(text)); ae=[e for e in events if isinstance(e,yaml.events.AliasEvent)]
ck([e.anchor for e in ae]==['id001','id002'],'alias_events_exact','P0')

ims=list(re.finditer(r'(?m)^identity_binding_contract:\r?$',text)); sms=list(re.finditer(r'(?m)^statistical_contract_repair:\r?$',text)); sts=list(re.finditer(r'(?m)^strata:\r?$',text))
ck(len(ims)==len(sms)==len(sts)==1,'single_blocks','P0')
ck(sms[0].start()<ims[0].start()<sts[0].start(),'placement','P0')
imb=re.search(rb'(?m)^identity_binding_contract:\r?$',raw); stb=re.search(rb'(?m)^strata:\r?$',raw)
projected=raw[:imb.start()]+raw[stb.start():]
ck(hb(projected)==OLD,'raw_projection','P0')
old_doc=yaml.load(projected.decode(),Loader=Strict); npj=copy.deepcopy(doc); ib=npj.pop('identity_binding_contract')
ck(npj==old_doc,'parsed_projection','P0')
keys=['schema_version','decision_ref','scientific_contract_change','canonical_serialization','grid_authority','payload_schemas','hmm_authority','ledger_accounting','cache_source','consumer_bindings','runtime_content','golden_vectors','validator_obligations']
ck(list(ib)==keys,'identity_13_keys','P0'); ck(ib['schema_version']=='coded_decoder_feedback.d0.identity_binding.v1','schema','P0'); ck(ib['decision_ref']=='D015','decision','P0'); ck(ib['scientific_contract_change']=='none','science_none','P0')
c=doc['control']; permissions=[(c['epoch'],12),(c['checkpoint'],'CP012'),(c['action_class'],'D0_TESTBED_IMPLEMENTATION'),(c['implementation_authorized'],True),(c['unit_test_authorized'],True),(c['engineering_benchmark_authorized'],True),(c['execution_authorized'],False),(c['scientific_experiment_authorized'],False),(doc['purpose']['not_mve'],True),(doc['purpose']['not_c1_extension'],True),(doc['statistical_contract_repair']['scientific_threshold_seed_and_gate_change'],'none')]
for i,(a,b) in enumerate(permissions): ck(a==b,'permission_'+str(i),'P0')

cs=ib['canonical_serialization']; cj=cs['canonical_json']
for k,a,b in [('encoding',cs['encoding'],'UTF-8'),('sort',cj['sort_keys'],True),('sep',cj['separators'],[',',':']),('ascii',cj['ensure_ascii'],False),('nan',cj['allow_nan'],False),('newline',cs['trailing_newline'],'forbidden'),('float',cs['json_float'],'forbidden_in_every_identity_payload')]: ck(a==b,'canonical_'+k)
ck(cs['typed_atom']['exact_object_field_order']==['type','value'],'atom_order'); ck(cs['typed_atom']['allowed_types']==['str','int','bool','none','float64_hex'],'atom_types'); ck(cs['ordered_field_entry']['exact_object_field_order']==['name','atom'],'field_entry')

# Full literal authority.
ck(np.__version__=='2.4.3','numpy_version')
eps=[float(x).hex() for x in np.concatenate((np.array([0.],dtype=np.float64),np.logspace(-7,-1,121,endpoint=True,base=10,dtype=np.float64)))]
ess=[float(x).hex() for x in np.array([0.,1e-5,1e-4,1e-3,1e-2,1e-1],dtype=np.float64)]
ga=ib['grid_authority']; po=ga['p_s']['standalone_payload']; so=ga['sigma_e2']['standalone_payload']; literal_ok=0
for name,obj,exp,count in [('p_s',po,eps,122),('sigma_e2',so,ess,6)]:
 vals=obj['values']; ck(ga[name]['count']==count,name+'_count'); ck(len(vals)==count,name+'_length'); ck(list(obj)==['schema','name','values'],name+'_payload_order'); ck(obj['schema']=='coded_decoder_feedback.d0.float64_grid.v1' and obj['name']==name,name+'_payload_header')
 parsed=[]
 for i,(v,h) in enumerate(zip(vals,exp)):
  ck(list(v)==['index','float64_hex'],f'{name}_{i}_keys'); ck(type(v['index']) is int and v['index']==i,f'{name}_{i}_index'); exact=ck(type(v['float64_hex']) is str and v['float64_hex']==h,f'{name}_{i}_hex')
  try: x=float.fromhex(v['float64_hex']); good=math.isfinite(x) and x.hex()==v['float64_hex'] and v['float64_hex']==v['float64_hex'].lower() and not(x==0 and math.copysign(1,x)<0); parsed.append(x)
  except Exception: good=False
  ck(good,f'{name}_{i}_canonical')
  if exact and good: literal_ok+=1
 ck(len({v['float64_hex'] for v in vals})==count,name+'_unique'); ck(all(parsed[i]<parsed[i+1] for i in range(len(parsed)-1)),name+'_increasing')
ck(ga['p_s']['anchors']=={0:eps[0],1:eps[1],61:eps[61],121:eps[121]},'anchors')
combo=ga['combined']['payload']; root_ok=0
for cond,label in [(rh(po)==ga['p_s']['sha256']==ROOTS['p_s'],'ps'),(rh(so)==ga['sigma_e2']['sha256']==ROOTS['sigma_e2'],'sigma'),(rh(combo)==ga['combined']['sha256']==ROOTS['combined'],'combined')]:
 if ck(cond,'root_'+label): root_ok+=1
ck(combo['p_s']==po and combo['sigma_e2']==so,'combined_deep_equal'); ck(list(combo)==['schema','p_s','sigma_e2'] and combo['schema']=='coded_decoder_feedback.d0.hmm_grid_commitment.v1','combined_shape')

# Domain/version/field-order authority.
pd=ib['payload_schemas']; expected={
'consumer_primary_key':('coded_decoder_feedback.d0.consumer_primary_key.v1',['schema','table','fields']),
'typed_work_key':('coded_decoder_feedback.d0.typed_work_key.v1',['schema','kind','fields']),
'hmm_group_identity':('coded_decoder_feedback.d0.hmm_group_identity.v1',['schema','kind','fields']),
'hmm_member_key_manifest':('coded_decoder_feedback.d0.hmm_member_key_manifest.v1',['schema','consumer_primary_key','members']),
'hmm_computation_binding':('coded_decoder_feedback.d0.hmm_computation_binding.v1',['schema','ordinal','member_primary_key','computation_id','cache_status','source_computation_id']),
'logical_computation_identity':('coded_decoder_feedback.d0.logical_computation_identity.v1',['schema','phase','operation','work_key']),
'computation_id_manifest':('coded_decoder_feedback.d0.computation_id_manifest.v1',['schema','group','aggregate','bindings']),
'consumer_binding_manifest':('coded_decoder_feedback.d0.consumer_binding_manifest.v1',['schema','binding_kind','bindings']),
'runtime_aggregate_content':('coded_decoder_feedback.d0.hmm_runtime_aggregate_content.v1',['schema','computation_ids_manifest_sha256','resolved_member_contents','normalized_nll_exact_sum_numerator_decimal','normalized_nll_exact_sum_denominator_power2','member_count'])}
ck(list(pd)==['global_rule']+list(expected),'payload_sections'); versions=[]
for k,(v,o) in expected.items(): versions.append(v); ck(pd[k]['version']==v,k+'_version'); ck(pd[k]['exact_object_field_order']==o,k+'_order'); ck(len(o)==len(set(o)),k+'_unique_order')
ck(len(versions)==len(set(versions)),'domain_unique')
ck(pd['consumer_primary_key']['field_entry_order']==['name','atom'],'cpk_field_order'); ck(pd['typed_work_key']['field_entry_order']==['name','atom'],'work_field_order'); ck(pd['hmm_group_identity']['fields_order']==['tuple_id','p_s_index','p_s_float64_hex','sigma_e2_index','sigma_e2_float64_hex','stratum_role','cell_id','polarization','pilot_count'],'group_order'); ck(pd['hmm_member_key_manifest']['member_entry_order']==['ordinal','member_primary_key'],'member_order'); ck(pd['computation_id_manifest']['group_entry_order']==['group_identity','chunk_id','consumer_primary_key','pilot_count'],'manifest_group_order'); ck(pd['computation_id_manifest']['aggregate_entry_order']==['algorithm','member_count'],'aggregate_order'); ck(pd['consumer_binding_manifest']['binding_entry_order']==['consumer_primary_key','logical_computation_id'],'binding_order'); ck(pd['runtime_aggregate_content']['resolved_content_entry_order']==['ordinal','content_sha256'],'content_order')
ck(ib['runtime_content']['preexecution_identity_excludes']==['resolved_member_content_sha256','exact_sum_numerator','exact_sum_denominator_power2'],'preexec_excludes'); ck(ib['runtime_content']['binds']==['computation_ids_manifest_sha256','ordered_resolved_member_content_sha256_with_ordinals','normalized_nll_exact_sum_numerator_decimal','normalized_nll_exact_sum_denominator_power2','member_count'],'runtime_binds'); ck(ib['runtime_content']['ordinary_order_dependent_float_sum']=='forbidden','runtime_no_float_sum')

bad=[]; empty=[]
def walk(x,p='identity'):
 if isinstance(x,dict):
  if not x: empty.append(p)
  for k,v in x.items(): walk(v,p+'.'+str(k))
 elif isinstance(x,list):
  if not x: empty.append(p)
  for i,v in enumerate(x): walk(v,p+f'[{i}]')
 elif isinstance(x,str):
  if not x: empty.append(p)
  if re.fullmatch(r'(?i)(TODO|TBD|UNKNOWN|PLACEHOLDER|FILL_ME|OMITTED|EXAMPLE_ONLY|PENDING)',x) or '...' in x or '…' in x or re.search(r'<[^>]*>',x) or re.search(r'\{(?:placeholder|todo|tbd)[^}]*\}',x,re.I): bad.append((p,x))
walk(ib); ck(not bad,'no_placeholder'); ck(not empty,'no_illegal_empty')

# Independent payload builders.
def atom(v,t=None):
 if t is None: t='none' if v is None else 'bool' if type(v) is bool else 'int' if type(v) is int else 'str'
 return {'type':t,'value':v}
def ents(items): return [{'name':k,'atom':atom(v,t)} for k,v,t in items]
def cpk(table,items): return {'schema':pd['consumer_primary_key']['version'],'table':table,'fields':ents(items)}
def work(kind,items): return {'schema':pd['typed_work_key']['version'],'kind':kind,'fields':ents(items)}
def lid(phase,op,w): return 'd0c1-'+rh({'schema':pd['logical_computation_identity']['version'],'phase':phase,'operation':op,'work_key':w})
def group(tup,role,pol,pilot,cell='snr_10db__linewidth_10000hz',pi=0,ph='0x0.0p+0',si=0,sh='0x0.0p+0'):
 return {'schema':pd['hmm_group_identity']['version'],'kind':'HMM_GRID_CHUNK_GROUP','fields':ents([('tuple_id',tup,'str'),('p_s_index',pi,'int'),('p_s_float64_hex',ph,'float64_hex'),('sigma_e2_index',si,'int'),('sigma_e2_float64_hex',sh,'float64_hex'),('stratum_role',role,'str'),('cell_id',cell,'str'),('polarization',pol,'str'),('pilot_count',pilot,'int')])}
def chunkpk(tup,role,pol,ch,cell): return cpk('b2_hmm_grid_chunk',[('record_type','B2_HMM_GRID_CHUNK','str'),('tuple_id',tup,'str'),('p_s_index',0,'int'),('sigma_e2_index',0,'int'),('stratum_role',role,'str'),('cell_id',cell,'str'),('polarization',pol,'str'),('chunk_id',ch,'str')])
def cleanpk(tup,s,cell,pol): return cpk('b2_tuple_clean_dev',[('record_type','B2_TUPLE_CLEAN_DEV','str'),('tuple_id',tup,'str'),('seed',s,'int'),('cell_id',cell,'str'),('polarization',pol,'str')])
def ctrlpk(tup,s,cell,target,fix,row): return cpk('b2_tuple_controlled_dev',[('record_type','B2_TUPLE_CONTROLLED_DEV','str'),('tuple_id',tup,'str'),('seed',s,'int'),('cell_id',cell,'str'),('target_polarization',target,'str'),('fixture_id',fix,'str'),('row_polarization',row,'str')])
def hw(tup,role,s,cell,pol,target=None,fix=None):
 a=[('tuple_id',tup,'str'),('stratum_role',role,'str'),('seed',s,'int'),('cell_id',cell,'str'),('polarization',pol,'str')]
 if target is not None: a += [('target_polarization',target,'str'),('fixture_id',fix,'str')]
 return work('HMM_TRAJECTORY_FULL_122_BY_6_GRID',a)
def hid(tup,role,s,cell,pol,target=None,fix=None): return lid('B2_DEV','HMM_GRID_SCORE',hw(tup,role,s,cell,pol,target,fix))
fixtures=ib['hmm_authority']['fixture_owner_legal_order']; seeds=list(range(8000,8010)); cell='snr_10db__linewidth_10000hz'
def hmm(tup,role,pol,target=None):
 pilot=ib['hmm_authority']['pilot_count_by_tuple'][tup]; gp=group(tup,role,pol,pilot,cell); ch='hmmg1-'+rh(gp); consumer=chunkpk(tup,role,pol,ch,cell); members=[]; bindings=[]; axes=[(s,None) for s in seeds] if role=='CLEAN_INCLUDED' else [(s,f) for s in seeds for f in fixtures]
 for i,(s,f) in enumerate(axes):
  mp=cleanpk(tup,s,cell,pol) if role=='CLEAN_INCLUDED' else ctrlpk(tup,s,cell,target,f,pol); logical=hid(tup,role,s,cell,pol,target,f); status='EXECUTED'; source=None
  if tup=='M3_N100' or role=='CONTROLLED_SENTINEL_EXCLUDED':
   status='CACHE_READ'; st='M2_N100' if tup=='M3_N100' else tup; source=hid(st,'CLEAN_INCLUDED',s,cell,pol) if role in ('CLEAN_INCLUDED','CONTROLLED_SENTINEL_EXCLUDED') else hid(st,role,s,cell,pol,target,f)
  members.append({'ordinal':i,'member_primary_key':mp}); bindings.append({'schema':pd['hmm_computation_binding']['version'],'ordinal':i,'member_primary_key':mp,'computation_id':logical,'cache_status':status,'source_computation_id':source})
 mm={'schema':pd['hmm_member_key_manifest']['version'],'consumer_primary_key':consumer,'members':members}; cm={'schema':pd['computation_id_manifest']['version'],'group':{'group_identity':gp,'chunk_id':ch,'consumer_primary_key':consumer,'pilot_count':pilot},'aggregate':{'algorithm':'CANONICAL_BINARY64_EXACT_RATIONAL_SUM_V1','member_count':len(members)},'bindings':bindings}
 return {'group':gp,'chunk':ch,'members':members,'bindings':bindings,'mm':mm,'cm':cm}

G=ib['golden_vectors']; gp=0; grun=10
def gold(x,label):
 global gp
 if ck(x,'golden_'+label): gp+=1
gold(rh(po)==G['grid_commitments']['p_s_sha256'],'grid_ps'); gold(rh(so)==G['grid_commitments']['sigma_e2_sha256'],'grid_sigma'); gold(rh(combo)==G['grid_commitments']['combined_sha256'],'grid_combined')
cl=hmm('M2_N100','CLEAN_INCLUDED','X'); q=G['clean10']; gold(len(cl['members'])==10 and cl['chunk']==q['chunk_id'] and rh(cl['mm'])==q['member_key_manifest_sha256'] and rh(cl['cm'])==q['computation_ids_manifest_sha256'] and cl['bindings'][0]['computation_id']==q['first_logical_computation_id'],'clean10')
tg=hmm('M2_N100','CONTROLLED_TARGET_INCLUDED','X','X'); q=G['target90']; gold(len(tg['members'])==90 and tg['chunk']==q['chunk_id'] and rh(tg['mm'])==q['member_key_manifest_sha256'] and rh(tg['cm'])==q['computation_ids_manifest_sha256'] and tg['bindings'][0]['computation_id']==q['first_logical_computation_id'],'target90')
sn=hmm('M2_N100','CONTROLLED_SENTINEL_EXCLUDED','Y','X'); q=G['sentinel90_to_clean']; gold(len(sn['members'])==90 and sn['chunk']==q['chunk_id'] and rh(sn['mm'])==q['member_key_manifest_sha256'] and rh(sn['cm'])==q['computation_ids_manifest_sha256'] and sn['bindings'][0]['computation_id']==q['first_logical_computation_id'] and sn['bindings'][0]['source_computation_id']==q['first_source_computation_id'],'sentinel90')
m3=hmm('M3_N100','CLEAN_INCLUDED','X'); q=G['M3_N100_direct_to_M2']; gold(len(m3['members'])==10 and m3['chunk']==q['chunk_id'] and rh(m3['mm'])==q['member_key_manifest_sha256'] and rh(m3['cm'])==q['computation_ids_manifest_sha256'] and m3['bindings'][0]['computation_id']==q['first_logical_computation_id'] and m3['bindings'][0]['source_computation_id']==q['first_source_computation_id'],'m3_direct')

q=G['S2_off_nine_to_one']; z=q['inputs']; w=work('S2_B1_OFF_CANONICAL_B04',[('seed',z['seed'],'int'),('cell_id',z['cell_id'],'str'),('target_polarization',z['target_polarization'],'str'),('jump_present',False,'bool'),('method_id',z['method_id'],'str'),('canonical_owner_fixture_id',z['projected_owner_fixture_id'],'str')]); sl=lid('S2','B1_DECODE',w); sb=[]
for f in fixtures: sb.append({'consumer_primary_key':cpk('s2_method',[('record_type','S2_METHOD','str'),('seed',z['seed'],'int'),('cell_id',z['cell_id'],'str'),('target_polarization',z['target_polarization'],'str'),('fixture_id',f,'str'),('jump_present',False,'bool'),('method_id',z['method_id'],'str')]),'logical_computation_id':sl})
sm={'schema':pd['consumer_binding_manifest']['version'],'binding_kind':'S2_OFF_NINE_TO_ONE','bindings':sb}; gold(sl==q['shared_logical_computation_id'] and rh(sm)==q['consumer_binding_manifest_sha256'] and len(sb)==9 and len({x['logical_computation_id'] for x in sb})==1,'s2')
q=G['BPS_dual_pol_shared']; z=q['inputs']; w=work('BPS_DUAL_POL_SHARED',[('tuple_id',z['tuple_id'],'str'),('B',z['B'],'int'),('Nw',z['Nw'],'int'),('seed',z['seed'],'int'),('cell_id',z['cell_id'],'str')]); bl=lid('BPS_DEV','B1_DECODE',w); bb=[]
for pol in z['consumer_polarizations']: bb.append({'consumer_primary_key':cpk('bps_dev_score',[('record_type','BPS_DEV_SCORE','str'),('tuple_id',z['tuple_id'],'str'),('B',z['B'],'int'),('Nw',z['Nw'],'int'),('seed',z['seed'],'int'),('cell_id',z['cell_id'],'str'),('polarization',pol,'str')]),'logical_computation_id':bl})
bm={'schema':pd['consumer_binding_manifest']['version'],'binding_kind':'BPS_DUAL_POL_SHARED','bindings':bb}; gold(bl==q['shared_logical_computation_id'] and rh(bm)==q['consumer_binding_manifest_sha256'] and len(bb)==2 and len({x['logical_computation_id'] for x in bb})==1,'bps')
q=G['runtime_clean10_synthetic_exact_sum']; z=q['inputs']; rc=[{'ordinal':i,'content_sha256':hb(f'resolved-member-content-v1:{i}'.encode())} for i in range(10)]; rp={'schema':pd['runtime_aggregate_content']['version'],'computation_ids_manifest_sha256':z['computation_ids_manifest_sha256'],'resolved_member_contents':rc,'normalized_nll_exact_sum_numerator_decimal':z['normalized_nll_exact_sum_numerator_decimal'],'normalized_nll_exact_sum_denominator_power2':z['normalized_nll_exact_sum_denominator_power2'],'member_count':z['member_count']}; gold(rc[0]['content_sha256']==q['first_resolved_content_sha256'] and rc[-1]['content_sha256']==q['last_resolved_content_sha256'] and rh(rp)==q['content_sha256'],'runtime')

# Payloads contain no JSON float and no newline; field layouts are independently materialized.
payloads=[po,so,combo,cl['group'],cl['mm'],cl['cm'],tg['cm'],sn['cm'],m3['cm'],sm,bm,rp]
def floats(x):
 if type(x) is float: return 1
 if isinstance(x,dict): return sum(floats(v) for v in x.values())
 if isinstance(x,list): return sum(floats(v) for v in x)
 return 0
for i,p in enumerate(payloads): ck(floats(p)==0,'payload_no_float_'+str(i)); ck(not enc(p).endswith(b'\n'),'payload_no_newline_'+str(i))

# Fifteen fresh mutations.
req=set(ib['validator_obligations']['required']); rej=set(ib['validator_obligations']['reject_mutations']); mp=0; mrun=15
def mut(x,label,o=True):
 global mp
 if ck(x and o,'mutation_'+label): mp+=1
x=copy.deepcopy(cl['mm']); x['members'][-1]['member_primary_key']['fields'][2]['atom']['value']=9999; mut(rh(x)!=rh(cl['mm']),'replacement','equal_count_member_replacement' in rej)
x=copy.deepcopy(cl['mm']); x['members'][0],x['members'][1]=x['members'][1],x['members'][0]; mut(rh(x)!=rh(cl['mm']),'member_order','member_ordinal_exchange' in rej)
x=copy.deepcopy(cl['mm']); x['members'][0]['ordinal']=1; mut(rh(x)!=rh(cl['mm']),'ordinal','member_ordinal_exchange' in rej)
x=copy.deepcopy(cl['group']); x['fields'][6]['atom']['value']='other'; mut(rh(x)!=rh(cl['group']),'cell','group_role_cell_polarization_or_grid_exchange' in rej)
x=copy.deepcopy(cl['group']); x['fields'][5]['atom']['value']='CONTROLLED_TARGET_INCLUDED'; mut(rh(x)!=rh(cl['group']),'role','group_role_cell_polarization_or_grid_exchange' in rej)
x=copy.deepcopy(cl['group']); x['fields'][1]['atom']['value']=1; mut(rh(x)!=rh(cl['group']),'grid','group_role_cell_polarization_or_grid_exchange' in rej)
x=copy.deepcopy(cl['group']); x['fields'][2]['atom']['value']=eps[1]; mut(rh(x)!=rh(cl['group']),'hex','p_s_or_sigma_index_hex_exchange' in rej)
x=copy.deepcopy(rp); x['computation_ids_manifest_sha256']='0'*64; mut(rh(x)!=rh(rp),'runtime_manifest','runtime_content_root_manifest_ordered_content_exact_sum_and_count_exact' in req)
x=copy.deepcopy(rp); x['resolved_member_contents'][0]['content_sha256']='0'*64; mut(rh(x)!=rh(rp),'runtime_content','runtime_content_root_manifest_ordered_content_exact_sum_and_count_exact' in req)
x=copy.deepcopy(m3['cm']); x['bindings'][0]['source_computation_id']=x['bindings'][1]['computation_id']; mut(rh(x)!=rh(m3['cm']),'cache_chain','CACHE_READ_to_CACHE_READ_chain' in rej)
x=copy.deepcopy(sn['cm']); x['bindings'][0]['source_computation_id']='d0c1-'+'0'*64; mut(rh(x)!=rh(sn['cm']),'source_content','source_or_cache_content_mismatch' in rej)
x=copy.deepcopy(m3['cm']); x['bindings'][0]['computation_id']=x['bindings'][0]['source_computation_id']; mut(rh(x)!=rh(m3['cm']),'logical_swallow','logical_computation_id_replaced_by_source_id' in rej)
x=copy.deepcopy(sm); x['bindings'][0]['logical_computation_id']='d0c1-'+'f'*64; mut(rh(x)!=rh(sm),'s2_swap','same_phase_consumer_computation_exchange' in rej)
x=copy.deepcopy(sm); x['bindings'].pop(); mut(rh(x)!=rh(sm),'s2_orphan','forward_reverse_coverage_no_orphan_extra_duplicate' in req)
x=copy.deepcopy(ib['ledger_accounting']['dual_pol_pair_charge']); x['owner_polarization']='Y'; x['X_hmm_dual_pol_frame_parameter_pair_scores']=0; x['Y_hmm_dual_pol_frame_parameter_pair_scores']=732; mut(x!=ib['ledger_accounting']['dual_pol_pair_charge'],'charge_swap','X_pair_charge_732_Y_zero_and_XY_pairs_complete' in req)

# Six formula checks plus old-owner accounting cross-check.
la=ib['ledger_accounting']; vals={'chunks':5*122*6*3*12*2,'logical_trajectory_rows':5*10*12*2*(1+9+9),'logical_primitive_scores':22800*122*6,'executed_trajectory_rows':4*10*12*2*(1+9),'materialized_primitive_scores':9600*122*6,'cache_trajectory_rows':22800-9600}; cp=0; crun=6
for k,v in vals.items():
 if ck(la['formulas'][k]['expected']==v,'count_'+k): cp+=1
ck(la['cost_bearing_group_aggregate_row']=='forbidden','no_group_ledger'); ck(la['parameter_pair_ledger_row']=='forbidden','no_pair_ledger'); ck(la['per_logical_trajectory']['hmm_primitive_pol_trajectory_parameter_pair_scores']==732,'trajectory732'); ck(la['per_logical_trajectory']['materialized_primitive_scores']=='732_only_for_EXECUTED_and_zero_for_CACHE_READ','executed_only'); q=la['dual_pol_pair_charge']; ck(q['owner_polarization']=='X' and q['X_hmm_dual_pol_frame_parameter_pair_scores']==732 and q['Y_hmm_dual_pol_frame_parameter_pair_scores']==0,'X732Y0'); ck(q['logical_pair_owner_rows']*732==q['expected_total']==8344800,'total8344800')
ob=doc['statistical_contract_repair']['dev_exposure_and_cost']['b2_freeze']; ck(ob['logical_primitive_pol_trajectory_parameter_pair_scores']==16689600,'old_logical'); ck(ob['materialized_primitive_pol_trajectory_parameter_pair_scores_upper_bound']==7027200,'old_materialized'); ck(ob['logical_dual_pol_frame_parameter_pair_scores']==8344800,'old_dual')

# Cache/consumer/obligation coverage.
cache=ib['cache_source']; cb=ib['consumer_bindings']; ck(cache['canonical_N100_executed_owner']=='M2_N100','M2_owner'); ck(cache['M3_N100_sentinel_rule']=='directly_source_M2_N100_clean_EXECUTED_computation','M3_sentinel')
for s in ['source_cache_status_is_EXECUTED','source_source_computation_id_is_null','cache_chain_is_forbidden','logical_computation_id_is_preserved_and_never_replaced_by_source_id','CACHE_READ_and_source_content_sha256_are_equal']: ck(s in cache['source_requirements'],'cache_'+s)
ck(cache['reuse_scope']['forbidden']==['cross_M_downstream_B2_DECODE'],'no_crossM_decode'); ck(list(cb['projections'])==['S2_off','S2_on','S3','BPS','B2_clean','B2_controlled','HMM_chunk','S4'],'consumer_set'); ck(cb['projections']['S2_off']['canonical_owner_fixture_id']=='B04_K1' and cb['projections']['S2_off']['omitted']==['fixture_id'],'S2_projection'); ck(cb['projections']['BPS']['omitted']==['polarization'],'BPS_projection'); ck(cb['projections']['B2_clean']['omitted']==['polarization'],'B2clean_projection'); ck(cb['projections']['B2_controlled']['omitted']==['row_polarization'],'B2ctrl_projection'); ck(cb['projections']['S4']['implicit_or_prefixed_plan']=='forbidden','S4_explicit')
must={'all_122_p_s_literals_indexed_canonical_unique_strictly_increasing','all_6_sigma_literals_indexed_canonical_unique_strictly_increasing','standalone_grid_payloads_and_roots_exact','combined_payload_nested_deep_equal_and_root_exact','all_payload_domain_versions_and_field_orders_exact','all_six_count_formulas_exact','M3_N100_direct_sources_M2_N100','cache_chain_forbidden_and_logical_id_preserved','forward_reverse_coverage_no_orphan_extra_duplicate','same_phase_computation_exchange_rejected','runtime_content_root_manifest_ordered_content_exact_sum_and_count_exact','all_golden_vectors_recomputed_from_saved_inputs','scientific_projection_deep_equal_after_removing_this_block'}
for s in sorted(must): ck(s in req,'obligation_'+s)

# Protection and stable final bytes.
gothead=subprocess.run(['git','rev-parse','HEAD'],capture_output=True,text=True).stdout.strip(); ck(gothead==HEAD,'HEAD','P0'); staged=subprocess.run(['git','diff','--cached','--name-only'],capture_output=True,text=True); ck(staged.returncode==0 and not staged.stdout.strip(),'staging','P0')
for p,h in PROTECTED.items(): ck((ROOT/p).is_file() and hf(ROOT/p)==h,'protected_'+p,'P0')
census=(sum(1 for p in ROOT.rglob('*.pyc') if p.is_file()),sum(1 for p in ROOT.rglob('__pycache__') if p.is_dir()),sum(1 for p in ROOT.rglob('.pytest_cache') if p.is_dir())); ck(census==(202,41,4),'cache_census_'+repr(census),'P0')
dc=subprocess.run(['git','diff','--check'],capture_output=True,text=True); ck(dc.returncode==0 and not dc.stdout.strip(),'diff_check','P0'); end_sha=hf(OWNER); ck(end_sha==start_sha==FINAL,'owner_stable','P0'); ck(n>=240,'assertions_ge240','P2')

pc={s:sum(1 for q,_ in fails if q==s) for s in ('P0','P1','P2')}; complete=(grun==10 and mrun==15 and crun==6 and n>=240)
verdict='INCOMPLETE_REQUIRED_CHECK_NOT_RUN' if not complete else 'FAIL' if fails else 'OWNER_IDENTITY_CONTRACT_INDEPENDENTLY_VERIFIED'
summary={'verdict':verdict,'P0':pc['P0'],'P1':pc['P1'],'P2':pc['P2'],'assertions':n,'literal_pass':f'{literal_ok}/128','roots':f'{root_ok}/3','goldens':f'{gp}/{grun}','mutations':f'{mp}/{mrun}','counts':f'{cp}/{crun}','mismatch':len(fails),'projection':'PASS' if hb(projected)==OLD else 'FAIL','permission_drift':'none' if not any(label.startswith('permission_') for _,label in fails) else 'detected','aliases':'2 anchors + 2 aliases PASS' if not any('alias' in label for _,label in fails) else 'FAIL','protection':'PASS' if not any(sev=='P0' and (label.startswith('protected_') or label in ('HEAD','staging','diff_check','owner_stable')) for sev,label in fails) else 'FAIL','cache_census':list(census),'owner_start_sha256':start_sha,'owner_end_sha256':end_sha,'golden_details':{'s2_logical_actual':sl,'s2_logical_expected':G['S2_off_nine_to_one']['shared_logical_computation_id'],'s2_manifest_actual':rh(sm),'s2_manifest_expected':G['S2_off_nine_to_one']['consumer_binding_manifest_sha256'],'bps_logical_actual':bl,'bps_logical_expected':G['BPS_dual_pol_shared']['shared_logical_computation_id'],'bps_manifest_actual':rh(bm),'bps_manifest_expected':G['BPS_dual_pol_shared']['consumer_binding_manifest_sha256']},'failures':[{'severity':s,'label':l} for s,l in fails]}
payload=json.dumps(summary,sort_keys=True,separators=(',',':'),ensure_ascii=False); print(payload); print('stdout_payload_sha256='+hb(payload.encode())); sys.exit(0 if verdict=='OWNER_IDENTITY_CONTRACT_INDEPENDENTLY_VERIFIED' else 1)
```
<!-- verifier:end -->

## Execution receipt

### Terminal

`FAIL / P0/P1/P2=0/2/0`

The owner is **not** accepted as `OWNER_IDENTITY_CONTRACT_INDEPENDENTLY_VERIFIED`. This receipt does not close I05 and does not authorize benchmark or science.

### Exact execution transport

PowerShell read this file, extracted only the text between `<!-- verifier:start -->` and `<!-- verifier:end -->`, and piped that source through stdin to:

```text
C:\Users\zzt\scoop\apps\python311\current\python.exe -B -
PYTHONDONTWRITEBYTECODE=1
PYTHONHASHSEED=0
```

No temporary script or third file was created. Final process exit code: `1`.

The first process exposed a verifier-only Unicode-character-offset/UTF-8-byte-offset error in the old-owner projection and stopped before adjudication. A subsequent full run exposed two verifier-only false positives: formula multiplication tokens were overmatched as aliases, and the frozen schemas path was one directory too deep. The fenced source above preserves the corrected byte-regex projection, PyYAML `AnchorToken`/`AliasToken` scan, and actual schemas path. Neither correction changed owner bytes or acceptance criteria.

### Complete final stdout

```text
{"P0":0,"P1":2,"P2":0,"aliases":"2 anchors + 2 aliases PASS","assertions":720,"cache_census":[202,41,4],"counts":"6/6","failures":[{"label":"golden_s2","severity":"P1"},{"label":"golden_bps","severity":"P1"}],"golden_details":{"bps_logical_actual":"d0c1-35432848c9e7397e0ba59c5e816b7d2c7764dc403856fb692589a2305444e1cb","bps_logical_expected":"d0c1-35432848c9e7397e0ba59c5e816b7d2c7764dc403856fb692589a2305444e1cb","bps_manifest_actual":"a6e10d8d3dfb3e87bbf92a874429323c22b7c7e355f2b1c86f0deafb04a4e2e7","bps_manifest_expected":"51d43e149ceaa6467b97d94b6e7631591d1e049546d2ace03c1b2228f27c0a1f","s2_logical_actual":"d0c1-c9cedfe83204c8f37286e0f8b81d1bb35ed21bf22d9ff36a69191c157dc1197c","s2_logical_expected":"d0c1-c9cedfe83204c8f37286e0f8b81d1bb35ed21bf22d9ff36a69191c157dc1197c","s2_manifest_actual":"dff1cfc81b5928e714940a03163f37d92fddea60cb8a40aa0590ddf113b147dc","s2_manifest_expected":"ed1a72137f1b0bea3208ed46f482206c88ba101bc718cc69faec9246c58607b6"},"goldens":"8/10","literal_pass":"128/128","mismatch":2,"mutations":"15/15","owner_end_sha256":"9f12cd11d210aef10c08848ccf42f39183f1ebf5f061d7203d3879335278990d","owner_start_sha256":"9f12cd11d210aef10c08848ccf42f39183f1ebf5f061d7203d3879335278990d","permission_drift":"none","projection":"PASS","protection":"PASS","roots":"3/3","verdict":"FAIL"}
stdout_payload_sha256=1c5fd8677f9cdc2f2b403512f0b673723ff2809755229ebd5b1dabb07cb1bcb5
process_exit_code=1
```

`stdout_payload_sha256` is SHA256 of the first canonical-JSON stdout line encoded as UTF-8 with no trailing newline.

### Fresh verification totals

- assertions: `720` (`>=240` PASS)
- binary64 literals: `128/128` PASS
- grid roots: `3/3` PASS
- golden subcases: `8/10` FAIL
- fresh mutations: `15/15` PASS
- count formulas: `6/6` PASS
- mismatch: `2`
- raw-byte old-owner projection: PASS
- parsed projection deep equality: PASS
- permission/scientific drift: none
- approved YAML identity reuse: exactly `2 anchors + 2 aliases`, specified paths only, PASS
- HEAD/staging/frozen evidence/P05/cache census/diff-check/begin-end owner: PASS
- final owner SHA256 at both boundaries: `9f12cd11d210aef10c08848ccf42f39183f1ebf5f061d7203d3879335278990d`

## Findings

### P1 — S2 consumer-binding golden cannot be independently reproduced

The independently reconstructed S2 logical identity is exact:

```text
actual   d0c1-c9cedfe83204c8f37286e0f8b81d1bb35ed21bf22d9ff36a69191c157dc1197c
expected d0c1-c9cedfe83204c8f37286e0f8b81d1bb35ed21bf22d9ff36a69191c157dc1197c
```

The consumer-binding manifest root is not:

```text
actual   dff1cfc81b5928e714940a03163f37d92fddea60cb8a40aa0590ddf113b147dc
expected ed1a72137f1b0bea3208ed46f482206c88ba101bc718cc69faec9246c58607b6
```

The manifest schema requires an exact `binding_kind`, but neither the S2 golden raw inputs nor the S2 consumer projection freezes that canonical literal. The saved hash therefore cannot be independently reconstructed without guessing an author-only value.

### P1 — BPS consumer-binding golden cannot be independently reproduced

The independently reconstructed BPS logical identity is exact:

```text
actual   d0c1-35432848c9e7397e0ba59c5e816b7d2c7764dc403856fb692589a2305444e1cb
expected d0c1-35432848c9e7397e0ba59c5e816b7d2c7764dc403856fb692589a2305444e1cb
```

The consumer-binding manifest root is not:

```text
actual   a6e10d8d3dfb3e87bbf92a874429323c22b7c7e355f2b1c86f0deafb04a4e2e7
expected 51d43e149ceaa6467b97d94b6e7631591d1e049546d2ace03c1b2228f27c0a1f
```

As for S2, `consumer_binding_manifest.binding_kind` is hash-bearing but its exact literal is absent from the BPS golden raw inputs and projection authority. This leaves the golden opaque at the final manifest layer even though the logical identity itself is reproducible.

## Narrow continuation

Any repair should remain owner-only and additive: freeze the exact S2 and BPS `binding_kind` literals in the corresponding projection/golden raw inputs, then regenerate only the two affected manifest roots if the newly frozen values differ from the historical author inputs. A fresh independent verifier must rerun all checks on the repaired final bytes; this FAIL cannot be converted to PASS by explanation alone.
