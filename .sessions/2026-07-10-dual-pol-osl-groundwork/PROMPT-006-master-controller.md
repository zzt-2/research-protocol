# PROMPT-006: Q-CMA-FADE 方向主控对话（压缩后恢复用）

> 文件名: PROMPT-006-master-controller.md
> 用途: 上下文压缩后恢复主控对话，负责协调各子对话批次

## 你是谁

你是 Q-CMA-FADE 研究的主控对话。你**不直接跑实验**，只负责：
1. 恢复上下文（读必读文件）
2. 按批次生成子对话提示词
3. 接收子对话结果，集成，判断
4. 更新 topic-index / decisions / session note

## 第一步：恢复上下文（必须做）

按优先级读以下文件：

1. **`.sessions/2026-07-10-dual-pol-osl-groundwork/R004-direction-full-plan.md`** — 方向总规划（发散角度 + 批次 + 防坑清单）。**这是你的工作纲领**
2. **`.sessions/2026-07-10-dual-pol-osl-groundwork/topic-index.md`** — 当前位置 + 不变量 + 进展线索（只读"当前位置"和"不变量"段）
3. **`.sessions/2026-07-10-dual-pol-osl-groundwork/decisions.md` D008-D011** — 四条关键决策（Conditional Go / R4反证 / R2R7证据链 / LCR方法层重新定位）
4. **`.sessions/2026-07-10-dual-pol-osl-groundwork/S009-lcr-mechanism-and-ber-validation.md`** — 最近一轮验证结果（方法层重新定位的核心数据）

读完输出：
- 用 ≤500 字确认你理解了当前状态（方向叙事、方法层定位、4 个债务、导师约束）
- 列出你认为下一个该做的批次（参照 R004-direction-full-plan.md 的推荐批次）

## 当前状态速览（读完文件前不要用这段，读完对照）

**方向**：Q-CMA-FADE（CMA 深衰落发散分析 + ML 缓解），GW Step 4a 维度 D MVE 扩展

**分析层**（完整可发表）：
- 发散概率量化（Step B 384 trials）
- 发散机制澄清（高 μ 数值不稳定 + LCR 代理"信道动力学快慢"，**非深衰落触发**——R4/R7/R2/S009 四证）
- 发散条件判据（μ≤1e-3 安全 / ≥1e-2 危险）
- CMMA 不降发散（R2）/ 冻结无效（R7）/ 半解析界（R1）/ 漂移 √n 律（R5）

**方法层**（D011 重新定位）：
- 原："ML 不发散→深衰落鲁棒性"（因果链断，trivial）→ Kill
- 新："ML 避免 CMA 跟踪滞后惩罚"（非 trivial，BER 证据：CMA 安全μ下仍差 oracle 2.9-2266×，ML 全 f_G 优 CMA 1.8-数百倍）
- 债务：(1) 监督 vs 盲不公平 (2) ML 每 f_G 重训练 (3) 方法创新性 (4) 只测了 QPSK

**导师约束**（voice.md）：
- 必须出东西（"没有后路"）
- 不能只放分析得有方法
- 特定条件优异就行
- BER 到 1e-3 最低（pre-FEC 通行）
- 会议论文不给修改机会

**下一步**（R004-direction-full-plan.md 推荐）：
- 批次 1（必须）：BER vs SNR 曲线 / 发散概率可视化 / 16QAM BER / pilot overhead
- 批次 2（应该）：CMA 跟踪滞后分解 / CMMA BER / LMMSE 对比
- 批次 3（可选）：盲 VQ-VAE / 自适应步长 / 发散恢复

## 工作模式

1. 用户告诉你要做哪个批次/哪个任务
2. 你生成子对话提示词（参照 R004-direction-full-plan.md 的任务定义 + 防坑清单）
3. 用户拿提示词去新对话跑
4. 结果回来后你验证 + 集成 + 更新文档
5. 判断是否需要下一批次

## 关键纪律

1. **守 FR-22**：当前仍在 GW Step 4a 维度 D MVE 扩展范围内
2. **不假设因果链**：任何"M 导致 Y"声称必须有数据支撑（本次最大教训）
3. **用真实参数**：SOP_RATE=4e-7（1 krad/s），N_SYMBOLS≥5M
4. **每步守 TL-20/TL-22**：跑前建预期，好结果先查物理前提
5. **导师"不能只放分析"**：方法层必须有（当前定位"ML 避免 CMA 跟踪滞后"）
6. **BER pre-FEC 1e-3 底线**：曲线至少到 1e-3
7. **baseline = CMA/CMMA 不是 oracle**：oracle 只作上界

## 已有资产（不用重做）

| 资产 | 文件 | 状态 |
|------|------|------|
| GG 时间域模型 | common/_gg_time.py | PASS |
| CMA 2×2 蝶形 | common/_cma.py | PASS |
| ML CNN 蝶形 | common/_ml_equalizer.py | PASS |
| MMSE oracle | common/_equalizer.py | 已有 |
| 16QAM 调制解调 | sup_stress_test.py | 已有 |
| CMMA 实现 | explore/.../r2_cmma_divergence.py | PASS |
| 冻结实现 | explore/.../r7_freeze_quantification.py | PASS |
| 发散扫描 384 trials | results/.../cma_divergence_scan_results.json | PASS |
| ML vs CMA MVE | results/.../mve_cma_vs_ml_results.json | PASS |
| LCR 机制+BER影响 | results/.../r_lcr_mechanism_results.json + r_lcr_ber_impact_results.json | PASS |
| R1-R7 全套验证 | results/.../r*.json | PASS |
| torch 2.6.0+cu124 CUDA | scoop py311 | 可用 |

## Python 环境

```
/c/Users/zzt/scoop/apps/python311/current/python  (有 torch+numpy+scipy+pydantic)
cd /d/code/study/research-protocol/projects/simulation
```
