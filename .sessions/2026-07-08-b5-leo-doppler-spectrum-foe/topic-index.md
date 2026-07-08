# Topic Index: B5-Q1 LEO Doppler 短时谱 FOE 第四候选

> slug: 2026-07-08-b5-leo-doppler-spectrum-foe
> status: active | created 2026-07-08 | last_updated 2026-07-08（S007 路 2 Step 4a sandbox 执行 → Kill。2×2 算子×FFT 分辨率消融实测：算子贡献 −1%（<10% Conditional-Kill 阈值），FFT 分辨率贡献 101%。M-C-A 的 A 假设（对数比小残频不稳）证伪：B/A σ 比=1.00，linear-log 相关 0.994。66% σ 差异全部来自 n_fft=16 参数选择（B5 锚公开工程参数，Vieira 可同样采用，非独占）。维度 A0+C 双 FAIL，无 salvage → Kill B5-Q1（D004/V001）。主线 V5 独立重算算子占比 −0.7% 可复现。新发现 experiment_C α 标定 bug（grid C 未为 n_fft=1024 重标 α，σ 14.1 被人为压低，真实 29.0；不影响 Kill 结论但修正 S005 旧归因）。H008 交用户决定候选池下一步）

## 专题定位（一句话）

B5-Q1（LEO Doppler 短时谱 FOE，正负功率谱面积比）第四候选 MVE 执行。与 NDA-ML（dormant）/ B7（active）/ B2-Q2（active）并行。**首要张力**：B5-Q1 不是 dB 增量是范围优势（±4.5GHz vs 传统 ±312.5MHz，15× 范围扩展），D005 "赢 baseline 几 dB" 标尺下不够格，靠范围维度够格（会议门槛放宽允许）。**开专题首验证够格路径**——范围优势在 D005 会议门槛下能不能当 Go 判据。**流程规划前置**（阶段 0 不写代码先定规约）防重蹈 NDA-ML 6 类混乱。

## 原始目标（冻结，不可修改）

对 B5-Q1 走 Step 4a 维度 D MVE，守 FR-21/TL-20/FR-18/FR-12 + D005 务实路线 + D006 红线 + **sim-preflight v1.3.0**（C6-C8 公式核对/三方对照/祖师爷警报 + V1-V6）。

**冻结边界**：
- 只做 B5-Q1（LEO Doppler 短时谱 FOE 正负功率谱面积比），不回头救 6 次 Kill
- 不跳框架（FR-22，当前在 Step 4a 维度 D）
- 不推翻 D006（前馈不撞 / 环路 TF 联合建模则撞）
- 不改框架文件（守"先测不改协议"）

## 范围边界

### 原始目标（冻结）
对 B5-Q1 走 Step 4a 维度 D MVE。

### 当前范围
- **阶段 0 前置规约**（不写代码，先定 6 项规约，防 NDA-ML 6 类混乱）：
  0.1 **够格路径验证**（范围优势在 D005 会议门槛下能不能当 Go 判据，对照切法地图 BUPT Arria 10 FPGA demo 会议模板 + 饱和池警示）—— B5-Q1 最高优先项
  0.2 dB/范围溯源核查（±4.5GHz 出处 + 残频指标 σ<140MHz / <5MHz / ±312.5MHz 精估范围，全读原文数值）
  0.3 架构定性（前馈频域找谱峰+星历预测调 LO，不撞 D006；但湍流致功率波动归一化是边界，前馈归一化合法 / 环路 TF 联合建模则撞）
  0.4 公平对照框架设计（baseline 是 [60] Leven Mth-power 还是传统 FFT FOE？范围 fair gain 怎么定义？工作点 BER 1e-3 还是 HD-FEC？叙事定位跟 B7/B4 LEO Doppler 主题差异化）
  0.5 参数真相源前置（Doppler ±4.5GHz / 56MHz/s 变化率 / 2.5GBaud / 1550nm / 600km 轨道 / 精估范围 ±312.5MHz 一开始进 params.py 单字段）
  0.6 文件组织规约（`explore/b5-leo-doppler-spectrum-foe/` 目录结构 + 命名规则）
