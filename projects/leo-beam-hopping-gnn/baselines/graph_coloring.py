"""Graph Coloring baseline — adapted L04 MCMF-TS-GC for single satellite.

L04 (IEEE WCL 2026) combines min-cost max-flow, tabu search, and graph coloring
for multi-satellite beam hopping. This single-satellite adaptation:

1. Builds an interference graph from the static gain matrix
2. Runs HEAD (Highest-degree-first) greedy coloring to partition beams into
   non-interfering groups
3. Uses demand-aware greedy selection at each slot, preferring beams that
   don't interfere with already-selected beams
4. Applies lightweight local-search refinement (single-swap perturbation)
"""
import sys
sys.path.insert(0, "projects/leo-beam-hopping-gnn")

import numpy as np
from simulator.env import BHEnv
from simulator.channel import compute_interference_graph


class GraphColoringScheduler:
    """Interference-aware scheduler using graph coloring + demand-greedy selection."""

    def __init__(self, env: BHEnv):
        self.env = env
        self.N = env.N
        self.K = env.K

        # --- Phase 1: Interference graph (static) ---
        gain = env.gain_matrix
        avg_signal = np.diag(gain).mean()
        # Edge if off-diagonal gain exceeds 1% of average signal gain
        self.adj = (gain > 0.01 * avg_signal).astype(np.float64)
        np.fill_diagonal(self.adj, 0)
        self.adj_bool = self.adj > 0

        # --- Phase 2: HEAD greedy coloring (static) ---
        self.colors = self._head_coloring()
        self.n_colors = int(self.colors.max()) + 1
        self.color_groups = [np.where(self.colors == c)[0] for c in range(self.n_colors)]

        # Refinement state
        self._best_schedule = None
        self._best_total = -np.inf

    def _head_coloring(self) -> np.ndarray:
        """Highest-degree-first greedy coloring.

        1. Sort vertices by degree (descending).
        2. For each vertex, assign the smallest color not used by neighbors.
        """
        degrees = self.adj_bool.sum(axis=1)
        order = np.argsort(-degrees)  # highest degree first
        colors = np.full(self.N, -1, dtype=np.int32)

        for v in order:
            neighbor_colors = set(colors[self.adj_bool[v]].tolist())
            c = 0
            while c in neighbor_colors:
                c += 1
            colors[v] = c

        return colors

    def policy(self, env: BHEnv, obs: np.ndarray) -> np.ndarray:
        """Interference-aware demand-greedy beam selection.

        Greedily pick the K beams with highest demand+queue, but skip beams
        that interfere with already-selected beams. Fill remaining slots with
        highest-demand beams if we can't find K non-interfering ones.
        """
        # Reconstruct demand + queue from observation
        total_demand = (
            obs[:, 0] * env.config.demand_max_mbps
            + obs[:, 1] * env.config.queue_capacity_mbps
        )

        # Sort beams by demand descending
        priority = np.argsort(-total_demand)

        selected = []
        selected_set = set()
        skipped = []  # beams skipped due to interference, kept as fallback

        for beam in priority:
            if len(selected) >= self.K:
                break
            # Check interference with already selected beams
            interferes = any(self.adj_bool[beam, s] for s in selected)
            if not interferes:
                selected.append(beam)
                selected_set.add(beam)
            else:
                skipped.append(beam)

        # Fill remaining slots with highest-demand skipped beams (relaxation)
        for beam in skipped:
            if len(selected) >= self.K:
                break
            selected.append(beam)

        # Build action scores
        scores = np.full(self.N, -1e9, dtype=np.float64)
        for i, beam in enumerate(selected):
            scores[beam] = float(self.K - i)  # higher priority = higher score
        return scores

    def refine(self, episode_data: list) -> tuple:
        """Lightweight local-search refinement over a recorded schedule.

        For each slot, try swapping one selected beam with one unselected beam.
        Keep the swap if it improves the step reward. Runs 3 iterations.
        Returns (schedule, rewards, components_list).
        """
        schedule = [step['active_beams'].copy() for step in episode_data]
        # Initialize rewards and components from original episode
        step_info = []
        for t, step in enumerate(episode_data):
            _, tp, fa, intf = self._evaluate_selection(step, schedule[t])
            step_info.append({'reward': step['reward'], 'tp': tp, 'fa': fa, 'intf': intf})

        for iteration in range(3):
            improved = False
            for t in range(len(schedule)):
                active = list(schedule[t])
                active_set = set(active)
                inactive = [b for b in range(self.N) if b not in active_set]

                best_reward = step_info[t]['reward']
                best_active = active[:]
                best_components = step_info[t].copy()

                for i_out_idx in range(len(active)):
                    for i_in in inactive:
                        trial = active[:]
                        trial[i_out_idx] = i_in
                        r, tp, fa, intf = self._evaluate_selection(
                            episode_data[t], np.array(trial)
                        )
                        if r > best_reward:
                            best_reward = r
                            best_active = trial[:]
                            best_components = {'reward': r, 'tp': tp, 'fa': fa, 'intf': intf}
                            improved = True

                schedule[t] = best_active
                step_info[t] = best_components

            if not improved:
                break

        rewards = [s['reward'] for s in step_info]
        return schedule, rewards, step_info

    def _evaluate_selection(self, step_data: dict, active_beams: np.ndarray) -> tuple:
        """Recompute step reward components for a given beam selection.

        Uses stored fading, demands, queues from the original episode to
        replay the reward computation deterministically.
        Returns (total_reward, r_throughput, r_fairness, p_interference).
        """
        from simulator.channel import compute_sinr

        total_demand = step_data['demands'] + step_data['queues']
        fading = step_data.get('fading', np.ones(self.N))

        sinr = compute_sinr(self.env.gain_matrix, active_beams, self.env.config, fading)
        cap = self.env.config.bandwidth_hz * np.log2(1.0 + sinr) / 1e6
        served_per_beam = np.minimum(cap, total_demand[active_beams])
        active_demand = total_demand[active_beams].sum()

        r_throughput = served_per_beam.sum() / active_demand if active_demand > 0 else 0.0

        # Fairness
        satisfaction = np.zeros(len(active_beams))
        for idx, beam_i in enumerate(active_beams):
            if total_demand[beam_i] > 0:
                satisfaction[idx] = served_per_beam[idx] / total_demand[beam_i]
        n_active = len(active_beams)
        s_sum = satisfaction.sum()
        s_sum_sq = (satisfaction ** 2).sum()
        r_fairness = (s_sum ** 2) / (n_active * s_sum_sq) if s_sum_sq > 0 else 1.0

        # Interference penalty
        sinr_threshold_linear = 10 ** (self.env.config.sinr_threshold_db / 10)
        deficit = np.maximum(sinr_threshold_linear - sinr, 0)
        p_interference = deficit.sum() / (n_active * sinr_threshold_linear) if n_active > 0 else 0.0

        reward = (
            self.env.config.reward_alpha * r_throughput
            + self.env.config.reward_beta * r_fairness
            - self.env.config.reward_gamma * p_interference
        )
        return reward, r_throughput, r_fairness, p_interference


