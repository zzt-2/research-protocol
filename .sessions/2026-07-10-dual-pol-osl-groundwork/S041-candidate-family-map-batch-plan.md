# [S041] CMA-fade/SOP lock-swap 候选族全景与批量执行计划

> 2026-07-16 | 方法层候选族盘点 | 状态：地图完成，待批次 0 基线审计

## 目标

从已有 CMA-fade/SOP lock-swap 仿真基点出发，完整列出目前可见的方法方向，按共享机制、代码接口和诊断指标分族，再确定批量执行顺序。此文不把任何未跑方向提前判 Go/Kill。

## 基点与统一观测

- 基点：`projects/simulation/explore/cma-fade-divergence/` 的 Gamma-Gamma + SOP 双偏振链路、standard-CMA/ML ButterflyCNN、D022/D027 结果。
- 参数债务：D022 历史域 `alpha=1.5,beta=0.8` 与当前正确新域 `4.2,1.4` 必须分开；standard-CMA 必须使用含 Godard z 因子的实现，`common/_cma.py` current 版本不能冒充标准基线。
- 每批统一输出：fixed-label BER、PI-BER、swap 率/首次 swap 位置、发散概率、fade 后恢复延迟、收敛长度、复杂度/延迟；PI-BER 只能作为第二口径，不能遮盖 fixed-label 结果。

## 候选地图

| 族 | 具体变体 | 当前状态 | 共享接口/诊断 | 备注 |
|---|---|---|---|---|
| A 训练损失 | SOP 不变性正则、swap 对比学习、盲 VAE | A1/A2 KILL（D031）；A3 撞车 DEFER | prompt024 loss/训练脚本 | 不再优先扩展，除非改变作用时段 |
| B 固定架构 | 复值网络、SOP attention、双分支、非对称调制阶数/脉冲/符号率/扩频标识 | B1–B3 defer（D033）；B2 功率分配 KILL（D038）；E1/E2 KILL/NO-GO（D041/D043） | ButterflyCNN 替换模块；需 test-state 证据 | 固定前馈不能解释 late swap，暂低优先 |
| C 训练流程 | 周期在线微调、SOP 增强、课程学习、meta-initialization、多步 DD 半监督 | C1 KILL；C2/C3 defer（D032）；更强 DD/meta 未跑 | prompt025 在线更新基建 | 只保留真正改变 test 状态的变体 |
| D CMA/ML 混合 | CMA 跟 SOP + ML 修复、检测后切换、CMA restart、滑窗 CMA、遗忘因子、DD、DFE、Kalman/粒子 SOP 跟踪、neural-CMA | D1/D2 KILL（D036）；D3 MMA KILL（D040）；其余多未跑 | prompt030/032 CMA、swap detector、paired seeds | 需要先区分“恢复能力”与“超越 ML-only 增量” |
| E 前端信息 | pilot-assisted SOP/Jones、两段式 pilot、半盲、互易、meta/neural-CMA | pilot/CSI DEFER（D037）；E3/E4 未跑 | prompt028 审计结构、pilot budget、因果状态 | 新颖性占点强，成本高；先做低成本信息增量/碰撞检查 |
| F/G 排除 | 电控偏振跟踪、HARQ/重传协议 | 明确不含 | 无 | 不得纳入当前族 |
| H 接受 swap | CRC/翻标签、swap 时刻预测、swap 概率建模、分段检测翻转、突发边界均衡、交织+FEC | H1 = PI-BER 重新发现（D039）；H2/H3 未跑 | fixed/flip/PI 三口径、事件定位 | 可能转变问题定义：从“阻止 swap”到“检测并可部署恢复” |
| 残差族 | `z_out=z_CMA+g(z_CMA)`、CMA+小型残差、CMA 输出作监督特征 | D044 DEFER；S038 无直接先例 | 需要与 CMA-only/raw-ML/fixed+PI/oracle 同批 | 保留为 D 族或独立组合，不占唯一主线 |

## 当前可见的未跑子方向

### D 族：test-time 状态处理

