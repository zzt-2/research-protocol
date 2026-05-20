"""
MVE v3: TD3 vs DDPG vs Random for RIS Phase Shift Optimization
Block-fading multi-step episodes with BLOCKED direct link.

v2 failed: direct link too strong (Rician kappa=10dB + MRT), random phase already near-optimal.
v3 fixes: Hd=0 (blocked direct link), all signal via BS->RIS->UE reflection path.
Uses absolute action: action in [-1,1]^N -> phase = (action+1)*pi.
"""

import time
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {DEVICE}")

STEPS_PER_EPISODE = 50
N_EPISODES = 160  # 160 * 50 = 8000 total steps
EVAL_INTERVAL = 20  # evaluate every 20 episodes
WARMUP_EPISODES = 4  # 4 episodes * 50 steps = 200 warmup steps


# =============================================================================
# Channel Model
# =============================================================================

def rician_channel(shape, kappa_db=10.0, device="cpu"):
    """Generate Rician fading channel."""
    kappa = 10 ** (kappa_db / 10.0)
    rows, cols = shape
    los = torch.ones(rows, cols, dtype=torch.cfloat, device=device) / np.sqrt(2)
    nlos_real = torch.randn(rows, cols, device=device)
    nlos_imag = torch.randn(rows, cols, device=device)
    nlos = torch.complex(nlos_real, nlos_imag) / np.sqrt(2)
    h = np.sqrt(kappa / (kappa + 1)) * los + np.sqrt(1 / (kappa + 1)) * nlos
    return h


def path_loss_db(d, f_carrier=3.5e9, scenario="NLOS"):
    """Simplified 3GPP TR 38.901 path loss (dB)."""
    c = 3e8
    fc = f_carrier
    if scenario == "LOS":
        pl = 32.4 + 21.0 * np.log10(d) + 30.0 * np.log10(fc / 1e9)
    else:
        pl = 35.3 * np.log10(d) + 22.4 + 21.3 * np.log10(fc / 1e9)
    return pl


class RISEnv:
    """MU-MISO RIS-aided environment. v3: direct link BLOCKED (Hd=0)."""

    def __init__(self, M=4, N=64, K=4, p_max_dbm=30, noise_dbm=-80,
                 kappa_db=10.0, device="cpu", steps_per_episode=50):
        self.M = M
        self.N = N
        self.K = K
        self.p_max = 10 ** (p_max_dbm / 10.0) / 1000.0
        self.noise_var = 10 ** (noise_dbm / 10.0) / 1000.0
        self.kappa_db = kappa_db
        self.device = device
        self.steps_per_episode = steps_per_episode

        self.d_bs_ris = 50.0
        self.d_ris_ue = 10.0
        # d_bs_ue not used since Hd=0

        self.pl_bs_ris = 10 ** (-path_loss_db(self.d_bs_ris, scenario="LOS") / 10.0)
        self.pl_ris_ue = 10 ** (-path_loss_db(self.d_ris_ue, scenario="LOS") / 10.0)

        # State: [Re(H1), Im(H1), Re(H2), Im(H2), cos(theta), sin(theta)]
        # No Hd in state since Hd=0 always
        self.state_dim = 2 * N * M + 2 * K * N + 2 * N
        self.action_dim = N

        self.current_step = 0
        self.phase = None
        self.H1 = None
        self.H2 = None

    def reset(self):
        """Start new episode: generate block-fading channels, random initial phase."""
        N, M, K = self.N, self.M, self.K

        self.H1 = rician_channel((N, M), self.kappa_db, self.device) * np.sqrt(self.pl_bs_ris)
        self.H2 = rician_channel((K, N), self.kappa_db, self.device) * np.sqrt(self.pl_ris_ue)
        # Hd = 0: direct link blocked

        self.phase = torch.rand(N, device=self.device) * 2 * np.pi
        self.current_step = 0

        return self._get_state()

    def _get_state(self):
        """State = [flat channels (H1, H2 only), cos/sin of current phase]."""
        h1_flat = torch.view_as_real(self.H1).reshape(-1)
        h2_flat = torch.view_as_real(self.H2).reshape(-1)
        phase_enc = torch.cat([torch.cos(self.phase), torch.sin(self.phase)])
        return torch.cat([h1_flat, h2_flat, phase_enc])

    def _compute_sum_rate(self, phase):
        """Compute sum rate with MRT beamforming on cascaded channel (Hd=0)."""
        N, M, K = self.N, self.M, self.K
        diag_phase = torch.diag(torch.exp(1j * phase))
        # Cascaded channel: h_eff_k = H2[k,:] @ diag(exp(j*theta)) @ H1
        H_eff = self.H2 @ diag_phase @ self.H1  # (K, M)

        p_per_user = self.p_max / K
        W = torch.zeros(K, M, dtype=torch.cfloat, device=self.device)
        for k in range(K):
            h_k = H_eff[k, :]
            norm_k = torch.sqrt(torch.sum(torch.abs(h_k) ** 2))
            if norm_k > 1e-12:
                W[k, :] = h_k / norm_k * np.sqrt(p_per_user)

        sum_rate = torch.tensor(0.0, device=self.device)
        for k in range(K):
            h_eff_k = H_eff[k, :]
            signal = torch.abs(torch.vdot(h_eff_k, W[k, :])) ** 2
            interf = torch.tensor(0.0, device=self.device)
            for j in range(K):
                if j != k:
                    interf += torch.abs(torch.vdot(h_eff_k, W[j, :])) ** 2
            sinr_k = signal / (interf + self.noise_var)
            sum_rate = sum_rate + torch.log2(1 + sinr_k)

        return sum_rate

    def step(self, action):
        """Apply absolute action: action in [-1,1]^N -> phase = (action+1)*pi.

        Absolute action lets the agent directly learn optimal phase shifts
        rather than incrementally adjusting (critical when direct link is zero).
        """
        with torch.no_grad():
            self.phase = (action + 1.0) * np.pi  # maps [-1,1] -> [0, 2*pi]
            sum_rate = self._compute_sum_rate(self.phase)

        self.current_step += 1
        done = (self.current_step >= self.steps_per_episode)

        next_state = self._get_state()
        return next_state, sum_rate.item(), done