- **阶段 1 sandbox 三方对照**（B5 短时谱 FOE / [60] Leven Mth-power / 传统 FFT FOE）
- **阶段 2 TL-20 理论预期表**（仿 N1-MVE-SPEC.md §2）
- **阶段 3 MVE + consistency**（守 sim-preflight v1.3.0 C6-C8 + V1-V6）

### 明确不含
- ❌ 不回头救 6 次 Kill
- ❌ 不判 NDA-ML/B7/B2 那边的方向决策（那是各自专题的事）
- ❌ 不改框架文件
- ❌ 不跳框架（FR-22，当前在 Step 4a 维度 D）
- ❌ 不推翻 D006（前馈不撞 / 环路 TF 联合建模则撞）
- ❌ 不污染 common（explore 阶段探针不直接进 experiments，MVE 通过才转正）

### 范围变更记录
- **2026-07-08 D002**：撤回 S005 MVE PASS 建议。S005 报"MVE 三项全 PASS 建议判 Go"建立在错误前提上（V3 选错对照对象 [60]Leven→应选同族 Vieira PSA + sandbox 对照不公平 + BER 全 fail 幽灵）。新增"范围优势结实度审计"（3 决定性问题：BER 根因/公平范围对照/同族 PSA 对照），审计结果决定 B5 去留。原因：用户追问"范围优势到底有没有"+ 3 角度并行证伪侧审计发现致命盲点。**D001 不动**（开专题决策仍 active），撤回的是 S005 的 Go 倾向解读
- **2026-07-08 D003 + S006**：路 2 重定位后的 Step 3 补精读。精读发现 H006 初稿的 M-C-A 多处需修正（见 S006 §2 表格），但**不构成方向变更**（路 2 同族精度改进路线不变，只是 baseline 参数和归因设计更精确）。当前范围仍 = 路 2 Step 4a 重走
- **2026-07-08 D004 + S007**：路 2 Step 4a 维度 A0+C 双 FAIL → Kill B5-Q1。2×2 消融证伪 M-C-A 核心（算子贡献 −1%，对数比小残频不稳不成立），66% σ 差全部来自 FFT 分辨率参数。范围终止：B5-Q1 不再推进，候选池决策交用户

## 不变量（动任何一条必须重新讨论）

