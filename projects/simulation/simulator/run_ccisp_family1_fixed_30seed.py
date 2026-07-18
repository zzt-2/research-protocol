"""Formal fixed DA/NDA/oracle results, isolated from legacy JSON."""
import argparse, hashlib, importlib.util, sys
from pathlib import Path
import numpy as np
SIM=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(SIM)); from params import CCISP_FIXED_SNR_DB
spec=importlib.util.spec_from_file_location("formal_a",Path(__file__).with_name("run_ccisp_family1_selector_a_30seed.py")); F=importlib.util.module_from_spec(spec); spec.loader.exec_module(F); P=F.P
N_SEEDS=30; N_WINDOWS=400; SCENES=("awgn","weak","moderate","strong"); SNR_AWGN_DB=tuple(CCISP_FIXED_SNR_DB); SNR_TURB_DB=tuple(CCISP_FIXED_SNR_DB)
def authority(scenes,snrs,command,n_seeds=N_SEEDS,n_windows=N_WINDOWS):
 a=F.authority(scenes,(),command,n_seeds,n_windows); a["script_sha256"]=F.sha(__file__); a["route"]="fixed"; a["grid"]["snr_db"]={k:list(v) for k,v in snrs.items()} if isinstance(snrs,dict) else list(snrs); return a
def run(scenes,n_seeds,n_windows,out,command,smoke=False):
 raw=[]
 for s in scenes:
  for g in ((5.,) if smoke else (SNR_AWGN_DB if s=="awgn" else SNR_TURB_DB)):
   for i in range(n_seeds):
    if s=="awgn":
     seed=F.P.SEED_AWGN+i+int(g*1000); rng=np.random.default_rng(seed+7); bits=rng.integers(0,2,n_windows*F.P.N_DFT*F.P.BITS_PER_SYM); tx=F.S.m16apsk_mod(bits); rx,phi=F.S.awgn_wiener_channel(tx,g,seed); ne_n,nb_n=F.S.ber_nda_awgn(rx,bits); ne_d,nb_d=F.S.ber_da_awgn(rx,bits); ne_o,nb_o=F.S.ber_oracle_awgn(rx,bits,phi); h=hashlib.sha256()
     for x in (np.asarray([seed],dtype=np.int64),bits,tx,rx,phi): h.update(np.ascontiguousarray(x).view(np.uint8).tobytes())
     raw.append({"key":f"{s}|{g}|{i}","scene":s,"snr_db":g,"seed_index":i,"n_windows":n_windows,"window_seed_start":seed,"window_seed_end":seed,"realization_identity_sha256":h.hexdigest(),"nda_errors":ne_n,"nda_bits":nb_n,"da_errors":ne_d,"da_bits":nb_d,"oracle_errors":ne_o,"oracle_bits":nb_o,"nda_ber":ne_n/nb_n,"da_ber":ne_d/nb_d,"oracle_ber":ne_o/nb_o})
    else:
     c=F.run_case(s,g,i,n_windows); raw.append({**{k:v for k,v in c.items() if k not in ("selected_errors","selected_output_sha256","n_select_da","n_select_nda")},"nda_errors":c["fixed_nda_errors"],"nda_bits":c["n_bits"],"da_errors":c["fixed_da_errors"],"da_bits":c["n_bits"],"oracle_errors":c["true_oracle_errors"],"oracle_bits":c["true_oracle_bits"],"nda_ber":c["fixed_nda_errors"]/c["n_bits"],"da_ber":c["fixed_da_errors"]/c["n_bits"],"oracle_ber":c["true_oracle_errors"]/c["true_oracle_bits"]})
 grids={"awgn":list((5.,) if smoke else SNR_AWGN_DB),"turbulence":list((5.,) if smoke else SNR_TURB_DB)}
 F.save_results({"authority":authority(scenes,grids,command,n_seeds,n_windows),"raw":raw},str(out),Path(__file__).name)
def main():
 ap=argparse.ArgumentParser(); ap.add_argument("--smoke",action="store_true"); ap.add_argument("--out",type=Path,default=SIM/"results"/"ccisp_family1_fixed_30seed.json"); z=ap.parse_args(); run(("weak",) if z.smoke else SCENES,1 if z.smoke else N_SEEDS,2 if z.smoke else N_WINDOWS,z.out," ".join(sys.argv),z.smoke)
if __name__=="__main__": main()
