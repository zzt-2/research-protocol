# Decisions — 星地相干 FSO AMC Groundwork

> 架构决策、方向选择、路线失败记录。每条有取代/被取代字段形成血缘链。旧决策标 `superseded` 不删。

## D001: 新系统层范围与旧轴边界

> 2026-08-02 | status: active | 取代: 无 | 被取代: 无

**决策**: 本专题范围 = 星地相干 FSO + Gamma-Gamma 湍流 + 真实编码链/信息不确定性背景下的**自适应编码调制 (adaptive modulation and coding, AMC) 或链路适配**问题，作为毕业论文潜在第二项贡献的独立 Groundwork。明确**不属于**旧 receiver method-production campaign（载波同步/均衡/双偏振）；旧 campaign 的 negatives 不是 AMC 证据，旧工程资产（P08-R2 LDPC/prefix-LS/bit-true/info-boundary）只作可复用工程资产，不引用为 AMC 科学结论。

**边界（继承历史 dead-end，逐条见 topic-index dead-end ledger）**:
1. 不复活 ISL AMC prediction（确定性信道输给简单方法，`domain-comms.md:243-247`）。
2. 不复活链路自适应反馈环（反馈延迟 > 相干时间 2-10ms，TL-03）。
3. 不重新包装 ③ MCS 排程窄切片（oracle 上界 0.09 dB）。
4. 不复活"AMC + CPR 联合设计"（ω_n 跨调制一致使前提崩塌，C4-12）。
5. 不把自适应交织/纯PS/N1/coded-chain repair 换名冒充 AMC。
6. 不把 P08-R2 工程资产当 AMC 科学证据。
7. 新 AMC 须不同系统层真实动作，不能是既有 DA/NDA 自适应 CPR 换名。
8. 检索须识别并排除 "automatic modulation classification" 假命中。
9. 须解耦 AMC↔Ch4 BER 循环依赖（前馈或独立量度）。

**依据**:
- 用户执行提示词 §四"必须继承的历史边界"（8 条）。
- FR-26 核验：8 条中 #1/#2/#3/#6/#7/#8/#9 + #4 经 grep/Read 在 cited 文件确认；#5 经 registry 专题边界确认（详见 topic-index dead-end ledger 证据指针列）。
- `method-production-campaign-thesis-map.md`（A/B/C 级资产分级）。
- master-state.md §2 当前控制面桥接（AMC 须另开专题）。

**触发原话**: 无（技术推导 + 用户执行提示词派发；用户本轮未给态度原话，voice.md 记执行提示词关键约束 verbatim）。

**影响**: 锁定本专题范围与旧轴隔离；R001 候选族须逐条对照本决策的 9 条边界打勾。
