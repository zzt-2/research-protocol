"""Independent verification from raw formal records; summaries are ignored."""
import argparse, hashlib, json, math, statistics, sys
from pathlib import Path

SCENES=("weak","moderate","strong")
SNRS=tuple(map(float,range(5,26,2)))
N_SEEDS=30
N_WINDOWS=400
N_BITS=N_WINDOWS*768
T_CRIT_DF29=2.045229642132703

def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def _live_turbulence(sim_root):
 sys.path.insert(0,str(sim_root))
 try:
  from params import SimulationConfig
  d=SimulationConfig().get_turb_dict()
 finally: sys.path.pop(0)
 return {k:(float(d[k][0]),float(d[k][1])) for k in SCENES}

def verify_authority(d,sim_root,route):
 assert d.get("_meta",{}).get("script"), "result was not written through save_results"
 a=d["authority"]
 assert a["authority_status"]=="formal"
 assert a.get("route")==route
 assert a["params_sha256"]==sha(sim_root/"params.py")
 expected_script={"A":"run_ccisp_family1_selector_a_30seed.py","B":"run_ccisp_family1_branchrouted_b_30seed.py"}[route]
 assert a["script_sha256"]==sha(sim_root/"simulator"/expected_script)
 for rel,digest in a["imported_file_sha256"].items(): assert sha(sim_root/rel)==digest
 grid=a["grid"]
 assert tuple(grid["scenes"])==SCENES and tuple(grid["snr_db"])==SNRS
 assert grid["n_seeds"]==N_SEEDS and grid["windows_per_seed"]==N_WINDOWS
 assert grid["window_symbols"]==256 and grid["common_bits"]==768
 live=_live_turbulence(sim_root)
 for k in SCENES:
  assert (float(a["turbulence"][k]["alpha"]),float(a["turbulence"][k]["beta"]))==live[k]

def _validate_raw(raw,route):
 expected={(s,g,i) for s in SCENES for g in SNRS for i in range(N_SEEDS)}
 seen=set()
 for x in raw:
  key=(x["scene"],float(x["snr_db"]),x["seed_index"]); assert key not in seen; seen.add(key)
  assert x["key"]==f"{key[0]}|{key[1]}|{key[2]}"
  assert x["n_windows"]==N_WINDOWS and x["n_bits"]==N_BITS
  assert x["window_seed_end"]-x["window_seed_start"]+1==N_WINDOWS
  assert isinstance(x.get("realization_identity_sha256"),str) and len(x["realization_identity_sha256"])==64
  assert isinstance(x.get("selected_output_sha256"),str) and len(x["selected_output_sha256"])==64
  assert x["n_select_da"]+x["n_select_nda"]==N_WINDOWS
  assert 0<=x["selected_errors"]<=x["n_bits"]
  if route=="B":
   for k in ("fixed_nda_errors","fixed_nda","oracle_errors","oracle","gain_db"):
    assert x.get(k) is None
 assert seen==expected

def verify_ab(a,b):
 A={x["key"]:x for x in a["raw"]}; B={x["key"]:x for x in b["raw"]}; assert A.keys()==B.keys()
 for k in A:
  x,y=A[k],B[k]
  for field in ("realization_identity_sha256","selected_output_sha256","selected_errors","n_select_da","n_select_nda","n_windows","n_bits","window_seed_start","window_seed_end"):
   assert x[field]==y[field],(k,field)
 return len(A)

