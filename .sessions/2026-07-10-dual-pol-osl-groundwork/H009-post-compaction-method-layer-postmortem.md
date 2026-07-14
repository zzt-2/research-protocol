# Handoff: 方法层全部寄了——压缩后回去复盘流程找漏掉的东西

> 来源: S016-S019（方法层多轮探索）| 交接目标: 压缩后系统复盘，搞清方法层为什么全军覆没，找漏掉的方向
> 文件名: H009-post-compaction-method-layer-postmortem.md
> 日期: 2026-07-14

## 已完成边界

Q-CMA-FADE 项目方法层经 ~10 轮探索，**所有方法层方向全部 Kill 或低天花板**。分析层完整且稳。压缩后要做的不是继续挖下一个方法坑，而是**系统复盘流程找漏掉的东西**。

## 不要做什么（Dead Ends，最高优先级——别重蹈）

### 方法层全部已验证失败的方向

1. ❌ **ML 缓解 CMA 发散（Q-CMA-FADE 方法层原点）**：D022 Go 但 D023 收窄——ML 优于 standard-CMA 只在 N=5M/f_G=30 窄域（30seeds p=1.19e-6）；N=2M 多参数点反转（f_G=1000 standard-CMA PI=0.0021 碾压 ML=0.0417，ML 只赢 1/5）。机制说不清（D020 H_a 代价函数证伪 / H_b 在线vs离线 unknown）。
2. ❌ **盲 VQ-VAE（PROMPT-014）**：D019 deferred。sanity gate 设计缺陷（首末 loss 不同 batch 不可比），11/30 cells 候选被拒。A/B 二选一挂起。
3. ❌ **交换质量机制深挖（PROMPT-013 Q2）**：D020。H_a/H_b 全失败。standard-CMA 在 2/3 high-gap seed 消除 ML 优势（0.033→4.5e-5）。
4. ❌ **自适应步长 CMA（R005 方向1）**：JR-CMA（L-DP8 ACP 2025）在同场景（FSO+深衰落）占点三机制（AGC+误差阈值重置+自适应步长）。成熟先例不能作原创。+ 自有 R7 冻结无效/R4 深衰落非触发反向证伪。
5. ❌ **Q-DP3 预测性 fade 检测驱动恢复（路线 B）**：D026 物理 Kill。压 μ MVE FAIL（PI 0.0362 比常规 0.0275 更差，0/5 胜，p=0.5）。**根因 = BER 恶化是 SOP 极化串扰（D014），不是 fade/发散**。三类恢复动作全失效：冻结（R7 无效）+ 压 μ（本次更差）+ CMA 重锁定（AFD/重收敛=0.25 来不及）。
6. ❌ **DD-CMA/酉约束/修正在线跟踪（PROMPT-011）**：成熟先例（DD/两级 CMA/SVD 文献充分覆盖）。
7. ❌ **盲目堆 ML 类型（CNN/LSTM/Transformer）**：都是 2×2 蝶形固定权重同构，都一样交换。

### 主控纪律 Dead End
8. ❌ **主控不自己占上下文跑诊断**：用户明确纠正过（"别忘了你是主控"）。诊断/实验交子 agent / 新对话，主控只负责核验+判断+封装提示词。

## 必读（压缩后恢复时按优先级读）

1. `.sessions/2026-07-10-dual-pol-osl-groundwork/topic-index.md`（**当前位置段 + 进展线索全量**——S001-S019 + R001-R006 的完整摘要都在）
2. `.sessions/2026-07-10-dual-pol-osl-groundwork/decisions.md` **D014**（SOP 极化串扰——**理解方法层为什么全寄的钥匙**）+ **D023**（ML 优势收窄）+ **D026**（Q-DP3 Kill，压μ FAIL）+ **D006**（发散 μ 主导）+ **D022**（ML 优于 standard-CMA 窄域 Go）
3. `.sessions/2026-07-10-dual-pol-osl-groundwork/S019-prompt019-mu-compress-mve-fail.md`（Q-DP3 死因定位——SOP 正交）
4. `projects/thesis-fso/literature_notes.md`（候选池 + 角度素材占点地图——**回候选池找漏掉的方向时必读**）
5. `.sessions/2026-07-09-thesis-writing/voice.md`（导师约束：必须出东西/不能只分析/BER 到 1e-3/会议不给修改机会）
6. `thesis-lessons.md`（TL-30 跳框架 / TL-04 增量非空白 / TL-27 上界 Kill）

## 接口变更（如有代码改动）

无（本轮无新代码改动，P019 脚本已由执行对话提交）

## 失败数据附录（方法层全军覆没的核心数据）

### 核心模式：所有方法层方向都在治"发散/fade"，但 BER 恶化真因是 SOP

