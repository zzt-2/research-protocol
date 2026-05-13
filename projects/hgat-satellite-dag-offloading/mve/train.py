"""train.py - PPO training loop for MVE."""
import torch
import torch.nn as nn
import numpy as np


def collect_episode(env, model, build_graph_fn):
    """Run one episode, store (graph, action, reward) for PPO update."""
    obs = env.reset()
    transitions = []
    while True:
        tid = obs["ready"][0] if obs["ready"] else None
        if tid is None:
            break
        g = build_graph_fn(obs)
        with torch.no_grad():
            logits, value = model(g)
        dist = torch.distributions.Categorical(logits=logits)
        action = dist.sample()
        obs, reward, done, info = env.step(tid, action.item())
        transitions.append({"graph": g, "action": action, "reward": reward})
        if done:
            break
    return transitions


def compute_returns(rewards, gamma=0.99):
    """Discounted returns."""
    ret = 0.0
    returns = []
    for r in reversed(rewards):
        ret = r + gamma * ret
        returns.insert(0, ret)
    return returns


def ppo_update(model, optimizer, transitions, clip=0.2, epochs=4):
    """PPO clipped update with recomputation."""
    rewards = [t["reward"] for t in transitions]
    returns = compute_returns(rewards)
    returns_t = torch.tensor(returns, dtype=torch.float32)

    # Compute old log_probs and values (detached)
    with torch.no_grad():
        old_lp, old_vals = [], []
        for t in transitions:
            logits, value = model(t["graph"])
            dist = torch.distributions.Categorical(logits=logits)
            old_lp.append(dist.log_prob(t["action"]))
            old_vals.append(value.squeeze())
    old_log_probs = torch.stack(old_lp).detach()
    old_values = torch.stack(old_vals).detach()

    advantages = returns_t - old_values
    advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)

    for _ in range(epochs):
        new_lp, new_vals = [], []
        for t in transitions:
            logits, value = model(t["graph"])
            dist = torch.distributions.Categorical(logits=logits)
            new_lp.append(dist.log_prob(t["action"]))
            new_vals.append(value.squeeze())
        new_log_probs = torch.stack(new_lp)
        new_values = torch.stack(new_vals)

        ratio = torch.exp(new_log_probs - old_log_probs)
        surr1 = ratio * advantages
        surr2 = torch.clamp(ratio, 1 - clip, 1 + clip) * advantages
        actor_loss = -torch.min(surr1, surr2).mean()
        critic_loss = nn.functional.mse_loss(new_values, returns_t)
        entropy = -torch.mean(new_log_probs)
        loss = actor_loss + 0.5 * critic_loss - 0.01 * entropy

        optimizer.zero_grad()
        loss.backward()
        nn.utils.clip_grad_norm_(model.parameters(), 0.5)
        optimizer.step()


def train(env, model, build_graph_fn, n_episodes=500, lr=3e-4, seed=0):
    """Train model, return per-episode costs."""
    torch.manual_seed(seed)
    np.random.seed(seed)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    costs = []
    for ep in range(n_episodes):
        env.rng = np.random.RandomState(seed * 10000 + ep)
        transitions = collect_episode(env, model, build_graph_fn)
        if not transitions:
            costs.append(0.0)
            continue
        ppo_update(model, optimizer, transitions)
        costs.append(-sum(t["reward"] for t in transitions))
    return costs
