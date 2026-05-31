# Handoff: RIS Phase DRL — SAC 实验

> 来源: D018-D021 (CCAN+TD3 4轮失败) | 交接目标: 尝试 CCAN+SAC，利用熵正则逃离 Fixed 吸引子
> 文件名: H003-sac-experiment.md

## 已完成

- CCAN Actor + CCANCritic 实现：`baselines/ccan.py`
- TD3Agent 已支持注入自定义 actor/critic：`baselines/td3.py`
- train.py/eval.py 已支持 `--algo ccan_td3 --ablation {a1,a2,a3}`
- 4 轮训练确认：avg 停在 Fixed 水平（~1290），best=1670 远超 PSO=1554
- 根因：TD3 的 Gaussian 探索噪声 + mean Q gradient 无法从稀疏好信号中学习
- 方向归档记录：decision_log D021, code-quality.md D3 模式

## 不要做什么

- 不要再用 TD3（已验证 4 轮不行）
- 不要修改 simulator 核心模块
- 不要改 Contract 的 hypothesis/success_signal/failure_signal
- 不要忘记之前的教训：先验证 SAC 能否超越 Fixed，再投入大量实验

## SAC 实验方案

### 动机
SAC 的熵正则项 `α * log π(a|s)` 鼓励策略保持随机性，天然对抗 Fixed 吸引子。TD3 是确定性策略 + 外加噪声，探索是被动的；SAC 是随机策略 + 熵奖励，探索是主动的。

### 实现步骤

1. **修改 SACAgent 支持自定义 actor/critic**：类似 TD3Agent 的修改，给 SACAgent 加 actor/critic 参数
2. **CCAN+SAC 集成**：
   - Actor: CCANActor（同 TD3 版本）
   - Critic: CCANCritic（同 TD3 版本）
   - SAC 的 entropy coefficient α 自动调节
3. **训练**：`--algo ccan_sac --seed 0 --episodes 500 --no-wandb` Quick Test
4. **对比**：与 TD3 的 avg/best 对比

### 关键文件

| 文件 | 路径 | 说明 |
|------|------|------|
| CCAN Actor/Critic | `baselines/ccan.py` | 已实现 |
| SAC Agent | `baselines/sac.py` | 需加 actor/critic 注入 |
| TD3 Agent (参考) | `baselines/td3.py` | 已修改的注入模式 |
| 训练入口 | `baselines/train.py` | 需加 ccan_sac 选项 |
| 评估 | `baselines/eval.py` | 需加 ccan_sac 选项 |
| Config | `simulator/config.py` | N=100, M=8, K=4, κ=10dB |

### 判定标准

- Quick Test 500 ep: 如果 SAC avg > 1320（>1.02× Fixed=1292），继续完整实验
- 如果 SAC avg 仍在 ~1290，确认 off-policy RL + LoS 主导 是死区，正式归档

## 关键 Baseline 数据（对比用）

| 方法 | avg (训练) | best | det eval avg |
|------|-----------|------|-------------|
| TD3+MLP | 1291 | ~1300 | 1281 |
| CCAN+TD3 | 1301 | 1670 | 1275 |
| Fixed (θ=π) | 1292 | ~1400 | 1292 |
| PSO | 1554 | ~1700 | — |
| Random | 430 | ~800 | — |
