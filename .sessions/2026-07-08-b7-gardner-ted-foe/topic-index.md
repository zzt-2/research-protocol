# Topic Index: B7 Gardner TED 复用 FOE 第二候选

> slug: 2026-07-08-b7-gardner-ted-foe
> status: closed | created 2026-07-08 | last_updated: 2026-07-09（**D008 Kill B7-Q1**——范围优势解决的是不存在的问题。LEO 光学 Doppler ±4.8GHz 被 4thpow ±6.25GHz 恰好覆盖，B7 范围优势只在 6.25-25GHz 区间成立但真实场景够不着；BER gain 公平条件≈0（D007）；OFC 已发叙事建立在 +4.08dB 虚高数据上。与 B5 D003 殊途同归——范围优势都因"baseline 在真实场景够用"而失去意义。三条增量路径全证伪。复用资产保留作 baseline 库扩展 + 教训素材）

## 专题定位（一句话）

B7-Q1（Gardner TED 复用 FOE）第二候选 MVE 执行。与 NDA-ML 单载波候选（step4a-mve-execution 专题）并行，NDA-ML 卡 D-008 双 bug + D-009 线宽/vs VV 持平陷阱期间推进。**流程规划前置**（阶段 0 不写代码先定规约）防重蹈 NDA-ML 6 类混乱。

## 原始目标（冻结，不可修改）

对 B7-Q1 走 Step 4a 维度 D MVE，守 FR-21/TL-20/FR-18/FR-12 + D005 务实路线 + D006 红线 + **sim-preflight v1.3.0 新增 C6-C8**（公式核对/三方对照/祖师爷警报）。

**冻结边界**：
- 只做 B7-Q1（Gardner TED 复用 FOE 星地 COSC 迁移），不回头救 6 次 Kill
- 不跳框架（FR-22，当前在 Step 4a 维度 D）
- 不推翻 D006（前馈不撞 / 环路 TF 联合建模则撞）
- 不改框架文件（守"先测不改协议"）

## 范围边界

### 原始目标（冻结）
对 B7-Q1 走 Step 4a 维度 D MVE。

### 当前范围
- **阶段 0 前置规约**（不写代码，先定 6 项规约，防 NDA-ML 6 类混乱）：
  0.1 锚论文公式完整性核查（OFC 2026 poster 全文 + 页码 + 公式编号 + 是否完整可实现）
  0.2 Gardner TED 数学同族性检查（跟 1986 原版 + VV + BPS 的数学关系）
  0.3 架构定性（前馈 vs 环路 TF，环路则撞 D006 必须前置决策）
  0.4 公平对照框架设计（B7 baseline PSA FOE 时域，fair gain 怎么定义，工作点 BER 2e-2 还是 HD-FEC）
  0.5 参数真相源前置（Doppler range / OSNR / LEO Doppler rate 一开始进 params.py 单字段）
  0.6 文件组织规约（`explore/b7-gardner-ted-foe/` 目录结构 + 命名规则）
- **阶段 1 sandbox 三方对照**（Gardner TED 改进版 / 1986 原版祖师爷 / PSA FOE baseline）
- **阶段 2 TL-20 理论预期表**（仿 N1-MVE-SPEC.md §2）
- **阶段 3 MVE + consistency**（守 sim-preflight v1.3.0 C6-C8 + V1-V6）

### 明确不含
- ❌ 不回头救 6 次 Kill
- ❌ 不判 NDA-ML 那边的线宽/方向决策（那是 step4a-mve-execution 专题的事，本专题只做 B7）
- ❌ 不改框架文件
- ❌ 不跳框架（FR-22，当前在 Step 4a 维度 D）
- ❌ 不推翻 D006（前馈不撞 / 环路 TF 联合建模则撞）
- ❌ 不污染 common（explore 阶段探针不直接进 experiments，MVE 通过才转正）

### 范围变更记录
- 无（专题首 session）

## 不变量（动任何一条必须重新讨论）