1. **继承上游专题 `2026-06-20-problem-driven-redirection` 全 9 条不变量**（D017/D018 判读框架 / D006 红线 / D005 务实路线最高优先级 / 范围硬门 / 问题从文献长出来 / 委托技术判断守 Go/Kill / 3 步上限 / 核查机制中性双向 / GW 流程强制门控）
2. **D005 务实路线（INVARIANT 最高优先级）**：Go 判据=赢传统未优化 baseline 几 dB（会议门槛放宽：纯仿真+鲁棒性 dB/范围/绝对指标/同族 dB 都算够格）；oracle 上界 FR-21 降级为参考不当 Kill 门
3. **FR-22 GW 流程强制门控**：当前在 Step 4a 维度 D（MVE），禁跳到 Contract/Execute
4. **FR-25 Go/Kill 标准分离**：Go 标准=赢传统 baseline / Kill 标准=A0 致命+MVE FAIL，FR-21 只在 A0 通过后做 Kill 工具
5. **切法地图是参照系不是答案**：B5-Q1 是饱和池 §A（B1-B5），跟 B4 共锚 Paillier 星地相干下行 ground receiver（43 篇大池）。引用模式不搬"切法地图说这个好"
6. **profile 第 9 次"急于推进"防线激活**：B5 流程规划阶段主线极易"阶段 0 太繁琐先跑起来再说"。**防线：阶段 0 六项规约必须全做完才进 sandbox，禁跳阶段 0 直接写代码**（NDA-ML 最大混乱就是阶段 0 没做）
7. **TL-26 参数溯源强制**：B5 每个关键参数（Doppler ±4.5GHz / 56MHz/s 变化率 / 2.5GBaud / 精估范围 ±312.5MHz）必须标文献来源（B5 锚 optcom.2024.130981 / [6] 卫星建模 Ref），禁拍参数。**且必须读原文数值不只引位置**（D-009 教训 5，FR-26 强化）
8. **TL-13 共用同一信道实现**：B5 必须从 `common/_channel.py` 导入，禁自建信道
9. **TL-20 先建理论预期**：MVE 跑之前必须写明理论预期表，仿 N1-MVE-SPEC.md §2
10. **核查机制中性双向**：子 agent 产出 + 主线独立 grep 核查，**子 agent 归因必须主线独立重算验证**（D-009 教训 6，只信原始数字不信归因）
11. **【B5 特殊·INVARIANT，D003+S006+S007 终判】够格路径 = B5-Q1 Kill**：~~原：范围优势（±4.5GHz vs ±312.5MHz，15×）~~ **D003 证伪**：范围优势是星历预补特权功劳（fft_foe 配星历即 19/19 持平，残留 1.00×）。~~路 2 重定位：同族 PSA 精度增量（B5 线性比 vs Vieira 对数比 σ 好 66%）~~ **D004/S007 证伪**：2×2 算子×FFT 分辨率消融实测算子贡献 **−1%**（<10% Conditional-Kill 阈值），66% σ 差全部来自 FFT 分辨率参数（n_fft=16 是 B5 锚公开工程参数，Vieira 可同样采用，非独占）。M-C-A 的 A 假设（对数比小残频不稳）证伪：B/A σ 比=1.00，linear-log 相关 0.994。维度 A0+C 双 FAIL，无 salvage → **Kill B5-Q1**。两条够格路径（范围优势 / 同族精度增量）双证伪，B5-Q1 不再推进
12. **【B5 特殊·INVARIANT】饱和池警示 + Paillier 大池竞争**：切法地图 §C 警示"Paillier 安全区恰恰是 dB 最难出区"（Spalvieri 85 同构）。B5 饱和池 §A 跟 B4 共锚 Paillier 星地相干下行 ground receiver（43 篇大池），**B5-Q1 的够格必须独立 MVE 产出**，不能引 Paillier 大池的 dB（B5 是范围优势不是 dB 增量）。**但 BUPT Arria 10 FPGA demo 是会议级模板**（绝对指标够发会议），B5 可走此路径
13. **【B5 特殊·INVARIANT】D006 边界残留（湍流致功率波动归一化）**：B5 前馈功率比假设信号幅度稳定，湍流致幅度衰落会污染功率比估计（`_B5-...-increment.md:162`）。**若把湍流致功率波动纳入前馈归一化（AGC/归一化功率比）则不撞 D006**；**若纳入环路 TF 联合建模则撞 D006**（边界，只标不砍，与 B6-Q2/B7-Q2 同模式）。阶段 0.3 架构定性必须定死走前馈归一化路径
14. **【B5 特殊·INVARIANT】代码基建新增需求（short_time_spectrum_foe）**：B5-Q1 核心算法"分块 FFT + 正负功率谱面积比 + 星历预测"common/ **没有**（现有 fft_foe 是 4 次幂 blind QPSK 找谱峰，fft_foe_m0_omega 是 M0 升幂找谱峰，**都不是 B5 的"正负功率谱面积比 Rp-n"机制**）。**需新增 `short_time_spectrum_foe`**，可参考 `fft_foe_m0_omega`（sc_nda_ml_sim.py:137）作起点骨架（分块 FFT 部分复用），但"正负功率谱面积比 Rp-n + 归一化频偏估计 Δfest（系数 α=6×10⁸）"核心算法需新写。信道侧完全复用（TL-13），参数族参考 `B7Params`（params.py:611-628）扩 B5Params

## 其他结论（普通技术决策）

### B5 特殊风险（vs NDA-ML/B7/B2 的差异点，决定流程重点）

