# [R001] CCISP 内容诊断与 Change Contract

> 2026-07-14 | 关联：2026-07-14-ccisp-content-expansion / S001

## 调研问题

当前 CCISP 论文是否存在可由真实、可追溯内容补足的篇幅缺口？哪些缺口同时通过 benchmark、argument、evidence 三门？在不运行新仿真、不修改数据或算法的前提下，应签订什么修改合同？

## 发现

### 1. 当前 phase 和范围

- 当前 phase：`PROPOSE`。
- 已完成：INTAKE、DIAGNOSE。
- 本轮明确不含：WRITE、论文正文修改、新仿真、数据/JSON/算法修改、未经批准的图形重做。
- 目标读者：CCISP 通信/信号处理审稿人；目的：用真实证据闭合论证并形成符合会议密度的 5–10 页完整稿。
- 官方约束证据：CCISP 官方投稿页 `https://www.ccisp.org/sub.html`，2026-07-13 已核验 full paper 5–10 pages、double-blind；本轮未重新联网访问。

### 2. 最新构建与版本身份

| 项目 | 结果 |
|---|---|
| 权威入口 | `projects/simulation/paper/ccisp2026/main.tex` |
| 完整命令 | `$env:Path = 'C:\Program Files\Git\usr\bin;C:\Users\zzt\AppData\Local\Programs\MiKTeX\miktex\bin\x64;' + $env:Path; latexmk -gg -pdf -interaction=nonstopmode -halt-on-error main.tex` |
| 构建结果 | exit 0；6 页；374,410 bytes |
| PDF 时间 | 2026-07-14 10:29:16.727 +08:00 |
| PDF SHA256 | `06CA499645595A5A8207B62C8D7F95FDA64210E20AEB9A23FBDF7598A85030B5` |
| 最新正文源 | `sections/method.tex`，2026-07-13 23:16:59.179 +08:00 |
| 一致性 | PASS：`-gg` 全量重建；`main.fls` 含六章节和三张输入图；源均早于 PDF |
| 最终日志 | 无 LaTeX error、未定义交叉引用、overfull/underfull；仅 MiKTeX 更新提示 |

G0 版本身份 PASS。编译器没有 undefined citation，不代表正文中 11 处红色显式引用占位已解决。

### 3. 有效内容量测

| 指标 | 当前值 |
|---|---:|
| 名义总页/栏 | 6 页 / 12 栏 |
| texcount 正文词 | 2,219 |
| 含标题、caption、脚注等 | 2,441 |
| 有效正文跨度 | 约 3.0–3.2 个双栏页；剔除两张占位图和占位表后更低 |
| 完全无正文页 | 第 5、6 页 |
| 完全空白栏 | 第 4 页右栏、第 6 页右栏，共 2/12 栏 |
| 图独占 | 第 5 页跨栏 BER 图独占整页；第 6 页仅左栏两图 |
| 参考文献 | 3 条，约占第 4 页左栏 12% 高度，约 0.06 个双栏页 |

逐页证据：`tmp/pdfs/ccisp-content-expansion/page-1.png` 至 `page-6.png`。

| 节 | 正文词 | 公式 | 图 | 表 | cite 命令/唯一键 | 显式未解析引用 |
|---|---:|---:|---:|---:|---:|---:|
| Abstract | 133 | 0 | 0 | 0 | 0/0 | 0 |
| Introduction | 420 | 0 | 0 | 0 | 4/3 | 4 |
| System Model | 341 | 2 | 1 占位 | 0 | 3/2 | 7 |
| Method | 715 | 3 | 1 占位 | 0 | 2/1 | 0 |
| Results | 513 | 0 | 3 | 1 占位 | 0/0 | 0 |
| Conclusion | 97 | 0 | 0 | 0 | 0/0 | 0 |

诊断：G6 明确成立；G1 为 PARTIAL，而非“缺两整页正文”。当前 2,219 正文词接近可比短会论文 OECC 的 2,247 词，低于既有 2,500–3,000 合理目标。可辩护净增量约 300–600 词；强行补到 3,500 词以上没有 benchmark 支持。

### 4. Benchmark 内容缺口矩阵

