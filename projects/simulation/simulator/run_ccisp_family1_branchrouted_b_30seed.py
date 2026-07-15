"""Formal branch-routed route B: decide first and execute one branch only."""
import argparse, hashlib, importlib.util, sys
from pathlib import Path
SIM=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("formal_a",Path(__file__).with_name("run_ccisp_family1_selector_a_30seed.py")); F=importlib.util.module_from_spec(spec); spec.loader.exec_module(F)
N_SEEDS=F.N_SEEDS; N_WINDOWS=F.N_WINDOWS; SCENES=F.SCENES; SNR_DB=F.SNR_DB
def authority(scenes,snrs,command,n_seeds=N_SEEDS,n_windows=N_WINDOWS):
 a=F.authority(scenes,snrs,command,n_seeds,n_windows); a["script_sha256"]=F.sha(__file__); a["route"]="B"; return a
def route_b_cell(c):
 return {**c,"fixed_nda_errors":None,"fixed_nda":None,"oracle_errors":None,"oracle":None,"gain_db":None}
def run_case(scene,snr,seed_index,n_windows=N_WINDOWS):
 cfg=F.SimulationConfig(); gl=10**(snr/10); start=F.P.SEED_TURB0+seed_index*N_WINDOWS; h=hashlib.sha256(); selected_h=hashlib.sha256(); sel=da=nda=0
 for b in range(n_windows):
  ws=start+b; r=F.generate_shared_realization_apsk(F.P.N_DFT,gl,scene,cfg.doppler.DOPPLER_HIGH,mod="m16apsk",seed=ws); F.digest_update(h,r,ws); raw,bits,tx=r["rx_raw"],r["bits"],r["tx"]; choice=F.A.decide(raw,snr,gl)
  if choice=="da": hp=F.S.estimate_h_pilot_perblock(raw,tx,gl); x=F.amp_limit(F.mmse_equalize(raw,hp,gl),3.0); ne,selected_rx=F.B.per_block_da(x,bits,tx); da+=1
  else: hb=F.S.estimate_h_blind_perblock(raw,gl); x=F.amp_limit(F.mmse_equalize(raw,hb,gl),3.0); _,ne,selected_rx=F.per_block_nda_receiver_output(x,bits); nda+=1
  F.selected_digest_update(selected_h,selected_rx)
  sel+=ne
 base={"key":f"{scene}|{snr}|{seed_index}","scene":scene,"snr_db":snr,"seed_index":seed_index,"n_windows":n_windows,"n_bits":n_windows*768,"window_seed_start":start,"window_seed_end":start+n_windows-1,"realization_identity_sha256":h.hexdigest(),"selected_output_sha256":selected_h.hexdigest(),"selected_errors":sel,"n_select_da":da,"n_select_nda":nda}
 return route_b_cell(base)
def run(scenes,snrs,n_seeds,n_windows,out,command):
 raw=[run_case(s,g,i,n_windows) for s in scenes for g in snrs for i in range(n_seeds)]; F.save_results({"authority":authority(scenes,snrs,command,n_seeds,n_windows),"raw":raw},str(out),Path(__file__).name)
def main():
 ap=argparse.ArgumentParser(); ap.add_argument("--smoke",action="store_true"); ap.add_argument("--out",type=Path,default=SIM/"results"/"ccisp_family1_branchrouted_b_30seed.json"); z=ap.parse_args(); run(("weak",) if z.smoke else SCENES,(5.,) if z.smoke else SNR_DB,1 if z.smoke else N_SEEDS,2 if z.smoke else N_WINDOWS,z.out," ".join(sys.argv))
if __name__=="__main__": main()
