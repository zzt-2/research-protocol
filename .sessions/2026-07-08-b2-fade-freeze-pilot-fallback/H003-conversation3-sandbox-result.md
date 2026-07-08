# Handoff: 阶段 1 sandbox 三方对照完成 —— C2 红线解除但核心增量三维度全失效，交主控定夺 Kill/重新定位/放松前馈化

> 来源: S003（阶段 1 sandbox 三方对照执行）| 交接目标: 主控对话核查 sandbox 结果 + 定夺 B2-Q2 方向（Kill / 重新定位 / 放松前馈化）
> 文件名: H003-conversation3-sandbox-result.md
> 日期: 2026-07-08

## 到哪了（状态）

**阶段 1 sandbox 三方对照全完成**（S003）。三方脚本 + 参数实测 + 结果 JSON 全落盘 `explore/b2-fade-freeze-pilot-fallback/`（7 份新产出：`_b2_params_draft.py` / `_sandbox_three_way.py` / `_gamma_th_sweep.py` / `_gamma_th_sweep.json` / `_rho_fade_measure.json` / `_sandbox_results.json` + S003）。

**两个必答问题全答了**：
- **必答 1（维度 C2 红线）= 红线不成立**：da_ml 在绝大多数 fade 场景（weak/moderate/strong 低中 SNR）**赢** blind NDA-ML（psa_foe 在 weak/moderate 赢，strong 高 SNR 输）。命题逻辑可以继续。
- **必答 2（动态恢复时间）= 结构性失效**：前馈架构（INVARIANT）下 A/C 非 fade 期用同一个估计器，fade→非fade 转换后第 1 块 BER 已近稳态（比值 0.80），N_recover A≈C 完全相同。**前馈化导致动态恢复测度失效**（架构-测度不匹配）。

**Go/Kill 判据核查**（三 Go 全 FAIL，Kill2/Kill3 部分）：
- Go1 动态恢复：FAIL（结构性失效）
- Go2 范围扩展：FAIL（A/C HD-FEC 可达性一致：weak 24/26dB, moderate 26dB, strong 全不可达）
- Go3 稳态 BER fair gain ≥0.5dB：FAIL（weak @HD-FEC gain=−0.187dB，C 微输）
- Kill1 C2 红线：不成立（不 Kill）
- Kill2 动态恢复无差：结构性成立（Kill 信号）
- Kill3 稳态退化：strong 中 SNR C/A=1.05~1.07（部分 Kill 信号）

**fade 块内直接对照（关键发现）**：moderate/strong 中高 SNR fade 块，**C（da_ml）输 A（freeze）**（C/A=1.10~1.43）。物理根因：fade 块 pilot SNR 极低，da_ml 估计噪声大；freeze hold 上一非 fade 高 SNR 估计反而更准。

## 下一步干什么（主控对话）

**主控对话需做的事**（核查 + 定夺）：

1. **核查 sandbox 数据**（V5 主控独立重算）：
   - grep `_sandbox_results.json` 核查 C2/fair gain/N_recover 数字
   - 核查方案 A freeze 是否严格实现 [79]（V3 祖师爷）—— `_B2-deep-fade-freeze-increment.md:33`
   - 核查 γ_th 选择策略修正（σ 标准化失效 → ρ_fade 控制变量）

2. **定夺 B2-Q2 方向**（三个选项，由主控 + 用户）：
   - **选项 1 Kill**（executor 建议）：核心增量三维度全失效 + 前馈化是架构约束级。阶段 0 规约投入即使 Kill也有价值。
   - **选项 2 放松前馈化 INVARIANT**：前馈化是动态恢复失效的根因。放松到闭环可能恢复测度意义，但有撞 D006 风险（[79] 原始就是闭环 freeze，B2-Q2 闭环版 vs [79] 闭环版差异更小）。
   - **选项 3 重新定位贡献**：sandbox 发现 da_ml 在 fade 赢 blind（C2 解除）但输 freeze。可探索 power-boosted pilot / 自适应阈值 / 别的 pilot-aided 变体（偏离原命题，需重新设计）。

3. **若 Kill**：记录 D003（sandbox 后 Kill，含失败数据 + 可复用部分）+ 更新 topic-index（status→closed 或 dormant）+ 更新 `_registry.yaml`。
4. **若继续**：写阶段 2 TL-20 理论预期表 + 阶段 3 MVE（但需先解决"哪个维度够格"——三 Go 全 FAIL 状态下继续需重新定位）。

## 纪律（和下一步直接相关的约束）

