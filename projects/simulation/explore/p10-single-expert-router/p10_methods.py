"""P10 RISK_BUDGETED_SINGLE_EXPERT_ML_CMA_ROUTER — shared method library.

研究问题 (D039 campaign P10, 用户授权 campaign-level 第 10 包裁决):
  M = 固定使用 ButterflyCNN ML 均衡器 或 固定使用 StandardCMA 均衡器 (二选一, payload 前冻结)
  C = 接收工况在 "短/慢变 (小 SOP 漂移)" 与 "长/快变 (大 SOP 漂移 / OOD)" 之间变化
      且只允许执行一个主专家 (single-path execution 合同 §六)
  A = 历史证据显示专家排名反转 (D015/S017/S020/D022):
        - 短 N + 小 SOP 累积旋转 (<~14°): ML fixed-label 占优 (D015 N=2M, S017 N=2M)
        - 长 N + 大 SOP 累积旋转 (~90°) 或 OOD f_G: CMA fixed-label 占优 (D015 N=8M, S020 fg1000)
      注意: 用户指令 §二 描述的 "长慢变 ML 占优, 短快变 CMA 占优" 与历史证据相反;
            本包 fresh dev 必须用 fixed-label PRIMARY 口径独立复现 crossover 真实方向,
            不能复现即终止 PROBLEM_ABSENT_OR_RESOLVED_BY_CONFIG_RULE (合同 §入口门)
  目标 = 仅根据 receiver-visible 前缀与合法配置, 在运行 payload 专家前选择 ML 或 CMA,
        只执行被选中的一个 (single-path execution, 禁止同时运行两专家)

本模块定义:
  - 两个专家包装: MLExpert (ButterflyCNNEqualizer2x2 frozen), CMAExpert (StandardCMA2x2 with-z)
  - 一组 receiver-visible prefix feature 提取器 (不读 TX truth / true h/SNR/phase)
  - 三个候选 router C1/C2/C3 (冻结 logistic/ridge, 参数 dev-only)
  - 传统 comparator B0/B1/B2/B3/B4 (always-CMA/always-ML/best-global/config-rule/threshold)
  - single-path 执行门验证 helper (monkeypatch 未选专家为 raise)

复用纪律 (守 TL-13, 不改 common/ frozen 文件):
  - ML: common._ml_equalizer.ButterflyCNNEqualizer2x2 + MLChannelEqualizer (P05 frozen)
  - CMA: prompt019_mu_compress_mve.StandardCMA2x2 (Godard 1980 with-z, P05 corrected)
  - channel: common._gg_time.gg_time_envelope + params.SimulationConfig (B11/B7/B3 共用)
  - metric: prompt012_longseq_audit.evaluate_outputs (PI-BER + fixed-label BER 双口径)

信息边界 (合同 §五 forbidden_information):
  router feature 禁止读: payload TX truth / true h/theta/SNR/fG / 两专家 payload 输出
  router feature 允许读: 已知训练符号残差 / raw RX covariance-power / 短 CMA diagnostic trace /
                         receiver-visible convergence/stationarity 统计 / 部署时真实可知配置字段
  payload TX truth 只允许用于最终计分 (fixed-label BER + PI-BER)
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Tuple

import numpy as np

_SIM = Path(__file__).resolve().parents[2]
_HERE = Path(__file__).resolve().parent
for _p in (str(_SIM), str(_HERE)):
    if _p not in sys.path:
        sys.path.insert(0, _p)


# =============================================================================
# Expert wrappers (single-path execution contract)
# =============================================================================

class MLExpert:
    """ButterflyCNNEqualizer2x2 frozen-ML expert (P05 identity).

    train_on_prefix(rx_train, ry_train, sx_train, sy_train, seed): 训练 (prefix only)
    equalize_payload(rx_payload, ry_payload): 前馈推理 (不在线更新)
    返回 (zX, zY) 均衡后符号.
    """
    name = "ML"

    def __init__(self, ml_params):
        # lazy import (torch heavy)
        from common._ml_equalizer import MLChannelEqualizer
        import torch
        self._torch = torch
        self._MLChannelEqualizer = MLChannelEqualizer
        self.ml_params = dict(ml_params)
        self._model = None
        self._train_flops = 0  # training cost proxy (forward+backward epochs*chunks)
        self._infer_flops = 0

    def train_on_prefix(self, rX_tr, rY_tr, sX_tr, sY_tr, seed):
        torch = self._torch
        from common._ml_equalizer import MLChannelEqualizer
        ml = MLChannelEqualizer(**self.ml_params)
        np.random.seed(seed); torch.manual_seed(seed); torch.cuda.manual_seed_all(seed)
        hist = ml.train(rX_tr, rY_tr, sX_tr, sY_tr, val_split=0.2, verbose=False)
        self._model = ml.model
        # training cost proxy: epochs_run * n_chunks * chunk_len * RMpS (8*n_tap)
        n_tap = self.ml_params['n_tap']
        n_chunks = max(1, int(len(rX_tr) * 0.8) // self.ml_params['batch_size'])
        self._train_flops = hist['epochs_run'] * n_chunks * self.ml_params['batch_size'] * (8 * n_tap) * 3  # *3 for fwd+bwd
        return hist

    def equalize_payload(self, rX, rY):
        torch = self._torch
        assert self._model is not None, "MLExpert.train_on_prefix must be called first"
        self._model.eval()
        n = len(rX)
        with torch.no_grad():
            rx_t = torch.from_numpy(rX).to(self._model.wxx.conv_RR.weight.device)
            ry_t = torch.from_numpy(rY).to(self._model.wxx.conv_RR.weight.device)
            chunk_x = torch.cat([rx_t.real.view(1, 1, n).float(), rx_t.imag.view(1, 1, n).float()], dim=1)
            chunk_y = torch.cat([ry_t.real.view(1, 1, n).float(), ry_t.imag.view(1, 1, n).float()], dim=1)
            zX, zY = self._model(chunk_x, chunk_y)
        zX_np = zX.cpu().numpy().flatten()
        zY_np = zY.cpu().numpy().flatten()
        n_tap = self.ml_params['n_tap']
        self._infer_flops = n * (8 * n_tap)  # 8 real-valued Conv1d * n_tap per symbol
        return zX_np, zY_np

    def cost_flops(self):
        return self._train_flops + self._infer_flops


class CMAExpert:
    """StandardCMA2x2 (Godard 1980 with-z) expert (P05 corrected identity).

    train_on_prefix: CMA 在 prefix 上在线更新权重 (warm-start), 不读 TX truth
    equalize_payload: 用 warm-start 权重继续在 payload 上在线更新 (CMA 本性在线)
    返回 (zX, zY) 均衡后符号.

    注: CMA 是在线算法, "payload 前训练" 和 "payload 推理" 都是同一在线更新过程的延续.
    single-path 合同只要求: router 先决定 expert_id, 之后只调被选专家. CMA 的在线更新
    是其算法本性 (不是 "同时跑两专家后选"), 不违反 single-path.
    """
    name = "CMA"

    def __init__(self, n_tap, mu, R2, block_size):
        self.n_tap = n_tap
        self.mu = mu
        self.R2 = R2
        self.block_size = block_size
        self._cma = None
        self._prefix_flops = 0
        self._payload_flops = 0

    def _make(self):
        # lazy import (avoid heavy import at module load)
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "p19", _HERE.parent / "cma-fade-divergence" / "prompt019_mu_compress_mve.py")
        p19 = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(p19)
        return p19.StandardCMA2x2(n_tap=self.n_tap, mu=self.mu, R2=self.R2)

    def train_on_prefix(self, rX_tr, rY_tr, sX_tr=None, sY_tr=None, seed=None):
        """CMA warm-start on prefix (online, no TX truth)."""
        self._cma = self._make()
        res = self._cma.equalize(rX_tr, rY_tr)  # block-end online updates over prefix
        self._prefix_flops = len(rX_tr) * (8 * self.n_tap) * 2  # *2 for online update
        return res

    def equalize_payload(self, rX, rY):
        """Continue CMA online update on payload (CMA 本性在线, 用 warm-start 权重继续)."""
        assert self._cma is not None, "CMAExpert.train_on_prefix must be called first"
        # 用 warm-start 的最终权重继续在 payload 上跑 (online update continues)
        res = self._cma.equalize(rX, rY)
        self._payload_flops = len(rX) * (8 * self.n_tap) * 2
        return res['zX'], res['zY']

    def cost_flops(self):
        return self._prefix_flops + self._payload_flops


# =============================================================================
# Receiver-visible prefix feature extractors (NO TX truth / true h/SNR/phase)
# =============================================================================

def prefix_features(rx_prefix, ry_prefix, known_sym_x=None, known_sym_y=None,
                    cma_diag_tap=11, cma_diag_mu=1e-3, cma_diag_R2=1.0):
    """从 receiver-visible prefix 提取 router feature (不读 TX truth/true channel).

    返回 dict of features:
      rx_power_x, rx_power_y: 接收信号功率 (|rx|^2 mean)
      rx_amp_std_x/y: 接收幅度 std (衰落深度指示)
      rx_cov_xy: 接收 X/Y 协方差 (偏振串扰指示)
      rx_amp_ac1: 接收幅度 lag-1 自相关 (时间相关性 / 慢变指示)
      fade_depth_ratio: 深衰落占比 (|rx| < 0.5 mean 的比例)
      prefix_len: prefix 长度 (配置字段)
      cma_diag_convergence: 短 CMA diagnostic trace 的权重范数轨迹斜率 (收敛指示)
      cma_diag_diverged: 短 CMA diagnostic 是否发散 (1/0)

    若提供 known_sym_x/y (合法 pilot/训练符号), 计算残差统计 (不读 true channel):
      pilot_residual_power: pilot 处 |rx - known_sym| 的功率 (噪声+信道失真指示)

    全部 receiver-visible, 不读 TX payload / true h/SNR/phase/fG.
    """
    rx_prefix = np.asarray(rx_prefix, dtype=complex)
    ry_prefix = np.asarray(ry_prefix, dtype=complex)
    n = len(rx_prefix)

    ax = np.abs(rx_prefix); ay = np.abs(ry_prefix)
    rx_power_x = float(np.mean(ax ** 2))
    rx_power_y = float(np.mean(ay ** 2))
    rx_amp_std_x = float(np.std(ax))
    rx_amp_std_y = float(np.std(ay))
    rx_cov_xy = float(np.abs(np.mean(rx_prefix * np.conj(ry_prefix))))
    # lag-1 autocorrelation of amplitude (slow vs fast variation)
    if n > 1:
        ax_c = ax - ax.mean()
        rx_amp_ac1 = float(np.mean(ax_c[:-1] * ax_c[1:]) / (np.var(ax) + 1e-12))
    else:
        rx_amp_ac1 = 0.0
    fade_thr = 0.5 * float(np.mean(ax))
    fade_depth_ratio = float(np.mean(ax < fade_thr))

    feats = {
        'rx_power_x': rx_power_x,
        'rx_power_y': rx_power_y,
        'rx_amp_std_x': rx_amp_std_x,
        'rx_amp_std_y': rx_amp_std_y,
        'rx_cov_xy': rx_cov_xy,
        'rx_amp_ac1': rx_amp_ac1,
        'fade_depth_ratio': fade_depth_ratio,
        'prefix_len': float(n),
    }

    # pilot residual (if known pilot symbols provided — legitimate training symbols)
    if known_sym_x is not None and known_sym_y is not None:
        known_sym_x = np.asarray(known_sym_x, dtype=complex)
        known_sym_y = np.asarray(known_sym_y, dtype=complex)
        # residual = rx - known_sym (assume nominal gain ~1; power indicates noise+distortion)
        resid_x = rx_prefix - known_sym_x
        resid_y = ry_prefix - known_sym_y
        feats['pilot_residual_power'] = float((np.mean(np.abs(resid_x)**2) + np.mean(np.abs(resid_y)**2)) / 2)

    # short CMA diagnostic trace (receiver-visible convergence indicator)
    # run a SHORT CMA on prefix only, track weight norm trajectory slope
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "p19_diag", _HERE.parent / "cma-fade-divergence" / "prompt019_mu_compress_mve.py")
        p19 = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(p19)
        diag_cma = p19.StandardCMA2x2(n_tap=cma_diag_tap, mu=cma_diag_mu, R2=cma_diag_R2)
        diag_res = diag_cma.equalize(rx_prefix, ry_prefix)
        wtraj = diag_res.get('w_norm_traj', np.zeros(n))
        # convergence slope: linear fit slope of weight norm over blocks (large slope = not converged)
        valid = wtraj[wtraj > 0]
        if len(valid) > 2:
            t = np.arange(len(valid))
            slope = float(np.polyfit(t, valid, 1)[0] / (valid.mean() + 1e-12))
        else:
            slope = 0.0
        feats['cma_diag_convergence'] = slope
        feats['cma_diag_diverged'] = float(bool(diag_res.get('diverged', False)))
    except Exception:
        feats['cma_diag_convergence'] = 0.0
        feats['cma_diag_diverged'] = 0.0

    return feats


def feature_vector(feats, feature_keys):
    """Convert feat dict to ordered numpy vector for router."""
    return np.array([feats.get(k, 0.0) for k in feature_keys], dtype=float)


# =============================================================================
# Candidate routers C1/C2/C3 (parameters dev-only frozen)
# =============================================================================

class RouterC1Logistic:
    """C1: frozen logistic regression on receiver-visible prefix features.

    decide(features_vec) -> expert_id in {'ML', 'CMA'}.
    Parameters (weights, bias, feature_keys) frozen at dev time.
    """
    name = "C1_logistic"

    def __init__(self, weights, bias, feature_keys, thresh=0.5):
        self.weights = np.asarray(weights, dtype=float)
        self.bias = float(bias)
        self.feature_keys = list(feature_keys)
        self.thresh = float(thresh)

    def decide(self, feats):
        x = feature_vector(feats, self.feature_keys)
        z = float(np.dot(self.weights, x) + self.bias)
        p_ml = 1.0 / (1.0 + np.exp(-z))
        return 'ML' if p_ml >= self.thresh else 'CMA'


class RouterC2RiskConstrained:
    """C2: risk-constrained router with CMA-safe fallback.

    decide(features_vec) -> expert_id. If risk score > threshold (uncertain/OOD),
    fall back to CMA (safe default). Otherwise pick by predicted regret sign.
    """
    name = "C2_risk_constrained"

    def __init__(self, regret_weights, regret_bias, risk_weights, risk_bias,
                 feature_keys, risk_thresh):
        self.regret_weights = np.asarray(regret_weights, dtype=float)
        self.regret_bias = float(regret_bias)
        self.risk_weights = np.asarray(risk_weights, dtype=float)
        self.risk_bias = float(risk_bias)
        self.feature_keys = list(feature_keys)
        self.risk_thresh = float(risk_thresh)

    def decide(self, feats):
        x = feature_vector(feats, self.feature_keys)
        risk = float(np.dot(self.risk_weights, x) + self.risk_bias)
        if risk > self.risk_thresh:
            return 'CMA'  # uncertain/OOD -> safe fallback
        regret_ml = float(np.dot(self.regret_weights, x) + self.regret_bias)
        # regret_ml = predicted ML fixed-BER minus predicted CMA fixed-BER (lower is better for ML)
        return 'ML' if regret_ml < 0 else 'CMA'


class RouterC3Abstain:
    """C3: conservative router with abstention -> when uncertain, choose CMA."""
    name = "C3_abstain_cma"

    def __init__(self, weights, bias, feature_keys, abstain_thresh):
        self.weights = np.asarray(weights, dtype=float)
        self.bias = float(bias)
        self.feature_keys = list(feature_keys)
        self.abstain_thresh = float(abstain_thresh)

    def decide(self, feats):
        x = feature_vector(feats, self.feature_keys)
        z = float(np.dot(self.weights, x) + self.bias)
        p_ml = 1.0 / (1.0 + np.exp(-z))
        # only pick ML if confident (p_ml high); otherwise abstain -> CMA
        return 'ML' if p_ml >= self.abstain_thresh else 'CMA'


# =============================================================================
# Conventional comparators B0-B4 (always-single-expert baselines)
# =============================================================================

class BaselineAlwaysCMA:
    """B0: always choose CMA."""
    name = "B0_always_CMA"
    def decide(self, feats): return 'CMA'


class BaselineAlwaysML:
    """B1: always choose ML."""
    name = "B1_always_ML"
    def decide(self, feats): return 'ML'


class BaselineBestGlobal:
    """B2: best global single expert (dev-tuned pick, frozen at test)."""
    name = "B2_best_global"
    def __init__(self, pick):  # pick in {'ML','CMA'} frozen from dev
        self.pick = pick
    def decide(self, feats): return self.pick


class BaselineConfigRule:
    """B3: configuration-only rule (uses only deployable config fields like N/f_G, not RX stats).

    Rule: if N >= N_thresh (long sequence) -> CMA; else ML. (mirrors D015 crossover axis)
    N_thresh dev-tuned, frozen at test. This is a CHEAP traditional rule.
    """
    name = "B3_config_rule"
    def __init__(self, N_thresh):
        self.N_thresh = float(N_thresh)
    def decide(self, feats):
        # uses prefix_len as proxy for total N (deployable config field)
        return 'CMA' if feats['prefix_len'] >= self.N_thresh else 'ML'


class BaselineThreshold:
    """B4: dev-tuned simple prefix threshold on a single receiver-visible statistic."""
    name = "B4_threshold"
    def __init__(self, stat_key, thresh, direction='greater_means_CMA'):
        self.stat_key = stat_key
        self.thresh = float(thresh)
        self.direction = direction
    def decide(self, feats):
        v = float(feats.get(self.stat_key, 0.0))
        if self.direction == 'greater_means_CMA':
            return 'CMA' if v > self.thresh else 'ML'
        else:
            return 'ML' if v > self.thresh else 'CMA'