# =============================================================================
# Sanity Check
# =============================================================================

def sanity_check(env):
    """Verify simulation correctness with Hd=0."""
    print("\n--- Sanity Check (Hd=0) ---")
    N = env.N

    # Test 1: zero phase shift -> sum rate should be > 0
    env.reset()
    phase_zero = torch.zeros(N, device=env.device)
    rate_zero = env._compute_sum_rate(phase_zero).item()
    print(f"  theta=0: sum_rate = {rate_zero:.4f} bps/Hz (should be > 0)")
    assert rate_zero > 0, f"Sanity check failed: zero phase gave rate={rate_zero}"

    # Test 2: random phase -> should give positive but potentially lower rate
    rates_random = []
    for _ in range(100):
        env.reset()
        phase_rand = torch.rand(N, device=env.device) * 2 * np.pi
        rates_random.append(env._compute_sum_rate(phase_rand).item())
    mean_rand = np.mean(rates_random)
    print(f"  random phase (100 trials): mean={mean_rand:.4f}, "
          f"std={np.std(rates_random):.4f}, "
          f"min={np.min(rates_random):.4f}, max={np.max(rates_random):.4f}")

    # Test 3: check that rate varies significantly across phases
    # Try all-same phase values at a few points
    rates_sweep = []
    for angle in np.linspace(0, 2 * np.pi, 36, endpoint=False):
        env.reset()
        phase_same = torch.full((N,), angle, device=env.device)
        rates_sweep.append(env._compute_sum_rate(phase_same).item())
    print(f"  uniform phase sweep: min={min(rates_sweep):.4f}, max={max(rates_sweep):.4f}, "
          f"ratio={max(rates_sweep)/min(rates_sweep):.2f}x")

    # Test 4: with Hd=0, random phase rate should be noticeably lower than v2's ~2.0
    print(f"  Expected: random rate << 2.0 bps/Hz (was ~2.0 in v2 with strong direct link)")
    assert mean_rand < 1.5, f"Random rate too high ({mean_rand:.4f}), possible bug"

    print("  Sanity checks PASSED\n")
    return mean_rand


# =============================================================================
# Replay Buffer
# =============================================================================

def _to_np(x):
    if isinstance(x, torch.Tensor):
        return x.detach().cpu().numpy()
    return np.asarray(x, dtype=np.float32)


