"""ML 长序列失效边界诊断 (PROMPT-010).

> 方向: Q-CMA-FADE / 状态: WIP / 创建: 2026-07-12
> 组织规范: ../../SIM-ORG.md (P1 结果进 results/; P5 标方向+状态)
> 来源: PROMPT-010 (主控派发, 开放诊断任务)

## 研究问题 (分层证伪)

Q1 (最关键): ML 在长序列下失效真实, 还是单 seed 偶然?
  - N ∈ {2M, 3M, 5M, 8M} × ≥10 seeds, f_G=30, SOP=4e-7, strong, 20dB, QPSK
  - 判据: N↑ 时 ML test-late BER 单调上升且 N=5M 显著 > early 段 → 失效真实

Q2: 失效边界 (SOP 临界角)
  - 固定 N=5M 扫 SOP_RATE ∈ {0, 1e-8, 1e-7, 4e-7, 1e-6, 1e-5}
  - 找 ML test-late BER vs test 段 SOP 累积旋转角的临界点

Q3: 失效机制 (对照 A/B/C)
  - A: 训练覆盖更大 SOP 角度 (用更大 SOP_RATE 数据训练) → test 同漂移下 ML 是否不崩?
  - B: 周期性重训练 (每 test 段 1/4 用前 1/4 重训练)
  - C: 非 ML 固定 LS-FIR (纯线性回归前馈) 复现 N=5M 失效

## TL-20 假设 (跑前写)

H1 (主控猜想): ML 长序列失效真实, 机制=固定权重跟不上 test 段 SOP 漂移.
  预测: N↑ → ML test-late BER↑; BER vs SOP 累积旋转角 r>0.7.
H2 (备选): ML 不失效, 主控单 seed 是 seed-bias.
  预测: 各 N 下 ML test-late BER mean<0.01 不随 N 单调上升.
证伪判据: H1 要求 r>0.7; 否则 H2 成立.

## 关键约束 (PROMPT-010 §6 陷阱)

1. seed-bias: 必须 ≥10 seeds + mean±std (D012 教训, h_mean CV≈1.0)
2. 切片对齐: test-late = test 段内后 1/4, 不是原序列后 1/4
3. 不改信号模型: 复用 r_lcr gen_channel (SOP=4e-7, GAMMA_BAR=100, T_S=1/2.5e9, BLOCK=100)
4. BER 做 4 旋转相位校正 (QPSK π/2 模糊)
5. 只报事实+数据, 不写 D### 决策

用法:
  cd projects/simulation && python explore/cma-fade-divergence/ml_long_seq_failure.py
  (支持 checkpoint 断点续跑, 中断后重跑自动跳过已完成项)
"""
import sys
import json
import time
import numpy as np
from pathlib import Path
from collections import defaultdict

# 路径设置: 确保从 projects/simulation/ 运行
SIM_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(SIM_DIR))

from params import SimulationConfig
from common._gg_time import gg_time_envelope
from common._cma import CMAEqualizer2x2
from common._ml_equalizer import MLChannelEqualizer
from common._equalizer import mmse_equalize
from common._config import BLOCK

cfg = SimulationConfig()
GAMMA_BAR = cfg.experiment.GAMMA_BAR_DEFAULT  # 100 (20 dB)
T_S = cfg.system.T_S

# ─── 实验参数 (跟 r_lcr / S009 / 批次1 一致, PROMPT-010 §4) ───
F_G = 30.0              # 固定 (PROMPT Q1)
MOD = 'qpsk'
TURB = 'strong'         # α=1.5, β=0.8
N_TAP = 11
SOP_RATE = 4e-7         # 1 krad/s (sat.1553 §6.3, 跟 S009/批次1 一致)
MU_SAFE = 1e-3
R2_QPSK = 1.0
# N 扫描 (Q1)
N_SWEEP = [2_000_000, 3_000_000, 5_000_000, 8_000_000]
N_SEEDS = 10            # PROMPT-010 Q1 要求 ≥10 seeds
# ML 训练参数 (跟 r_lcr 一致, PROMPT-010 §4)
ML_PARAMS = dict(n_tap=11, lr=0.005, batch_size=1024, n_epochs=20,
                 device='cuda', patience=5)
ML_TRAIN_FRAC = 0.5     # 前 50% 训练, 后 50% 测试

# Q2: SOP_RATE 扫描 (固定 N=5M)
N_Q2 = 5_000_000
SOP_SWEEP = [0.0, 1e-8, 1e-7, 4e-7, 1e-6, 1e-5]
N_SEEDS_Q2 = 8          # Q2 可降 seed (PROMPT §4)

RESULTS_DIR = SIM_DIR / 'results' / 'cma-fade-divergence'
CKPT_DIR = RESULTS_DIR / 'ml_long_seq_ckpts'


# ─── checkpoint 工具 ────────────────────────────────────────

def _ckpt_path(name):
    CKPT_DIR.mkdir(parents=True, exist_ok=True)
    return CKPT_DIR / f'{name}.json'