样本：Johst/WiSEE 2024、Le Bidan/ICSOS 2023、Panasiewicz/MWP 2022、OECC-PSC 2025、Paillier/ICSOS 2019。五篇均可用于论证职责；篇幅预算主要参考 Panasiewicz 2,650、OECC 2,247、Paillier 3,025 三篇短会稿。

| 内容项 | n/5 | 我方当前 | 结论 |
|---|---:|---|---|
| 背景、现有方法局限、散文式贡献 | 5/5 | 已有 | 非缺口 |
| 信道/信号/损伤模型 | 5/5 | 有，但块定义和参数来源冲突 | BLOCKED |
| 核心参数及选择依据 | 5/5 | `gamma_th` 无实际数值/两层判据 | 明确缺口，BLOCKED |
| 接收机/算法架构图 | 4/5 | 两张 DRAFT placeholder | 明确缺口 |
| 核心算法公式 | 4/5 | 已有 3 个核心式 | 非缺口，但 DA 式需一致性修复 |
| 替代方案比较/弃用理由 | 4/5 | 当前 Method 已覆盖 | 旧 R014 缺口已关闭 |
| 设计权衡 | 5/5 | 当前 Method 已覆盖 | 旧 R014 缺口已关闭 |
| 实现代价/延迟 | 4/5 | 有声称，无实现证据 | BLOCKED |
| 独立实验设置 | 5/5 | 当前 Results 已覆盖 | 旧 R014 缺口已关闭 |
| 同图 baseline 横比 | 3/5 | DA/NDA/AWGN/Oracle 图 | 有，但 Oracle 未定义、口径不一致 |
| 代表数字锚点 | 5/5 | 有三类数字 | benchmark PASS，evidence BLOCKED |
| 结果解释 | 3/5 | 有，但含反向/无证因果 | BLOCKED |
| 单独参数/增益表 | 1/5 | Table I 仍 TBD | 不支持为篇幅加表 |
| 链路几何 | 2/5 | 无 | 可选，但本文 argument/evidence gate 不过 |
| 完整推导链 | 2/5 | 无 | 不添加 |
| 伪代码 / 独立 Related Work | 0/5 / ≤1/5 | 无 | 禁止添加 |

关键更新：R014 基于旧稿认定的“替代方案比较、设计权衡、实验设置”三项缺口，在当前源中已经关闭，不能重复补一遍。

### 5. 专业性审计

| 维度 | 状态 | 证据摘要 |
|---|---|---|
| 术语与缩写 | GAP | `naive` 未定义；APSK/AWGN/HD-FEC 首次展开不完整；内部别名 B11 仍在正文 |
| 系统假设和场景 | BLOCKED | 信道块 `CH_BLOCK=100`，CPR/切换块 `N_DFT=256`；正文把二者写成同一 fading block |
| 公式与代码一致 | BLOCKED | DA 文字称多导频平均，式(1)仅单样本；正文单阈值，代码是 CV 门控 + blind-h effective SNR + 13 dB |
| 方法可复现性 | BLOCKED | 未报告 `gamma_eff_th=13.0`、`CV_MARGIN=1.10` 和 CV 模型 |
| 参数来源 | BLOCKED | 4 组来源、11 处显式引用 unresolved；上行 alpha/beta 是设计近似 |
| Baseline 定义/公平性 | BLOCKED | data/full BER 口径混用；Oracle 未定义；26/29 仅有临时审计指针 |
| 指标口径 | BLOCKED | Fig.4 实际是同 SNR 的 BER ratio dB，caption/正文称 SNR gain |
| 引用真实支撑 | BLOCKED | 仅 3 个正式 citekey，核心场景/参数仍依赖 4 组 unresolved |
| 结果数字和解释 | BLOCKED | 17.9/18.0、1.85/1.9、扫描范围冲突；29 的组成未定义 |
| 物理归因 | BLOCKED | crossover 左移却写 DA 优势窗口扩大，方向相反；多句因果无受控证据 |
| 内部代号/TBD/占位/空话 | GAP | 标题/作者 DRAFT；Fig.1/Fig.2 占位；Table I 三格 TBD；future work 无必要职责 |

### 6. 核心事实矩阵