1. **继承上游专题 `2026-06-20-problem-driven-redirection` 全 9 条不变量**（D017/D018 判读框架 / D006 红线 / D005 务实路线最高优先级 / 范围硬门 / 问题从文献长出来 / 委托技术判断守 Go/Kill / 3 步上限 / 核查机制中性双向 / GW 流程强制门控）
2. **D005 务实路线（INVARIANT 最高优先级）**：Go 判据=赢传统未优化 baseline 几 dB（会议门槛放宽：纯仿真+鲁棒性 dB/范围/绝对指标/同族 dB 都算够格）；oracle 上界 FR-21 降级为参考不当 Kill 门
3. **FR-22 GW 流程强制门控**：当前在 Step 4a 维度 D（MVE），禁跳到 Contract/Execute
4. **FR-25 Go/Kill 标准分离**：Go 标准=赢传统 baseline / Kill 标准=A0 致命+MVE FAIL，FR-21 只在 A0 通过后做 Kill 工具
5. **切法地图是参照系不是答案**：B7 是稀池 1 细分独占赛道（OFC 2026 会议样本 + 75%"既有方法失效"叙事），引用模式不搬"切法地图说这个好"
6. **profile 第 9 次"急于推进"防线激活**：B7 流程规划阶段主线极易"阶段 0 太繁琐先跑起来再说"。**防线：阶段 0 六项规约必须全做完才进 sandbox，禁跳阶段 0 直接写代码**（NDA-ML 最大混乱就是阶段 0 没做）
7. **TL-26 参数溯源强制**：B7 每个关键参数（Doppler range / OSNR / LEO Doppler rate / 符号率 / 线宽）必须标文献来源（B7 OFC 2026 / Paillier / sat.1553 / Fernandes），禁拍参数。**且必须读原文数值不只引位置**（D-009 教训 5，FR-26 强化）
8. **TL-13 共用同一信道实现**：B7 必须从 `common/_channel.py` 导入，禁自建信道
9. **TL-20 先建理论预期**：MVE 跑之前必须写明理论预期表，仿 N1-MVE-SPEC.md §2
10. **核查机制中性双向**：子 agent 产出 + 主线独立 grep 核查，**子 agent 归因必须主线独立重算验证**（D-009 教训 6，只信原始数字不信归因）
11. **【B7 特殊·INVARIANT】Gardner TED 1986 数学同族性前置检查**：Gardner TED 是 40 年前祖师爷方法（比 VV 1983 还老），B7 锚方法（OFC 2026 Gardner TED 复用 FOE）跟它比，**如果数学同族就是 NDA-ML D-008 陷阱重演**（vs VV 持平被当合理接受）。**必须在阶段 0.2 做深度数学同族性检查**，并在 sandbox 阶段做三方对照（改进版/1986 原版/PSA FOE）验证非同族
12. **【B7 特殊·INVARIANT】架构定性前置（前馈 vs 环路 TF）**：B7 锚方法是反馈环（TED→loop filter→NCO），**如果我们的实现也走反馈环，环路 TF 联合建模则撞 D006**。必须在阶段 0.3 定死：前馈化（合法不撞 D006）还是环路（撞 D006 需单独决策）。**禁边跑边定架构**（NDA-ML D-002 B11 OFDM→单载波重定位教训）
13. **【B7 特殊·INVARIANT】锚论文公式完整性前置核查**：B7 OFC 2026 poster 只有 90 行（比 B11 PTL 2025 的 226 行薄很多），**靠文字描述重建公式风险高于 NDA-ML**（LMMSE #15 复现失败教训：PDF→md 把公式转 picture omitted）。必须在阶段 0.1 核查所有公式完整可实现，**公式不全直接标红不硬磕**，切降级方案（定性引用或换 baseline）

## 其他结论（普通技术决策）

### B7 特殊风险（vs NDA-ML 的差异点，决定流程重点）