| 风险 | B5-Q1 情况 | NDA-ML 对照 | B7 对照 | B2 对照 | 流程对策 |
|---|---|---|---|---|---|
| 够格路径 | ⚠️ 不是 dB 是范围优势 | +2dB 达标 | 0.6dB OFC 原文 | +1dB 口径错位 | **阶段 0.1 够格路径首验证**（最高优先）|
| 饱和池竞争 | Paillier 43 篇大池 | 稀池独占 | 稀池独占 | 饱和池小池 3 篇 | 阶段 0.1 BUPT Arria 10 FPGA demo 会议模板对标 |
| D006 边界 | 湍流致功率波动归一化是边界 | 前馈不撞 | 前馈不撞 | 双模切换不撞 | 阶段 0.3 前馈归一化定死 |
| 代码新增需求 | short_time_spectrum_foe 需新写 | NDA-ML 已实现 | Gardner TED 已实现 | 4 估计器全有 | 阶段 0.6 文件组织 + fft_foe_m0_omega 作起点骨架 |
| A1 归属 | 加湍流+高阶调制+vs baseline dB（论文外改进空间窄）| ML 加权算法薄 | 场景迁移 | 双模切换算法创新 | A1 风险中等 |
| 主题撞车 | LEO Doppler 跟 B7/B4 机制正交 | (本身) | LEO Doppler | fade 跟 NDA-ML 撞 | 阶段 0.4 叙事定位（B5 频域功率比 vs B7 定时域 TED vs B4 双环）|

### NDA-ML 6 类混乱 + B5 防御措施（继承 B7/B2 框架）

| 混乱类 | NDA-ML 教训 | B5 防御措施 |
|---|---|---|
| A. 参数反复 | 线宽 500kHz→10kHz→疑似 0.1-1MHz，全量重跑 3 轮 | 阶段 0.5 参数真相源前置 + sim-preflight v1.2.0 param-source.md |
| B. 算法 bug | D003 双 bug + D-008 双 bug（漏 ML 加权+升幂未归一）| 阶段 0.2 dB/范围溯源核查 + V1 公式逐项核对（v1.3.0）|
| C. 验证失效 | consistency PASS 但算法错（两套都漏同一 bug）| V2 三方对照 + V3 祖师爷警报（v1.3.0 C7-C8）|
| D. 方向重定位 | B11 OFDM→单载波 / LMMSE 失败→VV/BPS | 阶段 0.3 架构定性前置（前馈归一化 vs 环路）|
| E. 文件混乱 | MVE 薄包装 + 双套参数共存 + 两 results 目录 | 阶段 0.6 文件组织规约 + 下游引用同步清单 |
| F. 文献引用 | D-007 引 Valjus 位置没读原文数值 | V6 FR-26 读原文数值（v1.3.0）|

## 已确认决策

- **D001**（2026-07-08，S001）：开 B5-Q1 专题 + 首验证够格路径策略（阶段 0.1 = 范围优势在 D005 会议门槛下能不能当 Go 判据，对标 BUPT Arria 10 FPGA demo 会议模板 + 饱和池警示）

## 悬而未决