| 论点 | 来源/对比/指标 | 代码/图表 | 允许强度 | 状态 |
|---|---|---|---|---|
| DA/NDA 在已测 SNR 区域发生交叉 | 30-seed DA vs NDA；data-symbol BER | `fair_comparison.py:98-109`；BER/crossover 图 | 仅写“在已测场景观察到交叉” | GAP：引用不完整 |
| crossover 随湍流增强左移 | 事后 log-BER 插值 | `plot_fig4_crossover.py`；Fig.5 | 只报观测值，不当算法阈值，不做物理归因 | BLOCKED：数字未统一 |
| 实际 switching | switching vs fixed DA/NDA；两层判据 | `_a4_switch_30seed_fixed.py:64-90`；JSON meta 13 dB/1.10 | 必须忠实写 CV 门控、blind h、固定 13 dB 后才可讨论 | BLOCKED |
| 26/29 选中工作点赢家 | data 口径；AWGN 8 + 三档各 7 = 29 | `decisions.md` D005；原脚本仅 `/tmp` | 只能称“历史审计报告，待持久证据复核” | BLOCKED |
| switching vs fixed NDA 低 SNR 改善 | 同一 SNR 下 `10log10(Pb,NDA/Pb,sw)` | `plot_fig3_gain.py:2-10,38` | 只能称 BER reduction in dB | BLOCKED：现稿错称 SNR gain |
| 强湍流约 1.2–1.9 dB | NDA vs DA；工作区/equal-BER 口径 | `fair_comparison.py:84-150`；既有 summary | 归属于 NDA 相对 DA，不归属于 switching | BLOCKED/G7 |
| 低复杂度 | 无测量；实际需 CV、h、两支估计 | `method.tex` 对比 switching 脚本 | 不得声称 one comparison/negligible overhead | BLOCKED |

主控复核：`plot_fig3_gain.py` 明示该指标“not an equal-BER horizontal shift”；`fair_comparison.py:109,147-149` 明示 1.9 dB 链是 NDA-vs-DA。现稿把 26/29、BER ratio dB、DA/NDA SNR 差捆成同一 switching 贡献，事实链不成立。

### 7. 论证链缺口

```text
DA/NDA 权衡问题
  -> [缺可靠引用] 固定选择在本文 16APSK/GG 场景的具体不足
  -> [概念存在] 按块选择 DA/NDA
  -> [实现失真] 正文单 SNR 阈值；代码为 CV + blind-h gamma_eff + 13 dB
  -> [实验错配] 100-symbol channel block 与 256-symbol CPR/switch block 混称
  -> [指标错接] BER ratio dB 被写成 SNR gain；1.9 dB 属于 NDA-vs-DA
  -> [结论越界] Abstract/Intro/Conclusion 把不同链路捆成 switching headline
```

- 重复：Results 同段两次列 crossover；Method 两次解释相同高低 SNR 权衡；Abstract/Intro/Conclusion 近似复读同一未闭合 claim。
- 错序：先宣称 switching 1.9 dB，再到 Results 才出现两个不同含义的“gain”，但未定义关系。
- 无职责/无证职责：复杂度、调制格式独立性、future work、crossover 物理因果。

### 8. 根因表

| ID | 症状 | 根因 | 证据 | 最小验证 | 否决条件 | G/L级别 | 影响位置 |
|---|---|---|---|---|---|---|---|
| RC-01 | 名义 6 页、正文约 3.1 页 | float 排布把 3 张图推到两页且两栏失衡 | page-4/5/6 PNG | 重新排版后逐栏量测 | 仍有 figure-only/全空栏 | G6/L3 | results/layout |
| RC-02 | 旧诊断称缺三项内容 | 当前源已补了比较、权衡、设置，但旧 R014 未更新 | method 36/38；results 4 | 对当前源重算 n/5 | 任一职责实际不存在 | G0/G1 | benchmark 基线 |
| RC-03 | switching 被写成 1.9 dB | 三条不同数据链在写作阶段被合并 | fig3 脚本、fair_comparison、Abstract | 建唯一 claim→JSON→metric 表 | 1.9 仍无 switching baseline | G7/L6 | 全文 headline |
| RC-04 | 方法公式不能复现实现 | 论文简化跨过信息流边界 | method 29-38 vs decide() 64-90 | 逐字段契约审计 | 省略 CV/13dB 会改变决策 | G4/L4-L5 | SM/Method |
| RC-05 | 块语义混乱 | channel block 与 DSP block 被合称 fading block | `_b11_params.py:35,39` | 追踪生成/估计/CPR边界 | 100 与 256 无合法对应 | G4/L4 | SM/Method |
| RC-06 | 物理解释方向反了 | 从共变曲线推因果且未做方向检查 | results 16；17.9→10.7 | 只保留数据事实或找证据 | 无受控证据支持因果 | G2/G4/L5 | Results |
| RC-07 | 关键参数/引用悬空 | 骨架只纳入 3 条白名单引用 | issues B-03；11 unresolved | 对每句逐引文核对 | 无真实一致来源 | G3/L1-L2 | Intro/SM |
| RC-08 | 想用扩写解决页数 | 把 G6 版面症状误当纯 G1 | 2,219 词 vs 2,247–3,025 benchmark | 以 2,500–3,000 词和职责闭环验收 | 需 >3,200 词才能满足主观页数 | G1/G6 | 全文 |

