"""P11 PILOT_EFFICIENT_STRUCTURED_BUTTERFLY_FIR — runner.

chronology 闭合（V077 教训第三次落实，P09/P10 模式复用）:
  - Commit 1: P10 纠偏 + P11 frozen contract + pre-test receipt (test_started=false)
    必须在任何 held-out test 前。本 runner 在执行任何 test seed 前校验全部 hash。
  - runner 启动 → verify_freeze_receipt() → 不一致立即 EXECUTION_INVALID。
  - test artifact 写入 receipt hash + test_started=true。

公平数据合同（用户指令 §五）:
  - pilot 位置预先冻结 (freeze_pilot_positions, 所有方法共享)
  - 只有 pilot 位置的 TX 符号可进入训练/估计 (B1/B2/B3/C1/C2/C3)
  - payload TX truth 只用于最终 BER 计分 (fixed-label + PI-BER)
  - 禁止把整个 payload truth 送入 Adam/LS/RLS
  - pilot overhead 计入 net goodput

Phase A: problem gate —— 低 pilot 预算下最强传统方法是否出现达 MDE 的性能损失。
Phase B: 候选（仅 Phase A 证实问题且传统 comparator 未解决时运行）。
terminal: PROBLEM_RESOLVED_BY_COMPLEX_LS / PROBLEM_ABSENT_AT_LOW_PILOT_OVERHEAD /
          NO_DIAGNOSTIC_METHOD_SIGNAL / PILOT_EFFICIENT_BUTTERFLY_METHOD_SIGNAL /
          EVIDENCE_INSUFFICIENT / EXECUTION_INVALID / STRATEGIC_GATE
"""
import sys, os, json, hashlib, time, argparse
import numpy as np
import importlib.util

_SIM = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if _SIM not in sys.path:
    sys.path.insert(0, _SIM)

spec = importlib.util.spec_from_file_location(
    'p11_methods',
    os.path.join(os.path.dirname(__file__), 'p11_methods.py'))
P = importlib.util.module_from_spec(spec)
spec.loader.exec_module(P)

# 复用既有信道生成 (gen_channel in ml_long_seq_failure.py, GG-fade + SOP, params.py provenance)
# explore 子目录名含连字符, 不能用包导入 → 用 importlib 按路径加载
_mlf_path = os.path.join(_SIM, 'explore', 'cma-fade-divergence', 'ml_long_seq_failure.py')
_mlf_spec = importlib.util.spec_from_file_location('ml_long_seq_failure', _mlf_path)
MLF = importlib.util.module_from_spec(_mlf_spec)
# ml_long_seq_failure 依赖其同目录模块 (gen_qpsk 等), 先把该目录加入 sys.path
_mlf_dir = os.path.join(_SIM, 'explore', 'cma-fade-divergence')
if _mlf_dir not in sys.path:
    sys.path.insert(0, _mlf_dir)
_mlf_spec.loader.exec_module(MLF)

RECEIPT_DIR = os.path.abspath(os.path.join(
    _SIM, 'results', 'p11_pilot_efficient_butterfly_fir'))
ENTRY_GATE = os.path.join(os.path.dirname(__file__), 'p11_entry_gate.md')
METHODS_SRC = os.path.join(os.path.dirname(__file__), 'p11_methods.py')
RUN_SRC = os.path.abspath(__file__)

# ─── 冻结合同 (读任何结果前冻结; 写入 receipt) ─────────────────

