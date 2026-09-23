# [R032] 备份方向侦察：失锁恢复（K01）证据路径 + 译码辅助信道细化备胎

> 2026-09-23 | 关联：专题 2026-08-30-thesis-advisor-text-outline / D055 / D056 / R031
> 场景：PROMPT-025 夜间执行轮的并行侦察——为"主选块死于诊断/被 EMA·RLS 吸收/导师拒对象"准备退路。两个只读子 agent 执行；零实验零代码。

## 调研问题

主选（跨窗信道跟踪）之外，还有哪个方向值得作为第三候选保留？重点核查：①K01 失锁恢复的问题存在性证据能否低成本补上（topic-index 问题 B 解锁条件②）；②"判决/译码辅助信道估计细化"（X-1 族）作为 EMA/RLS 吸收情景下算法化备胎的差异化空间。

## 发现

### 一、K01 失锁恢复：激活现实性 = 低（基本死路）

1. 设计卡 = Fade-Guarded DPLL Reacquisition Controller（TRACK/HOLD/REACQUIRE 三态 wrapper），当时裁决 REJECT—PROBLEM_EVIDENCE_INSUFFICIENT，reopen 需先用现有 receiver-visible trace 证明 post-fade 错误 NCO/重捕获延迟真实发生（`direction-lab/harvest/baseline-first-method-batch-001.md:117-148`）。
2. **死环**：当前主链 CPR 是逐窗一次性块估计（`post_ch4_ch3_bridge.py:356-365` 调 `da_ml_recovery` 返回单标量；`cpr_state_scope="per-polarization/observation-window-only"` :170）——无环路/无 NCO/无跨帧状态，"失锁"在这条链上**没有定义、没有载体、没有历史轨迹数据**（occurrence_raw 仅存块估计值）。要跑状态记录诊断必须先给平台引入跟踪式 CPR+锁定检测器 = 改 Ch3 章对象，与解锁条件①（导师接受载波侧对象）是同一阻塞，不可解耦。
3. 即使解锁：近亲 b2 闭环 hold（功率阈值 gate+跨块 NCO 状态）已实测 net fair gain −0.09~+0.16dB 边缘量级（`b2-fade-freeze-pilot-fallback/_fair_comparison_closed_loop.md:120`）。Ch3 自认失效边界也是窗口级 BER 平台（章节稿 3.6.3），无"错帧 vs 可恢复"的帧级状态概念。

### 二、译码辅助信道细化（X-1 族）：可行备胎，差异化空间大于 EMA/RLS

1. **资产齐**：X-1 设计卡（decoder 软符号一次重均衡，开放前提=确有可恢复 headroom+hard-DD 不完全吸收，`S027:54-66`，DESIGN_ONLY 未跑）；decode-failure-rescue 仪器化程度足以支撑回灌（soft twin 引擎、`final_llr_tx` 信道序软 LLR、warm-state 步进、可重编码——`rescue_decoder.py:136-177`）。
2. **机制区分成立**：plain RDE 是"自判决 DD"（最近环盲判决 `canonical_nearest_radius` :76-90，误差只回灌半径 :142，无 FEC 信息）；code-aided 的实质差别 = 判决来源（FEC 纠错符号 vs 盲环猜测）+ 估计形式（全帧批量加权 LS vs 逐符号随机梯度）+ 次数（一次回灌）。真正的廉价对手是 plain RDE（盲 DD），不是 EMA/RLS。
3. **结构性免疫"调遗忘因子"塌缩**：作用轴在帧内 payload 信息，与帧间先验正交——即便连续轨迹平台上跨窗跟踪被 EMA 吸收，本备胎吸收不掉。
4. **文献族**：库内 5 篇 code-aided（EM 盲估计/帧同步/相位模糊消解/迭代同步，`papers/_read_notes/`），族合法性有支撑；全部作用在标量相位/频偏对象，无一篇做 2×2 Jones 细化（注意：该语料是 C1 相位专题检索产物，是"本地无占用"线索而非空白证明，激活时须补本对象的碰撞检索）。
5. **与 Ch3 分工成立**：细化对象=W（每帧 2×2），Ch3=标量相位（`single_cell.py:254-261` 公共标量先乘、Jones 后混）；Jones 只能估计到 pilot 旋转等价类，模糊度划分须显式保留。
6. **身份风险中等**：两段骨架与救援同形——卖点必须钉在"纠错符号回灌的信道重估"，不能写成"失败码字二次救援"。
7. **Kill 诊断已可设计**：genie 符号全帧加权 LS 重估 W vs 64 导频 LS（复用 `generate_shared_correctness_realization` 的 truth/jones/w0），看 Jones 误差与冻结码链 FER 差；再加导频预算轴（64→16→8）把增益锚到导频开销/goodput（P11 的 1.98× goodput 口径先例）。
8. **与夜间诊断的联动**：若 PROMPT-025 阶段一的 O1（真值初始化）与 O2（纯真值 demux）都≈0，则整个"Jones 知识轴"（含本备胎的 genie 细化）大概率同死；若 O2>0 而 O1≈0，说明 RDE 吸收初始化误差但不吸收充分信道知识——本备胎的批量重估恰是绕开 RDE 吸收的路径，价值上升。

## 结论

K01 从备份清单除名（载体缺失+近亲边缘增益，投入诊断成本不划算）。备份序位更新为：**①译码辅助信道细化（X-1 落地版，等价 Jones 知识轴+帧内信息轴，激活条件=主选死且 O2 型 oracle 有 headroom）→ ②选择性 BICM-ID（R031 原备选）→ ③译码救援线按 D053 口径成章（保底）**。

## 对决策的影响

不改 D055 主选与 PROMPT-025 执行边界；本侦察结果供"主选死"情景的下一轮选型使用。X-1 的正式序位仍守 S027"单章池耗尽后"，激活前须补：genie oracle headroom 门（FR-21 式）→ hard-DD 吸收门 → 本对象碰撞检索。无新决策；K01 除名建议随本笔记供用户核可（不单开 D###，因其本就处于暂放未激活状态）。