| 风险 | B7 情况 | NDA-ML 对照 | 流程对策 |
|---|---|---|---|
| 锚论文薄 | OFC 2026 poster 90 行 | B11 PTL 2025 226 行 | 阶段 0.1 公式完整性核查最严 |
| 祖师爷警报 | Gardner TED 1986（40 年经典）| VV 1983（NDA-ML 已踩陷阱）| 阶段 0.2 数学同族性检查 + sandbox 三方对照 |
| 架构定性 | 反馈环（TED→loop filter→NCO）| 前馈闭式（不撞 D006）| 阶段 0.3 前馈化 vs 环路决策 |
| 公平对照 | baseline PSA FOE 时域 | DA ML pilot overhead | 阶段 0.4 fair gain 框架重新设计 |

### NDA-ML 6 类混乱 + B7 防御措施（S001 确立）

| 混乱类 | NDA-ML 教训 | B7 防御措施 |
|---|---|---|
| A. 参数反复 | 线宽 500kHz→10kHz→疑似 0.1-1MHz，全量重跑 3 轮 | 阶段 0.5 参数真相源前置 + sim-preflight v1.2.0 param-source.md |
| B. 算法 bug | D003 双 bug + D-008 双 bug（漏 ML 加权+升幂未归一）| 阶段 0.1 公式完整性核查 + V1 公式逐项核对（v1.3.0）|
| C. 验证失效 | consistency PASS 但算法错（两套都漏同一 bug）| V2 三方对照 + V3 祖师爷警报（v1.3.0 C7-C8）|
| D. 方向重定位 | B11 OFDM→单载波 / LMMSE 失败→VV/BPS | 阶段 0.3 架构定性前置（前馈 vs 环路）|
| E. 文件混乱 | MVE 薄包装 + 双套参数共存 + 两 results 目录 | 阶段 0.6 文件组织规约 + 下游引用同步清单 |
| F. 文献引用 | D-007 引 Valjus 位置没读原文数值 | V6 FR-26 读原文数值（v1.3.0）|

### S006 sandbox 实现发现（对话 7 正式 MVE 警示，暂不升 D###）

| 发现 | 内容 | 对话 7 警惕 |
|------|------|------------|
| A. B7 候选消歧边界 | `content.md:37` "TED2 std 判决"内在限制：TED2 std 小 ≠ BER 低（residual≈整数倍 baud rate 时 TR 收敛但 BER 爆）。实现：单峰清晰（第二峰<70%主峰）直接 argmax 不触发消歧 | 若正式 MVE B7 est 系统性偏到 baud rate 整数倍外，查这个消歧逻辑 |
| B. PSA 需 MP FOC 残余清理 | MVE 简化省略 MP FOC 对 PSA 不公平（PSA 谱不对称法对 f_D=0 有偏置，补偿后残余 ~0.3GHz 让 TR 失效）。修复：三方补偿后都加 M=4 次方残余 FOE 清理（对齐 `content.md:47` MP FOC）。D006 PSA coarse-only 弱扩展：不仅线性区窄，估准后还有残余偏置需清理 | fair gain BER gain 标为上界（D006），正式 MVE 的 PSA BER 可能因 MP FOC 清理能力受限而偏高 |
| C. BER 符号对齐 | TR loop 输出 vs 参考符号差整数 lag（依赖 loop 初始化）。`qpsk_hard_decision_ber` 自动扫 lag -4..+4 找最佳对齐 | 若 BER 系统性 0.25（QPSK 随机+1/4 偏移），查 lag 对齐 |

## 已确认决策

