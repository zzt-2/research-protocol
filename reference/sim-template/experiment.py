"""实验记录器模板 — 训练过程中自动记录配置、指标、训练曲线。

产出 JSON 与 templates.md 的 experiment_result 模板对齐。
使用方式：
    rec = ExperimentRecorder("results/exp001")
    rec.start(config, "hgat", seed=42)
    for ep in range(100):
        rec.log_episode(ep, reward, metrics={"sinr_mean": 12.3})
        rec.log_training(policy_loss=0.5, value_loss=0.3, entropy=1.2, lr=3e-4)
    rec.finish(final_metrics={"M1_mean": 0.85, "M1_std": 0.03})
"""
import json
import os
import subprocess
from dataclasses import asdict, fields, is_dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional


class ExperimentRecorder:
    """训练过程记录器，产出结构化 JSON 供 evaluate.py 和报告生成消费。"""

    # --- CUSTOMIZE --- 实验编号前缀，按项目修改
    EXPERIMENT_PREFIX = "E"

    _counter = 0  # 类级别计数器，自动递增实验 ID

    def __init__(self, output_dir: str = "results"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

        # 内部状态，start() 时初始化
        self._experiment_id: str = ""
        self._model: str = ""
        self._seed: int = 0
        self._config_snapshot: Dict[str, Any] = {}
        self._git_hash: str = ""
        self._timestamp: str = ""
        self._episode_rewards: List[float] = []
        self._episode_metrics: List[Dict[str, Any]] = []
        self._training_log: Dict[str, List[float]] = {
            "policy_loss": [],
            "value_loss": [],
            "entropy": [],
        }
        self._started = False

    # ------------------------------------------------------------------
    # 公开接口
    # ------------------------------------------------------------------

    def start(self, config: Any, model_name: str, seed: int) -> None:
        """开始记录：保存配置快照、git hash、timestamp。

        Args:
            config: SimConfig dataclass 实例（或其他可序列化配置对象）
            model_name: 模型/方法名称（如 "hgat", "dqn", "ppo_gnn"）
            seed: 随机种子
        """
        ExperimentRecorder._counter += 1
        self._experiment_id = f"{self.EXPERIMENT_PREFIX}{ExperimentRecorder._counter:03d}"
        self._model = model_name
        self._seed = seed
        self._config_snapshot = self._snapshot_config(config)
        self._git_hash = self._get_git_hash()
        self._timestamp = datetime.now().isoformat(timespec="seconds")
        self._started = True

    def log_episode(self, episode: int, reward: float,
                    metrics: Optional[Dict[str, Any]] = None) -> None:
        """记录每个 episode 的结果。

        Args:
            episode: episode 编号
            reward: 该 episode 总奖励
            metrics: 附加指标字典（如 sinr_mean、fairness_index）
        """
        self._assert_started()
        self._episode_rewards.append(reward)
        entry = {"episode": episode, "reward": reward}
        if metrics:
            entry.update(metrics)
        self._episode_metrics.append(entry)

    def log_training(self, policy_loss: float, value_loss: float,
                     entropy: float, lr: float) -> None:
        """记录训练曲线（每个 update step 调用一次）。

        Args:
            policy_loss: 策略损失
            value_loss: 价值损失
            entropy: 策略熵
            lr: 当前学习率
        """
        self._assert_started()
        self._training_log["policy_loss"].append(policy_loss)
        self._training_log["value_loss"].append(value_loss)
        self._training_log["entropy"].append(entropy)

    def finish(self, final_metrics: Optional[Dict[str, Any]] = None) -> str:
        """结束记录，生成 JSON 文件。

        Args:
            final_metrics: 最终评估指标（如 {"M1_mean": 0.85, "M1_std": 0.03}）

        Returns:
            生成的 JSON 文件路径
        """
        self._assert_started()

        # --- CUSTOMIZE --- type 字段根据 Experiment List 填写
        record = {
            "experiment_id": self._experiment_id,
            "type": "核心",  # 核心/对比/消融/鲁棒，按需修改
            "model": self._model,
            "seed": self._seed,
            "config_snapshot": self._config_snapshot,
            "git_hash": self._git_hash,
            "timestamp": self._timestamp,
            "episode_rewards": self._episode_rewards,
            "episode_metrics": self._episode_metrics,
            "training_log": self._training_log,
            "final_metrics": final_metrics or {},
        }

        fname = f"{self._experiment_id}_{self._model}_seed{self._seed}.json"
        fpath = os.path.join(self.output_dir, fname)
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(record, f, ensure_ascii=False, indent=2)

        self._started = False
        return fpath

    # ------------------------------------------------------------------
    # 内部工具
    # ------------------------------------------------------------------

    @staticmethod
    def _snapshot_config(config: Any) -> Dict[str, Any]:
        """将配置对象转为可序列化字典。支持 dataclass 和普通对象。"""
        if is_dataclass(config) and not isinstance(config, type):
            return asdict(config)
        # 降级：尝试 __dict__
        if hasattr(config, "__dict__"):
            result = {}
            for k, v in vars(config).items():
                try:
                    json.dumps({k: v})  # 测试可序列化
                    result[k] = v
                except (TypeError, ValueError):
                    result[k] = str(v)
            return result
        return {"_raw": str(config)}

    @staticmethod
    def _get_git_hash() -> str:
        """获取当前 git commit 的短 hash。"""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--short", "HEAD"],
                capture_output=True, text=True, timeout=5,
            )
            return result.stdout.strip() if result.returncode == 0 else "unknown"
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return "unknown"

    def _assert_started(self) -> None:
        if not self._started:
            raise RuntimeError("必须先调用 start() 再记录数据")
