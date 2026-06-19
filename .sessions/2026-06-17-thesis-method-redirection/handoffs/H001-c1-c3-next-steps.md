# Handoff: C3/C1 双候选推进 — C1 补 FR-21 + C3 定方法形态 + 评估合并

> 来源: S001 + 候选门控轮（2026-06-17）| 交接目标: 下一个对话推进 C1/C3 双候选
> 日期: 2026-06-17
> 文件名: H001-c1-c3-next-steps.md

## 到哪了（状态）

前序专题（2026-06-10-research-direction-exploration，已 dormant）三条方法腿全断。本专题复盘后列了 5 个候选面（C1-C5）做便宜门控，**5 个筛剩 2 个**：

- **C3（换损伤对象 beam wander/角抖动）= Kill 点 + FR-21 均 PASS**，可进 Groundwork。新损伤维度（Paillier plane-wave 没建模，grep beam wander=0 命中）。物理量级核算：0.57dB@0.47µrad（Micius 实测残余）/ 2.56dB@1µrad。**窗口窄但现实工况成立**。
- **C1（A3 换设定去 AO 复活）= Kill 点 PASS（有保留）**，**待 FR-21**。无 AO 主导损伤含 piston 相位（A3 pilot CPE 可攻）。保留：piston 必须进 DSP（SMF 单耦会 -23dB 砸信号，须多模/阵列接收）。
- ~~C2~~（换问题层）/~~C4~~（换上行链路）/~~C5~~（FPGA 当方法章）= **Killed**。

**C1 与 C3 攻正交 Zernike 模态**（C1=piston 相位，C3=tilt/指向）——理论上可能合并成一个更完整的方法，但方法形态都未定。

## 下一步干什么（按优先级）

### 1. C1 做 FR-21 上界门控（对齐 C3，必须做）
和 C3 一样的物理量级核算：无 AO 下 piston 相位残余（Belmonte 2009 给 σ²_φ）→ 接收耦合损失/相位方差 → dB 上界。<0.5dB Kill，>0.5dB 与 C3 平级。

### 2. C3 方法形态探索（C3 的真未知数）
C3 只确认"有缝"（beam wander 残余非 negligible），还没确认"怎么补"。可能方向：指向跟踪（feedback，**注意 TL-03 跨 RTT 红线**）/ 空间分集 / 编码 / 检测加权。**这是用户"不熟+新方向"的风险点**——先查 baseline（Yang 2024 / JASS tip-tilt）看主流怎么做，别凭空设计。

### 3. 评估 C1/C3 能否合并
若 C3 方法形态恰好也能处理 C1 的 piston 相位，合并比分开做强。但别过早假设——先看两者方法形态是否兼容。

## 纪律（防坑，和下一步直接相关）

1. **[FR-20] C1 的 FR-21 核算，参数必须标文献来源**。前序 A3 死在"AO 残余参数偏大 1885× 拍出来的"（TL-26/D010）。C1 用 Belmonte 2009 的 σ²_φ，查不到标"未验证 范围 X-Y"，**禁止取让方法好用的一端**。
2. **[TL-28] 门控过 ≠ 能做**。C3 过了 Kill 点 + FR-21，不代表最后 MVE 能成（前序 N1/③ 过了好几层门控最后死在 MVE）。**别 all-in C3，C1 做完 FR-21 再看**。
3. **[TL-03] C3 方法形态若涉及"指向跟踪反馈"，必查跨 RTT 红线**。beam wander 是低频（<30Hz），理论上可在 RTT 内反馈，但要显式验证，不能假设。
4. **编号约定**：本专题用按候选聚合结构（`candidates/{slug}/notes.md`），不是 S### 平铺。新记录加到对应候选的 notes.md，专题级记录才用 S###。**避免前序 4 次编号冲突**。
5. **baseline 路径已写死**（见下"关键文件"），用户 FPGA 背景/仿真不熟，别从零找参数，直接用已溯源的源。

## 关键文件（baseline + 参数源，写死避免从零找）

