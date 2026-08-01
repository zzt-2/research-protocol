"""P11 PILOT_EFFICIENT_STRUCTURED_BUTTERFLY_FIR — methods library.

研究对象（按真实实现命名）：linear Butterfly FIR（4 复 FIR = 8 实 Conv1d, bias=False,
无 activation/normalization; common/_ml_equalizer.py:104）。监督训练学 FIR 抽头系数。

公平数据合同（用户指令 §五）：pilot 位置预先冻结；只有 pilot 位置的 TX 符号可进入
训练/估计；payload TX truth 只用于最终计分；禁止把整个 payload truth 送入 Adam/LS/RLS；
所有方法共享 realization / pilot 位置 / payload / eval window。

baseline ladder（用户指令 §六）:
  B0  full-label Adam       — 前 50% 连续全段标签 (性能锚点, 50% overhead)
  B1  sparse-label Adam     — 同结构 Adam, 只用 pilot 位置标签 (同 B2 pilot 位置)
  B2  batch complex LS      — 同 tap/pilot, 闭式最小二乘 (sliding-window lstsq)
  B3  pilot RLS / LMS       — pilot 位置递归最小二乘 (在线) + pilot-LMS 对照
  B4  blind CMA             — Godard 1980 with-z, zero pilot (报告性能差)

候选（用户指令 §八, 最多三个, 单一主机制）:
  C1  LS-init + 少量 pilot Adam refinement
  C2  regularized structured 2x2 Toeplitz LS (Tikhonov)
  C3  pilot-init + receiver-visible confidence-gated DD refinement

身份溯源见 p11_entry_gate.md (file:line). 不复制 VAE ELBO (Qin 核心), 不重开 D032.
"""
import numpy as np
import torch
from numpy.lib.stride_tricks import sliding_window_view

# 复用既有资产 (不改 common/, 只 import)
import sys, os
_SIM_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if _SIM_ROOT not in sys.path:
    sys.path.insert(0, _SIM_ROOT)
from common._ml_equalizer import ButterflyCNNEqualizer2x2  # noqa: E402

N_TAP = 11  # 与 P05 / LS-FIR 对齐 (params.py provenance, ml_long_seq_failure.py)


# ─── pilot 位置生成 (公平合同: 冻结, 所有方法共享) ─────────────

def freeze_pilot_positions(N, pilot_frac, seed):
    """生成冻结的 pilot 位置索引 (均匀间隔 + 轻微抖动, 可复现).

    pilot_frac = pilot 数 / N. 返回排序后的唯一 pilot 索引数组。
    约束: pilot 位置 c 满足 half <= c < N-half (sliding-window 中心对齐合法)。
    公平合同: 这是所有 B1/B2/B3/C1/C2/C3 共享的"已知 TX 符号"集合。
    """
    rng = np.random.default_rng(seed)
    n_pilot = max(int(round(N * pilot_frac)), 1)
    half = N_TAP // 2
    grid = np.linspace(half, N - half - 1, n_pilot).astype(int)
    jitter = rng.integers(-1, 2, size=n_pilot)
    grid = np.clip(grid + jitter, half, N - half - 1)
    return np.unique(grid)


# ─── 构建 pilot 位置的实值增广设计矩阵 (公平合同核心) ──────────

