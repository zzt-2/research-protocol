# [S013] PROMPT-012 双口径重审与 PROMPT-013 交换质量机制续接

> 2026-07-13 | GW Step 4a 维度 D 审计 | 状态：完成
> 2026-07-13 | 续接 PROMPT-013 机制验证 | 状态：PARTIAL（Q1 PASS；机制未确认）

## 目标

用 fixed-label BER 与 permutation-invariant BER、每格 10 个共享 seeds，复核 S005 发散、D014 极化串扰、D015 ML 长序列失效、S009/D012 ML vs CMA 四项历史结论。

续接目标：按修订后的连续指标把 N=5M 扩至 30 seeds；若 Q1 通过，再用预注册高/低差组验证交换质量机制。

## 记录

执行了三个隔离审计：S005 四关键格共 40 trials；N=5M、f_G=30 的 CMA/ML/oracle 长序列 10 trials；N=2M、f_G=30/100/1000 的 CMA/ML/oracle 短序列 30 trials。所有 ML trial 显式记录 Torch seed；长/短序列把信号模型、SOP、T_S、GG 参数、CMA μ/tap、训练/评估切片冻结进实验签名，S005 在 parameters 中显式记录同类参数；结果 JSON 保存覆盖实际脚本依赖的 SHA。

四项结论：

1. S005 **需修正**：18/40 发散全是权重范数爆炸，交换未被计为发散；μ 主导保留，但 μ=1e-3 仍有 3/20 发散，只能称低风险。
2. D014 **需修正**：N=5M late 的 CMA 为 clean-swap 8/10、degraded-swap 2/10，无同源/非交换塌缩/发散；fixed `0.47672`→PI `0.03174`，不是“等于断开”。
3. D015 **需修正且真失效叙事被否证**：ML fixed `0.49741`→PI `0.00523`，10/10 clean-swap，接近 oracle `0.00423`。
4. S009/D012 **成立但限 N=2M**：三 f_G 的 full-test PI 下 ML 均比 CMA 低 3.04–3.83×，逐 seed 均为 10/10；fixed 与 PI 相同，差距不是排列假象。

完整数字、per-seed 与分类见 `projects/simulation/explore/cma-fade-divergence/PROMPT_012_REPORT.md`。三个独立 verifier 均在元数据缺口修复后给出 PASS；正式实验未因元数据修复而重跑，trials/summaries digest 保持不变。

### PROMPT-013 续接结果

Q1 的 30 seeds（1000–1029）中，ML 相对 current scalar-error CMA 的超额 PI-BER 逐 seed 30/30 更低；CMA/ML 超额均值为 `0.0147177/0.00115397`，精确双侧 Wilcoxon `W=0, p=1.8626e-9`。clean≤0.05 与 clean<0.01 的分类分别为 CMA `25/5`、`20/10`，ML `29/1`、`25/5`，只作描述。

Q2 固定高差 1006/1017/1011、低差 1024/1028/1029。H_a 证伪；H_b 因 oracle 窗口常数导致 10/12 个相关系数不可定义，严格为 unknown，但 current/standard freeze 主阈值均 0/3 达标。H_c 确认两者同为 88 实自由度；同时发现 ML 交叉支路实际中心初始化为 1，而注释称 0、CMA 为 0。Standard CMA 在 1006/1017 上将 PI-BER 从约 `0.033/0.032` 降至约 `4.4e-5/4.7e-5`，否决把当前差异直接归因于“ML 的 MSE 天然优于经典 CMA”。完整证据见 `PROMPT_013_REPORT.md`。

### 迭代计数器

- S005 元数据：1 轮 review（缺 script SHA）→ TDD 修复 → PASS。
- 长序列元数据：1 轮 review（缺显式 torch_seed）→ TDD 修复 → PASS。
- 短序列元数据：1 轮 review（experiment signature 未冻结 T_S）→ TDD 修复 → PASS。
- 否决条件：任一独立 verifier 重算不一致、seed/cell 不完整、脚本 SHA 不匹配即不得形成 D018；均未触发。
- PROMPT-013：Q2 首轮 review 发现 H_b 缺失指标误投支持、Q1 未独立重算、trace 错一 block；1 轮 RED→GREEN 修复后复审 Ready=YES。正式 Q1/Q2 后由新 verifier 重算；机制确认门控未通过，不再迭代补假设。

## 决策引用

- D018：双口径审计修正 D006/D014/D015，并确认 S009/D012 的 N=2M PI 优势（新建）。
- D020：拒绝把 current scalar-error CMA 的 30-seed 劣势写成 ML 相对经典 CMA 的机制贡献（新建）。

## 范围确认

- 本轮是否在 scope boundary 内：是（PROMPT-012/013 均属 GW Step 4a 维度 D 的既有结论审计与机制验证；未进入 Contract）。

## 后续

PROMPT-013 不形成机制贡献。若继续，先统一 standard CMA 与 ML 初始化合同，再预注册 30-seed 三方比较；不得把 current scalar-error CMA 泛称经典 CMA。PI-BER 必须连同 pilot/帧头流标识开销说明。PROMPT-014 的后续选择仍独立处理。