### 9. 候选补强包

#### 必须补/先解决

**P0 事实链与贡献归属校正（前置门，净字数可增可减）**

- 补什么：把 26/29、BER reduction dB、DA-vs-NDA SNR gain 分为三条事实链；正文与代码一致；统一块语义、DA 式、crossover 数字/扫描范围。
- 为什么：G4/G7 不解除，扩写只会扩大错误。
- benchmark：5/5 要求可解释参数/结果；4/5 方法链可复现。
- 本文证据：switching 脚本/JSON、fair_comparison、Fig.3/4 脚本、issues B-01～B-07。
- 内容量：不是凑字，预计净 -100～+150 词。
- 影响：Abstract、Intro、System Model、Method、Results、Conclusion、captions、issues。
- 停止：若不运行新仿真就无法给 switching 建合法独立增益，删除/降级该 headline，停止扩写并交用户决定定位。

**P1 系统/实验契约与参数溯源（预计 +150～250 词）**

- 补什么：区分 100-symbol channel block 和 256-symbol DSP block；定义上/下行参数仅为仿真 regimes；明确 modulation、pilot、BER 分母、seed、SNR sweep、Oracle/baseline 信息访问。
- benchmark：模型/参数 5/5，实验设置 5/5。
- 本文证据：`_b11_params.py`、SimulationConfig、现有 JSON、可核引用。
- 影响：System Model、Results setup、图注。
- 停止：核心参数无来源或块边界无法自洽。

**P2 真实 switching 信息流与阈值协议（预计 +120～220 词，替换现有失真段）**

- 补什么：CV 前置门控、blind h effective-SNR、固定 13 dB、候选分支、信息访问和实际计算成本；配已获视觉接受的真实机制图，未接受则不替换占位。
- benchmark：核心参数 5/5、架构图 4/5、实现代价 4/5。
- 本文证据：`decide()`、JSON meta、既有 Fig.2 资产。
- 影响：Method、Fig.2/caption。
- 停止：忠实描述会暴露方法无法支撑当前定位，转 P0 的 G7 决策，不做美化。

**P3 指标与结果解释闭环（预计 +80～150 词，但删除重复/无证归因）**

- 补什么：每张图定义对比对象、公式、工作点；只给有来源的代表锚点；把共变现象与因果解释分开。
- benchmark：代表数字 5/5、结果解释 3/5、图文分工 5/5。
- 本文证据：plot 脚本、现有 JSON、R015。
- 影响：Results、captions、Abstract/Conclusion 边界。
- 停止：指标不能由持久数据产物复现。

#### 可选补强

**P4 真实系统/方法图替换**：4/5 benchmark 支持，但它解决专业性和职责，不算正文补足；只使用已接受资产，不在本合同重做图。

**P5 最小领域定位句**：若可核引用支持，可用 1–2 句说明固定 DA/NDA 选择的具体不足；不新建 Related Work。

#### 禁止补/纯凑页

- 独立 Related Work、伪代码、完整推导链、链路几何、项目/标准化背景。
- 新参数表、更多表格、逐点数字堆砌；当前 Table I 不能仅因占页保留。
- 泛泛背景、空洞意义、limitations、future work、失败路线、弱场景负面定性。
- 无来源的物理归因、用图尺寸/参考文献/强制分页填页。

### 10. 正式 Change Contract