def _augmented_rows(rX_win, rY_win):
    """把 (n_p, L) 复窗口拆成实值增广矩阵 A 块 (2*n_p, 4L).

    复数卷积 z = wxx∗rX + wxy∗rY, w=w_r+j w_i, r=r_r+j r_i:
      z_real = wxx_r·rX_r - wxx_i·rX_i + wxy_r·rY_r - wxy_i·rY_i
      z_imag = wxx_r·rX_i + wxx_i·rX_r + wxy_r·rY_i + wxy_i·rY_r
    系数向量 w_vec = [wxx_r, wxx_i, wxy_r, wxy_i] (各 L 维, 共 4L)。
    返回 A (2*n_p, 4L) 使得 A @ w_vec = [z_real; z_imag] @ pilot。
    (逻辑同 run_ls_fir_trial ml_long_seq_failure.py:643-657)
    """
    n_p, L = rX_win.shape
    X = np.empty((n_p, 4 * L))
    X[:, :L] = rX_win.real
    X[:, L:2 * L] = rX_win.imag
    X[:, 2 * L:3 * L] = rY_win.real
    X[:, 3 * L:] = rY_win.imag
    A = np.empty((2 * n_p, 4 * L))
    A[:n_p, :L] = X[:, :L]
    A[:n_p, L:2 * L] = -X[:, L:2 * L]
    A[:n_p, 2 * L:3 * L] = X[:, 2 * L:3 * L]
    A[:n_p, 3 * L:] = -X[:, 3 * L:]
    A[n_p:, :L] = X[:, L:2 * L]
    A[n_p:, L:2 * L] = X[:, :L]
    A[n_p:, 2 * L:3 * L] = X[:, 3 * L:]
    A[n_p:, 3 * L:] = X[:, 2 * L:3 * L]
    return A


def _pilot_windows(rX, rY, pilot_idx):
    """取 pilot 中心的复窗口 (n_p, L) 对 rX/rY。边界 pilot 已由 freeze 保证合法。"""
    half = N_TAP // 2
    rXw = np.array([rX[c - half:c + half + 1] for c in pilot_idx])
    rYw = np.array([rY[c - half:c + half + 1] for c in pilot_idx])
    return rXw, rYw


def fit_butterfly_ls(rX, rY, sX, sY, pilot_idx, ridge=0.0):
    """batch complex LS: 解 2x2 蝶形 FIR (zX 用 wxx/wxy; zY 用 wyx/wyy).

    只用 pilot 位置的 TX 标签 (公平合同)。ridge>0 时 Tikhonov 正则 (C2 候选)。
    返回 dict(wxx,wxy,wyx,wyy 各 (L,) 复系数, n_pilot)。
    """
    rXw, rYw = _pilot_windows(rX, rY, pilot_idx)
    A = _augmented_rows(rXw, rYw)  # (2*n_p, 4L)
    n_p = len(pilot_idx)
    coeffs = {'n_pilot': n_p}
    for key, s_target in (('xy', sX), ('yy', sY)):
        y = np.concatenate([s_target[pilot_idx].real, s_target[pilot_idx].imag])
        if ridge > 0:
            AtA = A.T @ A + ridge * np.eye(4 * N_TAP)
            w = np.linalg.solve(AtA, A.T @ y)
        else:
            w, *_ = np.linalg.lstsq(A, y, rcond=None)
        w_a = w[:N_TAP] + 1j * w[N_TAP:2 * N_TAP]   # wxx 或 wyx
        w_b = w[2 * N_TAP:3 * N_TAP] + 1j * w[3 * N_TAP:]  # wxy 或 wyy
        if key == 'xy':
            coeffs['wxx'], coeffs['wxy'] = w_a, w_b
        else:
            coeffs['wyx'], coeffs['wyy'] = w_a, w_b
    return coeffs


def apply_butterfly(rX, rY, coeffs):
    """前馈推理: 用冻结复系数做 2x2 蝶形 FIR 均衡全段 (与 ML equalize 同口径)."""
    rXw = sliding_window_view(rX, N_TAP)  # (N-L+1, L)
    rYw = sliding_window_view(rY, N_TAP)
    zX = rXw @ coeffs['wxx'] + rYw @ coeffs['wxy']
    zY = rXw @ coeffs['wyx'] + rYw @ coeffs['wyy']
    half = N_TAP // 2
    # pad 前后 half 保持 N 长 (边界复制), 与 ML 输出同长对齐
    zX = np.concatenate([np.full(half, zX[0]), zX, np.full(half, zX[-1])])[:len(rX)]
    zY = np.concatenate([np.full(half, zY[0]), zY, np.full(half, zY[-1])])[:len(rY)]
    return zX, zY


# ─── B3: pilot-position RLS (在线递归, 同 pilot 位置) ───────────