class ReplayBuffer:
    def __init__(self, capacity, state_dim, action_dim, device):
        self.capacity = capacity
        self.device = device
        self.ptr = 0
        self.size = 0
        self.states = np.zeros((capacity, state_dim), dtype=np.float32)
        self.actions = np.zeros((capacity, action_dim), dtype=np.float32)
        self.rewards = np.zeros((capacity, 1), dtype=np.float32)
        self.next_states = np.zeros((capacity, state_dim), dtype=np.float32)
        self.dones = np.zeros((capacity, 1), dtype=np.float32)

    def push(self, state, action, reward, next_state, done):
        self.states[self.ptr] = _to_np(state)
        self.actions[self.ptr] = _to_np(action)
        self.rewards[self.ptr, 0] = reward
        self.next_states[self.ptr] = _to_np(next_state)
        self.dones[self.ptr, 0] = done
        self.ptr = (self.ptr + 1) % self.capacity
        self.size = min(self.size + 1, self.capacity)

    def sample(self, batch_size):
        idx = np.random.randint(0, self.size, size=batch_size)
        return (
            torch.tensor(self.states[idx], device=self.device),
            torch.tensor(self.actions[idx], device=self.device),
            torch.tensor(self.rewards[idx], device=self.device),
            torch.tensor(self.next_states[idx], device=self.device),
            torch.tensor(self.dones[idx], device=self.device),
        )


# =============================================================================
# Networks
# =============================================================================

class Actor(nn.Module):
    def __init__(self, state_dim, action_dim, hidden=256):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(state_dim, hidden),
            nn.ReLU(),
            nn.Linear(hidden, hidden),
            nn.ReLU(),
            nn.Linear(hidden, action_dim),
            nn.Tanh(),
        )

    def forward(self, state):
        return self.net(state)


class Critic(nn.Module):
    def __init__(self, state_dim, action_dim, hidden=256):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(state_dim + action_dim, hidden),
            nn.ReLU(),
            nn.Linear(hidden, hidden),
            nn.ReLU(),
            nn.Linear(hidden, 1),
        )

    def forward(self, state, action):
        return self.net(torch.cat([state, action], dim=-1))


# =============================================================================
# DDPG Agent
# =============================================================================

class DDPGAgent:
    def __init__(self, state_dim, action_dim, lr_a=1e-3, lr_c=1e-3,
                 gamma=0.99, tau=5e-3, device="cpu"):
        self.device = device
        self.gamma = gamma
        self.tau = tau
        self.action_dim = action_dim

        self.actor = Actor(state_dim, action_dim).to(device)
        self.actor_target = Actor(state_dim, action_dim).to(device)
        self.actor_target.load_state_dict(self.actor.state_dict())

        self.critic = Critic(state_dim, action_dim).to(device)
        self.critic_target = Critic(state_dim, action_dim).to(device)
        self.critic_target.load_state_dict(self.critic.state_dict())

        self.actor_opt = optim.Adam(self.actor.parameters(), lr=lr_a)
        self.critic_opt = optim.Adam(self.critic.parameters(), lr=lr_c)

    def select_action(self, state, noise_std=0.0):
        if isinstance(state, torch.Tensor):
            state_t = state.detach().unsqueeze(0)
        else:
            state_t = torch.tensor(state, dtype=torch.float32, device=self.device).unsqueeze(0)
        with torch.no_grad():
            action = self.actor(state_t).squeeze(0)
        if noise_std > 0:
            noise = torch.randn_like(action) * noise_std
            action = torch.clamp(action + noise, -1.0, 1.0)
        return action.cpu().numpy()

    def update(self, buffer, batch_size):
        s, a, r, s2, d = buffer.sample(batch_size)

        with torch.no_grad():
            a2 = self.actor_target(s2)
            q_target = r + self.gamma * (1 - d) * self.critic_target(s2, a2)
        q_val = self.critic(s, a)
        critic_loss = nn.MSELoss()(q_val, q_target)

        self.critic_opt.zero_grad()
        critic_loss.backward()
        self.critic_opt.step()

        a_pred = self.actor(s)
        actor_loss = -self.critic(s, a_pred).mean()

        self.actor_opt.zero_grad()
        actor_loss.backward()
        self.actor_opt.step()

        self._soft_update(self.actor, self.actor_target)
        self._soft_update(self.critic, self.critic_target)

    def _soft_update(self, source, target):
        for p, tp in zip(source.parameters(), target.parameters()):
            tp.data.copy_(self.tau * p.data + (1 - self.tau) * tp.data)


