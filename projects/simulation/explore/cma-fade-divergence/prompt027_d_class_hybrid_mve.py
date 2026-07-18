"""PROMPT-027 corrected 5-seed D-class CMA+ML hybrid MVE.

Review correction: permanent late swap is 2/5 seeds, not 5/5; PI-BER is evaluated on
the completed hybrid sequence and no segment-wise monotonicity is assumed.
Detector is causal at block granularity: correlation measured on CMA block b controls output
selection only from block b+1. It uses true transmitted symbols (genie/pilot upper bound).
"""
from __future__ import annotations
import json, os, sys, tempfile, time
from pathlib import Path
import numpy as np

SIM_DIR = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(SIM_DIR), str(HERE)]
from common._experiment import save_results
from params import SimulationConfig
from ml_long_seq_failure import (F_G, GAMMA_BAR, N_TAP, SOP_RATE, gen_channel,
                                 run_ml_trial, test_late_slice)
from prompt019_mu_compress_mve import StandardCMA2x2, MU_SAFE, R2_QPSK
from prompt012_longseq_audit import evaluate_outputs

N=5_000_000; SEEDS=(1000,1001,1002,1003,1004); BS=64; THR=0.5; HOLD=1000
# D022/H013 compatibility snapshot. Current dirty params.py changed "strong" to 4.2/1.4;
# this is a frozen historical-domain replay, not parameter tuning.
D022_STRONG_ALPHA=1.5; D022_STRONG_BETA=0.8
OUT=SIM_DIR/'results/cma-fade-divergence/prompt027_d_class_hybrid_mve_d022frozen.json'

def corr(a,b):
    d=np.sqrt(np.vdot(a,a).real*np.vdot(b,b).real)
    return float(abs(np.vdot(a,b))/d) if d>0 else 0.0

def causal_masks(zx_cma,sx,sy):
    """Block b detection applies at b+1: no same-block/future leakage."""
    nb=len(zx_cma)//BS; det=[]
    for b in range(nb):
        q=slice(b*BS,(b+1)*BS); cx,cy=corr(zx_cma[q],sx[q]),corr(zx_cma[q],sy[q])
        if cy>THR and cy>cx: det.append(b)
    perm=np.zeros(len(zx_cma),bool); selective=np.zeros(len(zx_cma),bool)
    if det:
        s=min((det[0]+1)*BS,len(perm)); perm[s:]=True
    for b in det:
        s=(b+1)*BS; e=min((b+1+HOLD)*BS,len(perm)); selective[s:e]=True
    return perm,selective,det

def metrics(zx,zy,sx,sy,div=False):
    e=evaluate_outputs(zx,zy,sx,sy,div)
    return {'fixed':float(e['fixed_label_ber']['mean']),
            'pi':float(e['permutation_invariant_ber']['mean']),
            'classification':e['classification']}

def save(payload):
    OUT.parent.mkdir(parents=True,exist_ok=True); fd,tmp=tempfile.mkstemp(dir=OUT.parent,suffix='.json'); os.close(fd)
    try: save_results(payload,tmp,'prompt027_d_class_hybrid_mve'); os.replace(tmp,OUT)
    finally:
        if os.path.exists(tmp): os.unlink(tmp)

def summarize(ts):
    names=['L0_ml_only','CMA_only','D1_permanent_switch','D2_selective_switch','forced_switch_ml_late']
    out={}; l0=np.array([t['methods']['L0_ml_only']['pi'] for t in ts])
    from scipy.stats import wilcoxon
    for n in names:
        v=np.array([t['methods'][n]['pi'] for t in ts]); row={'mean_pi':float(v.mean()),'mean_fixed':float(np.mean([t['methods'][n]['fixed'] for t in ts])),'per_seed_pi':v.tolist()}
        if n.startswith('D'):
            d=l0-v; p=1.0 if np.allclose(d,0) else float(wilcoxon(d,alternative='greater',method='exact').pvalue)
            row.update(wins=int(np.sum(v<l0)),p_one_sided=p,delta=float(d.mean()))
            row['verdict']='GO' if row['mean_pi']<float(l0.mean()) and row['wins']>=4 and p<0.05 else 'KILL'
        out[n]=row
    out['class_verdict']='GO' if any(out[n].get('verdict')=='GO' for n in names) else 'KILL'
    return out