def fit_pilot_rls(rX, rY, sX, sY, pilot_idx, lam=0.999, delta=1.0):
    """RLS 解 2x2 蝶形 FIR (zX 的 wxx/wxy; zY 的 wyx/wyy). pilot 位置顺序更新.

    标准 RLS (Haykin): P_0=delta^-1 I; 每 pilot:
      k = P x / (lam + x^H P x); w += k(d - x^H w); P = (P - k x^H P)/lam
    x = 实值增广 (4L,); d = Re/Im(sX@pilot)。两目标(Re/Im)共享 P, 分别更新 w 分量。
    delta=1.0 (非 1e2) 避免 P 初值过大致数值不稳定 (smoke test 暴露 NaN)。
    lam<1 遗忘因子 (在线跟踪); lam=1.0 退化为 batch LS。
    """
    rXw, rYw = _pilot_windows(rX, rY, pilot_idx)
    A = _augmented_rows(rXw, rYw)  # (2*n_p, 4L)
    n_p = len(pilot_idx)
    coeffs = {'n_pilot': n_p}
    for key, s_target in (('xy', sX), ('yy', sY)):
        P = np.eye(4 * N_TAP) / delta
        w = np.zeros(4 * N_TAP)
        y = np.concatenate([s_target[pilot_idx].real, s_target[pilot_idx].imag])
        for i in range(n_p):
            xr = A[i]
            xi = A[n_p + i]
            for x, d in ((xr, y[i]), (xi, y[n_p + i])):
                Px = P @ x
                denom = lam + x @ Px
                if not np.isfinite(denom) or abs(denom) < 1e-30:
                    continue
                k = Px / denom
                w = w + k * (d - x @ w)
                P = (P - np.outer(k, Px)) / lam
                if not np.isfinite(P).all():
                    break
        w_a = w[:N_TAP] + 1j * w[N_TAP:2 * N_TAP]
        w_b = w[2 * N_TAP:3 * N_TAP] + 1j * w[3 * N_TAP:]
        if key == 'xy':
            coeffs['wxx'], coeffs['wxy'] = w_a, w_b
        else:
            coeffs['wyx'], coeffs['wyy'] = w_a, w_b
    return coeffs


# ─── B1: sparse-label Adam (同 ButterflyCNN 结构, 只用 pilot 位置标签) ──

def fit_sparse_label_adam(rX, rY, sX, sY, pilot_idx, lr=5e-3, n_epochs=30,
                          device='cpu', seed=0):
    """同 ButterflyCNNEqualizer2x2 结构, Adam 训练但只用 pilot 位置标签.

    公平合同: 与 B2 LS 共享同一 pilot 位置集合。每个 pilot 贡献一个中心符号方程
    (窗口中心抽头输出 vs 该 pilot 的 TX 符号)。与 B0 唯一差是标签预算 (pilot vs 连续前缀)。
    """
    torch.manual_seed(seed)
    np.random.seed(seed)
    model = ButterflyCNNEqualizer2x2(n_tap=N_TAP).to(device)
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    crit = torch.nn.MSELoss()
    half = N_TAP // 2
    rXw, rYw = _pilot_windows(rX, rY, pilot_idx)

    def to_real2(c):
        t = torch.tensor(c, dtype=torch.complex64, device=device)
        return torch.cat([t.real.unsqueeze(1), t.imag.unsqueeze(1)], dim=1)
    rX_in = to_real2(rXw)   # (n_p, 2, L)
    rY_in = to_real2(rYw)
    sX_t = torch.tensor(sX[pilot_idx], dtype=torch.complex64, device=device)
    sY_t = torch.tensor(sY[pilot_idx], dtype=torch.complex64, device=device)

    for _ in range(n_epochs):
        opt.zero_grad()
        zX, zY = model(rX_in, rY_in)        # (n_p, L) 各窗口输出序列
        zXc = zX[:, half]                    # 中心抽头符号 (n_p,)
        zYc = zY[:, half]
        loss = crit(zXc.real, sX_t.real) + crit(zXc.imag, sX_t.imag) \
            + crit(zYc.real, sY_t.real) + crit(zYc.imag, sY_t.imag)
        loss.backward()
        opt.step()
    coeffs = _extract_butterfly_coeffs(model)
    coeffs['n_pilot'] = len(pilot_idx)
    return coeffs