1. ~~**范围优势够格路径**：阶段 0.1 核心问题——±4.5GHz vs 传统 ±312.5MHz 的 15× 范围扩展能不能当 Go 判据？~~ **✅ 已解决（S002）**：够格走路径 C（鲁棒性维度）为主 + 路径 A（BUPT 模板）+ 路径 B（补 dB 作 sandbox 验证维度）补充。B5-Q1 够格不转 Kill
2. **饱和池大池竞争**：B5 跟 B4 共锚 Paillier 43 篇大池，切法地图警示饱和池是 dB 最难出区。B5 走范围维度是否能绕开饱和池 dB 竞争？→ S002 判定 B5 走范围维度不直接跟饱和池 dB 竞争，但需 sandbox 验证范围优势在湍流下仍成立
3. ~~**D006 边界**：阶段 0.3 湍流致功率波动归一化走前馈路径（合法不撞 D006）还是环路 TF 联合建模（撞 D006）~~ **✅ 已解决（S003）**：走前馈归一化路径（AGC / 归一化功率比），禁环路 TF 联合建模。前馈归一化后范围优势三项验证 PASS（捕获范围确定成立 / 残频理论上成立带 sandbox 确认 / 收敛性成立应提升）
4. ~~**公平对照框架**：阶段 0.4 baseline 是 [60] Leven Mth-power 还是传统 FFT FOE？范围 fair gain 怎么定义？工作点 BER 1e-3 还是 HD-FEC？~~ **✅ 已解决（S003）**：baseline = 传统 FFT FOE 为主（任务环节对口）+ [60] Leven Mth-power 作祖师爷对照（C7 三方对照）。fair gain 二维报告（范围扩展 + 残频/BER）。双工作点 BER 1e-3 + HD-FEC 3.8e-3
5. ~~**LEO Doppler 主题差异化**：阶段 0.4 明确 B5/B7/B4 叙事定位~~ **✅ 已解决（S003）**：B5 频域功率比粗 CFO（15× 范围）/ B7 定时域 TED 精估（0.6dB OSNR）/ B4 双反馈环架构（MSE 4×）。机制正交无撞车，三种正交解法可作大论文跨章节统一叙事

## 当前位置

**🔴 B5-Q1 Kill（D004/S007，2026-07-08 对话 7）**：路 2 Step 4a 维度 A0+C 双 FAIL。2×2 算子×FFT 分辨率消融实测（主线 V5 独立重算可复现）：算子贡献 **−1%**（<10% Conditional-Kill 阈值），FFT 分辨率贡献 101%。M-C-A 的 A 假设（对数比小残频不稳）证伪——B/A σ 比=1.00，linear-log 算子相关 0.994。66% σ 差异全部来自 n_fft=16 参数选择（B5 锚公开工程参数，Vieira 可同样采用，非独占）。Salvage 评估无（既无算子贡献也无独占参数贡献）。守 D003"值得试≠强行 Go"→ Kill。两条够格路径（范围优势 D003 / 同族精度增量 D004）双证伪。新发现 experiment_C α 标定 bug（grid C 未为 n_fft=1024 重标 α，σ 14.1 被压低，真实 29.0；不影响 Kill 结论但修正 S005 旧归因）。H008 交用户决定候选池下一步。专题待转 closed。

## 进展线索