# =============================================================================
# TD3 Agent
# =============================================================================

class TD3Agent:
    def __init__(self, state_dim, action_dim, lr_a=1e-3, lr_c=1e-3,
                 gamma=0.99, tau=5e-3, policy_noise=0.2, noise_clip=0.5,
                 policy_delay=2, device="cpu"):
        self.device = device
        self.gamma = gamma
        self.tau = tau
        self.action_dim = action_dim
        self.policy_noise = policy_noise
        self.noise_clip = noise_clip
        self.policy_delay = policy_delay
        self.update_count = 0

        self.actor = Actor(state_dim, action_dim).to(device)
        self.actor_target = Actor(state_dim, action_dim).to(device)
        self.actor_target.load_state_dict(self.actor.state_dict())

        self.critic1 = Critic(state_dim, action_dim).to(device)
        self.critic1_target = Critic(state_dim, action_dim).to(device)
        self.critic1_target.load_state_dict(self.critic1.state_dict())

        self.critic2 = Critic(state_dim, action_dim).to(device)
        self.critic2_target = Critic(state_dim, action_dim).to(device)
        self.critic2_target.load_state_dict(self.critic2.state_dict())

        self.actor_opt = optim.Adam(self.actor.parameters(), lr=lr_a)
        self.critic_opt = optim.Adam(
            list(self.critic1.parameters()) + list(self.critic2.parameters()),
            lr=lr_c
        )

    def select_action(self, state, noise_std=0.0):
        if isinstance(state, torch.Tensor):
            state_t = state.detach().unsqueeze(0)
        else:
            state_t = torch.tensor(state, dtype=torch.float32, device=self.device).unsqueeze(0)
        with torch.no_grad():
            action = self.actor(state_t).squeeze(0)
        if noise_std > 0:
            noise = torch.randn_like(action) * noise_std
            action = torch.clamp(action + noise, -1.0, 1.0)
        return action.cpu().numpy()

    def update(self, buffer, batch_size):
        s, a, r, s2, d = buffer.sample(batch_size)
        self.update_count += 1

        with torch.no_grad():
            noise = (torch.randn_like(a) * self.policy_noise).clamp(
                -self.noise_clip, self.noise_clip
            )
            a2 = (self.actor_target(s2) + noise).clamp(-1.0, 1.0)
            q1_target = self.critic1_target(s2, a2)
            q2_target = self.critic2_target(s2, a2)
            q_target = r + self.gamma * (1 - d) * torch.min(q1_target, q2_target)

        q1_val = self.critic1(s, a)
        q2_val = self.critic2(s, a)
        critic_loss = nn.MSELoss()(q1_val, q_target) + nn.MSELoss()(q2_val, q_target)

        self.critic_opt.zero_grad()
        critic_loss.backward()
        self.critic_opt.step()

        if self.update_count % self.policy_delay == 0:
            a_pred = self.actor(s)
            actor_loss = -self.critic1(s, a_pred).mean()

            self.actor_opt.zero_grad()
            actor_loss.backward()
            self.actor_opt.step()

            self._soft_update(self.actor, self.actor_target)
            self._soft_update(self.critic1, self.critic1_target)
            self._soft_update(self.critic2, self.critic2_target)

    def _soft_update(self, source, target):
        for p, tp in zip(source.parameters(), target.parameters()):
            tp.data.copy_(self.tau * p.data + (1 - self.tau) * tp.data)


# =============================================================================
# Training Loop
# =============================================================================