def _extract_butterfly_coeffs(model):
    """从 ButterflyCNNEqualizer2x2 的 Conv1d 权重提取复系数 (中心抽头序).

    Conv1d weight shape (1,1,L), padding='same'+reflect → 权重即 FIR 系数 (顺序 [w[0]..w[L-1]])。
    ComplexFIRConv1d: z_real=conv_RR(r_real)-conv_RI(r_imag); z_imag=conv_RR(r_imag)+conv_RI(r_real)
    → wxx = conv_RR + j conv_RI (等价复卷积核)。同 MLChannelEqualizer 推理口径。
    """
    coeffs = {}
    for name in ['wxx', 'wxy', 'wyx', 'wyy']:
        fir = getattr(model, name)
        wr = fir.conv_RR.weight.detach().cpu().numpy().flatten()  # (L,)
        wi = fir.conv_RI.weight.detach().cpu().numpy().flatten()
        coeffs[name] = wr + 1j * wi
    return coeffs


# ─── B0: full-label Adam (复用 MLChannelEqualizer, 前 50% 连续标签) ──

def fit_full_label_adam(rX, rY, sX, sY, train_frac=0.5, lr=5e-3, batch=1024,
                        n_epochs=15, device='cpu', seed=0, val_split=0.2):
    """B0 性能锚点: 前 50% 连续全段标签 (现有训练方式, ml_long_seq_failure.py).

    返回 (zX, zY, overhead) — overhead = train_frac (50% 标签开销)。
    """
    from common._ml_equalizer import MLChannelEqualizer
    torch.manual_seed(seed)
    np.random.seed(seed)
    ml = MLChannelEqualizer(n_tap=N_TAP, lr=lr, batch_size=batch,
                            n_epochs=n_epochs, device=device)
    nt = int(len(rX) * train_frac)
    ml.train(rX[:nt], rY[:nt], sX[:nt], sY[:nt], val_split=val_split, verbose=False)
    out = ml.equalize(rX, rY)
    return out['zX'], out['zY'], train_frac


# ─── B4: blind CMA (Godard 1980 with-z, zero pilot) ─────────────

class _GodardWithZCMA:
    """corrected standard CMA 2x2 butterfly (Godard 1980, with z).

    Godard-with-z 更新: w += μ·(R²−|z|²)·z·r* (含 z 因子, 非 _cma.py scalar-error)。
    D036 冻结此为合法经典 CMA comparator (prompt019_mu_compress_mve.py:96)。
    P11 复用同梯度身份, block-end 更新, μ 独立 dev 调谐。
    """

    def __init__(self, n_tap=N_TAP, mu=1e-3, R2=1.0, block_size=64):
        self.n_tap = n_tap
        self.mu = mu
        self.R2 = R2
        self.block_size = block_size
        c = n_tap // 2
        self.wxx = np.zeros(n_tap, dtype=complex); self.wxx[c] = 1.0
        self.wyy = np.zeros(n_tap, dtype=complex); self.wyy[c] = 1.0
        self.wxy = np.zeros(n_tap, dtype=complex)
        self.wyx = np.zeros(n_tap, dtype=complex)

    def equalize(self, rX, rY):
        N = len(rX); L = self.n_tap; half = L // 2
        rXw = sliding_window_view(rX, L); rYw = sliding_window_view(rY, L)
        zX = np.zeros(N, dtype=complex); zY = np.zeros(N, dtype=complex)
        n_valid = N - L + 1; bs = self.block_size; n_blk = n_valid // bs
        for blk in range(n_blk):
            s, e = blk * bs, blk * bs + bs
            rXb, rYb = rXw[s:e], rYw[s:e]
            zxb = rXb @ self.wxx + rYb @ self.wxy
            zyb = rXb @ self.wyx + rYb @ self.wyy
            idx = s + half
            zX[idx:idx + bs] = zxb; zY[idx:idx + bs] = zyb
            eX = self.R2 - np.abs(zxb) ** 2
            eY = self.R2 - np.abs(zyb) ** 2
            self.wxx += self.mu * np.mean((eX * zxb)[:, None] * np.conj(rXb), axis=0)
            self.wxy += self.mu * np.mean((eX * zxb)[:, None] * np.conj(rYb), axis=0)
            self.wyx += self.mu * np.mean((eY * zyb)[:, None] * np.conj(rXb), axis=0)
            self.wyy += self.mu * np.mean((eY * zyb)[:, None] * np.conj(rYb), axis=0)
        return zX, zY