**合同版本**：`CCE-CC-001`  
**状态**：PROPOSED / NOT APPROVED  
**批准语句要求**：用户明确回复“批准 CCE-CC-001”或明确批准其修改版；普通“继续/开始/直接改”不算批准。

#### 修改批次和文件

1. **Batch A：P0 事实链前置门**
   - 文件：`sections/abstract.tex`、`introduction.tex`、`system_model.tex`、`method.tex`、`results.tex`、`conclusion.tex`、`issues.md`。
   - 内容：校正贡献归属、指标名、块语义、公式/实现、数字口径和无证物理归因。
   - 证据：现有代码、JSON、绘图脚本、D005/D008/R017、B-01～B-07。
   - Gate：所有核心论点有唯一 source→metric→comparison 链；否则停在 BLOCKED，不进 Batch B。

2. **Batch B：P1+P2+P3 真实内容补强**
   - 文件：`system_model.tex`、`method.tex`、`results.tex`，必要时同步 Abstract/Intro/Conclusion。
   - 新增：系统/实验契约、真实 switching 信息流、参数和 baseline/metric 定义、受支持的结果解释。
   - 证据：仅使用已存在且可追溯的代码/数据/公式/文献；不运行新仿真。

3. **Batch C：引用、术语、图表和版面收口**
   - 文件：`references.bib`、六章节、已批准的 Fig.1/Fig.2 资产、LaTeX float 设置。
   - 内容：关闭 11 个显式 unresolved；首次展开缩写；删除 DRAFT/TBD；替换已接受图；消除 figure-only page 和空白栏。
   - 限制：不新设计 Fig.1/Fig.2，不改数据图数值，不靠缩放/参考文献凑页。

#### 明确不动

- 仿真算法、实验参数、结果 JSON、原始数据、绘图数据和曲线数值。
- 未批准的 Fig.1/Fig.2 设计方向。
- 用户未提供的作者/单位/邮箱信息；双盲元数据另行确认。
- 范围外历史专题和旧债务。

#### B-01～B-07

- **必须先解决。** 其中 B-01/B-02/B-05/B-06/B-07 属 Batch A；B-03/B-04 是 Batch C/官方约束门。
- 新增阻塞：G4-块语义、G4-指标错名、G7-贡献错接、26/29 缺持久证据。

#### 验收标准

- 核心事实矩阵全部 PASS；无数字/指标/公式/代码/图表冲突。
- 正文词数目标 **2,500–2,900**；上限不是硬凑，若职责已闭环可低于 2,900。
- 有效正文目标约 **3.6–4.1 个双栏页**；官方 5–10 页按总稿计，不把“5 页纯文字”伪装成官方要求。
- 总稿 5–6 页优先；无 figure-only page、无完全空白栏、无异常页底空白。
- 0 个 `DRAFT/TBD/UNRESOLVED CITATION/B11/naive` 未定义残留。
- Fig./Table/caption 中每条 baseline 和 metric 自包含；Table I 若无非冗余职责则删除。
- fresh full rebuild + 全页 PNG 目检 + 确定性 grep + 独立 verifier；任一门失败只报 PARTIAL/BLOCKED。

#### 失败/停止条件

- 1.9 dB 无法合法归属于 switching 且用户不接受重定位/降级。
- 忠实写出实际判据后，核心 contribution 与冻结定位冲突。
- 任一关键参数/引用/指标无持久证据。
- 内容净增量需要超过约 600 词才满足主观页数；这意味着正在越过 benchmark gate。
- 需要新仿真、新数据或算法修改；立即退出写作流程，单独报告。

## 结论

当前“名义 6 页、实质正文约 3 页”事实成立，但根因不是单纯缺两页正文：G6 浮动体失衡很重，当前 2,219 正文词已经接近短会 benchmark 下沿；真正高优先级是 G4 实现/指标冲突与 G7 贡献错接。可辩护的真实补强量约 300–600 词，目标为 2,500–2,900 正文词和 3.6–4.1 个有效双栏页，再通过正常图文编排形成 5–6 页完整稿。

## 对决策的影响

- 需用户决定是否批准 `CCE-CC-001`。
- 在批准前不进入 WRITE。
- 若用户不同意先解决 G4/G7，则本专题保持 BLOCKED，不能只做内容扩写。