def train_agent(agent, env, buffer, n_episodes=N_EPISODES, batch_size=256,
                noise_std=0.1, eval_interval=EVAL_INTERVAL, warmup_episodes=WARMUP_EPISODES):
    """Train agent with block-fading multi-step episodes."""
    eval_results = []
    start_time = time.time()

    warmup_steps = warmup_episodes * env.steps_per_episode

    for ep in range(1, n_episodes + 1):
        state = env.reset()
        ep_reward = 0.0

        for t in range(env.steps_per_episode):
            total_step = (ep - 1) * env.steps_per_episode + t

            # Select action (absolute: [-1,1] -> phase)
            if total_step < warmup_steps:
                action = np.random.uniform(-1, 1, size=env.action_dim).astype(np.float32)
            else:
                action = agent.select_action(state, noise_std=noise_std)

            action_t = torch.tensor(action, device=DEVICE, dtype=torch.float32)
            next_state, reward, done = env.step(action_t)

            buffer.push(state, action, reward, next_state, float(done))
            ep_reward += reward
            state = next_state

            # Update agent
            if buffer.size >= batch_size and total_step >= warmup_steps:
                agent.update(buffer, batch_size)

            if done:
                break

        # Evaluate
        if ep % eval_interval == 0:
            avg_rate, first_rate, last_rate = evaluate(agent, env, n_eval=20)
            elapsed = time.time() - start_time
            eval_results.append((ep, avg_rate, first_rate, last_rate))
            print(f"  Episode {ep:5d} | Avg(last10): {avg_rate:.4f} | "
                  f"Step1: {first_rate:.4f} | Step50: {last_rate:.4f} | "
                  f"Ep-avg: {ep_reward/env.steps_per_episode:.4f} | "
                  f"Time: {elapsed:.1f}s")

    total_time = time.time() - start_time
    print(f"  Training complete in {total_time:.1f}s")
    return eval_results


def evaluate(agent, env, n_eval=20):
    """Evaluate agent: n_eval channels, 50 steps each, report last-10-step average."""
    last10_rates = []
    first_rates = []
    final_rates = []

    for _ in range(n_eval):
        state = env.reset()
        rates = []
        for t in range(env.steps_per_episode):
            action = agent.select_action(state, noise_std=0.0)
            action_t = torch.tensor(action, device=DEVICE, dtype=torch.float32)
            next_state, reward, done = env.step(action_t)
            rates.append(reward)
            state = next_state
            if done:
                break

        first_rates.append(rates[0] if rates else 0.0)
        final_rates.append(rates[-1] if rates else 0.0)
        last10_rates.append(np.mean(rates[-10:]) if len(rates) >= 10 else np.mean(rates))

    return np.mean(last10_rates), np.mean(first_rates), np.mean(final_rates)


def eval_random(env, n_eval=200):
    """Evaluate random phase baseline with multi-step episodes."""
    last10_rates = []
    first_rates = []
    final_rates = []

    for _ in range(n_eval):
        state = env.reset()
        rates = []
        for t in range(env.steps_per_episode):
            action = np.random.uniform(-1, 1, size=env.action_dim).astype(np.float32)
            action_t = torch.tensor(action, device=DEVICE, dtype=torch.float32)
            next_state, reward, done = env.step(action_t)
            rates.append(reward)
            state = next_state
            if done:
                break

        first_rates.append(rates[0] if rates else 0.0)
        final_rates.append(rates[-1] if rates else 0.0)
        last10_rates.append(np.mean(rates[-10:]) if len(rates) >= 10 else np.mean(rates))

    return np.mean(last10_rates), np.std(last10_rates), np.mean(first_rates), np.mean(final_rates)


