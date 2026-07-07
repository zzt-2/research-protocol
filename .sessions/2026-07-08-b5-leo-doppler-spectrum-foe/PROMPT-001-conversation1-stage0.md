# PROMPT-001: B5-Q1 对话 1 — 阶段 0.1-0.6 前置规约（够格路径验证 + dB/范围溯源）

> 专题: 2026-07-08-b5-leo-doppler-spectrum-foe
> 对话角色: 工作对话（主控对话派发的执行体）
> 来源: 主控对话 S001 + H001 交接
> 日期: 2026-07-08

## 你是谁

你是 B5-Q1 第四候选的工作对话（executor），承接主控对话（control tower）派发的任务。主控对话负责方向决策/跨候选调度/核查你的产出，你负责执行阶段 0.1-0.6 六项前置规约（不写代码）。

**纪律**：
- 主控对话交代的角色边界要守——你只执行阶段 0 六项规约，不进 sandbox 不写 MVE 代码
- 每个阶段开始前先一句话讲清"在干啥+为什么"再动手（profile 第 9 次"急于推进"防线）
- 子 agent 产出要主线独立 grep 核查（只信原始数字不信归因，D-009 教训 6）

## 你的任务（H001 交接，简版）

**执行阶段 0.1-0.6 六项前置规约**（不写代码），核心是阶段 0.1 验证范围优势够格路径：

- **阶段 0.1（最高优先）**：验证 B5-Q1 范围优势（±4.5GHz vs 传统 ±312.5MHz，15× 范围扩展）在 D005 会议门槛下能不能当 Go 判据。**B5-Q1 不是 dB 增量是范围优势**（`_cut-b4b5-verify.md:64-66` 明确"本体无 vs baseline 改善 X dB 对比只给绝对指标"）。够格路径 3 选项：A 对标 BUPT Arria 10 FPGA demo 会议模板 / B 补 dB 对比 / C 鲁棒性维度 / Kill
- **阶段 0.2**：dB/范围溯源核查（±4.5GHz 出处 + 残频指标 σ<140MHz / <5MHz / ±312.5MHz 精估范围，全读原文数值）
- **阶段 0.3**：架构定性（湍流致功率波动归一化走前馈路径合法不撞 D006，禁环路 TF 联合建模）
- **阶段 0.4**：公平对照框架（baseline [60] Leven 还是传统 FFT FOE？范围 fair gain？BER 1e-3 还是 HD-FEC？LEO Doppler 主题跟 B7/B4 差异化）
- **阶段 0.5**：参数真相源前置（Doppler ±4.5GHz / 56MHz/s / 2.5GBaud / 1550nm / 600km / ±312.5MHz，全标 source + 读原文数值，参考 B7Params 扩 B5Params 草稿）
- **阶段 0.6**：文件组织规约（`explore/b5-leo-doppler-spectrum-foe/` 目录 + short_time_spectrum_foe 接口定义）

**判定门控**：阶段 0.1 如果三条够格路径都不成立 → B5-Q1 转 Kill（合法选项，不是失败）

## 启动协议（必读，按优先级）

报到（session-governance Trigger 1）后读以下文件，**不读不许动手**（FR-22 框架强制门控）：

### 1. 本专题文件（最重要，必读全）
- `.sessions/2026-07-08-b5-leo-doppler-spectrum-foe/topic-index.md` — **14 不变量**（重点 11/12/13/14 B5 特殊风险）+ 阶段 0 规约设计 + 悬而未决
- `.sessions/2026-07-08-b5-leo-doppler-spectrum-foe/H001-conversation1-stage0-qualification-and-sourcing.md` — 完整交接（含 6 项规约详细动作 + 纪律 + 验证阈值）
- `.sessions/2026-07-08-b5-leo-doppler-spectrum-foe/S001-topic-opening-and-stage0-plan.md` — 开题 + 复用基建盘点
- `.sessions/2026-07-08-b5-leo-doppler-spectrum-foe/decisions.md` — D001 决策详情

### 2. B5 锚论文全文（阶段 0.1 核查对象，必读全 252 行）
- `papers/doi/10.1016_j.optcom.2024.130981/content.md` — abstract/intro/experiment/conclusion 四处一致 ±4.5GHz，残频指标全在

### 3. B5-Q1 详评（S003 已做 D006/D005/范围三维，本专题补 A1/复用）
- `papers/_read_notes/_B5-short-time-spectrum-cfo-increment.md` L55-60（M-C-A）+ L100-167（全文增量核验段）+ L162（D006 边界残留）
- `.sessions/2026-07-05-carrier-sync-v2-cut-pattern/_cut-b4b5-verify.md` L59-69（范围优势核验）+ L64-66（"本体无 vs baseline 改善 X dB"警示）
- `.sessions/2026-07-05-carrier-sync-v2-cut-pattern/_cut-map-final-b1-b12.md` §A L19-29（饱和池定位）+ §C L118-165（饱和池警示）
- `.sessions/2026-07-05-carrier-sync-v2-cut-pattern/_cut-b4b5-paillier-pool.md` L39-46（B5 切法动作 + Paillier 大池）