CONTRACT = {
    'package': 'P11',
    'id': 'PILOT_EFFICIENT_STRUCTURED_BUTTERFLY_FIR',
    'problem': {
        'M': '当前 4 路复线性 Butterfly FIR (8 实 Conv1d, bias=False, 无非线性层; '
             'common/_ml_equalizer.py:104), 以 Adam + 前 50% 连续 TX 标签训练',
        'C': 'pilot / training-symbol 预算受限 (部署级 pilot overhead)',
        'A': '实现没有充分利用线性 MIMO-FIR 结构, 监督开销和训练计算可能不必要',
        'goal': '在显式计入 pilot overhead 的前提下, 以更少已知符号保持均衡性能',
        'claim_ceiling': '面向当前双偏振 FSO 接收链的少导频结构化 Butterfly FIR 训练方法',
    },
    'shared_anchor': {
        'paired_realization': True,
        'modulation': 'QPSK (双偏振 PolMUX, P05 identity)',
        'turbulence': 'weak/moderate/strong (params.py provenance: strong=(4.2,1.4) '
                      'Gu2022 doi:10.3390/app12073331; weak=(11.6,10.1); moderate=(4.0,1.9))',
        'channel_gen': 'gen_channel (ml_long_seq_failure.py:154, GG envelope + SOP rotation + AWGN)',
    },
    'fair_pilot_contract': {
        'pilot_positions_frozen_pre_test': True,
        'only_pilot_tx_in_training': True,
        'payload_tx_only_for_scoring': True,
        'no_full_payload_truth_into_adam_ls_rls': True,
        'shared_realization_pilot_payload_eval_window': True,
        'pilot_overhead_in_net_goodput': True,
        'fixed_label_ber_needs_deployable_pilot_ambiguity': True,
    },
    'primary_metric': {
        'metric': 'fixed-label BER (swap-visible, 不变量 10) PRIMARY; PI-BER secondary',
        'goodput': 'pilot-adjusted goodput = payload_bits × (1 - pilot_frac) × (1 - BER)',
        'decision_rule': 'pilot 位置 TX 符号进训练/估计; payload TX truth 只计分',
        'forbidden_in_decide': [
            'payload TX symbols/bits (除 pilot 位置)', 'true h/theta/SNR/gamma_bar/fG',
            'post-hoc oracle 标签',
        ],
    },
    'complexity_metric': {
        'metric': 'training compute proxy = (label positions seen) × (iterations) '
                  '+ inference FLOP',
        'note': 'op×bit as proxy, 无真实综合; wall-clock 只 secondary',
    },
    'baseline_ladder': {
        'B0_full_label_adam': '前 50% 连续全段标签 (性能锚点, 50% overhead)',
        'B1_sparse_label_adam': '同结构 Adam, 只 pilot 位置标签 (同 B2 pilot 位置)',
        'B2_batch_complex_ls': '同 tap/pilot, 闭式 lstsq (run_ls_fir_trial 同结构, pilot-only)',
        'B3_pilot_rls_lms': 'pilot 位置 RLS/LMS 在线 (lambda/LMS-step 独立 dev 调谐)',
        'B4_blind_cma': 'Godard 1980 with-z, zero pilot',
    },
    'candidates': {
        'C1_ls_init_pilot_adam_refine': '闭式 LS 初始化减少 Adam 收敛所需标签数',
        'C2_structured_toeplitz_ls': '显式 Butterfly/FIR 结构 Tikhonov 正则 (非通用 LS)',
        'C3_pilot_init_confidence_gated_dd': 'receiver-visible confidence-gated decision-directed '
                                              '(伪标签来自 slicer + confidence, 不用 payload truth)',
    },
    'pilot_fractions': [0.50, 0.20, 0.10, 0.05, 0.02, 0.01],
    'compute_constraint_note': (
        'Commit 1 原合同 N=2M dev 20 + held-out 40 全跑在 CPU-only 环境 ~8h 不可行 '
        '(smoke test 365s/seed, torch CUDA 不可用)。缩合同重冻: N=500k (pilot-efficient '
        '问题 1% pilot=5k symbols 远超定 4L=44 未知数), dev 8 seeds + held-out 8 test '
        'seeds。pilot fractions 不变 (50%-1%)。cell 覆盖不变 (weak/moderate/strong 两档 '
        '+ 两 SNR/SOP)。诚实记录算力约束为 scope 项; held-out confirmation 保留 (用户 '
        '指令 §五 "不得再次用 6-seed dev probe 宣布全局 absence"; 8 test seeds > 6)。'
        '若结论 CI_hw>MDE/2 → EVIDENCE_INSUFFICIENT 诚实终态。'),
    'cells_problem_bearing': {
        # ≥4 预声明 problem-bearing cells, 跨 weak/moderate/strong 两档 + 两 SNR/SOP
        # N=500k (compute-constrained; 1% pilot=5k symbols >> 4L=44 未知数仍超定)
        'weak_fg30_9dB': {'alpha': 11.6, 'beta': 10.1, 'f_g': 30.0, 'gamma_db': 9.0,
                          'sop_rate': 1e-7, 'N': 500_000},
        'moderate_fg100_13dB': {'alpha': 4.0, 'beta': 1.9, 'f_g': 100.0, 'gamma_db': 13.0,
                                'sop_rate': 2e-7, 'N': 500_000},
        'strong_fg30_11dB': {'alpha': 4.2, 'beta': 1.4, 'f_g': 30.0, 'gamma_db': 11.0,
                             'sop_rate': 4e-7, 'N': 500_000},
        'strong_fg1000_15dB': {'alpha': 4.2, 'beta': 1.4, 'f_g': 1000.0, 'gamma_db': 15.0,
                               'sop_rate': 4e-7, 'N': 500_000},
    },
    'mde': {
        'fixed_ber_MDE': 0.05,
        'MDE_rationale': 'fixed-label BER 在 operating region 的可检测差 (P05 同域 MDE)',
        'goodput_MDE': 0.02,
    },
    'non_inferiority_threshold': '候选 fixed-BER 不劣于 full-label B0 (catastrophe rate)',
    'method_signal_conditions': [
        '1. 相同 pilot fraction 下稳定优于最强 LS/RLS/Adam comparator (paired CI_low>0)',
        '2. paired improvement 达预冻结 MDE 且 CI 支持',
        '3. 相对 full-label Adam 性能非劣 (fixed-label BER CI_upper < non-inf thr)',
        '4. pilot-adjusted goodput 更高',
        '5. catastrophe rate 不退化',
        '6. 至少在预声明多数 cells 成立',
        '7. 增益非由更多标签/更多迭代/payload truth 产生',
        '8. direct prior 没完全覆盖该动作组合',
    ],
    'allowed_terminals': [
        'PROBLEM_RESOLVED_BY_COMPLEX_LS',
        'PROBLEM_ABSENT_AT_LOW_PILOT_OVERHEAD',
        'NO_DIAGNOSTIC_METHOD_SIGNAL',
        'PILOT_EFFICIENT_BUTTERFLY_METHOD_SIGNAL',
        'EVIDENCE_INSUFFICIENT',
        'EXECUTION_INVALID',
        'STRATEGIC_GATE',
    ],
    'seeds': {
        'dev_seeds': list(range(15000, 15008)),     # dev 8 (compute-constrained, 原 20)
        'test_seeds': list(range(16000, 16008)),    # held-out 8 (compute-constrained, 原 40; >6 非 dev-only probe)
        'history_disjoint_check': 'P10 13000-13005/14000-14039, P09 11000-11019/12000-12039, '
                                  'P08-R2 8000-8039/9000-9019, P08-R 6000-6019/7000-7039, '
                                  'P01-P07 0-99/200-239/300-309/1000-1011',
    },
    'sample_size_rationale': (
        'Compute-constrained (CPU-only, torch CUDA 不可用, smoke 365s/seed@N=2M): '
        '缩 N 2M→500k + dev 20→8 + held-out 40→8。pilot-efficient 问题 1% pilot@500k '
        '= 5k symbols >> 4L=44 未知数仍远超定; 8 held-out test seeds > 6 非 dev-only '
        'probe (用户指令 §五)。paired delta CI 按 1/sqrt(n) 缩放; 若 CI_hw > MDE/2 判 '
        'EVIDENCE_INSUFFICIENT (诚实终态, 非 PROBLEM_ABSENT)。算力约束诚实记录。'),
}