1. fade gate/freeze；2. 步长调度；3. 梯度裁剪/trust region；4. fade 后软重置；5. checkpoint 回退；6. DD 多步更新；7. CMA restart；8. 滑窗 CMA；9. 遗忘因子；10. Kalman SOP；11. particle SOP；12. DFE/decision-directed；13. H2 swap 时刻预测；14. H3 swap 概率建模。

### E/H 族：信息访问和可恢复性

15. 小 pilot 估计 SOP；16. 两段式 pilot；17. 半盲；18. 互易/双向约束；19. 分段检测翻转；20. 突发边界均衡；21. 交织+FEC；22. swap 后可部署重标定。

### 组合候选

23. fade-freeze + swap-safe re-lock；24. CMA + DD + swap detector；25. 小 pilot + CMA；26. swap predictor + selective relock；27. neural-CMA + pilot state；28. CMA residual + test-time state；29. swap recovery + FEC/交织；30. fade gate + H2/H3。

## 批次排序

### Batch 0 — 基线与参数域审计（先做）

冻结当前 `4.2/1.4` 域与 D022 历史域的输入，复现 standard-CMA、ML-only、CMA-only、oracle，统一 fixed/PI/swap/fade 指标。没有这一步，旧结果不能横向比较。

### Batch 1 — Fade 单轴族（最低成本、最高信息增量）

gate/freeze、步长调度、trust-region、fade 后 reset/relock、遗忘因子。每个只改一个机制，先看发散概率、恢复延迟、首次 swap，再看 BER。

### Batch 2 — Lock/swap 单轴族

H2/H3 事件诊断、swap detector、CMA restart、滑窗 CMA、DD/DFE、Kalman/particle。先做离线 detector 上界，再做因果在线版本；不能把 post-hoc 真值检测冒充部署方法。

### Batch 3 — 接受与恢复族

分段翻转、突发边界均衡、可部署重标定、交织+FEC。固定 PI-BER 不作为唯一胜利标准，必须说明新增信息访问和实际开销。

### Batch 4 — 前端信息族

小 pilot、两段式 pilot、半盲、互易、neural-CMA。先做 pilot 开销/碰撞/信息增量审计，再决定是否进入性能实验。

### Batch 5 — 组合族

只有 Batch 1–4 中各自有机制诊断信号的单轴 winner 才组合；至少做 none/A/B/A+B 消融，避免组合掩盖因果。

## 批次晋级规则

- sandbox：≥3 paired seeds、≥2 个条件；机制诊断朝预期方向，主指标相对基线不恶化，才扩展。
- 扩展：≥5 seeds，覆盖当前强 fade、非 fade、至少一档不同长度/调制条件；平均增益或恢复指标达到预设阈值，且不被最强简单先验覆盖。
- 退出：连续两轮改善 <10%、只在单 seed/单条件有效、clean/no-fade 退化、或上界显示增益不足时停止该变体。
- 晋级正式 GW：只有能写成清晰 M-C-A、具备独立信息增量、并在同族横向比较中胜出的候选才补完整 Step 1→4a/Contract。

## 决策引用

- D030：方法层解冻、归类批量、可能有优化就试。
- D031–D041：已跑族的失败机制和可复用基建。
- D045：深耕基点—候选族—批量排跑—晋级工作流。

## 范围确认

- 本轮是否在 scope boundary 内：是。仍限于软件 DSP/ML；F1/G2 明确不含。

## 后续

先执行 Batch 0 基线审计；Batch 0 未稳定前不运行任何新方法族。

## 工作流 skill 验证

- `C:\Users\zzt\.agents\skills\method-family-batch-exploration\SKILL.md` 已创建并通过 `quick_validate.py`。
- 前向压力测试 PASS：独立 worker 在只给原始任务时输出了 CandidateMap、BatchPlan、机制诊断、paired seeds、消融和晋级/退出规则，未退回“逐个微变体完整跑协议”。
- 创建前的基线失败样例是本轮 residual cascade：单候选独占主线、完成 5 篇全文后在一个 UNKNOWN 上阻断，未先建立候选族地图；该失败被 skill 的“protocol literalism”护栏覆盖。