def _statistics(raw):
 out=[]
 for scene in SCENES:
  for snr in SNRS:
   cells=[x for x in raw if x["scene"]==scene and float(x["snr_db"])==snr]
   cells.sort(key=lambda x:x["seed_index"]); assert [x["seed_index"] for x in cells]==list(range(N_SEEDS))
   gains=[10*math.log10((x["fixed_nda_errors"]+0.5)/(x["selected_errors"]+0.5)) for x in cells]
   mean=statistics.fmean(gains); half=T_CRIT_DF29*statistics.stdev(gains)/math.sqrt(N_SEEDS)
   fixed=sum(x["fixed_nda_errors"] for x in cells); selected=sum(x["selected_errors"] for x in cells)
   out.append({"scene":scene,"snr_db":snr,"n_seed_units":N_SEEDS,"zero_count_correction":0.5,
               "mean_gain_db":mean,"ci95_low_db":mean-half,"ci95_high_db":mean+half,
               "pooled_gain_db":10*math.log10((fixed+0.5)/(selected+0.5)),
               "pooled_selected_errors":selected,"pooled_fixed_nda_errors":fixed,"pooled_bits":N_SEEDS*N_BITS})
 return out

def verify(a,b,sim_root):
 sim_root=Path(sim_root)
 verify_authority(a,sim_root,"A"); verify_authority(b,sim_root,"B")
 _validate_raw(a["raw"],"A"); _validate_raw(b["raw"],"B")
 n=verify_ab(a,b); da=sum(x["n_select_da"] for x in a["raw"]); nda=sum(x["n_select_nda"] for x in a["raw"])
 total=da+nda; assert da and nda and max(da,nda)/total<0.99
 return {"status":"PASS","a_b_exact_cells":n,"branch_counts":{"da":da,"nda":nda},"paired_statistics":_statistics(a["raw"])}

def verify_fixed(d,sim_root):
 sim_root=Path(sim_root); a=d["authority"]
 sys.path.insert(0,str(sim_root))
 try: from params import CCISP_FIXED_SNR_DB
 finally: sys.path.pop(0)
 fixed_snrs=tuple(map(float,CCISP_FIXED_SNR_DB))
 assert d.get("_meta",{}).get("script") and a["authority_status"]=="formal" and a["route"]=="fixed"
 assert a["params_sha256"]==sha(sim_root/"params.py")
 assert a["script_sha256"]==sha(sim_root/"simulator"/"run_ccisp_family1_fixed_30seed.py")
 for rel,digest in a["imported_file_sha256"].items(): assert sha(sim_root/rel)==digest
 grid=a["grid"]; assert tuple(grid["scenes"])==("awgn",)+SCENES
 assert tuple(grid["snr_db"]["awgn"])==fixed_snrs
 assert tuple(grid["snr_db"]["turbulence"])==fixed_snrs
 assert grid["n_seeds"]==30 and grid["windows_per_seed"]==400
 expected={(s,g,i) for s in ("awgn",)+SCENES for g in fixed_snrs for i in range(30)}
 seen=set()
 for x in d["raw"]:
  key=(x["scene"],float(x["snr_db"]),x["seed_index"]); assert key not in seen; seen.add(key)
  assert x["key"]==f"{key[0]}|{key[1]}|{key[2]}" and x["n_windows"]==400
  assert isinstance(x.get("realization_identity_sha256"),str) and len(x["realization_identity_sha256"])==64
  expected_bits={"nda":400*(1024 if x["scene"]=="awgn" else 768),"da":400*768,"oracle":400*1024}
  for method,denominator in expected_bits.items():
   assert x[f"{method}_bits"]==denominator and 0<=x[f"{method}_errors"]<=denominator
  if x["scene"]=="awgn": assert x["window_seed_end"]==x["window_seed_start"]
  else: assert x["window_seed_end"]-x["window_seed_start"]+1==400
 assert seen==expected
 return {"status":"PASS","fixed_cells":len(seen)}

def main():
 ap=argparse.ArgumentParser(); ap.add_argument("--a",type=Path,required=True); ap.add_argument("--b",type=Path,required=True); ap.add_argument("--report",type=Path,required=True); z=ap.parse_args()
 a=json.loads(z.a.read_text(encoding="utf-8")); b=json.loads(z.b.read_text(encoding="utf-8")); report=verify(a,b,z.a.resolve().parents[1]); report.update({"a_sha256":sha(z.a),"b_sha256":sha(z.b)})
 z.report.write_text(json.dumps(report,indent=2),encoding="utf-8")
if __name__=="__main__": main()