- **C3 同构 baseline**：`papers/doi/10.1088_1742-6596_2906_1_012002/`（Yang 2024，星地 16QAM 相干+AO+残余瞄准 BER，**仅摘要**，正文 IOPscience 被 Radware 反爬）
- **C3 残余参数源**：Wang 2021 Micius（DOI 10.1364/AO.416811，角微振动 9.3→0.47µrad 实测）+ `papers/_read_notes/10.3390_aerospace12100869.md`（1 arcsec 抖动）
- **C1 baseline**：Belmonte & Kahn 2009（DOI 10.1364/oe.17.002763，无 AO 相干 FSO 容量，log-normal+Gaussian phase）+ Paillier 2020（`papers/arxiv/1911.11851/content.md` L145 无AO flux penalty -23dB / L167 piston not corrected by AO）
- **物理判据基础**：`papers/arxiv/1911.11851/content.md`（Paillier，AO mode 91/5kHz/plane-wave L57）
- **C3 完整门控记录**：`candidates/c3-beam-wander/notes.md`（Kill 点 + FR-21 + 物理量级核算表）
- **候选总览**：`candidates/_index.md`（5 候选门控结果 + 排除约束）

## 失败数据附录（前序三条腿，避免重蹈）

### N1（静态 PCS）— 前序 D007
- 核心失败机制：MB on 16-QAM 全 18 组 gain≈0，优化器自选均匀
- 已排除：MB 分布的 PCS（16-QAM 阶数整形空间不足 + MB 破坏 Gray）
- 可复用：估计器三法交叉验证（TL-29）、oracle 上界门控方法

### ③（过境 MCS 排程）— 前序 D009
- 核心失败机制：oracle 上界 12 组最大 0.09dB，与 N1 同根（参数空间窄）
- 已排除：MCS/编码率/调制阶数排程

### A3（导频前馈 CPE）— 前序 D010（推翻 D008）
- 核心失败机制：S013 Go 基于偏大 1885× 的 AO 残余参数（strong=300kHz vs Paillier 159Hz），改回后 gap 缩 136×、pilot 反而加噪声
- 已排除：pilot CPE 补 AO 校正后的残余相位（在当前设定 AO 把残余抹平到 negligible）
- 可复用：A3 MVE 工程代码（`explore/a3-pilot-cpe-mve/`，pilot 注入调试 + Cheng 2013 Eq.5 迁移）、TL-26/27
- **C1 复活 A3 的前提**：去掉 AO 让残余相位回来（piston 在无 AO 时不被校正，Paillier L167）

## 验证阈值（本专题候选门控标准）

| 验证项 | PASS 标准 | 阈值来源 | 历史通过 |
|--------|----------|---------|-----------|
| Kill 点（有无物理缝） | 损伤在目标设定下非 negligible，且有 baseline | 前序 D003 方法 | C1/C3 PASS |
| FR-21 上界门控 | oracle/物理量级上界 ≥0.5dB | gw-feasibility §D step 5（刚缝） | C3 PASS（0.57dB@0.47µrad，边界性）/ C1 待做 |
| FR-20 参数溯源 | 每个物理参数标文献来源 | gw-feasibility §D step 4（刚缝） | C3 全闭合（Micius实测+Paillier+经典公式）/ C1 待闭合 |
| TL-03 边界 | 方法不跨 RTT（离线静态/前馈） | TL-03/04 | C3 方法形态未定，待验 |

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落（开题标题未锁 AO/相干/16-QAM；老师要 xx 方法+指标提升；路由红线；TL-03/04）
- [ ] 已验证本文件中的至少 3 条关键事实声称：
  - 声称1：Paillier plane-wave 假设 + grep beam wander=0 → 验证：读 `papers/arxiv/1911.11851/content.md` L57 + grep
  - 声称2：C3 FR-21 上界 0.57dB@0.47µrad → 验证：读 `candidates/c3-beam-wander/notes.md` 核算表
  - 声称3：前序 A3 Go 被推翻因参数偏大 1885× → 验证：读前序 `S015-a3-mve-section-D-kill.md`
- [ ] 已检查 _registry.yaml：本专题 active + depends_on 前序专题（dormant）
- [ ] 已确认当前范围未违反"明确不含"（不做 MVE/不改代码/不重复前序已验方向除非换设定）

## 下一轮

1. C1 做 FR-21 物理量级核算（Belmonte 2009 σ²_φ → dB，FR-20 参数溯源）
2. C3 方法形态探索（查 Yang 2024/JASS tip-tilt 主流怎么做指向残余补偿，TL-03 验证）
3. C1/C3 合并可行性评估
4. 定方向后 → 开执行专题（本专题只管定方向）