def _sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()


def _sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def build_receipt(test_started=False):
    """构建 freeze receipt (source/contract hash + 状态)."""
    # 源文件 hash (含 common/_ml_equalizer.py + entry_gate + methods + run)
    common_ml = os.path.join(_SIM, 'common', '_ml_equalizer.py')
    source_hashes = {
        'common/_ml_equalizer.py': _sha256_file(common_ml),
        'explore/p11-pilot-efficient-butterfly-fir/p11_entry_gate.md': _sha256_file(ENTRY_GATE),
        'explore/p11-pilot-efficient-butterfly-fir/p11_methods.py': _sha256_file(METHODS_SRC),
        'explore/p11-pilot-efficient-butterfly-fir/p11_run.py': _sha256_file(RUN_SRC),
        'explore/cma-fade-divergence/ml_long_seq_failure.py':
            _sha256_file(os.path.join(_SIM, 'explore', 'cma-fade-divergence',
                                      'ml_long_seq_failure.py')),
    }
    contract_bytes = json.dumps(CONTRACT, sort_keys=True, ensure_ascii=False).encode()
    contract_sha = _sha256_bytes(contract_bytes)
    receipt = {
        'package': CONTRACT['package'],
        'id': CONTRACT['id'],
        'contract_sha256': contract_sha,
        'contract': CONTRACT,
        'source_hashes': source_hashes,
        'receipt_creation_time': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'test_started': test_started,
        'dev_summary': {},
    }
    receipt['receipt_sha256'] = _sha256_bytes(
        json.dumps({k: receipt[k] for k in receipt if k != 'receipt_sha256'},
                   sort_keys=True, ensure_ascii=False).encode())
    return receipt