- **D001**（2026-07-08，S002）：Gardner TED 1986 公式源 = 用户本地 Matlab 代码（`毕设/旧本科代码/PSKTimingErrDetector.m` + `Tx2Rx.m` L176-214 定时环），不切降级方案。B7 "TED 增益↔Doppler 映射"解析式缺失但可数值重建。阶段 0.1 通过，进 0.2。
- **D002**（2026-07-08，S003）：B7 数学同族性 = 弱同族 (B) + 机制数值验证成立。G(f_D) 以 baud rate 25 GHz 周期（铁证 G(0)=0.132142，FFT 主频能量 >90%）；B7 vs 1986 共享 TED 公式但任务正交（FOE vs STR）；B7 vs VV/BPS 非同族（无 NDA-ML 陷阱路径）。阶段 0.2 通过，进 0.3。残留风险：~~B7 未给 TED_gain(f_D) 解析式，sandbox 前补解析推导 + Leven 对比~~ → **已闭合（S005/D006）**：G(f_D)=K_max·|cos(πf_D/B)| 解析成立，Leven 对比三层运算不等价判弱同族 B。
- **D003**（2026-07-08，S003）：B7-Q1 架构定性 = FOE 前馈扫频 + Gardner TR 保留反馈环（跟踪 τ 不是 φ_T）+ 载波同步禁建模湍流相位。不撞 D006（B7 不涉湍流 + FOE 前馈无环路 TF + TR 是定时环非载波同步环）。阶段 0.3 通过，进 0.4。
- **D004**（2026-07-08，S004）：B7 fair gain = 二维报告（BER gain @ 双工作点 HD-FEC 主+BER 2e-2 锚校验 + Doppler 范围比 1.9×）+ PSA FOE baseline 必须 sandbox 重写（谱不对称法，非 pilot-aided）。阶段 0.4 通过，进 0.5。common `_recovery.py:435` psa_foe_recovery 概念错债务登记。
- **D005**（2026-07-08，S004）：B7Params 修正版草稿（15 字段全溯源 content.md 行号，修正 LEO_DOPPLER_RATE 30e3→1e9，删 PSA_PILOT_SPACING，补 7 新字段）+ B7 锚论文原参数 25GBaud/1.8kHz 不跟 NDA-ML 统一（用户决策，防 D-007 覆辙）+ explore 目录结构落盘。阶段 0.5+0.6 通过，**阶段 0 六项规约全收尾**。
- **D006**（2026-07-08，S005）：sandbox 步骤 1-3 诚实发现登记——① B7Params 回写 params.py 完成（15 字段，14 OK + 1 WARNING，0 DEAD/CRITICAL）② PSA FOE coarse-only baseline 线性区 ~1GHz 限制（25GBaud/β=0.1 物理结果非 bug，fair gain BER gain 标为上界）③ Leven 2007 DOI 修正 891597→891893（论文已落盘）④ D002 残留风险闭合（G(f_D)=K_max·|cos(πf_D/B)| 解析成立，弱同族 B 不降级 C）。
- **D007**（2026-07-09，S007）：V5 核查未记录 MVE 数据 + LPF2 不公平 bug 登记 + BER gain 虚高结论 + 范围优势机制本质确认。① LPF2（L851）只给 B7 加其他 baseline 全无，apples-to-oranges 不公平 ② +4.08dB 三重虚高（LPF2独享+PSA弱+Kay估偏），公平条件下 B7 vs 4thpow gain≈0（+0.03dB）③ 范围优势经公平对照+数学证明是机制本质（4thpow 4次方混叠±6.25GHz vs B7 TED周期±25GHz），非 B5 D003 特权假象。BER gain 维度 FAIL，范围维度 PASS，Go/Kill 交用户。
- **D008**（2026-07-09，S007 续）：**Kill B7-Q1**——范围优势解决的是不存在的问题。用户追问"能大多少"触发真实需求核查：LEO 光学 Doppler ±4.8GHz 被 4thpow ±6.25GHz 恰好覆盖，B7 范围优势只在 6.25-25GHz 区间成立但真实场景够不着；星历预补后残频 <100MHz 所有方法都够。与 B5 D003 殊途同归——范围优势真实但"baseline 够用"使其失去意义。三条增量路径全证伪（BER gain≈0 / 范围优势无用 / OFC 已发基于虚高数据）。专题 closed，复用资产保留。

## 悬而未决

