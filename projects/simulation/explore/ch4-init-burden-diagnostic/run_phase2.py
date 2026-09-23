"""Phase-2 continuous-trajectory tracking arms (R031 tasks ③④, contract_phase2.yaml).

Continuous contract: GG block AR(1) via common/_gg_time (tau_c=1/(2*pi*f_G)),
SOP linear drift J(t)=expm(1j*theta(t)A)@J0 at 4e-7 rad/symbol, continuous
doppler/Wiener phase across the whole trajectory, T077 noise semantics.
Receiver chain (preamble LS / RDE / DA CPR / ambiguity / LLR / 20-iter decode)
is reused unmodified from the frozen modules; only the RDE initialization
differs per arm.  Truth (per-frame ideal demux of the PREVIOUS frame) enters
the ORC arm only.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from hashlib import sha256
from pathlib import Path
from typing import Any

import numpy as np
from scipy.linalg import expm

from run_diagnostic import (
    BR,
    CH4,
    RESULTS_ROOT,
    SC,
    _array_sha256,
    make_init_runner,
)
from common._gg_time import gg_time_envelope, gg_time_envelope_blockwise

PH2_BOOTSTRAP_SEED = 2026092302
PH2_BOOTSTRAP_RESAMPLES = 10000
T_S = 1.0 / 2.5e9
FRAME_TOTAL = 260
SOP_RATE_DEFAULT = 4.0e-7
F_G_DEFAULT = 100.0
PH2_ARMS = ("B0star", "ORC", "EMA", "RLS", "C40", "EMA0")

LAYOUTS = {
    "dev": {"info": (70000, 70255), "traj": (80000, 80007)},
    "eval": {"info": (71000, 71511), "traj": (81000, 81015)},
}


# ── statistics (phase-2 seed) ────────────────────────────────────────────────


def exact_binomial_two_sided(wins: int, losses: int) -> tuple[float, float]:
    import math

    d = wins + losses
    if d == 0:
        return 1.0, 1.0
    lo = min(wins, losses)
    tail = sum(math.comb(d, i) for i in range(0, lo + 1)) / 2**d
    return min(1.0, 2 * tail), tail


def paired_fer_contrast(frames: list[dict[str, Any]], arm_hi: str, arm_lo: str) -> dict[str, Any]:
    a = np.array([f["arms"][arm_hi]["fer"] for f in frames], dtype=np.int64)
    b = np.array([f["arms"][arm_lo]["fer"] for f in frames], dtype=np.int64)
    n = len(frames)
    rng = np.random.default_rng(PH2_BOOTSTRAP_SEED)
    diffs = np.empty(PH2_BOOTSTRAP_RESAMPLES)
    for k in range(PH2_BOOTSTRAP_RESAMPLES):
        idx = rng.integers(0, n, size=n)
        diffs[k] = a[idx].mean() - b[idx].mean()
    wins = int(np.sum((a == 1) & (b == 0)))
    losses = int(np.sum((a == 0) & (b == 1)))
    p2, p1 = exact_binomial_two_sided(wins, losses)
    return {
        "contrast": f"{arm_hi}_minus_{arm_lo}",
        "n": n,
        "point": float(a.mean() - b.mean()),
        "ci95": [float(np.percentile(diffs, 2.5)), float(np.percentile(diffs, 97.5))],
        "wins_hi": wins,
        "losses_hi": losses,
        "discordant": wins + losses,
        "exact_two_sided_p": p2,
        "exact_one_sided_p": p1,
    }


def paired_ber_contrast(frames: list[dict[str, Any]], arm_hi: str, arm_lo: str) -> dict[str, Any]:
    a = np.array([f["arms"][arm_hi]["bit_errors"] for f in frames], dtype=np.int64)
    b = np.array([f["arms"][arm_lo]["bit_errors"] for f in frames], dtype=np.int64)
    n = len(frames)
    rng = np.random.default_rng(PH2_BOOTSTRAP_SEED)
    diffs = np.empty(PH2_BOOTSTRAP_RESAMPLES)
    for k in range(PH2_BOOTSTRAP_RESAMPLES):
        idx = rng.integers(0, n, size=n)
        diffs[k] = (a[idx].sum() - b[idx].sum()) / (n * 1024.0)
    return {
        "contrast": f"{arm_hi}_minus_{arm_lo}",
        "n": n,
        "point_ber_diff": float((a.sum() - b.sum()) / (n * 1024.0)),
        "bit_diff_total": int(a.sum() - b.sum()),
        "ci95": [float(np.percentile(diffs, 2.5)), float(np.percentile(diffs, 97.5))],
    }


# ── continuous trajectory generator ─────────────────────────────────────────


def random_traceless_hermitian(rng: np.random.Generator) -> np.ndarray:
    a, b, c = rng.standard_normal(3)
    H = np.array([[a, b + 1j * c], [-b + 1j * c, -a]], dtype=np.complex128)
    return H / np.linalg.norm(H)


def continuous_phase(n_total: int, cell: dict[str, Any], rng: np.random.Generator) -> np.ndarray:
    """doppler_phase formula evaluated continuously over the whole trajectory."""
    k = np.arange(n_total)
    return (
        2 * np.pi * cell["residual_frequency_hz"] * k * T_S
        + np.pi * cell["frequency_slope_hz_per_s"] * (k * T_S) ** 2
        + np.sqrt(2 * np.pi * cell["linewidth_hz"] * T_S)
        * np.cumsum(rng.standard_normal(n_total))
    )


def generate_trajectory(
    codec: Any,
    *,
    traj_seed: int,
    info_seeds: list[int],
    f_g_hz: float,
    sop_rate: float,
    manifest: dict[str, Any],
) -> list[dict[str, Any]]:
    cell = manifest["cell"]
    n_frames = len(info_seeds)
    n_total = n_frames * FRAME_TOTAL
    tau_c = 1.0 / (2.0 * np.pi * f_g_hz)
    # GG block chain at 256-symbol AR(1) spacing, frame-aligned per the T077
    # convention (amendment v1.1): frame t uses chain entries (2t, 2t+1) for its
    # first 256 / last 4 symbols.  At rho=0 this reproduces the frozen layout
    # (two iid blocks, transition confined to the final 4 symbols); the drifted
    # global tiling exposed a deep->strong mid-frame transition that diverges
    # the frozen plain RDE (implementation-probe evidence, worker log).
    gg_blocks = gg_time_envelope_blockwise(
        2 * n_frames,
        cell["turbulence_alpha"],
        cell["turbulence_beta"],
        tau_c,
        block=cell["gamma_gamma_block"],
        t_s=T_S,
        method="gar",
        seed=int(traj_seed),
    )
    rng = np.random.default_rng(int(traj_seed) + 90000)
    j0 = CH4.random_su2(rng)
    gen = random_traceless_hermitian(rng)
    phi = continuous_phase(n_total, cell, rng)
    noise_var = 10.0 ** (-cell["snr_db"] / 10.0)
    ch4_tx = CH4.orthogonal_pilots(manifest["ch4"]["acquisition_pilots"])
    frames: list[dict[str, Any]] = []
    for t, info_seed in enumerate(info_seeds):
        sl = slice(t * FRAME_TOTAL, (t + 1) * FRAME_TOTAL)
        gg_frame = np.concatenate(
            (
                np.full(cell["gamma_gamma_block"], gg_blocks[2 * t]),
                np.full(FRAME_TOTAL - cell["gamma_gamma_block"], gg_blocks[2 * t + 1]),
            )
        )
        scalar = np.sqrt(gg_frame) * np.exp(1j * phi[sl])
        theta = sop_rate * (t * FRAME_TOTAL + FRAME_TOTAL / 2.0)
        jones = expm(1j * theta * gen) @ j0
        info_rng = np.random.default_rng(np.random.SeedSequence([int(info_seed), 77, 5]))
        info = info_rng.integers(0, 2, size=(1, 1024), dtype=np.uint8)
        coded = np.asarray(codec.encode(info), dtype=np.uint8)
        mapping = SC.build_dp_symbol_frame(coded[0])
        transmitted = np.concatenate((ch4_tx, mapping["symbols"]), axis=1)
        pre_noise = jones @ (transmitted * scalar[None, :])
        noise = np.sqrt(noise_var / 2.0) * (
            rng.standard_normal(pre_noise.shape) + 1j * rng.standard_normal(pre_noise.shape)
        )
        received = pre_noise + noise
        config = BR.BridgeConfig.correctness_fixture(
            seed=int(info_seed),
            n_symbols=cell["observation_symbols_per_polarization"],
            observation_stop=cell["observation_symbols_per_polarization"],
            snr_db=cell["snr_db"],
            turbulence_alpha=cell["turbulence_alpha"],
            turbulence_beta=cell["turbulence_beta"],
            gamma_gamma_block=cell["gamma_gamma_block"],
            f_residual_hz=cell["residual_frequency_hz"],
            f_dot_hz_per_s=cell["frequency_slope_hz_per_s"],
            linewidth_hz=cell["linewidth_hz"],
            ch4_pilot_count=manifest["ch4"]["acquisition_pilots"],
            pilot_indices=tuple(int(v) for v in SC.PILOT_INDICES),
            pilot_label_shift=manifest["ch3"]["polarization_1_label_shift"],
            scope=("PHASE2_CONTINUOUS_TRAJECTORY", "DIAGNOSTIC_ONLY", "NO_PARAMETER_TUNING"),
            cell_id=f"phase2-cont-fg{f_g_hz:g}",
            window_id=f"traj{int(traj_seed)}-f{t}",
            config_id="continuous-tracking.phase2.v1",
            source_id="R031-task3-4/D055/D056",
        )
        receiver = BR.ReceiverVisibleInput(
            rx=received[:, ch4_tx.shape[1] :],
            ch4_pilot_rx=received[:, : ch4_tx.shape[1]],
            ch4_pilot_tx=ch4_tx,
            pilot_indices=SC.PILOT_INDICES.copy(),
            pilot_symbols=mapping["symbols"][:, SC.PILOT_INDICES].copy(),
            pilot_labels=mapping["point_labels"][:, SC.PILOT_INDICES].copy(),
            known_mask=mapping["known_mask"].copy(),
            observation_stop=cell["observation_symbols_per_polarization"],
            config=config,
        )
        w_ideal = CH4.pilot_ls_demux(
            jones @ (ch4_tx * scalar[: ch4_tx.shape[1]]), ch4_tx
        )
        frames.append(
            {
                "traj_index": t,
                "info_seed": int(info_seed),
                "receiver": receiver,
                "info": info,
                "truth": {
                    "jones": jones,
                    "scalar": scalar,
                    "gg": gg_frame,
                    "w_ideal": w_ideal,
                },
                "physical": {
                    "received_observation_sha256": _array_sha256(receiver.rx),
                    "codeword_sha256": _array_sha256(coded[0].astype(np.uint8)),
                },
            }
        )
    return frames


# ── trajectory arm state machine ────────────────────────────────────────────


class TrackerState:
    """Cross-frame deployable state + oracle prior bookkeeping.

    v1.2: all cross-frame combination happens in the common-phase-canonical
    domain (W <- W*exp(j*angle(det W)/2), det becomes real-positive).  The
    continuous contract advances the common channel phase by ~0.653 rad/frame
    (1 MHz residual x 260 symbols x 0.4 ns); averaging phase-rotated phasors
    collapses the magnitude (round-1 dev diagnosis: EMA/RLS/C40-strong FER
    0.69-0.93 while phase-free arms stayed ~0.12).  RDE updates are exactly
    radial (z_i phase is invariant) and DA CPR removes constant per-pol phase,
    so canonicalization costs nothing and restores the Jones/gain tracking
    semantics the contract intends (phase belongs to Ch3).
    """

    def __init__(self, *, beta: float, lam_rls: float, lam_c40: float):
        self.beta = float(beta)
        self.lam_rls = float(lam_rls)
        self.lam_c40 = float(lam_c40)
        self.w_ema: np.ndarray | None = None
        self.rls_r: np.ndarray | None = None
        self.rls_p: np.ndarray | None = None
        self.w_c40: np.ndarray | None = None
        self.prev_w_ideal: np.ndarray | None = None
        self.ref: np.ndarray | None = None

    @staticmethod
    def canon(w: np.ndarray) -> np.ndarray:
        """Remove the common channel phase: det becomes real-positive.

        w ~ e^{-j*phi}*U (U phase-free) => angle(det w) = -2*phi (mod 2*pi),
        so the factor is exp(-0.5j*angle(det w)) = e^{+j*phi}.
        """
        d = np.linalg.det(np.asarray(w, dtype=np.complex128))
        return np.asarray(w, dtype=np.complex128) * np.exp(-0.5j * np.angle(d))

    def _align(self, wc: np.ndarray) -> np.ndarray:
        """Resolve the +/-1 half-angle branch against the running reference.

        angle(det) wraps by 2pi as the common phase advances ~0.65 rad/frame,
        which would flip canonicalized matrices by -1 between adjacent frames
        and collapse any cross-frame average.
        """
        if self.ref is not None and np.real(np.trace(self.ref.conj().T @ wc)) < 0:
            return -wc
        return wc

    def frame_inits(self, receiver: Any) -> tuple[dict[str, np.ndarray], np.ndarray]:
        y = np.asarray(receiver.ch4_pilot_rx, dtype=np.complex128)
        x = np.asarray(receiver.ch4_pilot_tx, dtype=np.complex128)
        w0 = CH4.pilot_ls_demux(y, x)
        w0c = self._align(self.canon(w0))
        self.ref = w0c
        xy_c = self._align(self.canon(x @ y.conj().T))
        yy = y @ y.conj().T
        inits: dict[str, np.ndarray] = {"B0star": w0}
        inits["ORC"] = w0 if self.prev_w_ideal is None else self.prev_w_ideal
        if self.w_ema is None:
            self.w_ema = w0c.copy()
        else:
            self.w_ema = self.beta * self.w_ema + (1.0 - self.beta) * w0c
        inits["EMA"] = self.w_ema.copy()
        inits["EMA0"] = self.w_ema.copy()
        if self.rls_r is None:
            self.rls_r = yy.copy()
            self.rls_p = xy_c.copy()
        else:
            self.rls_r = self.lam_rls * self.rls_r + yy
            self.rls_p = self.lam_rls * self.rls_p + xy_c
        inits["RLS"] = self._align(
            self.canon(np.linalg.solve(self.rls_r.T, self.rls_p.T).T)
        )
        if self.w_c40 is None:
            self.w_c40 = w0c.copy()
        else:
            rhs = xy_c + self.lam_c40 * self.w_c40
            lhs = yy + self.lam_c40 * np.eye(2, dtype=np.complex128)
            self.w_c40 = self._align(self.canon(np.linalg.solve(lhs.T, rhs.T).T))
        inits["C40"] = self.w_c40.copy()
        return inits, w0

    def advance_oracle(self, w_ideal_t: np.ndarray) -> None:
        self.prev_w_ideal = self.canon(w_ideal_t)


def run_trajectory(
    codec: Any,
    frames: list[dict[str, Any]],
    *,
    mu: float,
    beta: float,
    lam_rls: float,
    lam_c40: float,
    arms: tuple[str, ...],
    manifest: dict[str, Any],
) -> list[dict[str, Any]]:
    n0 = 10.0 ** (-manifest["cell"]["snr_db"] / 10.0)
    arm_spec = BR.FrozenCh4Arm(
        arm_id=f"plain-rde-mu{mu:g}", mode="plain", mu=float(mu)
    )
    state = TrackerState(beta=beta, lam_rls=lam_rls, lam_c40=lam_c40)
    records: list[dict[str, Any]] = []
    for frame in frames:
        receiver = frame["receiver"]
        inits, w0 = state.frame_inits(receiver)
        w_ideal = frame["truth"]["w_ideal"]
        w_ideal_c = state._align(TrackerState.canon(w_ideal))
        arm_records: dict[str, Any] = {}
        init_errors: dict[str, float] = {}
        for name in arms:
            freeze = name == "EMA0"
            runner = make_init_runner(inits[name], freeze=freeze)
            bundle, compensated = BR.run_bridge_with_observation(
                receiver, arm_spec, ch4_runner=runner
            )
            if compensated.shape != (2, 256) or not np.all(np.isfinite(compensated)):
                raise RuntimeError(f"INVALID_TESTBED: phase-2 arm {name} observation invalid")
            llr = SC.build_b0_llr(compensated, nominal_complex_noise_power=n0)
            decoded, _receipt = codec.decode_fresh(llr["llr"])
            errors = int(np.count_nonzero(decoded != frame["info"]))
            arm_records[name] = {
                "bit_errors": errors,
                "fer": int(errors > 0),
                "decoder_input_sha256": llr["llr_sha256"],
            }
            init_errors[name] = float(
                np.linalg.norm(state._align(TrackerState.canon(inits[name])) - w_ideal_c)
            )
        state.advance_oracle(w_ideal)
        gg = frame["truth"]["gg"]
        records.append(
            {
                "info_seed": frame["info_seed"],
                "arms": arm_records,
                "init_frob_errors_vs_current_ideal": init_errors,
                "gg_stats": {
                    "obs_mean": float(np.mean(gg[4:])),
                    "block1": float(gg[0]),
                    "abs_scalar_pre_mean": float(np.mean(np.abs(frame["truth"]["scalar"][:4]))),
                },
                "physical": frame["physical"],
            }
        )
    return records


def run_layout(
    *,
    layout: str,
    f_g_hz: float,
    sop_rate: float,
    mu: float,
    beta: float,
    lam_rls: float,
    lam_c40: float,
    arms: tuple[str, ...],
    manifest: dict[str, Any],
    codec: Any,
) -> list[dict[str, Any]]:
    spec = LAYOUTS[layout]
    info_seeds = list(range(spec["info"][0], spec["info"][1] + 1))
    traj_seeds = list(range(spec["traj"][0], spec["traj"][1] + 1))
    frames_per_traj = len(info_seeds) // len(traj_seeds)
    all_records: list[dict[str, Any]] = []
    for i, traj_seed in enumerate(traj_seeds):
        chunk = info_seeds[i * frames_per_traj : (i + 1) * frames_per_traj]
        frames = generate_trajectory(
            codec,
            traj_seed=traj_seed,
            info_seeds=chunk,
            f_g_hz=f_g_hz,
            sop_rate=sop_rate,
            manifest=manifest,
        )
        records = run_trajectory(
            codec,
            frames,
            mu=mu,
            beta=beta,
            lam_rls=lam_rls,
            lam_c40=lam_c40,
            arms=arms,
            manifest=manifest,
        )
        for rec in records:
            rec["traj_seed"] = int(traj_seed)
        all_records.extend(records)
        print(f"[{layout} fg={f_g_hz:g}] trajectory {i+1}/{len(traj_seeds)} done", flush=True)
    return all_records


# ── tuning / eval / sensitivity drivers ─────────────────────────────────────


def _save(data: dict[str, Any], name: str) -> None:
    from common import save_results

    RESULTS_ROOT.mkdir(parents=True, exist_ok=True)
    save_results(data, str(RESULTS_ROOT / name), f"init-burden-diagnostic:{name}")


def cmd_rho_check() -> int:
    manifest = SC.load_manifest()
    codec = SC._correctness().TargetApskCodec()
    records = run_layout(
        layout="eval",
        f_g_hz=1.0e7,
        sop_rate=0.0,
        mu=manifest["ch4"]["mu"],
        beta=0.9,
        lam_rls=0.99,
        lam_c40=2.0,
        arms=("B0star",),
        manifest=manifest,
        codec=codec,
    )
    fer = float(np.mean([r["arms"]["B0star"]["fer"] for r in records]))
    gg_mean = float(np.mean([r["gg_stats"]["obs_mean"] for r in records]))
    report = {
        "schema_version": "continuous-tracking.rho-check.v1",
        "f_g_hz": 1.0e7,
        "sop_rate": 0.0,
        "n_frames": len(records),
        "B0star_fer": fer,
        "gg_obs_mean": gg_mean,
        "accept_fer_band": [0.20, 0.36],
        "accept_gg_band": [0.9, 1.1],
    }
    report["gate"] = (
        "PASS" if (0.20 <= fer <= 0.36 and 0.9 <= gg_mean <= 1.1) else "FAIL"
    )
    _save(report, "phase2_rho_check.json")
    print(json.dumps(report, indent=2))
    return 0 if report["gate"] == "PASS" else 1


def _tune_grid(
    grid_name: str,
    values: list[float],
    *,
    apply_key: str,
    base: dict[str, float],
    manifest: dict[str, Any],
    codec: Any,
    arms_subset: tuple[str, ...],
) -> dict[str, Any]:
    rows = []
    for value in values:
        params = dict(base)
        params[apply_key] = value
        records = run_layout(
            layout="dev",
            f_g_hz=F_G_DEFAULT,
            sop_rate=SOP_RATE_DEFAULT,
            mu=params["mu"],
            beta=params["beta"],
            lam_rls=params["lam_rls"],
            lam_c40=params["lam_c40"],
            arms=arms_subset,
            manifest=manifest,
            codec=codec,
        )
        fer = float(np.mean([r["arms"][arms_subset[0]]["fer"] for r in records]))
        bits = int(sum(r["arms"][arms_subset[0]]["bit_errors"] for r in records))
        rows.append({apply_key: value, "fer": fer, "bit_errors": bits})
        print(f"[tune {grid_name}] {apply_key}={value:g}: FER={fer:.4f} bits={bits}", flush=True)
    best_index = min(
        range(len(rows)), key=lambda i: (rows[i]["fer"], rows[i]["bit_errors"], i)
    )
    best = rows[best_index]
    return {"grid": grid_name, "rows": rows, "selected": best, "tie_break": ["fer", "bit_errors", "first_in_grid"]}


def cmd_tune() -> int:
    manifest = SC.load_manifest()
    codec = SC._correctness().TargetApskCodec()
    base = {"mu": 1e-3, "beta": 0.9, "lam_rls": 0.99, "lam_c40": 2.0}
    mu_grid = _tune_grid(
        "mu_star", [5e-4, 1e-3, 3e-3, 1e-2], apply_key="mu", base=base,
        manifest=manifest, codec=codec, arms_subset=("B0star",),
    )
    base["mu"] = mu_grid["selected"]["mu"]
    beta_grid = _tune_grid(
        "beta", [0.5, 0.8, 0.9, 0.95, 0.98], apply_key="beta", base=base,
        manifest=manifest, codec=codec, arms_subset=("EMA",),
    )
    base["beta"] = beta_grid["selected"]["beta"]
    rls_grid = _tune_grid(
        "lam_rls", [0.9, 0.95, 0.99, 0.995, 0.999], apply_key="lam_rls", base=base,
        manifest=manifest, codec=codec, arms_subset=("RLS",),
    )
    base["lam_rls"] = rls_grid["selected"]["lam_rls"]
    c40_grid = _tune_grid(
        "lam_c40", [0.5, 2.0, 8.0, 32.0], apply_key="lam_c40", base=base,
        manifest=manifest, codec=codec, arms_subset=("C40",),
    )
    base["lam_c40"] = c40_grid["selected"]["lam_c40"]
    tuning = {
        "schema_version": "continuous-tracking.tuning.v1",
        "protocol": "dev 256 frames, FER then bit_errors then first-in-grid; frozen before eval",
        "mu_star": mu_grid,
        "beta": beta_grid,
        "lam_rls": rls_grid,
        "lam_c40": c40_grid,
        "frozen_hypers": base,
    }
    _save(tuning, "phase2_tuning.json")
    print("frozen hypers:", json.dumps(base))
    return 0


def summarize_phase2(records: list[dict[str, Any]], *, batch: str, f_g_hz: float) -> dict[str, Any]:
    arm_rates = {}
    for arm in PH2_ARMS:
        arm_rates[arm] = {
            "fer": float(np.mean([r["arms"][arm]["fer"] for r in records])),
            "fer_count": int(sum(r["arms"][arm]["fer"] for r in records)),
            "bit_errors": int(sum(r["arms"][arm]["bit_errors"] for r in records)),
            "ber": float(sum(r["arms"][arm]["bit_errors"] for r in records) / (len(records) * 1024)),
        }
    contrasts = {
        "B0star_minus_ORC": paired_fer_contrast(records, "B0star", "ORC"),
        "B0star_minus_EMA": paired_fer_contrast(records, "B0star", "EMA"),
        "B0star_minus_RLS": paired_fer_contrast(records, "B0star", "RLS"),
        "B0star_minus_C40": paired_fer_contrast(records, "B0star", "C40"),
        "C40_minus_EMA": paired_fer_contrast(records, "C40", "EMA"),
        "C40_minus_RLS": paired_fer_contrast(records, "C40", "RLS"),
        "EMA0_minus_EMA": paired_fer_contrast(records, "EMA0", "EMA"),
    }
    ber = {
        "B0star_minus_ORC": paired_ber_contrast(records, "B0star", "ORC"),
        "B0star_minus_C40": paired_ber_contrast(records, "B0star", "C40"),
        "C40_minus_EMA": paired_ber_contrast(records, "C40", "EMA"),
        "C40_minus_RLS": paired_ber_contrast(records, "C40", "RLS"),
    }
    # stratify by frame gg quartiles
    gg = np.array([r["gg_stats"]["obs_mean"] for r in records])
    q25, q50, q75 = np.quantile(gg, [0.25, 0.5, 0.75])
    edges = [-np.inf, q25, q50, q75, np.inf]
    strata = []
    for i in range(4):
        mask = (gg > edges[i]) & (gg <= edges[i + 1])
        sub = [r for r, m in zip(records, mask) if m]
        if not sub:
            continue
        row = {
            "stratum": f"Q{i+1}",
            "n": len(sub),
            "gg_range": [float(np.min(gg[mask])), float(np.max(gg[mask]))],
        }
        for arm in PH2_ARMS:
            row[f"fer_{arm}"] = float(np.mean([r["arms"][arm]["fer"] for r in sub]))
        strata.append(row)
    init_err = {}
    for arm in PH2_ARMS:
        values = [r["init_frob_errors_vs_current_ideal"][arm] for r in records]
        init_err[arm] = {"mean": float(np.mean(values)), "median": float(np.median(values))}
    # gates
    def status(c):
        lo, hi = c["ci95"]
        if lo > 0:
            return "alive"
        if hi < 0:
            return "significantly_worse"
        return "flat" if c["point"] < 0.005 else "gray"

    gate_a = status(contrasts["B0star_minus_ORC"])
    gate_b = (
        "PASS"
        if contrasts["C40_minus_EMA"]["ci95"][0] > 0
        and contrasts["C40_minus_RLS"]["ci95"][0] > 0
        else "FAIL"
    )
    verdict = (
        "STOP_TIME_AXIS_DEAD"
        if gate_a == "flat"
        else ("IDENTITY_COLLAPSE" if gate_b == "FAIL" else "C40_PASSES")
    )
    return {
        "batch": batch,
        "f_G_hz": f_g_hz,
        "n_frames": len(records),
        "arm_rates": arm_rates,
        "fer_contrasts": contrasts,
        "ber_contrasts": ber,
        "stratified": {"quantile_edges": [float(q25), float(q50), float(q75)], "strata": strata},
        "init_error_vs_current_ideal": init_err,
        "gates": {
            "gate_A_time_axis": gate_a,
            "gate_B_identity_C40_beats_EMA_and_RLS": gate_b,
            "verdict": verdict,
        },
    }


def cmd_run_eval(tag: str, f_g_hz: float, hypers: dict[str, float] | None) -> int:
    manifest = SC.load_manifest()
    codec = SC._correctness().TargetApskCodec()
    if hypers is None:
        tuning_path = RESULTS_ROOT / "phase2_tuning.json"
        tuning = json.loads(tuning_path.read_text(encoding="utf-8"))
        tuning.pop("_meta", None)
        hypers = tuning["frozen_hypers"]
    records = run_layout(
        layout="eval",
        f_g_hz=f_g_hz,
        sop_rate=SOP_RATE_DEFAULT,
        mu=hypers["mu"],
        beta=hypers["beta"],
        lam_rls=hypers["lam_rls"],
        lam_c40=hypers["lam_c40"],
        arms=PH2_ARMS,
        manifest=manifest,
        codec=codec,
    )
    raw = {
        "schema_version": f"continuous-tracking.{tag}.raw.v1",
        "contract": "explore/ch4-init-burden-diagnostic/contract_phase2.yaml (FROZEN_BEFORE_EXECUTION)",
        "manifest_hash": SC.manifest_sha256(),
        "f_G_hz": f_g_hz,
        "hypers": hypers,
        "arms": list(PH2_ARMS),
        "frames": records,
    }
    _save(raw, f"phase2_{tag}_raw.json")
    summary = summarize_phase2(records, batch=tag, f_g_hz=f_g_hz)
    summary["manifest_hash"] = raw["manifest_hash"]
    summary["hypers"] = hypers
    _save(summary, f"phase2_{tag}_summary.json")
    print(json.dumps(summary["gates"], indent=2))
    print(json.dumps(summary["arm_rates"], indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rho-check", action="store_true")
    parser.add_argument("--tune", action="store_true")
    parser.add_argument("--run-eval", action="store_true")
    parser.add_argument("--run-sensitivity", choices=["30", "300"])
    args = parser.parse_args()
    if args.rho_check:
        return cmd_rho_check()
    if args.tune:
        return cmd_tune()
    if args.run_eval:
        return cmd_run_eval("eval", F_G_DEFAULT, None)
    if args.run_sensitivity:
        return cmd_run_eval(f"sens{args.run_sensitivity}", float(args.run_sensitivity), None)
    parser.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