### 4. 复用基建（部分复用需新增）
- `projects/simulation/common/_recovery.py` — fft_foe (L37) / 其他估计器
- `projects/simulation/simulator/sc_nda_ml_sim.py:137` — fft_foe_m0_omega（short_time_spectrum_foe 起点骨架）
- `projects/simulation/params.py` L611-628 — B7Params（B5Params 参数族模板参考）

### 5. 框架文件 + 教训
- `stages/gw-feasibility.md` §D 维度 D MVE 11 步
- `thesis-lessons.md` TL-13（共用信道）/ TL-20（先建理论预期）/ TL-26（参数溯源读原文数值）/ TL-27（oracle 上界前置）
- `.agents/skills/sim-preflight/SKILL.md` §1.6 C6-C8 + `rules/mve-validation.md` V1-V6 + `rules/interrupt.md` 第 10-12 条

### 6. 上游决策链 + S031
- `.sessions/2026-06-20-problem-driven-redirection/decisions.md` — D005 务实路线 / D006 红线 / D017/D018 判读框架
- `.sessions/2026-06-20-problem-driven-redirection/S031-step4a-priority-and-go-kill-top5.md` — B5-Q1 排第二档 #6 依据

### 7. 参照候选（LEO Doppler 主题交叉，机制正交）
- `.sessions/2026-07-08-b7-gardner-ted-foe/` — B7 Gardner TED（LEO Doppler rate 适配，定时域机制正交）
- `.sessions/2026-07-06-step4a-mve-execution/decisions.md` L113/119/247 — NDA-ML Doppler 已建模但是残余级（F_RESIDUAL=1MHz），不是 B5 ±4.5GHz 全量程

## 接收方验证（读完文件后必须完成）

逐项打钩后才能动手（H001 §接收方验证）：

- [ ] 已读取 topic-index 14 不变量（重点 11/12/13/14 B5 特殊）
- [ ] 已验证 3 条关键事实声称：
  - [ ] B5 本体无"vs baseline 改善 X dB"对比只给绝对残频/范围指标（核查 `_cut-b4b5-verify.md:64-66`）
  - [ ] ±4.5GHz 出处 B5 锚 abstract/intro/experiment/conclusion 四处一致（核查 `papers/doi/10.1016_j.optcom.2024.130981/content.md:23, 29, 143, 167`）
  - [ ] B5 不撞 D006（前馈频域找谱峰，核查 `_B5-short-time-spectrum-cfo-increment.md:145, 162`）
- [ ] 已检查 _registry.yaml 中本专题 depends_on（4 依赖全稳定）
- [ ] 已确认当前范围未违反"明确不含"（不回头救 6 次 Kill / 不判 NDA-ML/B7/B2 决策 / 不改框架 / 不跳框架 / 不推翻 D006 / 不污染 common）

## 执行节奏（守 3 步上限）

**本轮 3 步**：
1. 报到 + 读必读清单 1-7（尤其 B5 锚 content.md 全文 + S003 详评）
2. 阶段 0.1 够格路径验证（派子 agent 核查 B5 范围优势具体指标 + 主线验证够格路径 3 选项）
3. 阶段 0.2 dB/范围溯源核查（主线定，不一定要子 agent）

**超 3 步主动建议分对话**。阶段 0.3-0.6 留下一对话（H001 §下一轮）。

## 产出物（本轮交付）

1. `explore/b5-leo-doppler-spectrum-foe/_qualification_path_validation.md` — 阶段 0.1 够格路径验证（3 选项分析 + 判定门控）
2. `explore/b5-leo-doppler-spectrum-foe/_db_range_sourcing_audit.md` — 阶段 0.2 dB/范围溯源核查
3. S002 session note — 本轮记录
4. H002 handoff — 交下一对话执行阶段 0.3-0.6

**explore/ 目录在 `projects/simulation/explore/b5-leo-doppler-spectrum-foe/`**（不是根目录的 explore/）。

## 红线（违反必须停）

1. **禁直接当 Go 跑 MVE**（范围优势够格路径未验证 + 饱和池警示双红旗）
2. **禁跳阶段 0 直接写代码**（profile 第 9 次防线 + INVARIANT 6）
3. **禁默认够格**（范围优势够格路径必须阶段 0.1 验证具体走 BUPT 模板 / 补 dB / 鲁棒性哪条）
4. **禁走环路 TF 联合建模**（阶段 0.3 湍流致功率波动归一化必须走前馈路径）
5. **禁自建信道**（TL-13，从 common/_channel.py 导入）
6. **禁污染 common**（explore 探针不进 experiments，MVE 通过才转正）

## 开场怎么报

按 session-governance Trigger 1 报到，简版即可：

> 续接 B5-Q1 专题（2026-07-08-b5-leo-doppler-spectrum-foe），主控对话 S001 + H001 派发。本轮目标：执行阶段 0.1-0.2（够格路径验证 + dB/范围溯源核查），不写代码。已读 [列出读过的关键文件]。接收方验证 [N 条全打钩]。开始阶段 0.1。

---

**主控对话跟进点**（你产出后主控对话会核查）：
- 阶段 0.1 的够格路径验证是否真对标了 BUPT Arria 10 FPGA demo 会议模板（不是绕过）
- 阶段 0.2 的 dB/范围溯源是否全读原文数值（不只引位置）
- B5 vs B7/B4 的 LEO Doppler 主题差异化是否明确