1. **Go/Kill 是用户的**（profile + INVARIANT 继承）：executor 只产实测数据 + 建议，Kill/继续由主控 + 用户定夺。
2. **架构-测度不匹配是关键发现**：前馈化 INVARIANT（阶段 0.3）→ 动态恢复测度失效。若放松前馈化需重新讨论 D006（闭环有撞 D006 风险）。
3. **C2 红线解除但不是 Go**：红线解除只意味命题逻辑不崩塌，不代表够格。三 Go 维度全 FAIL。
4. **公平性 bug 已修**（fade 块 h 均衡）：A 全程 blind h（fade 块也 blind h），C2 测试 blind 配 blind h / pilot 配 pilot h。修复后结论稳健。
5. **γ_th 选择策略修正**（V4）：σ 标准化 [γ̄−3σ, γ̄−1σ] 在 strong 失效（功率分布右偏）→ 改用 ρ_fade=0.15 反推 γ_th。三方对照在相同 ρ_fade 下公平。
6. **ρ_fade 物理发现**：跟湍流强度**反**相关（阶段 0.4 §3.2"strong ρ_fade 高"直觉错）。weak ρ_fade≈0.12, strong ρ_fade≈0.008（γ̄−1σ 处）。实测 0.15 反推 γ_th 后三方公平。

## 接口变更（代码改动）

sandbox 阶段首次写代码，新增 explore 私有 `_` 前缀文件（不进 common，不进 experiments）：
- `explore/b2-fade-freeze-pilot-fallback/_b2_params_draft.py`（B2Params，修正阶段 0.5 草稿 import：`from common._config import TURB`，不是不存在的 `GammaGammaParams`）
- `explore/b2-fade-freeze-pilot-fallback/_gamma_th_sweep.py` + `_gamma_th_sweep.json` + `_rho_fade_measure.json`
- `explore/b2-fade-freeze-pilot-fallback/_sandbox_three_way.py` + `_sandbox_results.json`
- **不修改** `common/` 任何文件（4 估计器 + 信道只 import，守 INVARIANT）
- import 路径：`fft_foe_m0_omega` / `estimate_h_blind_perblock` / `estimate_h_pilot_perblock` 从 step4a 锚脚本 `_time_domain_crlb.py` 用 importlib 加载（文件名 `_` 前缀，避免命名耦合，复用 step4a 已验证实现）

## 失败数据附录（核心，B2-Q2 当前形态增量失效）

### fade 块内 BER 对照（维度 C2 + fade 期直接增量，关键数字）

| turb | γd_dB | C2: da_ml | C2: psa_foe | C2: blind_nda | A(freeze) fade | C(dual) fade |
|---|---|---|---|---|---|---|
| weak | 5 | 0.4231 | 0.4315 | 0.4636 | 0.4472 | 0.4231 |
| weak | 10 | 0.2701 | 0.3002 | 0.3967 | 0.2833 | 0.2701 |
| weak | 15 | 0.0832 | 0.1171 | 0.1164 | 0.0827 | 0.0832 |
| moderate | 5 | 0.4485 | 0.4520 | 0.4742 | — | — |
| moderate | 10 | 0.3385 | 0.3540 | 0.4280 | — | — |
| moderate | 15 | 0.1634 | 0.2092 | 0.2054 | — | — |
| strong | 5 | 0.4840 | 0.4752 | 0.4841 | — | — |
| strong | 10 | 0.4166 | 0.4264 | 0.4618 | — | — |
| strong | 15 | 0.3146 | 0.3475 | 0.3638 | — | — |

（完整 21 点数据在 `_sandbox_results.json`）

**关键归因（主线独立核查）**：
- da_ml vs blind_nda（C2 红线）：da 多数赢 → 红线不成立
- da_ml(fade) vs freeze(fade)（B2-Q2 fade 期增量）：moderate/strong 中高 SNR da 输 freeze → freeze 在 fade 块更好
- 物理根因：fade 块 h 极低（true_h=0.44 vs 非 fade 1.07），pilot SNR 极低，da_ml 估计噪声大；freeze hold 上一非 fade 高 SNR 估计反而更准

### 三方全局 BER + HD-FEC 可达性

- weak：HD-FEC 可达 @ 24/26dB（A/B/C 都可达，无范围扩展）
- moderate：HD-FEC 可达 @ 26dB（A/B/C 都可达）
- strong：HD-FEC 全不可达（物理上限，D005 已证）
- fair gain @ HD-FEC（weak）：C vs A = −0.187dB（C 微输，C overhead=0.187dB）

### N_recover 结构性失效证据

- A_recover == C_recover（完全相同，前馈架构 A/C 非 fade 期同估计器）
- fade→非fade 转换后第 1 块 BER/稳态 = 0.80（已近稳态，无收敛）
- N_recover 在前馈架构下无意义（[79] 闭环 freeze 才有恢复收敛）