- **S001** 开题 + B5 特殊风险 + 阶段 0 六项规约设计 + 复用基建清单（2026-07-08，主控对话）
- **S002** 阶段 0.1-0.2 执行——够格路径验证（路径 C 鲁棒性维度够格）+ dB/范围溯源核查（20 字段全溯源 + [60] Leven 7dB penalty 溯源到原文 L123 + 残频上限公式溯源到 sat.1553 引 [60] Leven 公式 27）（2026-07-08，工作对话对话 1）
- **S003** 阶段 0.3-0.6 执行——架构定性（前馈归一化路径定死不撞 D006 + 范围优势三项验证 PASS：捕获范围确定/残频理论成立带 sandbox 确认/收敛性成立应提升）+ 公平对照框架（baseline=传统 FFT FOE 主 + [60] Leven 祖师爷 + fair gain 二维 + 双工作点 BER 1e-3+HD-FEC + B5/B7/B4 机制正交）+ B5Params 20 字段全溯源 + short_time_spectrum_foe 接口定义（参考 fft_foe_m0_omega 起点骨架 + 下游引用同步清单）。阶段 0 六项规约全收尾可进 sandbox（2026-07-08，工作对话对话 2）
- **S004** 阶段 1 sandbox 三方对照执行——B5 短时谱 FOE（short_time_spectrum_foe，598 行，分块 FFT + Rp-n + 星历预测 + 迭代收敛 + normalize_mode 三方案）+ [60] Leven Mth-power（leven_mthpower_foe，290 行）实现 + 三方对照 sandbox 脚本 + 3 结果 JSON + B5Params 落盘 params.py。路径 C sandbox PASS：范围扩展 14.4× + 湍流下残频 σ max 16.20MHz << 140MHz + 收敛性 19/19。主线独立核查（V5）全数字一致。关键发现：α=6×10⁸ 暗 ratio 模式 + block≡ratio + 星历预测预补偿覆盖 ±4.5GHz 全量程。可进 MVE（2026-07-08，工作对话对话 3）
- **S005** 阶段 2-3 MVE + consistency 执行——B5-MVE-SPEC.md（12 节 MVE 契约 + TL-20 理论预期表 + FR-11 架构摘要）+ mve_b5_short_time_spectrum.py（复用 sandbox + 3 新实验：V3 祖师爷警报/星历残差扫描/consistency）+ 2 结果 JSON。MVE 三项全 PASS：V3 未触发（83.8%>5%）+ 星历残差 max σ 10.03MHz<<140MHz + consistency 三项 0 ulp。V5 主线独立核查全一致。common 转正（short_time_spectrum_foe + leven_mthpower_foe 进 _recovery.py）。**Go 建议后撤回**（D002：V3 选错对照对象 + sandbox 不公平 + BER 幽灵）
- **S005 续** 范围优势结实度审计（D002/D003）——3 角度并行证伪侧审计发现致命盲点 → 修正版审计 3 决定性问题实测：① BER 根因非 bug（B5 估噪 6.8MHz >> fft_foe 0.05MHz）② **范围优势归零**（fft_foe 配星历 19/19=B5 19/19，残留 1.00×，Kill 级）③ **同族 PSA 增量**（B5 线性 vs Vieira 对数 σ 好 66%，V3 未触发，救命级）。D003：原定位崩塌转路 2 同族精度改进重定位（不 Kill，候选池偏弱+方向稀缺）。H006 交新对话（2026-07-08，对话 4 续）
- **S006** 路 2 Step 3 补精读 + 新 M-C-A 构建（对话 6）——Vieira 2023 全文精读 + Diniz 2011 abstract 级（paywall 锁，穷尽 6 源失败）。精读推翻 H006 多项初稿：① Vieira 公式 α·ln 是推断非 verbatim（L345 图片 PDF→md 丢失）② α=17GHz 原文值非 sandbox 自标定 6.12e8 ③ ±13GHz 是两阶段联合范围非粗估 ④ Vieira 无多块均值（单窗 1024 样本），B5 1024×16 是结构性增量非算子增量 ⑤ Vieira 报 BER penalty 非 σ。路 2 新 M-C-A 构建（M=Vieira 对数比/C=LEO 残频精度/A=对数比小残频数值噪声假设，过四判据）。增量归因 2×2 消融设计（算子线性/对数 × 块结构单窗/16均值，判定算子贡献>30% Go/<10% Kill）。精读笔记落盘 papers/_read_notes/_vieira2023-diniz2011-psi-same-family.md。H007 交下一对话执行 Step 4a sandbox（守单对话 3 步上限）（2026-07-08，对话 6）
- **S007** 路 2 Step 4a sandbox 执行 → Kill（对话 7）——2×2 算子×FFT 分辨率消融（修正 H007/S006 的"块结构"误解：sandbox Vieira 已 16 块均值，真实公平轴是算子×n_fft）。实测四格 σ：A 线性 n16=11.4 / B 对数 n16=11.4 / C 线性 n1024=29.0 / D 对数 n1024=28.7 MHz。主线 V5 独立重算：算子贡献 −0.7%（<10% Kill），FFT 分辨率贡献 101%。A0 假设证伪（B/A=1.00，linear-log 相关 0.994）。新发现 experiment_C α 标定 bug（grid C 未为 n_fft=1024 重标 α）。维度 A0+C 双 FAIL，无 salvage → Kill B5-Q1（D004/V001）。66% σ 差全部来自 n_fft=16（B5 锚公开工程参数，非独占）。H008 交用户决定候选池下一步（2026-07-08，对话 7）