| 方向 | 死因 | 共同根问题 |
|---|---|---|
| ML 缓解发散 | 优势窄+机制不清 | D014: 真因是 SOP 串扰不是发散 |
| 盲 VAE | gate 崩 | 不解决 SOP |
| 交换质量机制 | H_a/H_b 失败 | 还是 SOP |
| 自适应步长 | JR-CMA 占点 | 成熟先例 |
| Q-DP3 fade 检测恢复 | 压μ FAIL | **BER 恶化是 SOP 不是 fade，恢复动作无载体** |

**可能漏掉的东西（压缩后系统复盘时重点想）**：D014 的 SOP 极化串扰发现是最有价值的分析层产出，但**从来没被转成方法层方向**——一直在发散/fade 上打转。SOP 串扰 = 2×2 蝶形在 SOP 旋转下锁定跳变（X 路锁到 Y 路）。如果方法层直接针对 SOP 串扰（而非发散/fade）设计，是否有空间？这个角度从未评估过。

### 各方向的关键数字（主控独立核验过）

- D022 ML 优于 standard-CMA：30/30 → 29/30, exact p=1.19e-6, 仅 N=5M/f_G=30
- D023 收窄：N=2M f_G=1000 standard-CMA PI=0.0021 vs ML=0.0417, ML 赢 1/5
- D024 fade 前兆：85% 事件可提前 ≥2µs，中位 9µs（子agent#1 悲观被推翻）
- D026 压μ FAIL：PI 0.0362 vs 常规 0.0275, 0/5 胜, p=0.5
- 分析层稳：发散 μ 主导（384 trials）+ SOP 串扰（D014）+ CMMA 不降发散（R2）+ 冻结无效（R7 ΔP_div=0 全24组合）+ LCR 伪相关（R4）

## 已知债务

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|---|---|---|---|
| 方法层无好方向 | 导师"必须出东西/不能只分析" | 全 Kill 或低天花板 | 压缩后系统复盘找漏掉的 |
| 监督 vs 盲不公平 | D008 债务1 | D019 deferred | 方法层重新定位后 |
| 方法照搬 Qin | D008 债务2 | 改动1 新颖性 PASS 但收益域窄 | 同上 |
| seed-bias | h_mean CV≈1.0 | 论文 limitations | 写作时 |
| feasibility_report 帧时长错误 | R006 发现 | L-DP5: 74µs→74ns; L-DP6: 1µs→1.024ms | Q-DP3 节标注 Kill 时一并修 |
| Q-DP3 code z 因子 | D017 形式问题 | standard-CMA 已实现含 z | 写作时统一 |

## 验证阈值

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|---|---|---|---|
| ML vs standard-CMA | 30seeds p<0.05 + ML≥25/30 | D022 预注册 | PASS（仅 N=5M/f_G=30） |
| fade 前兆可辨识 | 触底前 ≥50block 趋势显著 | D024 | PASS（85%） |
| 压μ救 BER | PI 显著低于常规 p<0.05 | D025 生死前置 | **FAIL（0/5, p=0.5）** |

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落
- [ ] 已验证本文件中的至少 3 条关键事实声称：
  - [ ] D026 压μ PI=0.0362 > 常规 0.0275 → 查 prompt019_mu_compress.json 原始 trials
  - [ ] D023 f_G=1000 ML 赢 1/5 → 查 prompt016_param_sweep.json
  - [ ] D014 SOP 串扰是 BER 恶化真因 → 查 decisions.md D014
- [ ] 已检查 _registry.yaml 中本专题的 depends_on 和 conflicts_with
- [ ] 已确认当前范围未违反"明确不含"

## 下一轮

**压缩后系统复盘，不是继续挖方法坑。** 具体要回答：
1. **为什么方法层全军覆没？** 核心模式是"治错病"——所有方向治发散/fade，但 BER 真因是 SOP 串扰（D014）。这个判断对不对？
2. **D014 SOP 串扰为什么没被转成方法层方向？** 这是最大的分析层产出，但方法层从没针对它设计。是漏掉了，还是有已知原因它不能做方法？
3. **回候选池系统评估**——当初 D005 合并出 Q-CMA-FADE（=Q-DP2 分析+Q-ML1 ML），候选池还有 Q-DP3（已 Kill）、Q-ML3（载波恢复，种子）、Q-ML4（双频补偿）。有没有当时被攒材料压下去、现在值得重新评估的？
4. **导师约束 vs 现实**——如果方法层确实只能交低天花板版本（Q-CMA-FADE ML 窄域优势 + 改动1），够不够交差？还是要回候选池？

**纪律**：这次复盘必须先读 topic-index 全量进展线索 + decisions.md D014/D023/D026，不能凭压缩后的记忆。复盘产出是一个**判断**（方法层怎么走），不是直接开跑新实验。
