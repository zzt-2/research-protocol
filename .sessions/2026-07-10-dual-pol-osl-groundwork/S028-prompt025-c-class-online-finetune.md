# [S028] PROMPT-025 C 类在线微调探索

> 2026-07-16 | GW Step 1 + Step 4a 维度 D | 完成

## 目标

按 H013 只执行 C 类：先检索，再用 D031 过滤 C2/C3，对 C1 跑预注册在线微调 MVE，并立即落盘 Go/Kill。

## 记录

### 框架位置与门控

- 当前步骤：GW Step 1 防撞车检索 → Step 4a 四判据快判 → 维度 D MVE。
- C1 四判据全过：攻 test 段固定权重随 SOP 漂移失配；产出为周期在线适配；L0/D022 baseline 明确；可同信道同初始化配对。
- C2 SOP 数据增强、C3 curriculum 均不触及 test 段状态，依 D031 时序正交 defer。

### 检索

项目工具 `bash tools/search` 首轮因 Exa 额度耗尽未落盘；随后显式使用 S2/OpenAlex/arXiv 重跑，落盘：

- `search-archive/2026-07-16/online-fine-tuning-optical-equalizer.json`
- `search-archive/2026-07-16/online-adaptation-neural-network-optical-communication.json`

强邻近先例为 AdaNN 2020 JLT 在线半监督均衡与 2023 JLT joint PMD tracking/decision-directed online learning；未命中同一星地 FSO+GG+SOP lock-swap 场景，依 D030 允许迁移适配进入 MVE。

### MVE

隔离脚本 `projects/simulation/explore/cma-fade-divergence/prompt025_c1_online_finetune.py`，未修改 common/。每 seed 只离线训练一次 L0，再克隆完全相同权重给六档 C1 和 lr=0 消融；test 状态连续，每 K blocks 用最近 1024 个已知符号监督更新一步。该访问属于 pilot/genie-assisted 可行性上界，非 blind。

结果 `projects/simulation/results/cma-fade-divergence/prompt025_c1_online_finetune.json` 完整 5 seeds：六档均 0/5 胜、p=1.0，mean PI 全不低于 L0；lr=0 逐 seed 完全返回 L0。结论 KILL，见 D032。

复现债务：确定性 torch seed 下 L0 mean PI=`7.936e-5`，显著低于 D031 `0.01020`。本轮只采用同初始权重配对增量结论，不用绝对值推翻历史决策。

## 决策引用

- D032：C 类 C1 KILL、C2/C3 defer（新建）

## 范围确认

- 本轮是否在 scope boundary 内：是（H013 方法层增强 C 类；分析层与 common/ 均未动）

## 后续

主控按 H013 顺序进入 B 类。若未来复活 C1 的 decision-directed/meta-learning 化身，须因邻近先例重新做新颖性边界与信息访问公平性门控。