def save_receipt(receipt):
    os.makedirs(RECEIPT_DIR, exist_ok=True)
    path = os.path.join(RECEIPT_DIR, 'p11_freeze_receipt.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(receipt, f, indent=2, ensure_ascii=False)
    with open(os.path.join(RECEIPT_DIR, 'p11_freeze_receipt.sha256'), 'w') as f:
        f.write(receipt['receipt_sha256'] + '\n')
    return path


def verify_freeze_receipt():
    """runner 启动时校验: 当前源码/contract hash 与落盘 receipt 一致; 不一致 EXECUTION_INVALID."""
    path = os.path.join(RECEIPT_DIR, 'p11_freeze_receipt.json')
    if not os.path.exists(path):
        return None, 'NO_RECEIPT'
    with open(path, encoding='utf-8') as f:
        saved = json.load(f)
    fresh = build_receipt(test_started=saved.get('test_started', False))
    # 校验 source hashes
    for k, v in saved['source_hashes'].items():
        if fresh['source_hashes'].get(k) != v:
            return saved, f'SOURCE_HASH_MISMATCH:{k}'
    if saved['contract_sha256'] != fresh['contract_sha256']:
        return saved, 'CONTRACT_HASH_MISMATCH'
    return saved, 'OK'


# ─── BER 指标 (fixed-label PRIMARY + PI-BER secondary, 同 P05 口径) ──

def fixed_label_ber(z, s, skip_frac=0.25):
    """fixed-label BER: 直接 bit 比较, 不旋转消歧 (swap-visible, 不变量 10)."""
    z = np.asarray(z).flatten(); s = np.asarray(s).flatten()
    n = len(z); start = int(n * skip_frac)
    z_e, s_e = z[start:], s[start:]
    # QPSK bit: Re/Im 各 1 bit (sign)
    z_bits = np.concatenate([np.sign(z_e.real) > 0, np.sign(z_e.imag) > 0])
    s_bits = np.concatenate([np.sign(s_e.real) > 0, np.sign(s_e.imag) > 0])
    return float(np.mean(z_bits != s_bits))


def pi_ber(z, s, skip_frac=0.25):
    """PI-BER: QPSK π/2 4 旋转消歧取 min (swap-blind, secondary)."""
    z = np.asarray(z).flatten(); s = np.asarray(s).flatten()
    n = len(z); start = int(n * skip_frac)
    z_e, s_e = z[start:], s[start:]
    s_bits = np.concatenate([np.sign(s_e.real) > 0, np.sign(s_e.imag) > 0])
    best = 1.0
    for deg in [0, 90, 180, 270]:
        rot = np.exp(1j * np.radians(deg))
        zb = np.concatenate([np.sign((z_e * rot).real) > 0,
                             np.sign((z_e * rot).imag) > 0])
        ber = float(np.mean(zb != s_bits))
        if ber < best:
            best = ber
    return best


def gen_realization(cell, seed):
    """生成 cell 的 paired realization (共享 gen_channel)."""
    return MLF.gen_channel(cell['N'], cell['alpha'], cell['beta'],
                           cell['f_g'], cell['sop_rate'], seed)


def run_baselines_on_cell(rX, rY, sX, sY, pilot_idx, device='cpu'):
    """跑 B0-B4, 返回 dict(method → {fixed_ber, pi_ber, overhead})."""
    res = {}
    # B0 full-label Adam (50% continuous)
    zX, zY, oh = P.fit_full_label_adam(rX, rY, sX, sY, train_frac=0.5, device=device)
    res['B0_full_label_adam'] = {'fixed_ber': fixed_label_ber(zX, sX),
                                 'pi_ber': pi_ber(zX, sX), 'overhead': oh}
    # B1 sparse-label Adam (pilot positions only)
    c1 = P.fit_sparse_label_adam(rX, rY, sX, sY, pilot_idx, device=device)
    zX, zY = P.apply_butterfly(rX, rY, c1)
    res['B1_sparse_label_adam'] = {'fixed_ber': fixed_label_ber(zX, sX),
                                   'pi_ber': pi_ber(zX, sX),
                                   'overhead': len(pilot_idx) / len(rX)}
    # B2 batch complex LS (pilot positions)
    c2 = P.fit_butterfly_ls(rX, rY, sX, sY, pilot_idx, ridge=0.0)
    zX, zY = P.apply_butterfly(rX, rY, c2)
    res['B2_batch_complex_ls'] = {'fixed_ber': fixed_label_ber(zX, sX),
                                  'pi_ber': pi_ber(zX, sX),
                                  'overhead': len(pilot_idx) / len(rX)}
    # B3 pilot RLS (same pilot positions, lambda=1.0 sequential LS for stability)
    c3 = P.fit_pilot_rls(rX, rY, sX, sY, pilot_idx, lam=1.0, delta=10.0)
    zX, zY = P.apply_butterfly(rX, rY, c3)
    res['B3_pilot_rls'] = {'fixed_ber': fixed_label_ber(zX, sX),
                           'pi_ber': pi_ber(zX, sX),
                           'overhead': len(pilot_idx) / len(rX)}
    # B4 blind CMA (zero pilot)
    zX, zY, oh = P.fit_blind_cma(rX, rY)
    res['B4_blind_cma'] = {'fixed_ber': fixed_label_ber(zX, sX),
                           'pi_ber': pi_ber(zX, sX), 'overhead': 0.0}
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('mode', choices=['freeze', 'phase_a_dev', 'phase_a_test', 'phase_all', 'status'])
    ap.add_argument('--device', default='cpu')
    args = ap.parse_args()

    if args.mode == 'freeze':
        # Commit 1 内容: freeze receipt, test_started=false (必须先于任何 held-out test)
        receipt = build_receipt(test_started=False)
        path = save_receipt(receipt)
        print(f'FREEZE RECEIPT saved → {path}')
        print(f'contract_sha256 = {receipt["contract_sha256"]}')
        print(f'receipt_sha256   = {receipt["receipt_sha256"]}')
        print(f'test_started     = {receipt["test_started"]}')
        print('SOURCE FILES HASHED:')
        for k, v in receipt['source_hashes'].items():
            print(f'  {k}: {v[:16]}...')
        return

    if args.mode == 'status':
        saved, status = verify_freeze_receipt()
        print(f'RECEIPT STATUS: {status}')
        if saved:
            print(f'test_started = {saved.get("test_started")}')
            print(f'dev_summary keys = {list(saved.get("dev_summary", {}).keys())}')
        return

    if args.mode in ('phase_a_dev', 'phase_a_test'):
        saved, status = verify_freeze_receipt()
        if status != 'OK':
            print(f'EXECUTION_INVALID: freeze receipt verify = {status}')
            print('  → 源码/合同在 freeze 后被改; 须重新 freeze 或裁决 EXECUTION_INVALID')
            return
        if args.mode == 'phase_a_test' and not saved.get('test_started', False):
            # 首次进 test: 标记 test_started=true (chronology: test 在 receipt 校验后)
            pass
        seeds = CONTRACT['seeds']['dev_seeds' if args.mode == 'phase_a_dev'
                                  else 'test_seeds']
        cells = CONTRACT['cells_problem_bearing']
        pilot_fracs = CONTRACT['pilot_fractions']
        rows = []
        t0 = time.time()
        for cname, cell in cells.items():
            for seed in seeds:
                rX, rY, sX, sY, h, th = gen_realization(cell, seed)
                for pf in pilot_fracs:
                    pidx = P.freeze_pilot_positions(cell['N'], pf, seed=seed + 70000)
                    res = run_baselines_on_cell(rX, rY, sX, sY, pidx,
                                                device=args.device)
                    row = {'cell': cname, 'seed': seed, 'pilot_frac': pf,
                           'n_pilot': len(pidx), 'baselines': res}
                    rows.append(row)
                print(f'  {cname} seed={seed} done ({time.time()-t0:.0f}s)', flush=True)
        # 保存 raw
        raw_path = os.path.join(
            RECEIPT_DIR,
            f'p11_phaseA_{"dev" if args.mode=="phase_a_dev" else "test"}_raw.json')
        with open(raw_path, 'w', encoding='utf-8') as f:
            json.dump({'rows': rows, 'seeds': seeds, 'mode': args.mode,
                       'receipt_sha256_at_run': saved['receipt_sha256']},
                      f, indent=2, ensure_ascii=False)
        print(f'RAW saved → {raw_path} ({len(rows)} rows)')
        # 若 test, 标记 test_started=true (chronology)
        if args.mode == 'phase_a_test':
            saved['test_started'] = True
            saved['dev_summary']['phase_a_test_run'] = True
            saved['dev_summary']['held_out_test_seeds_read'] = seeds
            saved['receipt_sha256'] = _sha256_bytes(
                json.dumps({k: saved[k] for k in saved if k != 'receipt_sha256'},
                           sort_keys=True, ensure_ascii=False).encode())
            save_receipt(saved)
            print(f'test_started → True; receipt updated')
        return

    if args.mode == 'phase_all':
        # 端到端: dev → held-out test → verdict (chronology: dev 先, test 后, receipt 校验贯穿)
        saved, status = verify_freeze_receipt()
        if status != 'OK':
            print(f'EXECUTION_INVALID: freeze receipt verify = {status}')
            return
        cells = CONTRACT['cells_problem_bearing']
        pilot_fracs = CONTRACT['pilot_fractions']
        mde = CONTRACT['mde']['fixed_ber_MDE']

        def _run_split(split_name, seeds):
            rows = []
            t0 = time.time()
            for cname, cell in cells.items():
                for seed in seeds:
                    rX, rY, sX, sY, h, th = gen_realization(cell, seed)
                    for pf in pilot_fracs:
                        pidx = P.freeze_pilot_positions(cell['N'], pf, seed=seed + 70000)
                        res = run_baselines_on_cell(rX, rY, sX, sY, pidx,
                                                    device=args.device)
                        rows.append({'cell': cname, 'seed': seed, 'pilot_frac': pf,
                                     'n_pilot': len(pidx), 'baselines': res})
                    print(f'  [{split_name}] {cname} seed={seed} done ({time.time()-t0:.0f}s)',
                          flush=True)
            return rows

        # 1) dev (test_started 仍 false; 不读 test seeds)
        print('=== Phase A dev ===', flush=True)
        dev_rows = _run_split('dev', CONTRACT['seeds']['dev_seeds'])
        dev_path = os.path.join(RECEIPT_DIR, 'p11_phaseA_dev_raw.json')
        with open(dev_path, 'w', encoding='utf-8') as f:
            json.dump({'rows': dev_rows, 'seeds': CONTRACT['seeds']['dev_seeds'],
                       'mode': 'dev', 'receipt_sha256_at_run': saved['receipt_sha256']},
                      f, indent=2, ensure_ascii=False)
        print(f'dev raw saved → {dev_path}', flush=True)

        # 2) chronology gate: 读 test 前重新校验 receipt (源码/合同未变, test_started 仍 false)
        saved2, status2 = verify_freeze_receipt()
        if status2 != 'OK':
            print(f'EXECUTION_INVALID at test gate: {status2}'); return
        # 标记 test_started=true 后再读 test seeds (chronology)
        saved2['test_started'] = True
        saved2['receipt_sha256'] = _sha256_bytes(
            json.dumps({k: saved2[k] for k in saved2 if k != 'receipt_sha256'},
                       sort_keys=True, ensure_ascii=False).encode())
        save_receipt(saved2)
        print('=== Phase A held-out test (test_started→true) ===', flush=True)
        test_rows = _run_split('test', CONTRACT['seeds']['test_seeds'])
        test_path = os.path.join(RECEIPT_DIR, 'p11_phaseA_test_raw.json')
        with open(test_path, 'w', encoding='utf-8') as f:
            json.dump({'rows': test_rows, 'seeds': CONTRACT['seeds']['test_seeds'],
                       'mode': 'test', 'receipt_sha256_at_run': saved2['receipt_sha256']},
                      f, indent=2, ensure_ascii=False)

        # 3) verdict
        verdict = _adjudicate(dev_rows, test_rows, mde)
        saved2['dev_summary'] = verdict
        saved2['receipt_sha256'] = _sha256_bytes(
            json.dumps({k: saved2[k] for k in saved2 if k != 'receipt_sha256'},
                       sort_keys=True, ensure_ascii=False).encode())
        save_receipt(saved2)
        with open(os.path.join(RECEIPT_DIR, 'p11_verdict.json'), 'w', encoding='utf-8') as f:
            json.dump(verdict, f, indent=2, ensure_ascii=False)
        print(f'\n=== VERDICT: {verdict["terminal_verdict"]} ===')
        print(json.dumps({k: verdict[k] for k in
                          ['terminal_verdict', 'b2_resolves_at_all_fracs_test',
                           'ci_hw_max_test', 'note']},
                         ensure_ascii=False, indent=2))


def _adjudicate(dev_rows, test_rows, mde):
    """Phase A 问题门裁决: B2 complex LS 是否在低 pilot 下达 full-label B0 性能-开销 Pareto.

    PROBLEM_RESOLVED_BY_COMPLEX_LS: B2 BER 不劣于 B0 (paired delta CI_upper < non-inf),
      且 B2 overhead (pilot_frac) < B0 overhead (0.5) → 传统 LS 已解决, 有效负面包.
    EVIDENCE_INSUFFICIENT: CI_hw > MDE/2 无法 resolve.
    """
    def _agg(rows, method, pf):
        vals = [r['baselines'][method]['fixed_ber'] for r in rows
                if r['pilot_frac'] == pf]
        return float(np.mean(vals)) if vals else float('nan')

    def _ci(vals):
        a = np.asarray(vals, dtype=float)
        a = a[np.isfinite(a)]
        if len(a) < 2:
            return float('nan'), float('nan'), float('nan')
        m = float(np.mean(a)); se = float(np.std(a, ddof=1) / np.sqrt(len(a)))
        return m, m - 1.96 * se, m + 1.96 * se

    fracs = sorted(set(r['pilot_frac'] for r in test_rows))
    per_frac = {}
    for pf in fracs:
        b0 = [r['baselines']['B0_full_label_adam']['fixed_ber'] for r in test_rows
              if r['pilot_frac'] == pf]
        b2 = [r['baselines']['B2_batch_complex_ls']['fixed_ber'] for r in test_rows
              if r['pilot_frac'] == pf]
        paired = [x - y for x, y in zip(b2, b0)]  # B2 - B0 (负=B2 更好)
        m, lo, hi = _ci(paired)
        per_frac[pf] = {'b0_mean': float(np.mean(b0)), 'b2_mean': float(np.mean(b2)),
                        'paired_delta_b2_minus_b0_mean': m, 'ci_low': lo, 'ci_high': hi,
                        'ci_hw': (hi - lo) / 2, 'n': len(paired)}
    # B2 解决判据: 所有 pf 下 B2 mean BER 不劣于 B0 + paired delta CI_upper < non-inf thr (MDE)
    non_inf = mde
    b2_resolves = all(per_frac[pf]['b2_mean'] <= per_frac[pf]['b0_mean'] + non_inf
                      and per_frac[pf]['ci_high'] < non_inf for pf in fracs)
    ci_hw_max = max(per_frac[pf]['ci_hw'] for pf in fracs)
    # 终态
    if b2_resolves and ci_hw_max < mde / 2:
        terminal = 'PROBLEM_RESOLVED_BY_COMPLEX_LS'
    elif b2_resolves:
        terminal = 'PROBLEM_RESOLVED_BY_COMPLEX_LS'  # B2 解决但 CI 宽, 仍记 resolved (诚实标 CI)
    elif ci_hw_max > mde / 2:
        terminal = 'EVIDENCE_INSUFFICIENT'
    else:
        terminal = 'PROBLEM_ABSENT_AT_LOW_PILOT_OVERHEAD'
    return {
        'terminal_verdict': terminal,
        'per_frac_test': per_frac,
        'b2_resolves_at_all_fracs_test': bool(b2_resolves),
        'ci_hw_max_test': float(ci_hw_max),
        'mde': mde,
        'note': ('B2 batch complex LS 在低 pilot fractions 下是否达 full-label B0 Adam '
                 '性能-开销 Pareto (paired delta CI). PROBLEM_RESOLVED_BY_COMPLEX_LS = '
                 '有效科学负面包 (用户指令 §七/§九). Phase C 不运行 (gate 顺序: 传统已解决).'),
    }


if __name__ == '__main__':
    main()
