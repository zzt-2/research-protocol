# [S013] PROMPT-012 双口径历史结论重审

> 2026-07-13 | GW Step 4a 维度 D 审计 | 状态：完成

## 目标

用 fixed-label BER 与 permutation-invariant BER、每格 10 个共享 seeds，复核 S005 发散、D014 极化串扰、D015 ML 长序列失效、S009/D012 ML vs CMA 四项历史结论。

## 记录

执行了三个隔离审计：S005 四关键格共 40 trials；N=5M、f_G=30 的 CMA/ML/oracle 长序列 10 trials；N=2M、f_G=30/100/1000 的 CMA/ML/oracle 短序列 30 trials。所有 ML trial 显式记录 Torch seed；长/短序列把信号模型、SOP、T_S、GG 参数、CMA μ/tap、训练/评估切片冻结进实验签名，S005 在 parameters 中显式记录同类参数；结果 JSON 保存覆盖实际脚本依赖的 SHA。

四项结论：

1. S005 **需修正**：18/40 发散全是权重范数爆炸，交换未被计为发散；μ 主导保留，但 μ=1e-3 仍有 3/20 发散，只能称低风险。
2. D014 **需修正**：N=5M late 的 CMA 为 clean-swap 8/10、degraded-swap 2/10，无同源/非交换塌缩/发散；fixed `0.47672`→PI `0.03174`，不是“等于断开”。
3. D015 **需修正且真失效叙事被否证**：ML fixed `0.49741`→PI `0.00523`，10/10 clean-swap，接近 oracle `0.00423`。
4. S009/D012 **成立但限 N=2M**：三 f_G 的 full-test PI 下 ML 均比 CMA 低 3.04–3.83×，逐 seed 均为 10/10；fixed 与 PI 相同，差距不是排列假象。

完整数字、per-seed 与分类见 `projects/simulation/explore/cma-fade-divergence/PROMPT_012_REPORT.md`。三个独立 verifier 均在元数据缺口修复后给出 PASS；正式实验未因元数据修复而重跑，trials/summaries digest 保持不变。

### 迭代计数器

- S005 元数据：1 轮 review（缺 script SHA）→ TDD 修复 → PASS。
- 长序列元数据：1 轮 review（缺显式 torch_seed）→ TDD 修复 → PASS。
- 短序列元数据：1 轮 review（experiment signature 未冻结 T_S）→ TDD 修复 → PASS。
- 否决条件：任一独立 verifier 重算不一致、seed/cell 不完整、脚本 SHA 不匹配即不得形成 D018；均未触发。

## 决策引用

- D018：双口径审计修正 D006/D014/D015，并确认 S009/D012 的 N=2M PI 优势（新建）。

## 范围确认

- 本轮是否在 scope boundary 内：是（GW Step 4a 维度 D 的既有结论审计；未实现新方法、未进入 Contract）。

## 后续

主控下一轮只需基于 D018 决定论文叙事和方法层是否继续；不得恢复“ML 长序列真失效”或“偏振交换等于断开”的旧表述。PI-BER 必须连同 pilot/帧头流标识开销说明。