def main():
    if OUT.exists():
        try: payload=json.loads(OUT.read_text(encoding='utf-8'))
        except Exception: payload={}
    else: payload={}
    payload.setdefault('experiment','PROMPT-027 corrected D-class hybrid MVE')
    payload.setdefault('preregistered',{'go':'any D mean PI<L0, >=4/5 wins, one-sided exact Wilcoxon p<0.05','threshold':THR,'D2_hold_blocks':HOLD})
    payload.setdefault('information_access','genie/pilot: true sX/sY correlations; detection on block b affects b+1 only')
    payload.setdefault('metric_signature','late[4.375M,5M), fixed and PI BER evaluated on complete sequence')
    payload.setdefault('state_lifecycle','CMA shadow runs continuously; ML offline fixed; D1 one-way switch; D2 ML hold then CMA unless retriggered')
    payload.setdefault('domain_snapshot',{'source':'D022/H013 historical strong GG compatibility','alpha':D022_STRONG_ALPHA,'beta':D022_STRONG_BETA,'current_params_drift':{'alpha':4.2,'beta':1.4},'not_tuning':True})
    payload.setdefault('trials',[])
    done={t['seed'] for t in payload['trials']}; a,b=D022_STRONG_ALPHA,D022_STRONG_BETA
    for seed in SEEDS:
        if seed in done: continue
        t=time.time(); rx,ry,sx,sy,h,theta=gen_channel(N,a,b,F_G,SOP_RATE,seed)
        cma=StandardCMA2x2(n_tap=N_TAP,mu=MU_SAFE,R2=R2_QPSK); cr=cma.equalize(rx,ry,block_size=BS)
        zmx,zmy,_,mr=run_ml_trial(rx,ry,sx,sy)
        ls,le=test_late_slice(N); zcx,zcy=cr['zX'][ls:le],cr['zY'][ls:le]; mlx,mly=zmx[ls:le],zmy[ls:le]; tx,ty=sx[ls:le],sy[ls:le]
        m1,m2,det=causal_masks(zcx,tx,ty)
        d1x,d1y=zcx.copy(),zcy.copy(); d1x[m1],d1y[m1]=mlx[m1],mly[m1]
        d2x,d2y=zcx.copy(),zcy.copy(); d2x[m2],d2y[m2]=mlx[m2],mly[m2]
        methods={'L0_ml_only':metrics(mlx,mly,tx,ty), 'CMA_only':metrics(zcx,zcy,tx,ty,cr['diverged']),
                 'D1_permanent_switch':metrics(d1x,d1y,tx,ty), 'D2_selective_switch':metrics(d2x,d2y,tx,ty),
                 'forced_switch_ml_late':metrics(mlx.copy(),mly.copy(),tx,ty)}
        payload['trials'].append({'seed':seed,'trigger_blocks_late':det,'n_triggers':len(det),'D1_ml_fraction':float(m1.mean()),'D2_ml_fraction':float(m2.mean()),'methods':methods,'elapsed_s':time.time()-t})
        payload['checkpoint']={'completed':[x['seed'] for x in payload['trials']],'pending':[s for s in SEEDS if s not in {x['seed'] for x in payload['trials']}],'complete':False}; save(payload)
        print(seed,len(det),{k:round(v['pi'],6) for k,v in methods.items()},flush=True)
    payload['summary']=summarize(payload['trials'])
    triggered={t['seed'] for t in payload['trials'] if t['n_triggers']>0}
    assert triggered=={1000,1003}, f'D022 V0 compatibility FAIL: triggered={triggered}'
    assert all(t['methods']['forced_switch_ml_late']==t['methods']['L0_ml_only'] for t in payload['trials'])
    payload['v0_compatibility_assertion']={'expected_triggered':[1000,1003],'actual_triggered':sorted(triggered),'pass':True}
    payload['forced_switch_ablation']={'definition':'actual copied ML late output passed through evaluate_outputs',
        'per_seed_equal_to_L0':True,'pass':True}
    payload['historical_swap_mismatch']={'root_cause':'params.py strong GG drift 1.5/0.8 -> 4.2/1.4','status':'RESOLVED_BY_D022_COMPATIBILITY_SNAPSHOT'}
    payload['checkpoint']['complete']=len(payload['trials'])==5; save(payload); print(json.dumps(payload['summary'],indent=2))

if __name__=='__main__': main()