def fit_blind_cma(rX, rY, mu=1e-3, block_size=64):
    """B4: blind Godard-with-z CMA, zero pilot overhead (报告性能差)."""
    cma = _GodardWithZCMA(mu=mu, block_size=block_size)
    zX, zY = cma.equalize(rX, rY)
    return zX, zY, 0.0  # zero pilot overhead


# ─── 候选 (用户指令 §八, 单一主机制, 不复制 VAE / 不重开 D032) ────

def cand_c1_ls_init_adam_refine(rX, rY, sX, sY, pilot_idx, refine_steps=50,
                                lr=1e-3, device='cpu', seed=0):
    """C1: LS-init + 少量 pilot Adam refinement.

    主机制 = 闭式 LS 初始化减少 Adam 收敛所需标签数。须证明不是"多跑几步 Adam":
    调用方应与 B1 同总 Adam 步数预算对比 (refine_steps 计入)。
    LS 系数 → 载入 ButterflyCNNEqualizer2x2 中心抽头权重 → pilot 位置 Adam 微调。
    """
    torch.manual_seed(seed); np.random.seed(seed)
    ls_c = fit_butterfly_ls(rX, rY, sX, sY, pilot_idx, ridge=0.0)
    model = ButterflyCNNEqualizer2x2(n_tap=N_TAP).to(device)
    _load_butterfly_coeffs(model, ls_c)
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    crit = torch.nn.MSELoss()
    half = N_TAP // 2
    rXw, rYw = _pilot_windows(rX, rY, pilot_idx)

    def to_real2(c):
        t = torch.tensor(c, dtype=torch.complex64, device=device)
        return torch.cat([t.real.unsqueeze(1), t.imag.unsqueeze(1)], dim=1)
    rX_in = to_real2(rXw); rY_in = to_real2(rYw)
    sX_t = torch.tensor(sX[pilot_idx], dtype=torch.complex64, device=device)
    sY_t = torch.tensor(sY[pilot_idx], dtype=torch.complex64, device=device)
    for _ in range(refine_steps):
        opt.zero_grad()
        zX, zY = model(rX_in, rY_in)   # (n_p, L)
        zXc = zX[:, half]; zYc = zY[:, half]   # 中心抽头符号
        loss = (crit(zXc.real, sX_t.real) + crit(zXc.imag, sX_t.imag) +
                crit(zYc.real, sY_t.real) + crit(zYc.imag, sY_t.imag))
        loss.backward(); opt.step()
    coeffs = _extract_butterfly_coeffs(model)
    coeffs['n_pilot'] = len(pilot_idx); coeffs['refine_steps'] = refine_steps
    coeffs['main_mechanism'] = 'closed_form_LS_init_reduces_labels'
    return coeffs


def cand_c2_structured_toeplitz_ls(rX, rY, sX, sY, pilot_idx, ridge):
    """C2: regularized structured 2x2 Toeplitz LS (Tikhonov on butterfly structure).

    主机制 = 显式利用 Butterfly/FIR 结构约束 (Tikhonov 正则), 非通用 LS。
    ridge 由 dev 调谐 (调用方传入)。区别 B2 的 ridge=0。
    """
    coeffs = fit_butterfly_ls(rX, rY, sX, sY, pilot_idx, ridge=ridge)
    coeffs['main_mechanism'] = 'explicit_butterfly_structure_Tikhonov'
    coeffs['ridge'] = ridge
    return coeffs


