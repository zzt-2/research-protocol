import hashlib, importlib.util, json
from pathlib import Path
import pytest
import numpy as np
SIM=Path(__file__).resolve().parents[1]
def load(rel):
 p=SIM/rel; s=importlib.util.spec_from_file_location(p.stem,p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
@pytest.mark.parametrize("n",["fixed","selector_a","branchrouted_b"])
def test_frozen_defaults_and_authority(n):
 m=load(f"simulator/run_ccisp_family1_{n}_30seed.py")
 assert m.N_SEEDS==30 and m.N_WINDOWS==400
 a=m.authority(["weak"],[5.],"cmd")
 for k in ("authority_status","params_sha256","script_sha256","imported_file_sha256","command","git_head","git_dirty","grid","turbulence"):
  assert k in a
 assert a["authority_status"]=="formal"
def test_b_schema_has_only_null_structural_na():
 m=load("simulator/run_ccisp_family1_branchrouted_b_30seed.py")
 c=m.route_b_cell({"selected_errors":2,"n_select_da":1,"n_select_nda":2,"n_windows":3,"n_bits":9,"realization_identity_sha256":"a"})
 assert c["fixed_nda"] is None and c["oracle"] is None and c["gain_db"] is None
 assert 0 not in (c["fixed_nda"],c["oracle"],c["gain_db"])
def test_verifier_rejects_digest_mismatch_and_nonnull_b():
 v=load("verify/verify_ccisp_family1_formal.py")
 a={"raw":[{"key":"x","selected_errors":1,"n_select_da":1,"n_select_nda":0,"realization_identity_sha256":"a"}]}
 b={"raw":[{"key":"x","selected_errors":1,"n_select_da":1,"n_select_nda":0,"realization_identity_sha256":"b","fixed_nda":None,"oracle":None,"gain_db":None}]}
 with pytest.raises(AssertionError): v.verify_ab(a,b)

def _authority(route="A", scenes=("weak", "moderate", "strong"), snrs=tuple(range(5, 26, 2)), n_seeds=30, n_windows=400):
 params_hash=hashlib.sha256((SIM/"params.py").read_bytes()).hexdigest()
 script={"A":"run_ccisp_family1_selector_a_30seed.py","B":"run_ccisp_family1_branchrouted_b_30seed.py"}[route]
 return {"authority_status":"formal","route":route,"params_sha256":params_hash,
         "script_sha256":hashlib.sha256((SIM/"simulator"/script).read_bytes()).hexdigest(),
         "imported_file_sha256":{"params.py":params_hash},"command":"formal",
         "grid":{"scenes":list(scenes),"snr_db":list(map(float,snrs)),"n_seeds":n_seeds,
                 "windows_per_seed":n_windows,"window_symbols":256,"common_bits":768},
         "turbulence":load("simulator/run_ccisp_family1_selector_a_30seed.py").turbulence()}

def _cell(scene, snr, seed, selected=10, fixed=20):
 return {"key":f"{scene}|{float(snr)}|{seed}","scene":scene,"snr_db":float(snr),
         "seed_index":seed,"n_windows":400,"n_bits":307200,
         "window_seed_start":10000+seed*400,"window_seed_end":10399+seed*400,
         "realization_identity_sha256":"1"*64,"selected_output_sha256":"2"*64,
         "selected_errors":selected,"fixed_nda_errors":fixed,
         "n_select_da":200,"n_select_nda":200}

def test_verifier_recomputes_full_990_cell_statistics_and_pooled_diagnostic():
 v=load("verify/verify_ccisp_family1_formal.py")
 raw=[_cell(s,g,i) for s in ("weak","moderate","strong") for g in range(5,26,2) for i in range(30)]
 a={"authority":_authority(),"_meta":{"script":"a.py"},"raw":raw}
 b={"authority":_authority("B"),"_meta":{"script":"b.py"},"raw":[{**x,"fixed_nda_errors":None,"fixed_nda":None,"oracle":None,"gain_db":None} for x in raw]}
 report=v.verify(a,b,sim_root=SIM)
 assert report["a_b_exact_cells"]==990
 assert len(report["paired_statistics"])==33
 assert report["branch_counts"]["da"]==198000
 assert report["branch_counts"]["nda"]==198000
 assert report["paired_statistics"][0]["n_seed_units"]==30
 assert "mean_gain_db" in report["paired_statistics"][0]
 assert "ci95_low_db" in report["paired_statistics"][0]
 assert "pooled_gain_db" in report["paired_statistics"][0]

@pytest.mark.parametrize("mutation",["missing_output_digest","bad_denominator","nonnull_b","bad_params_hash","missing_save_meta"])
def test_verifier_rejects_incomplete_or_non_authoritative_formal_records(mutation):
 v=load("verify/verify_ccisp_family1_formal.py")
 raw=[_cell(s,g,i) for s in ("weak","moderate","strong") for g in range(5,26,2) for i in range(30)]
 a={"authority":_authority(),"_meta":{"script":"a.py"},"raw":raw}
 b={"authority":_authority("B"),"_meta":{"script":"b.py"},"raw":[{**x,"fixed_nda_errors":None,"fixed_nda":None,"oracle":None,"gain_db":None} for x in raw]}
 if mutation=="missing_output_digest": b["raw"][0].pop("selected_output_sha256")
 elif mutation=="bad_denominator": a["raw"][0]["n_bits"]-=1
 elif mutation=="nonnull_b": b["raw"][0]["fixed_nda"]=0
 elif mutation=="bad_params_hash": a["authority"]["params_sha256"]="0"*64
 else: a.pop("_meta")
 with pytest.raises(AssertionError): v.verify(a,b,sim_root=SIM)

def test_fixed_authority_uses_unified_5_to_35_db_two_db_grid_from_params():
 m=load("simulator/run_ccisp_family1_fixed_30seed.py")
 params=load("params.py")
 expected=tuple(map(float,range(5,36,2)))
 assert tuple(params.CCISP_FIXED_SNR_DB)==expected
 assert tuple(m.SNR_AWGN_DB)==expected
 assert tuple(m.SNR_TURB_DB)==expected

def test_fixed_metric_signatures_keep_method_specific_denominators():
 m=load("simulator/run_ccisp_family1_fixed_30seed.py")
 src=(SIM/"verify/verify_ccisp_family1_formal.py").read_text(encoding="utf-8")
 assert '"nda":400*(1024 if x["scene"]=="awgn" else 768)' in src
 assert '"da":400*768' in src and '"oracle":400*1024' in src
 a=m.authority(m.SCENES,{"awgn":list(m.SNR_AWGN_DB),"turbulence":list(m.SNR_TURB_DB)},"formal")
 assert a["grid"]["snr_db"]=={"awgn":list(m.SNR_AWGN_DB),"turbulence":list(m.SNR_TURB_DB)}

def test_real_route_authority_and_cells_carry_comparable_selected_output_digest():
 a=load("simulator/run_ccisp_family1_selector_a_30seed.py")
 b=load("simulator/run_ccisp_family1_branchrouted_b_30seed.py")
 assert a.authority(["weak"],[5.],"smoke",1,1)["route"]=="A"
 ac=a.run_case("weak",5.,0,1)
 bc=b.run_case("weak",5.,0,1)
 assert len(ac["selected_output_sha256"])==64
 assert ac["selected_output_sha256"]==bc["selected_output_sha256"]

def test_nda_receiver_output_digest_is_independent_of_posthoc_labels():
 a=load("simulator/run_ccisp_family1_selector_a_30seed.py")
 cfg=a.SimulationConfig(); r=a.generate_shared_realization_apsk(a.P.N_DFT,10.0,"weak",cfg.doppler.DOPPLER_HIGH,mod="m16apsk",seed=24680)
 hb=a.S.estimate_h_blind_perblock(r["rx_raw"],10.0); x=a.amp_limit(a.mmse_equalize(r["rx_raw"],hb,10.0),3.0)
 _,_,out1=a.per_block_nda_receiver_output(x,r["bits"]); _,_,out2=a.per_block_nda_receiver_output(x,1-r["bits"])
 assert np.array_equal(out1,out2)

def test_verifier_recomputes_fixed_1920_cell_contract():
 v=load("verify/verify_ccisp_family1_formal.py"); f=load("simulator/run_ccisp_family1_fixed_30seed.py")
 raw=[]
 for scene in f.SCENES:
  snrs=f.SNR_AWGN_DB if scene=="awgn" else f.SNR_TURB_DB
  for snr in snrs:
   for seed in range(30):
    nda_bits=409600 if scene=="awgn" else 307200
    raw.append({"key":f"{scene}|{float(snr)}|{seed}","scene":scene,"snr_db":float(snr),"seed_index":seed,
      "n_windows":400,"window_seed_start":seed*400,"window_seed_end":seed*400+(0 if scene=="awgn" else 399),
      "realization_identity_sha256":"3"*64,"nda_errors":1,"nda_bits":nda_bits,
      "da_errors":2,"da_bits":307200,"oracle_errors":0,"oracle_bits":409600})
 authority=f.authority(f.SCENES,{"awgn":list(f.SNR_AWGN_DB),"turbulence":list(f.SNR_TURB_DB)},"formal")
 authority["grid"]["snr_db"]={"awgn":list(f.SNR_AWGN_DB),"turbulence":list(f.SNR_TURB_DB)}
 report=v.verify_fixed({"authority":authority,"_meta":{"script":"fixed.py"},"raw":raw},SIM)
 assert report["fixed_cells"]==1920