1. ~~B7 锚论文 OFC 2026 poster 是否已落盘~~ → **已解决（S002）**
2. ~~Gardner TED 1986 数学同族性结论~~ → **已解决（S003/D002）**：弱同族 (B)，非 NDA-ML 陷阱
3. ~~B7 机制（周期相关）是否真实~~ → **已解决（S003/D002）**：数值验证成立，周期=baud rate
4. ~~架构定性结论~~ → **已解决（S003/D003）**：FOE 前馈化 + Gardner TR 保留反馈环，不撞 D006
5. ~~公平对照框架~~ → **已解决（S004/D004）**：二维报告 + 双工作点 + PSA FOE 重写债务
6. ~~符号率/线宽场景统一决策~~ → **已解决（S004/D005 + 用户决策）**：B7 锚论文原参数不统一
7. ~~B7 TED_gain(f_D) 解析式 + Leven 对比~~ → **已解决（S005/D006）**：G(f_D)=K_max·|cos(πf_D/B)| 解析成立，弱同族 B 不降级 C
8. **sandbox 后半 + MVE 执行**：~~CRB 下界 + 三方对照主脚本 + MVE + consistency（对话 6）~~ → 脚本+SPEC+smoke test 完成（S006），正式 MVE 已跑完（未记录对话，S007 V5 核查），LPF2 不公平 bug + BER gain 虚高 + 范围优势公平性审计（S007/D007）→ **D008 Kill B7-Q1**（范围优势解决不存在的问题）。专题 closed

## 当前位置

**🔴 D008 Kill B7-Q1（2026-07-09，对话 7 续）**：用户追问"能大多少"触发真实需求核查——LEO 光学 Doppler ±4.8GHz 被 4thpow ±6.25GHz 恰好覆盖，B7 范围优势解决的是不存在的问题。与 B5 D003 殊途同归：范围优势真实但"baseline 在真实场景够用"使其失去意义。三条增量路径全证伪（BER gain 公平≈0 / 范围优势无用武之地 / OFC 已发基于虚高数据）。专题转 closed。复用资产（Gardner TR Python + PSA 谱不对称法 + 4thpow/Kay + G(f_D) 解析式）保留作 baseline 库扩展 + 教训素材。

## 进展线索