def _load_ckpt(name):
    p = _ckpt_path(name)
    if p.exists():
        try:
            with open(p, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def _save_ckpt(name, data):
    try:
        with open(_ckpt_path(name), 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=1, default=str)
    except Exception as e:
        print(f"  [warn] ckpt save fail: {e}")


# ─── 调制/解调 (复用 r_lcr) ─────────────────────────────────

def gen_qpsk(N, rng):
    bits = rng.integers(0, 2, N * 2)
    s = ((1 - 2 * bits[0::2]) + 1j * (1 - 2 * bits[1::2])) / np.sqrt(2)
    return s, bits


def qpsk_demap(z):
    z = np.asarray(z).flatten()
    bits = np.zeros(len(z) * 2, dtype=int)
    bits[0::2] = (z.real < 0).astype(int)
    bits[1::2] = (z.imag < 0).astype(int)
    return bits


# ─── BER (4 旋转相位校正, r_lcr compute_ber_phase_corrected) ──

def compute_ber_phase_corrected(z, s, skip_frac=0.0):
    """QPSK BER, 4 旋转相位校正取最低 (消除 π/2 相位模糊)."""
    z = np.asarray(z).flatten()
    s = np.asarray(s).flatten()
    n = len(z)
    start = int(n * skip_frac)
    z_eval = z[start:]
    s_eval = s[start:]
    s_bits = qpsk_demap(s_eval)
    best_ber = 1.0
    for deg in [0, 90, 180, 270]:
        rot = np.exp(1j * np.radians(deg))
        ber = float(np.mean(qpsk_demap(z_eval * rot) != s_bits))
        if ber < best_ber:
            best_ber = ber
    return best_ber


# ─── 信道生成 (复用 r_lcr gen_channel, 不改信号模型) ─────────
# 注: sop_rate 作为参数暴露, Q2 扫描用

def gen_channel(N, alpha, beta, f_g, sop_rate, seed):
    """生成双偏振 GG 衰落 + SOP 旋转信道 (QPSK). 返回 rX, rY, sX, sY, h, theta."""
    rng = np.random.default_rng(seed)
    tau_c = cfg.gg_time.tau_c_from_fg(f_g)
    h = gg_time_envelope(N, alpha, beta, tau_c, block=BLOCK, t_s=T_S,
                         method='gar', seed=seed)
    sX, _ = gen_qpsk(N, rng)
    sY, _ = gen_qpsk(N, rng)
    theta = sop_rate * np.arange(N)  # SOP 累积旋转
    cos_t = np.cos(theta)
    sin_t = np.sin(theta)
    nv = 1.0 / (2 * GAMMA_BAR)
    rX = np.sqrt(h) * (cos_t * sX + sin_t * sY) \
        + np.sqrt(nv) * (rng.standard_normal(N) + 1j * rng.standard_normal(N))
    rY = np.sqrt(h) * (-sin_t * sX + cos_t * sY) \
        + np.sqrt(nv) * (rng.standard_normal(N) + 1j * rng.standard_normal(N))
    return rX, rY, sX, sY, h, theta


def oracle_equalize(rX, rY, h, theta, gamma_bar):
    """oracle: 撤销 SOP + MMSE (完美 CSI 下界)."""
    cos_t = np.cos(-theta)
    sin_t = np.sin(-theta)
    rX_u = cos_t * rX + sin_t * rY
    rY_u = -sin_t * rX + cos_t * rY
    zX = mmse_equalize(rX_u, h, gamma_bar)
    zY = mmse_equalize(rY_u, h, gamma_bar)
    return zX, zY


# ─── 辅助: test 段切片 (陷阱3) ──────────────────────────────

def test_late_slice(n_total, train_frac=ML_TRAIN_FRAC, late_frac=0.25):
    """返回 test 段内后 late_frac 部分的索引范围 [start, end).

    test 段 = [n_train, n_total]; test-late = test 段内后 1/4.
    返回 (start, end) 绝对索引.
    """
    n_train = int(n_total * train_frac)
    n_test = n_total - n_train
    late_start = n_train + int(n_test * (1.0 - late_frac))
    return late_start, n_total


def test_early_slice(n_total, train_frac=ML_TRAIN_FRAC, early_frac=0.25):
    """test 段内前 early_frac 部分 (对照: test-early)."""
    n_train = int(n_total * train_frac)
    n_test = n_total - n_train
    early_end = n_train + int(n_test * early_frac)
    return n_train, early_end


# ─── 单 ML trial (训练前 train_frac, 推理全段, BER 分段算) ───

def run_ml_trial(rX, rY, sX, sY, ml_params=None):
    """训练 ML (前 train_frac) 并推理全段. 返回 zX_ml, zY_ml 全段 + n_train."""
    mp = ml_params or ML_PARAMS
    n_total = len(rX)
    n_train = int(n_total * ML_TRAIN_FRAC)
    ml = MLChannelEqualizer(**mp)
    ml.train(rX[:n_train], rY[:n_train], sX[:n_train], sY[:n_train],
             val_split=0.2, verbose=False)
    res = ml.equalize(rX, rY)
    return res['zX'].flatten(), res['zY'].flatten(), n_train, res


def run_cma_trial(rX, rY, sX, mu=MU_SAFE):
    """CMA 均衡全段 (对照). 返回 zX, zY, diverged, diverge_idx."""
    cma = CMAEqualizer2x2(n_tap=N_TAP, mu=mu, R2=R2_QPSK)
    res = cma.equalize(rX, rY)
    return res['zX'], res['zY'], bool(res['diverged']), res['diverge_idx']


# ─── Q1: ML test-late BER vs N (多 seed) ────────────────────

def run_q1():
    """Q1: N ∈ {2M,3M,5M,8M} × 10 seeds, 报 ML test-late BER mean±std.

    同时记 ML test-early BER, CMA test-late BER, oracle BER 作对照.
    """
    print("\n" + "=" * 70)
    print("Q1: ML 长序列失效多 seed 多 N 确认")
    print(f"参数: f_G={F_G}, SOP={SOP_RATE} (1krad/s), turb={TURB}, "
          f"20dB, QPSK, N∈{N_SWEEP}, {N_SEEDS} seeds")
    print("=" * 70)
    alpha, beta = cfg.turbulence.as_dict()[TURB]

    ckpt = _load_ckpt('q1')
    results = ckpt.get('results', {})

    print(f"{'N':>10} {'ML_late':>12} {'ML_early':>12} {'CMA_late':>10} "
          f"{'oracle':>10} {'n_div':>6} {'n':>3}")
    print("-" * 70)

    for N in N_SWEEP:
        sk = str(N)
        # 跳过已完成 (达到 seed 数)
        if sk in results and len(results[sk].get('ml_late_ber', [])) >= N_SEEDS:
            v = results[sk]
            print(f"{N:>10d} {np.mean(v['ml_late_ber']):>12.4f} "
                  f"{np.mean(v['ml_early_ber']):>12.4f} "
                  f"{np.mean(v['cma_late_ber']):>10.4f} "
                  f"{np.mean(v['oracle_ber']):>10.4f} "
                  f"{int(sum(v['cma_diverged'])):>6d} "
                  f"{len(v['ml_late_ber']):>3d} (cached)", flush=True)
            continue

        ml_late, ml_early, cma_late, orc = [], [], [], []
        cma_div = []
        ml_w_norm, ml_max_z = [], []
        seeds_done = 0

        for seed in range(N_SEEDS):
            # 断点: 跳过已完成 seed
            if sk in results and seed < len(results[sk].get('ml_late_ber', [])):
                continue
            seed_int = 1000 + seed  # 确定性 seed scheme (跟 task1 一致, 非 hash)
            t0 = time.time()
            rX, rY, sX, sY, h, theta = gen_channel(
                N, alpha, beta, F_G, SOP_RATE, seed_int)

            # ML: 训练 + 推理
            zX_ml, zY_ml, n_train, ml_res = run_ml_trial(rX, rY, sX, sY)
            # 切片 (陷阱3: test 段内后 1/4)
            late_s, late_e = test_late_slice(N)
            early_s, early_e = test_early_slice(N)
            ml_late_ber = compute_ber_phase_corrected(
                zX_ml[late_s:late_e], sX[late_s:late_e], 0.0)
            ml_early_ber = compute_ber_phase_corrected(
                zX_ml[early_s:early_e], sX[early_s:early_e], 0.0)

            # CMA 对照 (同信道)
            zX_cma, zY_cma, div, div_idx = run_cma_trial(rX, rY, sX, MU_SAFE)
            if div and div_idx is not None and div_idx < late_s:
                # CMA 在 test-late 前就发散 → 取发散前 valid 段
                valid_end = max(int(div_idx), 1)
                cma_late_ber = compute_ber_phase_corrected(
                    zX_cma[:valid_end], sX[:valid_end], 0.1) if valid_end > 100 else 0.5
            else:
                cma_late_ber = compute_ber_phase_corrected(
                    zX_cma[late_s:late_e], sX[late_s:late_e], 0.0)

            # oracle 对照
            zX_or, _ = oracle_equalize(rX, rY, h, theta, GAMMA_BAR)
            orc_ber = compute_ber_phase_corrected(
                zX_or[late_s:late_e], sX[late_s:late_e], 0.0)

            ml_late.append(float(ml_late_ber))
            ml_early.append(float(ml_early_ber))
            cma_late.append(float(cma_late_ber))
            orc.append(float(orc_ber))
            cma_div.append(int(div))
            ml_w_norm.append(float(ml_res['w_norm']))
            ml_max_z.append(float(ml_res['max_z_amp']))
            seeds_done += 1

            # 每 seed 存 ckpt
            results[sk] = {
                'ml_late_ber': ml_late, 'ml_early_ber': ml_early,
                'cma_late_ber': cma_late, 'oracle_ber': orc,
                'cma_diverged': cma_div,
                'ml_w_norm': ml_w_norm, 'ml_max_z': ml_max_z,
                'n_train': n_train,
                'sop_late_rot_deg': float(SOP_RATE * (late_e - late_s) * 180 / np.pi),
            }
            _save_ckpt('q1', {'results': results})
            print(f"  N={N} seed{seed}: ML_late={ml_late_ber:.4f} "
                  f"ML_early={ml_early_ber:.4f} CMA_late={cma_late_ber:.4f} "
                  f"orc={orc_ber:.4f} ({time.time()-t0:.0f}s)", flush=True)

        v = results[sk]
        print(f"{N:>10d} {np.mean(v['ml_late_ber']):>12.4f} "
              f"{np.mean(v['ml_early_ber']):>12.4f} "
              f"{np.mean(v['cma_late_ber']):>10.4f} "
              f"{np.mean(v['oracle_ber']):>10.4f} "
              f"{int(sum(v['cma_diverged'])):>6d} "
              f"{len(v['ml_late_ber']):>3d}", flush=True)

    # 汇总 mean±std
    summary = {}
    for N in N_SWEEP:
        v = results[str(N)]
        summary[str(N)] = {
            'ml_late_mean': float(np.mean(v['ml_late_ber'])),
            'ml_late_std': float(np.std(v['ml_late_ber'])),
            'ml_late_list': [float(x) for x in v['ml_late_ber']],
            'ml_early_mean': float(np.mean(v['ml_early_ber'])),
            'ml_early_std': float(np.std(v['ml_early_ber'])),
            'ml_early_list': [float(x) for x in v['ml_early_ber']],
            'cma_late_mean': float(np.mean(v['cma_late_ber'])),
            'cma_late_list': [float(x) for x in v['cma_late_ber']],
            'oracle_mean': float(np.mean(v['oracle_ber'])),
            'oracle_list': [float(x) for x in v['oracle_ber']],
            'n_cma_diverged': int(np.sum(v['cma_diverged'])),
            'n_seeds': len(v['ml_late_ber']),
            'sop_test_late_rot_deg': float(v.get('sop_late_rot_deg', 0.0)),
            'ml_w_norm_mean': float(np.mean(v.get('ml_w_norm', [0]))),
            'ml_max_z_mean': float(np.mean(v.get('ml_max_z', [0]))),
        }
    return summary


# ─── Q2: ML test-late BER vs SOP_RATE (固定 N=5M) ───────────

def run_q2():
    """Q2: 固定 N=5M 扫 SOP_RATE, 找 ML 失效 SOP 临界角."""
    print("\n" + "=" * 70)
    print("Q2: ML 失效 SOP 边界 (固定 N=5M)")
    print(f"SOP_RATE ∈ {SOP_SWEEP}, {N_SEEDS_Q2} seeds, f_G={F_G}")
    print("=" * 70)
    alpha, beta = cfg.turbulence.as_dict()[TURB]

    ckpt = _load_ckpt('q2')
    results = ckpt.get('results', {})

    print(f"{'SOP_RATE':>10} {'rad/s':>8} {'ML_late':>12} {'CMA_late':>10} "
          f"{'oracle':>10} {'test_rot°':>10} {'n':>3}")
    print("-" * 70)

    for sop in SOP_SWEEP:
        sk = str(sop)
        if sk in results and len(results[sk].get('ml_late_ber', [])) >= N_SEEDS_Q2:
            v = results[sk]
            sop_rads = sop * 2.5e9 / 1e3 if sop > 0 else 0.0
            print(f"{sop:>10.1e} {sop_rads:>8.1f} "
                  f"{np.mean(v['ml_late_ber']):>12.4f} "
                  f"{np.mean(v['cma_late_ber']):>10.4f} "
                  f"{np.mean(v['oracle_ber']):>10.4f} "
                  f"{v['test_late_rot_deg']:>10.1f} "
                  f"{len(v['ml_late_ber']):>3d} (cached)", flush=True)
            continue

        ml_late, cma_late, orc = [], [], []
        cma_div = []
        late_s, late_e = test_late_slice(N_Q2)
        test_late_rot_deg = float(sop * (late_e - late_s) * 180 / np.pi)

        for seed in range(N_SEEDS_Q2):
            if sk in results and seed < len(results[sk].get('ml_late_ber', [])):
                continue
            seed_int = 2000 + seed
            t0 = time.time()
            rX, rY, sX, sY, h, theta = gen_channel(
                N_Q2, alpha, beta, F_G, sop, seed_int)

            zX_ml, zY_ml, n_train, ml_res = run_ml_trial(rX, rY, sX, sY)
            ml_late_ber = compute_ber_phase_corrected(
                zX_ml[late_s:late_e], sX[late_s:late_e], 0.0)

            zX_cma, zY_cma, div, div_idx = run_cma_trial(rX, rY, sX, MU_SAFE)
            if div and div_idx is not None and div_idx < late_s:
                valid_end = max(int(div_idx), 1)
                cma_late_ber = compute_ber_phase_corrected(
                    zX_cma[:valid_end], sX[:valid_end], 0.1) if valid_end > 100 else 0.5
            else:
                cma_late_ber = compute_ber_phase_corrected(
                    zX_cma[late_s:late_e], sX[late_s:late_e], 0.0)

            zX_or, _ = oracle_equalize(rX, rY, h, theta, GAMMA_BAR)
            orc_ber = compute_ber_phase_corrected(
                zX_or[late_s:late_e], sX[late_s:late_e], 0.0)

            ml_late.append(float(ml_late_ber))
            cma_late.append(float(cma_late_ber))
            orc.append(float(orc_ber))
            cma_div.append(int(div))

            results[sk] = {
                'ml_late_ber': ml_late, 'cma_late_ber': cma_late,
                'oracle_ber': orc, 'cma_diverged': cma_div,
                'test_late_rot_deg': test_late_rot_deg,
            }
            _save_ckpt('q2', {'results': results})
            print(f"  SOP={sop:.1e} seed{seed}: ML_late={ml_late_ber:.4f} "
                  f"CMA_late={cma_late_ber:.4f} orc={orc_ber:.4f} "
                  f"({time.time()-t0:.0f}s)", flush=True)

        v = results[sk]
        sop_rads = sop * 2.5e9 / 1e3 if sop > 0 else 0.0
        print(f"{sop:>10.1e} {sop_rads:>8.1f} "
              f"{np.mean(v['ml_late_ber']):>12.4f} "
              f"{np.mean(v['cma_late_ber']):>10.4f} "
              f"{np.mean(v['oracle_ber']):>10.4f} "
              f"{v['test_late_rot_deg']:>10.1f} "
              f"{len(v['ml_late_ber']):>3d}", flush=True)

    summary = {}
    for sop in SOP_SWEEP:
        v = results[str(sop)]
        summary[str(sop)] = {
            'ml_late_mean': float(np.mean(v['ml_late_ber'])),
            'ml_late_std': float(np.std(v['ml_late_ber'])),
            'ml_late_list': [float(x) for x in v['ml_late_ber']],
            'cma_late_mean': float(np.mean(v['cma_late_ber'])),
            'cma_late_list': [float(x) for x in v['cma_late_ber']],
            'oracle_mean': float(np.mean(v['oracle_ber'])),
            'oracle_list': [float(x) for x in v['oracle_ber']],
            'test_late_rot_deg': float(v['test_late_rot_deg']),
            'n_seeds': len(v['ml_late_ber']),
        }
    return summary


# ─── Q3: 失效机制对照 ───────────────────────────────────────

def run_q3(N=N_Q2, n_seeds=5):
    """Q3: 失效机制对照 A/B/C.

    对照 A: 训练覆盖更大 SOP 角度 — 用 SOP_RATE_TRAIN 更大的数据训练,
            测试同 SOP_RATE_TEST 漂移下 ML 是否不崩.
            具体: train 用 SOP=4e-7 的前段(累积旋转小), 但把训练数据 SOP
            旋转范围人为扩到 [0, 2π] (周期性 wrap), 让 ML 见过全角度.
            实现: 训练前对 (rX,rY) 做 theta_train = arange(N_train)·sop_random,
            使训练段覆盖更大旋转. 简化: 用 SOP_RATE_TRAIN=4e-6(10×) 训练,
            test 用 SOP_RATE_TEST=4e-7.
    对照 B: 周期重训练 — test 段每 1/4 用前 1/4 重训练 ML.
    对照 C: 非 ML 固定 LS-FIR (纯线性回归前馈) 复现 N=5M 失效.
    """
    print("\n" + "=" * 70)
    print(f"Q3: 失效机制对照 (N={N}, {n_seeds} seeds)")
    print("=" * 70)
    alpha, beta = cfg.turbulence.as_dict()[TURB]

    ckpt = _load_ckpt('q3')
    results = ckpt.get('results', {
        'A_train_wider_sop': [], 'A_baseline': [],
        'B_retrain': [], 'B_baseline': [],
        'C_ls_fir': [], 'C_baseline': [],
    })

    late_s, late_e = test_late_slice(N)

    # ─── 对照 A: 训练覆盖更大 SOP 角度 ───
    print("\n--- 对照 A: 训练覆盖更大 SOP 角度 ---")
    print("  训练用 SOP_RATE_TRAIN=4e-6 (10× test), test 用 SOP=4e-7")
    print("  预期: 若机制='训练 SOP 范围不足', A 使 ML 不崩")
    SOP_TRAIN = 4e-6  # 10× test, 训练段 SOP 累积旋转 10× 大
    while len(results['A_train_wider_sop']) < n_seeds:
        seed = len(results['A_train_wider_sop'])
        seed_int = 3000 + seed
        t0 = time.time()
        # 生成训练信道 (大 SOP) 和测试信道 (正常 SOP) — 用同一 seed 的符号但不同 SOP
        rng = np.random.default_rng(seed_int)
        tau_c = cfg.gg_time.tau_c_from_fg(F_G)
        h = gg_time_envelope(N, alpha, beta, tau_c, block=BLOCK, t_s=T_S,
                             method='gar', seed=seed_int)
        sX, _ = gen_qpsk(N, rng)
        sY, _ = gen_qpsk(N, rng)
        nv = 1.0 / (2 * GAMMA_BAR)
        noise_X = rng.standard_normal(N) + 1j * rng.standard_normal(N)
        noise_Y = rng.standard_normal(N) + 1j * rng.standard_normal(N)

        n_train = int(N * ML_TRAIN_FRAC)
        # 训练段用大 SOP, 测试段用正常 SOP (连续, 但 train 段 SOP 速率 10×)
        theta = np.empty(N)
        theta[:n_train] = SOP_TRAIN * np.arange(n_train)  # train 大 SOP
        # test 段从 train 末角度继续, 用正常 SOP 速率
        theta[n_train:] = theta[n_train-1] + SOP_RATE * np.arange(1, N - n_train + 1)
        cos_t = np.cos(theta)
        sin_t = np.sin(theta)
        rX = np.sqrt(h) * (cos_t * sX + sin_t * sY) + np.sqrt(nv) * noise_X
        rY = np.sqrt(h) * (-sin_t * sX + cos_t * sY) + np.sqrt(nv) * noise_Y

        zX_ml, zY_ml, _, ml_res = run_ml_trial(rX, rY, sX, sY)
        ml_late_A = compute_ber_phase_corrected(
            zX_ml[late_s:late_e], sX[late_s:late_e], 0.0)
        results['A_train_wider_sop'].append(float(ml_late_A))

        # baseline: 正常 SOP 全段 (跟 Q1 N=5M 一致)
        rX2, rY2, sX2, sY2, h2, th2 = gen_channel(
            N, alpha, beta, F_G, SOP_RATE, seed_int)
        zX_ml2, _, _, _ = run_ml_trial(rX2, rY2, sX2, sY2)
        ml_late_base = compute_ber_phase_corrected(
            zX_ml2[late_s:late_e], sX2[late_s:late_e], 0.0)
        results['A_baseline'].append(float(ml_late_base))

        _save_ckpt('q3', {'results': results})
        print(f"  seed{seed}: A_wider={ml_late_A:.4f} baseline={ml_late_base:.4f} "
              f"({time.time()-t0:.0f}s)", flush=True)

    # ─── 对照 B: 周期重训练 ───
    print("\n--- 对照 B: 周期重训练 (每 test 段 1/4 用前 1/4 重训练) ---")
    print("  预期: 若机制='权重需随 SOP 更新', B 解决")
    while len(results['B_retrain']) < n_seeds:
        seed = len(results['B_retrain'])
        seed_int = 4000 + seed
        t0 = time.time()
        rX, rY, sX, sY, h, theta = gen_channel(
            N, alpha, beta, F_G, SOP_RATE, seed_int)

        # 把 test 段分 4 份, 每份用前一份重训练
        n_train = int(N * ML_TRAIN_FRAC)
        n_test = N - n_train
        q_len = n_test // 4  # 每份长度
        zX_full = np.zeros(N, dtype=complex)
        # 初始训练 (前 train_frac)
        train_end = n_train
        ml = MLChannelEqualizer(**ML_PARAMS)
        ml.train(rX[:train_end], rY[:train_end], sX[:train_end], sY[:train_end],
                 val_split=0.2, verbose=False)

        for qi in range(4):
            qs = n_train + qi * q_len
            qe = qs + q_len if qi < 3 else N
            res = ml.equalize(rX[qs:qe], rY[qs:qe])
            zX_full[qs:qe] = res['zX'].flatten()
            # 用本段重训练下一段 (除最后一段)
            if qi < 3:
                ml = MLChannelEqualizer(**ML_PARAMS)
                ml.train(rX[qs:qe], rY[qs:qe], sX[qs:qe], sY[qs:qe],
                         val_split=0.2, verbose=False)

        ml_late_B = compute_ber_phase_corrected(
            zX_full[late_s:late_e], sX[late_s:late_e], 0.0)
        results['B_retrain'].append(float(ml_late_B))

        # baseline: 跟 A 共用 baseline (同 seed 正常 ML) — 复用 A_baseline[seed]
        if seed < len(results['A_baseline']):
            results['B_baseline'].append(results['A_baseline'][seed])
        else:
            rX2, rY2, sX2, sY2, _, _ = gen_channel(
                N, alpha, beta, F_G, SOP_RATE, seed_int)
            zX_ml2, _, _, _ = run_ml_trial(rX2, rY2, sX2, sY2)
            results['B_baseline'].append(float(
                compute_ber_phase_corrected(zX_ml2[late_s:late_e],
                                            sX2[late_s:late_e], 0.0)))

        _save_ckpt('q3', {'results': results})
        print(f"  seed{seed}: B_retrain={ml_late_B:.4f} "
              f"baseline={results['B_baseline'][-1]:.4f} ({time.time()-t0:.0f}s)",
              flush=True)

    # ─── 对照 C: 非 ML 固定 LS-FIR (纯线性回归前馈) ───
    print("\n--- 对照 C: 非 ML 固定 LS-FIR (纯线性回归前馈) ---")
    print("  预期: 复现主控 N=5M LS-FIR BER≈0.50 失效 (固定权重通病性)")
    while len(results['C_ls_fir']) < n_seeds:
        seed = len(results['C_ls_fir'])
        seed_int = 5000 + seed
        t0 = time.time()
        rX, rY, sX, sY, h, theta = gen_channel(
            N, alpha, beta, F_G, SOP_RATE, seed_int)

        # LS-FIR: 用训练段最小二乘解 2×2 蝶形 FIR 系数, 固定前馈推理
        ls_ber = run_ls_fir_trial(rX, rY, sX, sY, N, late_s, late_e)
        results['C_ls_fir'].append(float(ls_ber))

        if seed < len(results['A_baseline']):
            results['C_baseline'].append(results['A_baseline'][seed])
        else:
            zX_ml2, _, _, _ = run_ml_trial(rX, rY, sX, sY)
            results['C_baseline'].append(float(
                compute_ber_phase_corrected(zX_ml2[late_s:late_e],
                                            sX[late_s:late_e], 0.0)))

        _save_ckpt('q3', {'results': results})
        print(f"  seed{seed}: C_ls_fir={ls_ber:.4f} "
              f"baseline={results['C_baseline'][-1]:.4f} ({time.time()-t0:.0f}s)",
              flush=True)

    return results


def run_ls_fir_trial(rX, rY, sX, sY, N, late_s, late_e):
    """非 ML 固定 LS-FIR: 最小二乘解 2×2 蝶形 FIR, 前馈推理.

    跟 ML 同结构 (wxx/wxy 蝶形 zX = wxx∗rX + wxy∗rY), 但系数用闭式最小二乘
    (非 CNN 训练), 固定后前馈推理. 用于测"固定权重方法通病性".
    """
    L = N_TAP
    half = L // 2
    n_train = int(N * ML_TRAIN_FRAC)
    # 训练段: 构建 X 矩阵 (滑动窗口), 解最小二乘 w = pinv(X) @ sX
    from numpy.lib.stride_tricks import sliding_window_view
    rX_train = rX[:n_train]
    rY_train = rY[:n_train]
    sX_train = sX[:n_train]
    # 训练段窗口 (n_train-L+1, L)
    rXw = sliding_window_view(rX_train, L)
    rYw = sliding_window_view(rY_train, L)
    # 拼成 (n, 2L) 实值 [rX_real, rX_imag, rY_real, rY_imag]
    n_samp = rXw.shape[0]
    Xmat = np.empty((n_samp, 4 * L))
    Xmat[:, :L] = rXw.real
    Xmat[:, L:2*L] = rXw.imag
    Xmat[:, 2*L:3*L] = rYw.real
    Xmat[:, 3*L:] = rYw.imag
    # 目标 sX (中心对齐): sX[half : half+n_samp]
    y_real = sX_train[half:half+n_samp].real
    y_imag = sX_train[half:half+n_samp].imag
    # 最小二乘 (实值拆分): [wxx_r, wxx_i, wxy_r, wxy_i]
    # zX = wxx∗rX + wxy∗rY = (wxx_r+j wxx_i)∗(rX_r+j rX_i) + ...
    # 重排: z_real = wxx_r·rX_r - wxx_i·rX_i + wxy_r·rY_r - wxy_i·rY_i
    #      z_imag = wxx_r·rX_i + wxx_i·rX_r + wxy_r·rY_i + wxy_i·rY_r
    # 构建增广矩阵让 LS 解 4L 系数
    A = np.empty((2 * n_samp, 4 * L))
    A[:n_samp, :L] = Xmat[:, :L]            # wxx_r · rX_r
    A[:n_samp, L:2*L] = -Xmat[:, L:2*L]     # -wxx_i · rX_i
    A[:n_samp, 2*L:3*L] = Xmat[:, 2*L:3*L]  # wxy_r · rY_r
    A[:n_samp, 3*L:] = -Xmat[:, 3*L:]       # -wxy_i · rY_i
    A[n_samp:, :L] = Xmat[:, L:2*L]         # wxx_r · rX_i
    A[n_samp:, L:2*L] = Xmat[:, :L]         # wxx_i · rX_r
    A[n_samp:, 2*L:3*L] = Xmat[:, 3*L:]     # wxy_r · rY_i
    A[n_samp:, 3*L:] = Xmat[:, 2*L:3*L]     # wxy_i · rY_r
    y = np.concatenate([y_real, y_imag])
    w, *_ = np.linalg.lstsq(A, y, rcond=None)

    # 前馈推理全段
    rXw_full = sliding_window_view(rX, L)
    rYw_full = sliding_window_view(rY, L)
    n_full = rXw_full.shape[0]
    Xf = np.empty((n_full, 4 * L))
    Xf[:, :L] = rXw_full.real
    Xf[:, L:2*L] = rXw_full.imag
    Xf[:, 2*L:3*L] = rYw_full.real
    Xf[:, 3*L:] = rYw_full.imag
    Af = np.empty((2 * n_full, 4 * L))
    Af[:n_full, :L] = Xf[:, :L]
    Af[:n_full, L:2*L] = -Xf[:, L:2*L]
    Af[:n_full, 2*L:3*L] = Xf[:, 2*L:3*L]
    Af[:n_full, 3*L:] = -Xf[:, 3*L:]
    Af[n_full:, :L] = Xf[:, L:2*L]
    Af[n_full:, L:2*L] = Xf[:, :L]
    Af[n_full:, 2*L:3*L] = Xf[:, 3*L:]
    Af[n_full:, 3*L:] = Xf[:, 2*L:3*L]
    z_out = Af @ w
    zX_ls = z_out[:n_full] + 1j * z_out[n_full:]
    # 中心对齐补齐 (前 half 个无窗口输出, 填 0)
    zX_full = np.zeros(N, dtype=complex)
    zX_full[half:half + n_full] = zX_ls

    return compute_ber_phase_corrected(
        zX_full[late_s:late_e], sX[late_s:late_e], 0.0)


# ─── 主入口 ─────────────────────────────────────────────────

def main():
    t0 = time.time()
    print("=" * 70)
    print("PROMPT-010: ML 长序列失效边界诊断")
    print("=" * 70)
    print(f"参数: f_G={F_G}, SOP={SOP_RATE} (1krad/s), turb={TURB}, "
          f"γ̄={GAMMA_BAR} (20dB), QPSK, tap={N_TAP}")
    print(f"Q1: N∈{N_SWEEP} × {N_SEEDS} seeds")
    print(f"Q2: SOP∈{SOP_SWEEP} × {N_SEEDS_Q2} seeds (N={N_Q2})")
    print(f"工作目录: {SIM_DIR}")

    # Q1 优先 (最关键)
    print(f"\n[Q1] ML 长序列失效多 seed 多 N 确认...")
    t1 = time.time()
    q1 = run_q1()
    print(f"  Q1 耗时: {time.time()-t1:.0f}s")

    # Q2: SOP 边界
    print(f"\n[Q2] ML 失效 SOP 边界...")
    t2 = time.time()
    q2 = run_q2()
    print(f"  Q2 耗时: {time.time()-t2:.0f}s")

    # Q3: 机制对照
    print(f"\n[Q3] 失效机制对照 A/B/C...")
    t3 = time.time()
    q3 = run_q3()
    print(f"  Q3 耗时: {time.time()-t3:.0f}s")

    # 汇总保存
    out = {
        'meta': {
            'direction': 'Q-CMA-FADE',
            'step': 'PROMPT-010 ML 长序列失效边界诊断',
            'timestamp': time.strftime('%Y-%m-%dT%H:%M:%S'),
            'elapsed_s': time.time() - t0,
            'params': {
                'mod': MOD, 'turbulence': TURB,
                'f_g': F_G, 'sop_rate': SOP_RATE,
                'gamma_bar': GAMMA_BAR, 'n_tap': N_TAP,
                'n_sweep_q1': N_SWEEP, 'n_seeds_q1': N_SEEDS,
                'sop_sweep_q2': SOP_SWEEP, 'n_seeds_q2': N_SEEDS_Q2,
                'ml_train_frac': ML_TRAIN_FRAC,
            },
            'tl20_hypothesis': {
                'H1': 'ML 长序列失效真实, 机制=固定权重跟不上 test 段 SOP 漂移. '
                      '预测 N↑→ML test-late BER↑, r>0.7',
                'H2': 'ML 不失效, 主控单 seed 是 seed-bias. 预测各 N BER<0.01',
                'falsification': 'H1 要求 BER vs SOP 旋转角 r>0.7; 否则 H2',
            },
        },
        'q1_ml_vs_n': q1,
        'q2_ml_vs_sop': q2,
        'q3_mechanism': q3,
    }
    out_path = RESULTS_DIR / 'ml_long_seq_failure_results.json'
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2, ensure_ascii=False, default=str)
    print(f"\n结果已保存: {out_path}")
    print(f"总耗时: {time.time()-t0:.0f}s")
    return out


if __name__ == '__main__':
    main()