## 已知债务

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| D002 前馈化 INVARIANT 未正式登记 | 阶段 0.3 建议 | pending | 主控确认升 D002（或 sandbox 后若放松前馈化则 D002 取消）|
| B2Params 草稿 GammaGammaParams import 错误 | 阶段 0.5 草稿 | ✅ S003 已修正（用 common._config.TURB）| — |
| GG α/β 文献来源 | TL-26 + 阶段 0.5 #3 | ✅ S003 已查证（设计选择典型值，非 sat.1553 scenario）| — |
| γ_th 选择策略 | FR-20/TL-26 | ✅ S003 已修正（σ 标准化失效→ρ_fade 控制变量）| — |
| 动态恢复测度 vs 前馈架构 | 阶段 0.3 INVARIANT | 🔴 S003 发现架构-测度不匹配 | 主控定夺：Kill / 放松前馈化 / 重新定位 |
| B2-Q2 核心增量三维度全失效 | 阶段 0.4 Go 标准 | 🔴 S003 sandbox 实证 | 主控 + 用户定夺 Kill/继续 |

## 验证阈值（sandbox 后更新）

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 | sandbox 结果 |
|--------|----------|---------|-----------|------------|
| sandbox 三方对照 | 三方归因可信 + 维度 C2 回答 + 动态恢复测量 | V2+C7 (v1.3.0) | — | ✅ 三方全跑，归因主线独立核查 |
| sandbox 维度 C2 | 非全输（至少一个 pilot-aided 变体在 fade 赢或持平 NDA-ML）| INVARIANT 11 红线 | — | ✅ PASS（da_ml 多数赢 blind，红线不成立）|
| sandbox 动态恢复 | N_recover,B2Q2 < N_recover,freeze 显著 | 阶段 0.4 核心增量 | — | ❌ FAIL（前馈架构结构性失效，A≈C）|
| sandbox 范围扩展 | strong 某 OSNR 点 C 可达 HD-FEC 而 A 不可达 | INVARIANT 13 饱和池对策 | — | ❌ FAIL（A/C 可达性一致）|
| sandbox 稳态 BER fair gain | ≥0 dB（不退化）+ 最好 ≥0.5 dB | 阶段 0.4 | — | ⚠️ PARTIAL（weak 持平/微输，strong 中 SNR 退化）|
| MVE fair gain | ≥0.5dB @ HD-FEC 或范围/鲁棒性维度够格 | D005 + INVARIANT 13 | — | 不进 MVE（sandbox 三 Go 全 FAIL，待主控定夺）|

## 接收方验证（主控对话核查时必须完成）

- [ ] 已读取 topic-index 的不变量段落（14 条，重点 11/12/13/14 B2 特殊 + 前馈化推导）
- [ ] 已验证本文件中的至少 3 条关键事实声称：
  - [ ] 维度 C2 红线不成立（核查 `_sandbox_results.json` fade 块 BER: da_ml vs blind_nda，主线已重算 da 多数赢）
  - [ ] 动态恢复结构性失效（核查 `_sandbox_results.json` n_recover_A == n_recover_C，fade→非fade 第 1 块 BER/稳态≈0.80）
  - [ ] fade 块内 C 输 A（核查 `_sandbox_results.json` strong 15-20dB: C fade BER > A fade BER）
- [ ] 已检查公平性 bug 修复（A 全程 blind h / C2 测试 blind 配 blind h）—— 核查 `_sandbox_three_way.py` L169-186
- [ ] 已检查 γ_th 选择策略修正（σ 标准化 → ρ_fade 控制变量）—— 核查 `_gamma_th_sweep.json` meta.gamma_th_selection_strategy
- [ ] 已确认架构-测度不匹配发现（前馈化 → 动态恢复失效）是否需升 D003 + 放松前馈化讨论

## 下一轮

**主控对话核查 sandbox 结果 + 定夺 B2-Q2 方向**：

- **若 Kill**（executor 建议）：记录 D003（Kill + 失败数据 + 可复用：C2 红线解除方法论 + 前馈架构-测度不匹配发现）+ 更新 topic-index（status→closed/dormant）+ 更新 `_registry.yaml`
- **若放松前馈化**：重新讨论 D006 边界（闭环 freeze 撞 D006 风险）+ 可能升 D004（放松前馈化）+ 重设计 sandbox（闭环版三方对照）
- **若重新定位**：基于 C2 解除 + da_ml 赢 blind 发现，探索 power-boosted pilot / 自适应阈值 / 别的 pilot-aided 变体（偏离原命题，需重新走阶段 0.1 张力验证）