- **S001** 专题开题 + 流程规划前置 + H001 交接（2026-07-08）
- **S002** 阶段 0.1 公式完整性核查 + D001（2026-07-08）：用户本地 Matlab 代码作 Gardner TED 1986 公式源，B7 映射靠数值重建，不切降级
- **S003** 阶段 0.2+0.3 + D002+D003（2026-07-08）：0.2 子 agent 数值重建 + 同族性分析判弱同族 (B) + 主线 V5 独立重算；0.3 架构定性 FOE 前馈化 + Gardner TR 保留反馈环不撞 D006
- **S004** 阶段 0.4-0.6 + D004+D005（2026-07-08）：0.4 fair gain 二维报告（HD-FEC 主+BER 2e-2 锚+范围比 1.9×）+ PSA FOE 概念错债务登记；0.5 B7Params 修正版 15 字段全溯源 content.md 行号 + B7 锚论文原参数不统一（用户决策）；0.6 explore 目录结构落盘 + 下游引用同步清单。**阶段 0 全收尾，可进 sandbox**
- **S005** sandbox 前半 3 步 + 步骤 4 CRB + D006（2026-07-08）：步骤 1 B7Params 回写 params.py（15 字段 14 OK + 1 WARNING，0 DEAD/CRITICAL，下游无断链）；步骤 2 PSA FOE 谱不对称法 baseline 重写（Vieira 2023 L343-347 Δf̂=α·ln(P+/P−)/2，α_calib=0.953GHz，coarse-only 线性区 ~1GHz 限制登记非 bug）；步骤 3 TED_gain 解析 G(f_D)=K_max·|cos(πf_D/B)| + Leven 2007 对比（DOI 修正 891597→891893，三层运算不等价判弱同族 B 不降级 C，D002 残留风险闭合）；步骤 4 CRB 下界（N=1024 OSNR=17dB CRB std=59.42kHz << 扫频间隔 1GHz，精度瓶颈是量化非 CRB，FR-21 不卡）。主线 V5 独立核查全 PASS
- **S006** 对话 6 三方对照主脚本 + MVE-SPEC + smoke test（2026-07-08）：b7_gardner_ted_mve.py 三方实现（B7 proposed FOE 前馈扫频 + Gardner 1986 TR Python 重写 + PSA FOE 谱不对称法 import）+ B7-MVE-SPEC.md 契约（10 节，仿 SC-NDA-ML SPEC）+ smoke test PASS（n_sym=4096×1seed×5f_D×OSNR17dB，14.4s）。systematic-debugging 修 3 bug：① BER 符号对齐（make_tx 直接返回 QPSK 符号作参考，不从 rx 重建）② 单边扫频 0-23GHz（poster content.md:49，避免跨 baud 周期模糊）③ PSA 残余 FOE 清理（M=4 次方 MP FOC，对齐 poster content.md:47 DSP 链）。B7 est 全准 err=0，B7 BER~1e-2 稳定，1986 全爆（V3 祖师爷警报不触发），PSA >12GHz 退化（D006 体现）。**剩对话 7：正式 MVE 跑数 + Go/Kill 判断**
- **S007** 对话 7 V5 核查未记录 MVE + LPF2 bug + 范围公平性审计（2026-07-09）：发现 H005 已被 H006 取代 + 正式 MVE 已在未记录对话跑完（593.4s + osnr_sweep 180.7s，未提交无 S###）。V5 主线独立核查原始 JSON：BER gain +4.08dB vs poster 0.6dB 偏离触发 TL-20。systematic-debugging Phase1-3 定位根因 = LPF2 不公平（L851 只给 B7 加，其他 baseline 全无），Phase3 验证全加 LPF2 后 B7 vs 4thpow gain≈0（+0.03dB，三重虚高：LPF2独享+PSA弱+Kay估偏）。用户提示翻日志找到 B5 D003 先例（范围优势特权假象），B7 做公平范围对照 + 数学本质分析：4thpow 4 次方混叠 ±6.25GHz 铁律 vs B7 TED 周期 ±25GHz，**范围优势机制本质非特权假象**。D007 登记。**续：用户追问"能大多少"触发真实需求核查 → LEO Doppler ±4.8GHz 被 4thpow ±6.25GHz 恰好覆盖 → D008 Kill B7-Q1**（范围优势解决不存在的问题，与 B5 D003 殊途同归）。专题 closed。

### S007 V5 核查发现（Go/Kill 判断材料，带进用户决策）

| 发现 | 内容 | 对判断的影响 |
|------|------|------------|
| A. LPF2 不公平 bug | b7_gardner_ted_mve.py L851 只给 B7 加 _lpf2，PSA/4thpow/Kay 全无 → +4.08dB 三重虚高 | BER gain 维度 FAIL（公平条件 gain≈0）；修脚本重跑拿干净数据 pending 用户决策 |
| B. BER gain 公平后≈0 | 全加 LPF2 后 B7 vs 4thpow +0.03dB（f_D=5GHz 线性区内，都估准时） | B7 FOE 方法本身在线性区内无 BER 增量，贡献不在 BER gain |
| C. 范围优势机制本质 | 4thpow 4 次方混叠 ±6.25GHz（铁律）vs B7 TED 周期 ±25GHz；公平对照（全加LPF2）后 4thpow >6.25GHz 仍全爆 | 范围优势真实，非 B5 D003 特权假象，不能用 B5 逻辑 Kill |
| D. B5 D003 先例边界 | B5 范围优势是特权假象（给 baseline 星历后归零）；B7 是机制本质（baseline 数学限制不可突破）| 后续候选声称范围优势时，公平对照判据 = baseline 限制是人为还是数学本质 |