def run_experiment(N, n_episodes=N_EPISODES, eval_interval=EVAL_INTERVAL):
    """Run full MVE v3 experiment for a given RIS size N."""
    print(f"\n{'='*60}")
    print(f"Running MVE v3 (Hd=0, absolute action): N={N}")
    print(f"Episodes: {n_episodes}, Steps/ep: {STEPS_PER_EPISODE}, "
          f"Total steps: {n_episodes * STEPS_PER_EPISODE}")
    print(f"{'='*60}")

    M, K = 4, 4
    env = RISEnv(M=M, N=N, K=K, device=DEVICE, steps_per_episode=STEPS_PER_EPISODE)
    print(f"State dim: {env.state_dim}, Action dim: {env.action_dim}")

    # --- Sanity check ---
    rand_sanity = sanity_check(env)

    # --- Random baseline ---
    print(f"--- Random Phase Baseline ---")
    rand_mean, rand_std, rand_first, rand_last = eval_random(env, n_eval=200)
    print(f"Random: last10-avg={rand_mean:.4f} +/- {rand_std:.4f}, "
          f"step1={rand_first:.4f}, step50={rand_last:.4f}")

    # --- DDPG ---
    print(f"\n--- DDPG Training ---")
    buffer_ddpg = ReplayBuffer(100000, env.state_dim, env.action_dim, DEVICE)
    ddpg_agent = DDPGAgent(env.state_dim, env.action_dim, device=DEVICE)
    ddpg_results = train_agent(
        ddpg_agent, env, buffer_ddpg,
        n_episodes=n_episodes, batch_size=256,
        noise_std=0.1, eval_interval=eval_interval, warmup_episodes=WARMUP_EPISODES
    )

    # --- TD3 ---
    print(f"\n--- TD3 Training ---")
    buffer_td3 = ReplayBuffer(100000, env.state_dim, env.action_dim, DEVICE)
    td3_agent = TD3Agent(env.state_dim, env.action_dim, device=DEVICE)
    td3_results = train_agent(
        td3_agent, env, buffer_td3,
        n_episodes=n_episodes, batch_size=256,
        noise_std=0.1, eval_interval=eval_interval, warmup_episodes=WARMUP_EPISODES
    )

    # --- Final evaluation (more samples) ---
    print(f"\n--- Final Evaluation (50 episodes) ---")
    ddpg_avg, ddpg_first, ddpg_last = evaluate(ddpg_agent, env, n_eval=50)
    td3_avg, td3_first, td3_last = evaluate(td3_agent, env, n_eval=50)
    print(f"DDPG: last10={ddpg_avg:.4f}, step1={ddpg_first:.4f}, step50={ddpg_last:.4f}")
    print(f"TD3:  last10={td3_avg:.4f}, step1={td3_first:.4f}, step50={td3_last:.4f}")

    return {
        "N": N,
        "random_mean": rand_mean,
        "random_std": rand_std,
        "random_first": rand_first,
        "random_last": rand_last,
        "ddpg_final": ddpg_avg,
        "ddpg_first": ddpg_first,
        "ddpg_last": ddpg_last,
        "ddpg_history": ddpg_results,
        "td3_final": td3_avg,
        "td3_first": td3_first,
        "td3_last": td3_last,
        "td3_history": td3_results,
    }


def format_results(result):
    """Format experiment results."""
    N = result["N"]
    rand_mean = result["random_mean"]
    rand_first = result["random_first"]
    rand_last = result["random_last"]
    ddpg_final = result["ddpg_final"]
    ddpg_first = result["ddpg_first"]
    ddpg_last = result["ddpg_last"]
    td3_final = result["td3_final"]
    td3_first = result["td3_first"]
    td3_last = result["td3_last"]

    td3_vs_random = td3_final / rand_mean if rand_mean > 0 else 0
    td3_vs_ddpg = ((td3_final - ddpg_final) / ddpg_final * 100) if ddpg_final > 0 else 0

    td3_history = result["td3_history"]
    ddpg_history = result["ddpg_history"]

    td3_converged = _check_convergence(td3_history)
    ddpg_converged = _check_convergence(ddpg_history)

    lines = []
    lines.append(f"## MVE v3 Result (Hd=0, absolute action)")
    lines.append("")
    lines.append(f"### N={N}")
    lines.append(f"| Method | Last10-Avg Rate (bps/Hz) | Step1 Rate | Step50 Rate | Episode Gain |")
    lines.append(f"|--------|-------------------------|------------|-------------|-------------|")
    lines.append(f"| Random | {rand_mean:.4f} | {rand_first:.4f} | {rand_last:.4f} | {rand_last - rand_first:+.4f} |")
    lines.append(f"| DDPG   | {ddpg_final:.4f} | {ddpg_first:.4f} | {ddpg_last:.4f} | {ddpg_last - ddpg_first:+.4f} |")
    lines.append(f"| TD3    | {td3_final:.4f} | {td3_first:.4f} | {td3_last:.4f} | {td3_last - td3_first:+.4f} |")
    lines.append("")
    lines.append(f"TD3 vs Random: {td3_vs_random:.2f}x")
    lines.append(f"TD3 vs DDPG: {td3_vs_ddpg:+.1f}%")
    lines.append("")

    # Convergence curve description
    lines.append("### Convergence Behavior")
    lines.append(_describe_curve(ddpg_history, "DDPG"))
    lines.append(_describe_curve(td3_history, "TD3"))
    lines.append("")

    # Episode-internal learning check
    td3_ep_gain = td3_last - td3_first
    ddpg_ep_gain = ddpg_last - ddpg_first
    rand_ep_gain = rand_last - rand_first
    lines.append(f"### Episode-Internal Refinement")
    lines.append(f"Random episode gain (step50-step1): {rand_ep_gain:+.4f}")
    lines.append(f"DDPG episode gain (step50-step1): {ddpg_ep_gain:+.4f}")
    lines.append(f"TD3 episode gain (step50-step1): {td3_ep_gain:+.4f}")
    td3_refines = td3_ep_gain > rand_ep_gain * 1.5
    lines.append(f"TD3 refines within episode: {'Yes' if td3_refines else 'No'}")
    lines.append("")

    # Pass/Fail
    lines.append("### Pass/Fail")
    lines.append(f"1. TD3 converged: {'PASS' if td3_converged else 'FAIL'}")
    pass_15x = td3_vs_random >= 1.5
    lines.append(f"2. TD3 > 1.5x Random: {'PASS' if pass_15x else 'FAIL'} ({td3_vs_random:.2f}x)")
    pass_ge_ddpg = td3_final >= ddpg_final
    lines.append(f"3. TD3 >= DDPG: {'PASS' if pass_ge_ddpg else 'FAIL'} ({td3_vs_ddpg:+.1f}%)")
    lines.append("")

    # Training history table
    lines.append("### Training History (eval points)")
    lines.append("| Episode | DDPG (last10) | TD3 (last10) | DDPG step1 | TD3 step1 | DDPG step50 | TD3 step50 |")
    lines.append("|---------|--------------|-------------|------------|-----------|-------------|------------|")
    for (ep_d, r_d, f_d, l_d), (ep_t, r_t, f_t, l_t) in zip(ddpg_history, td3_history):
        lines.append(f"| {ep_d} | {r_d:.4f} | {r_t:.4f} | {f_d:.4f} | {f_t:.4f} | {l_d:.4f} | {l_t:.4f} |")

    return "\n".join(lines)


