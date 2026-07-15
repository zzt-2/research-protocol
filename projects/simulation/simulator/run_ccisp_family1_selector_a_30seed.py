"""Formal offline route-A evaluator for CCISP Family-1."""
import argparse, hashlib, inspect, json, os, platform, subprocess, sys
from pathlib import Path
import numpy as np
SIM=Path(__file__).resolve().parents[1]; EXP=SIM/"explore"/"nda-awgn-tracking-sandbox"; sys.path[:0]=[str(SIM),str(SIM/"simulator"),str(EXP)]
import _b11_params as P
import _a4_switch_common768_30seed as A
import _a4_branchrouted_30seed as B
import sc_nda_ml_sim as S
from common import amp_limit, generate_shared_realization_apsk, mmse_equalize, save_results
from params import SimulationConfig
N_SEEDS=30; N_WINDOWS=400; SCENES=("weak","moderate","strong"); SNR_DB=tuple(map(float,range(5,26,2))); SIGMA_R2={"weak":0.2,"moderate":1.6,"strong":3.5}
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def turbulence():
 c=SimulationConfig(); d=c.get_turb_dict(); return {k:{"alpha":d[k][0],"beta":d[k][1],"sigma_R2":SIGMA_R2[k]} for k in SCENES}
def authority(scenes,snrs,command,n_seeds=N_SEEDS,n_windows=N_WINDOWS):
 imports=[Path(inspect.getsourcefile(x)).resolve() for x in (A,B,S,SimulationConfig,generate_shared_realization_apsk)]
 return {"authority_status":"formal","route":"A","params_sha256":sha(SIM/"params.py"),"script_sha256":sha(__file__),"imported_file_sha256":{str(p.relative_to(SIM)):sha(p) for p in imports},"command":command,"git_head":subprocess.run(["git","rev-parse","HEAD"],cwd=SIM,capture_output=True,text=True).stdout.strip(),"git_dirty":bool(subprocess.run(["git","status","--porcelain"],cwd=SIM,capture_output=True,text=True).stdout.strip()),"grid":{"scenes":list(scenes),"snr_db":list(snrs),"n_seeds":n_seeds,"windows_per_seed":n_windows,"window_symbols":256,"common_bits":768},"turbulence":turbulence(),"python":platform.python_version()}
def digest_update(h,r,seed):
 h.update(np.asarray([seed],dtype=np.int64).tobytes())
 for k in ("bits","tx","h","phi","rx_raw"): h.update(np.ascontiguousarray(r[k]).view(np.uint8).tobytes())
def selected_digest_update(h,x):
 h.update(np.ascontiguousarray(x).view(np.uint8).tobytes())
def per_block_nda_receiver_output(rx_blind,bits):
 """Return label-free NDA receiver output plus post-hoc BER counts."""
 omega=B.S.fft_foe_m0_omega(rx_blind,B.P.M0); k=np.arange(B.P.N_DFT)
 rc_nda,_,_,_=B.nda_ml_recovery(rx_blind*np.exp(-1j*omega*k),B.P.M0,mod="m16apsk",assume_df_zero=True)
 tb=bits[:B.P.N_DFT*B.P.BITS_PER_SYM]
 resolved=B.resolve_m16apsk_blockwise(rc_nda,tb,block_size=B.P.BLOCK_SIZE_RESOLVE)
 dm=B.m16apsk_demod(resolved); ne_all=int(np.sum(tb!=dm)); pidx=np.arange(0,B.P.N_DFT,B.P.DA_PILOT_SPACING)
 is_data=np.ones(B.P.N_DFT,dtype=bool); is_data[pidx]=False
 ne_common=int(np.sum(tb.reshape(B.P.N_DFT,B.P.BITS_PER_SYM)[is_data]!=dm.reshape(B.P.N_DFT,B.P.BITS_PER_SYM)[is_data]))
 return ne_all,ne_common,rc_nda
def run_case(scene,snr,seed_index,n_windows=N_WINDOWS,route_b=False):
 cfg=SimulationConfig(); gl=10**(snr/10); start=P.SEED_TURB0+seed_index*N_WINDOWS; h=hashlib.sha256(); selected_h=hashlib.sha256(); c={"fixed_nda_errors":0,"fixed_da_errors":0,"selected_errors":0,"lower_count_bound_errors":0,"true_oracle_errors":0,"true_oracle_bits":0,"n_select_da":0,"n_select_nda":0}
 for b in range(n_windows):
  ws=start+b; r=generate_shared_realization_apsk(P.N_DFT,gl,scene,cfg.doppler.DOPPLER_HIGH,mod="m16apsk",seed=ws); digest_update(h,r,ws); raw,bits,tx=r["rx_raw"],r["bits"],r["tx"]
  hb=S.estimate_h_blind_perblock(raw,gl); hp=S.estimate_h_pilot_perblock(raw,tx,gl); blind=amp_limit(mmse_equalize(raw,hb,gl),3.0); pilot=amp_limit(mmse_equalize(raw,hp,gl),3.0); nn,nd,nc=A.per_block(blind,pilot,bits,tx); choice=A.decide(raw,snr,gl)
  trueh=amp_limit(mmse_equalize(raw,r["h"],gl),3.0); no,nob=S.ber_oracle_turb(trueh,bits,r["phi"]); c["true_oracle_errors"]+=no; c["true_oracle_bits"]+=nob
  if choice=="da": _,selected_rx=B.per_block_da(pilot,bits,tx)
  else: _,_,selected_rx=per_block_nda_receiver_output(blind,bits)
  selected_digest_update(selected_h,selected_rx)
  c["fixed_nda_errors"]+=nc; c["fixed_da_errors"]+=nd; c["lower_count_bound_errors"]+=min(nc,nd); c["selected_errors"]+=nd if choice=="da" else nc; c["n_select_"+choice]+=1
 return {"key":f"{scene}|{snr}|{seed_index}","scene":scene,"snr_db":snr,"seed_index":seed_index,"n_windows":n_windows,"n_bits":n_windows*768,"window_seed_start":start,"window_seed_end":start+n_windows-1,"realization_identity_sha256":h.hexdigest(),"selected_output_sha256":selected_h.hexdigest(),**c}
def run(scenes,snrs,n_seeds,n_windows,out,command):
 raw=[run_case(s,g,i,n_windows) for s in scenes for g in snrs for i in range(n_seeds)]; data={"authority":authority(scenes,snrs,command,n_seeds,n_windows),"raw":raw}; save_results(data,str(out),Path(__file__).name)
def main():
 ap=argparse.ArgumentParser(); ap.add_argument("--smoke",action="store_true"); ap.add_argument("--out",type=Path,default=SIM/"results"/"ccisp_family1_selector_a_30seed.json"); z=ap.parse_args(); run(("weak",) if z.smoke else SCENES,(5.,) if z.smoke else SNR_DB,1 if z.smoke else N_SEEDS,2 if z.smoke else N_WINDOWS,z.out," ".join(sys.argv))
if __name__=="__main__": main()
