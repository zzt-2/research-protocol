"""训练后统一评估器模板 — 评估、对比、绘图、报告生成。

使用方式：
    evaluator = Evaluator(env, config)
    results = evaluator.evaluate(model, n_episodes=10, seeds=[42, 123, 456])
    comparison = evaluator.compare([results_a, results_b], ["HGAT", "DQN"])
    evaluator.plot_convergence({"HGAT": rewards_a, "DQN": rewards_b},
                               ["HGAT", "DQN"], "convergence.png")
    evaluator.plot_comparison([results_a, results_b], ["HGAT", "DQN"], "bar.png")
    report = evaluator.generate_report([results_a, results_b], ["HGAT", "DQN"])
"""
import os
from typing import Any, Dict, List, Optional, Tuple

import numpy as np


class Evaluator:
    """训练后统一评估：多种子评估 + 统计检验 + 可视化 + 报告。"""

    def __init__(self, env: Any, config: Any):
        """
        Args:
            env: gymnasium.Env 实例
            config: SimConfig dataclass 实例
        """
        self.env = env
        self.config = config

    # ------------------------------------------------------------------
    # 评估
    # ------------------------------------------------------------------

    def evaluate(self, model: Any, n_episodes: int = 10,
                 seeds: Optional[List[int]] = None) -> dict:
        """加载模型 → eval 模式 → 跑 N episode → 收集指标。

        Args:
            model: 训练好的模型（需实现 eval() 和 act() 方法）
            n_episodes: 每个 seed 评估的 episode 数
            seeds: 随机种子列表（默认 [42, 123, 456]）

        Returns:
            {
                "seeds": [42, 123],
                "per_seed_rewards": [[ep0_r, ep1_r, ...], ...],
                "mean_reward": float, "std_reward": float,
                "ci_95": float,
                "metrics": {"M1_mean": ..., "M1_std": ..., ...}
            }
        """
        if seeds is None:
            seeds = [42, 123, 456]

        model.eval()  # --- CUSTOMIZE --- 如果是 PyTorch 模型

        per_seed_rewards: List[List[float]] = []
        per_seed_metrics: List[Dict[str, float]] = []

        for seed in seeds:
            seed_rewards = []
            seed_metrics_sum: Dict[str, float] = {}

            for ep in range(n_episodes):
                # --- CUSTOMIZE --- 适配你的 env.reset / model.act 接口
                try:
                    import torch
                    obs, info = self.env.reset(seed=seed + ep)
                except Exception:
                    obs = self.env.reset(seed=seed + ep)
                    info = {}

                total_reward = 0.0
                done = False
                step_metrics: Dict[str, float] = {}

                while not done:
                    # --- CUSTOMIZE --- 模型推理，需要 torch.no_grad
                    try:
                        import torch
                        with torch.no_grad():
                            action = model.act(obs)
                    except ImportError:
                        action = model.act(obs)

                    # --- CUSTOMIZE --- env.step 返回值适配
                    step_result = self.env.step(action)
                    if len(step_result) == 5:
                        obs, reward, terminated, truncated, info = step_result
                        done = terminated or truncated
                    else:
                        obs, reward, done, info = step_result

                    total_reward += reward
                    # 从 info 中提取指标
                    if isinstance(info, dict):
                        for k, v in info.items():
                            if isinstance(v, (int, float)):
                                step_metrics[k] = step_metrics.get(k, 0.0) + v

                seed_rewards.append(total_reward)
                # 平均化 step 级指标
                for k, v in step_metrics.items():
                    seed_metrics_sum[k] = seed_metrics_sum.get(k, 0.0) + v / n_episodes

            per_seed_rewards.append(seed_rewards)
            per_seed_metrics.append(seed_metrics_sum)

        # 汇总：跨 seed 的 mean ± std + 95% CI
        all_mean_rewards = [np.mean(rs) for rs in per_seed_rewards]
        mean_reward = float(np.mean(all_mean_rewards))
        std_reward = float(np.std(all_mean_rewards, ddof=1)) if len(all_mean_rewards) > 1 else 0.0
        # 95% CI: t_{0.025, df=n-1} * std / sqrt(n)，小样本用近似值
        ci_95 = 0.0
        if len(all_mean_rewards) > 1:
            from scipy import stats as _sci_stats
            t_val = _sci_stats.t.ppf(0.975, df=len(all_mean_rewards) - 1)
            ci_95 = float(t_val * std_reward / np.sqrt(len(all_mean_rewards)))

        return {
            "seeds": seeds,
            "per_seed_rewards": per_seed_rewards,
            "mean_reward": mean_reward,
            "std_reward": std_reward,
            "ci_95": ci_95,
            "per_seed_metrics": per_seed_metrics,
        }

    # ------------------------------------------------------------------
    # 统计对比
    # ------------------------------------------------------------------

    def compare(self, results_list: List[dict],
                labels: List[str]) -> dict:
        """多模型对比：配对 t 检验 / Wilcoxon → 生成对比表格。

        Args:
            results_list: 每个模型的 evaluate() 返回值
            labels: 模型名称列表

        Returns:
            {
                "comparisons": [
                    {"A": "HGAT", "B": "DQN",
                     "p_value": 0.03, "test": "ttest_rel", "significant": true}
                ],
                "summary_table": "markdown 表格字符串"
            }
        """
        # 提取每个模型跨 seed 的平均 reward
        model_means = []
        for res in results_list:
            means = [np.mean(rs) for rs in res["per_seed_rewards"]]
            model_means.append(means)

        comparisons = []
        for i in range(len(results_list)):
            for j in range(i + 1, len(results_list)):
                a_means = model_means[i]
                b_means = model_means[j]

                p_val, test_name = self._paired_test(a_means, b_means)
                comparisons.append({
                    "A": labels[i],
                    "B": labels[j],
                    "p_value": round(p_val, 4),
                    "test": test_name,
                    "significant": p_val < 0.05,
                })

        # 生成汇总表格
        header = "| 模型 | Mean Reward | Std | 95% CI |"
        sep = "|------|------------|-----|--------|"
        rows = []
        for label, res in zip(labels, results_list):
            rows.append(
                f"| {label} | {res['mean_reward']:.4f} | "
                f"{res['std_reward']:.4f} | ±{res['ci_95']:.4f} |"
            )
        # 添加显著性检验行
        sig_rows = []
        for c in comparisons:
            sig_mark = "**" if c["significant"] else ""
            sig_rows.append(
                f"| {c['A']} vs {c['B']} | p={c['p_value']} "
                f"({c['test']}) | {sig_mark}{'显著' if c['significant'] else '不显著'}{sig_mark} | |"
            )

        summary_table = "\n".join([header, sep] + rows + [""] + sig_rows)

        return {"comparisons": comparisons, "summary_table": summary_table}

    # ------------------------------------------------------------------
    # 可视化
    # ------------------------------------------------------------------

    def plot_convergence(self, rewards_dict: Dict[str, List[float]],
                         labels: List[str], output_path: str) -> None:
        """收敛曲线图（reward vs episode）。

        Args:
            rewards_dict: {模型名: episode_rewards 列表}
            labels: 图例标签
            output_path: 输出图片路径
        """
        try:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
        except ImportError:
            print("[WARN] matplotlib 未安装，跳过绘图")
            return

        fig, ax = plt.subplots(figsize=(10, 6))
        for label in labels:
            rewards = rewards_dict.get(label, [])
            if not rewards:
                continue
            # --- CUSTOMIZE --- 窗口大小根据 episode 总数调整
            window = max(1, len(rewards) // 20)
            smoothed = np.convolve(rewards, np.ones(window) / window, mode="valid")
            ax.plot(smoothed, label=label, alpha=0.9)
            ax.plot(rewards, alpha=0.2)  # 原始曲线（半透明）

        ax.set_xlabel("Episode")
        ax.set_ylabel("Reward")
        ax.set_title("训练收敛曲线")
        ax.legend()
        ax.grid(True, alpha=0.3)
        fig.tight_layout()
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        fig.savefig(output_path, dpi=150)
        plt.close(fig)

    def plot_comparison(self, results_list: List[dict],
                        labels: List[str], output_path: str) -> None:
        """多场景柱状图（mean + std error bar）。

        Args:
            results_list: 每个模型的 evaluate() 返回值
            labels: 模型名称
            output_path: 输出图片路径
        """
        try:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
        except ImportError:
            print("[WARN] matplotlib 未安装，跳过绘图")
            return

        means = [r["mean_reward"] for r in results_list]
        stds = [r["std_reward"] for r in results_list]

        fig, ax = plt.subplots(figsize=(8, 5))
        x = np.arange(len(labels))
        bars = ax.bar(x, means, yerr=stds, capsize=5, alpha=0.8,
                       color=["#4C72B0", "#DD8452", "#55A868", "#C44E52"][:len(labels)])

        # 标注数值
        for bar, m, s in zip(bars, means, stds):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + s + 0.01,
                    f"{m:.3f}±{s:.3f}", ha="center", va="bottom", fontsize=9)

        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.set_ylabel("Mean Reward")
        ax.set_title("模型对比（mean ± std）")
        ax.grid(True, axis="y", alpha=0.3)
        fig.tight_layout()
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        fig.savefig(output_path, dpi=150)
        plt.close(fig)

    # ------------------------------------------------------------------
    # 报告生成
    # ------------------------------------------------------------------

    def generate_report(self, results_list: List[dict],
                        labels: List[str]) -> str:
        """生成 markdown 报告（与 templates.md 的 experiment_result 模板对齐）。

        Returns:
            markdown 格式的报告字符串
        """
        lines = ["# 评估报告\n"]
        lines.append("## 定量结果\n")

        # 表头
        header = "| 指标 |"
        sep = "|------|"
        for label in labels:
            header += f" {label} |"
            sep += "------|"
        header += " 单位 |"
        sep += "------|"
        lines.append(header)
        lines.append(sep)

        # Reward 行
        reward_row = "| Mean Reward |"
        for res in results_list:
            reward_row += f" {res['mean_reward']:.4f}±{res['std_reward']:.4f} |"
        reward_row += " - |"
        lines.append(reward_row)

        # --- CUSTOMIZE --- 添加更多 Contract 指标行
        # 从 per_seed_metrics 中提取通用指标
        all_metric_keys: List[str] = []
        for res in results_list:
            if res.get("per_seed_metrics"):
                for k in res["per_seed_metrics"][0]:
                    if k not in all_metric_keys:
                        all_metric_keys.append(k)

        for mk in all_metric_keys:
            row = f"| {mk} |"
            for res in results_list:
                if res.get("per_seed_metrics"):
                    vals = [m.get(mk, 0.0) for m in res["per_seed_metrics"]]
                    m, s = np.mean(vals), np.std(vals)
                    row += f" {m:.4f}±{s:.4f} |"
                else:
                    row += " - |"
            row += " - |"
            lines.append(row)

        # 统计显著性
        lines.append("\n## 统计显著性\n")
        comparison = self.compare(results_list, labels)
        for c in comparison["comparisons"]:
            sig = "显著" if c["significant"] else "不显著"
            lines.append(
                f"- {c['A']} vs {c['B']}: p = {c['p_value']:.4f} "
                f"（{c['test']}），{sig}"
            )

        # 统计汇总表
        lines.append(f"\n## 汇总表\n")
        lines.append(comparison["summary_table"])

        return "\n".join(lines)

    # ------------------------------------------------------------------
    # 内部工具
    # ------------------------------------------------------------------

    @staticmethod
    def _paired_test(a: List[float], b: List[float]) -> Tuple[float, str]:
        """配对统计检验。优先 scipy ttest_rel，降级为简单差值比较。

        Returns:
            (p_value, test_name)
        """
        if len(a) < 2 or len(b) < 2:
            return 1.0, "insufficient_samples"

        try:
            from scipy.stats import ttest_rel, wilcoxon
            # 样本量 >= 10 优先 Wilcoxon（非参数）
            if len(a) >= 10:
                try:
                    stat, p = wilcoxon(a, b)
                    return float(p), "wilcoxon"
                except Exception:
                    pass
            stat, p = ttest_rel(a, b)
            return float(p), "ttest_rel"
        except ImportError:
            # 无 scipy 时降级：用均值差 / 合并标准差近似
            diff = np.array(a) - np.array(b)
            if np.std(diff) < 1e-10:
                return 1.0, "no_variance_fallback"
            z = abs(np.mean(diff)) / (np.std(diff) / np.sqrt(len(diff)))
            return 0.05 if z > 2.0 else 0.5, "z_approximation_fallback"