def run_episode(env: BHEnv, scheduler: GraphColoringScheduler, seed: int = 42,
                refine: bool = False) -> dict:
    """Run one episode with the graph coloring scheduler.

    Returns dict with total reward, components, and optional per-step data
    for refinement.
    """
    obs, info = env.reset(seed=seed)
    total_reward = 0.0
    components = {'throughput': 0.0, 'fairness': 0.0, 'interference': 0.0}
    episode_data = [] if refine else None

    for _ in range(env.T):
        # Capture pre-step state for refinement replay
        pre_demands = env.demands.copy()
        pre_queues = env.queues.copy()
        pre_fading = env.fading.copy()

        action = scheduler.policy(env, obs)
        obs, reward, terminated, truncated, info = env.step(action)
        total_reward += reward
        components['throughput'] += info['reward_throughput']
        components['fairness'] += info['reward_fairness']
        components['interference'] += info['penalty_interference']

        if refine:
            episode_data.append({
                'active_beams': info['active_beams'].copy(),
                'reward': reward,
                'demands': pre_demands,            # demands used in this step
                'queues': pre_queues,              # queues used in this step
                'fading': pre_fading,              # fading used in this step
            })

        if terminated:
            break

    result = {'total': total_reward, **components}
    if refine and episode_data:
        result['episode_data'] = episode_data
    return result