def _check_convergence(history, window=3, threshold=0.05):
    """Check if last few eval points are stable."""
    if len(history) < window + 1:
        return False
    last_vals = [h[1] for h in history[-window:]]
    mean_val = np.mean(last_vals)
    if mean_val < 1e-6:
        return False
    variation = np.std(last_vals) / mean_val
    return variation < threshold


def _describe_curve(history, name):
    """Describe learning curve trend."""
    if len(history) < 2:
        return f"{name}: insufficient data"
    first_val = history[0][1]
    last_val = history[-1][1]
    peak_val = max(h[1] for h in history)
    peak_ep = max(history, key=lambda h: h[1])[0]
    trend = "upward" if last_val > first_val * 1.1 else ("stable" if last_val > first_val * 0.9 else "downward")
    return (f"{name}: Start={first_val:.4f}, End={last_val:.4f}, "
            f"Peak={peak_val:.4f}@ep{peak_ep}. Trend: {trend}.")


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    torch.manual_seed(42)
    np.random.seed(42)

    print("=" * 60)
    print("MVE v3: RIS Phase Shift Optimization with DRL")
    print("Hd=0 (direct link blocked), absolute action [-1,1]->[0,2pi]")
    print(f"Config: {N_EPISODES} episodes x {STEPS_PER_EPISODE} steps = "
          f"{N_EPISODES * STEPS_PER_EPISODE} total steps")
    print("=" * 60)

    # Run N=64 experiment
    t0 = time.time()
    result_64 = run_experiment(N=64, n_episodes=N_EPISODES, eval_interval=EVAL_INTERVAL)
    t64 = time.time() - t0
    print(f"\nN=64 total time: {t64:.1f}s")

    output_64 = format_results(result_64)
    print(f"\n{'='*60}")
    print(output_64)

    # If N=64 took less than 6 minutes, try N=128
    if t64 < 360:
        remaining_budget = 600 - t64  # 10 min total budget
        if remaining_budget > 120:
            print(f"\n\nN=64 completed in {t64:.0f}s, running N=128...")
            result_128 = run_experiment(N=128, n_episodes=N_EPISODES, eval_interval=EVAL_INTERVAL)
            output_128 = format_results(result_128)
            print(f"\n{'='*60}")
            print(output_128)
        else:
            print(f"\nInsufficient time budget ({remaining_budget:.0f}s left), skipping N=128")
    else:
        print(f"\nN=64 took {t64:.0f}s, skipping N=128 (time budget exceeded)")

    print("\nDone.")