def cand_c3_pilot_init_confidence_gated_dd(rX, rY, sX, sY, pilot_idx,
                                           mu_dd=1e-3, conf_thresh=0.3,
                                           block_size=64):
    """C3: pilot-init + receiver-visible confidence-gated DD refinement.

    主机制 = confidence-gated decision-directed。pilot warm-start (B2 LS 系数)
    → 之后每 block: receiver slicer decision + confidence (|R²-|z|²|) 决定是否更新。
    伪标签只来自 receiver decision + 合法 confidence, **不使用 payload truth**。
    """
    coeffs0 = fit_butterfly_ls(rX, rY, sX, sY, pilot_idx, ridge=0.0)
    wxx, wxy, wyx, wyy = (coeffs0['wxx'].copy(), coeffs0['wxy'].copy(),
                          coeffs0['wyx'].copy(), coeffs0['wyy'].copy())
    R2 = 1.0  # QPSK Godard radius (与 B4 同)
    N = len(rX); L = N_TAP; half = L // 2
    rXw = sliding_window_view(rX, L); rYw = sliding_window_view(rY, L)
    zX = np.zeros(N, dtype=complex); zY = np.zeros(N, dtype=complex)
    n_valid = N - L + 1; n_blk = n_valid // block_size
    n_updated = 0
    pilot_set = set(int(p) for p in pilot_idx)
    for blk in range(n_blk):
        s, e = blk * block_size, blk * block_size + block_size
        rXb, rYb = rXw[s:e], rYw[s:e]
        zxb = rXb @ wxx + rYb @ wxy
        zyb = rXb @ wyx + rYb @ wyy
        idx = s + half
        zX[idx:idx + block_size] = zxb; zY[idx:idx + block_size] = zyb
        # pilot block (含 pilot 位置): 用真 pilot label (合法, 同 B2)
        block_range = range(s + half, s + half + block_size)
        has_pilot = any((b in pilot_set) for b in block_range)
        if has_pilot:
            # pilot block: 维持 pilot LS 解 (不 DD), 与 B2 一致
            continue
        # non-pilot block: confidence-gated DD (receiver slicer, 无 TX truth)
        conf = 1.0 / (1.0 + np.abs(R2 - np.abs(zxb) ** 2))  # receiver-visible
        gate = conf.mean()
        if gate < conf_thresh:
            continue  # 低置信不更新
        # receiver slicer decision (QPSK, 4-quadrant) 作伪标签
        dxb = _qpsk_slicer(zxb); dyb = _qpsk_slicer(zyb)
        # LMS on slicer error (decision-directed, Godard-with-z 梯度身份)
        eX = R2 - np.abs(zxb) ** 2; eY = R2 - np.abs(zyb) ** 2
        wxx += mu_dd * np.mean((eX * zxb)[:, None] * np.conj(rXb), axis=0)
        wxy += mu_dd * np.mean((eX * zxb)[:, None] * np.conj(rYb), axis=0)
        wyx += mu_dd * np.mean((eY * zyb)[:, None] * np.conj(rXb), axis=0)
        wyy += mu_dd * np.mean((eY * zyb)[:, None] * np.conj(rYb), axis=0)
        n_updated += 1
    coeffs = {'wxx': wxx, 'wxy': wxy, 'wyx': wyx, 'wyy': wyy,
              'n_pilot': len(pilot_idx), 'n_dd_blocks_updated': n_updated,
              'conf_thresh': conf_thresh, 'main_mechanism':
              'receiver_confidence_gated_decision_directed'}
    return coeffs


def _qpsk_slicer(z):
    """QPSK 4-quadrant slicer (receiver decision, 不用 TX truth)."""
    return (np.sign(z.real) + 1j * np.sign(z.imag)) / np.sqrt(2)


def _load_butterfly_coeffs(model, coeffs):
    """把复 LS 系数载入 ButterflyCNNEqualizer2x2 的 Conv1d 权重 (中心抽头序)."""
    half = N_TAP // 2
    with torch.no_grad():
        for name in ['wxx', 'wxy', 'wyx', 'wyy']:
            fir = getattr(model, name)
            w = coeffs[name]
            fir.conv_RR.weight.copy_(torch.from_numpy(w.real).float().view(1, 1, -1))
            fir.conv_RI.weight.copy_(torch.from_numpy(w.imag).float().view(1, 1, -1))