def run_baseline(n_episodes: int = 30, seed_start: int = 0,
                 do_refine: bool = False) -> list:
    """Run baseline evaluation over multiple episodes."""
    env = BHEnv()
    scheduler = GraphColoringScheduler(env)
    results = []

    for ep in range(n_episodes):
        r = run_episode(env, scheduler, seed=seed_start + ep * 100, refine=do_refine)
        if do_refine and 'episode_data' in r:
            schedule, step_rewards, step_info = scheduler.refine(r['episode_data'])
            r['total'] = sum(step_rewards)
            r['throughput'] = sum(s['tp'] for s in step_info)
            r['fairness'] = sum(s['fa'] for s in step_info)
            r['interference'] = sum(s['intf'] for s in step_info)
        results.append(r)

    return results


def run_random_baseline(n_episodes: int = 30, seed_start: int = 0) -> list:
    """Run random baseline for comparison."""
    env = BHEnv()
    results = []
    for ep in range(n_episodes):
        obs, info = env.reset(seed=seed_start + ep * 100)
        total_reward = 0.0
        components = {'throughput': 0.0, 'fairness': 0.0, 'interference': 0.0}
        for _ in range(env.T):
            action = env._rng.standard_normal(env.N)
            obs, reward, terminated, truncated, info = env.step(action)
            total_reward += reward
            components['throughput'] += info['reward_throughput']
            components['fairness'] += info['reward_fairness']
            components['interference'] += info['penalty_interference']
            if terminated:
                break
        results.append({'total': total_reward, **components})
    return results


def summarize(results, name=""):
    """Print summary statistics for a set of episode results."""
    totals = np.array([r['total'] for r in results])
    tp = np.array([r['throughput'] for r in results])
    fa = np.array([r['fairness'] for r in results])
    intf = np.array([r['interference'] for r in results])
    print(f"  [{name}] total={totals.mean():.4f} +/- {totals.std():.4f}  "
          f"tp={tp.mean():.4f}  fair={fa.mean():.4f}  intf={intf.mean():.4f}")
    return {'total_mean': totals.mean(), 'total_std': totals.std()}


if __name__ == "__main__":
    N_EP = 30

    # Build env and scheduler to print graph coloring info
    env = BHEnv()
    scheduler = GraphColoringScheduler(env)

    print("=== Graph Coloring Baseline (adapted L04 MCMF-TS-GC) ===")
    print()
    print(f"Interference graph: {scheduler.N} beams, "
          f"{int(scheduler.adj_bool.sum())} edges "
          f"(density={scheduler.adj_bool.sum() / (scheduler.N * (scheduler.N - 1)):.3f})")
    print(f"Graph coloring: {scheduler.n_colors} colors")
    for c, group in enumerate(scheduler.color_groups):
        print(f"  Color {c}: beams {group.tolist()} ({len(group)} beams)")
    print()

    # --- Graph Coloring baseline ---
    print("--- Evaluation (30 episodes) ---")
    gc_results = run_baseline(n_episodes=N_EP)
    gc_summary = summarize(gc_results, "GraphColoring")

    # --- Graph Coloring with refinement ---
    gc_ref_results = run_baseline(n_episodes=N_EP, do_refine=True)
    gc_ref_summary = summarize(gc_ref_results, "GC+Refine")

    # --- Random baseline for reference ---
    rand_results = run_random_baseline(n_episodes=N_EP)
    rand_summary = summarize(rand_results, "Random")

    print()
    print("--- Comparison ---")
    delta = gc_summary['total_mean'] - rand_summary['total_mean']
    print(f"  GC vs Random: {delta:+.4f} ({delta / rand_summary['total_mean'] * 100:+.1f}%)")
    delta_ref = gc_ref_summary['total_mean'] - rand_summary['total_mean']
    print(f"  GC+Refine vs Random: {delta_ref:+.4f} ({delta_ref / rand_summary['total_mean'] * 100:+.1f}%)")
