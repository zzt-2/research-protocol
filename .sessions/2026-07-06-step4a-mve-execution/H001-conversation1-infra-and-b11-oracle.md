# Handoff: 对话 1 — 仿真基建增量扩充 + B11 oracle 上界前置门控

> 来源: S001（专题开题 + 基建盘点 + 组织方案）| 交接目标: 新对话执行基建扩充 + B11 CRB 推导
> 文件名: H001-conversation1-infra-and-b11-oracle.md
> 日期: 2026-07-06

## 到哪了（状态）

专题 `.sessions/2026-07-06-step4a-mve-execution/` 刚开。上游 2026-06-20-problem-driven-redirection S031 已对 35 Q# 排优先级 + 对前 5 名判 Go/Kill：

- **B11-Q1 NDA-ML STO+CPE**：Conditional Go（最干净，前馈闭式 ML 无环路 TF 不撞 D006 + (8,8)-16APSK 跟 DVB-S2 同源 + PTL 2025 已发会议样本）。**关键条件 = FSO 湍流迁移 MVE 验证（B11 仿真未建模 FSO 行 33 假设湍流/Doppler 已补偿，星地湍流下是否仍 +2dB 需 MVE）+ 格式绑定 (8,8)-16APSK**
- B3-Q2 Conditional Go（dB 最高 +2~3dB，但 4 支路→星地单链路迁移风险 + A1 归属 jphot+oe 已做联合）
- B7-Q1 Conditional Go 会议最稳（OFC 2026 已发 + baseline PSA FOE 传统 + 范围 in 星地 COSC，但 dB 偏低 0.6dB）

切法地图专题 `2026-07-05-carrier-sync-v2-cut-pattern/` 已转 closed（参照系校准使命达成）。完整切法地图 `_cut-map-final-b1-b12.md` 是 MVE 执行的参照系（不是答案）。

仿真基建已盘点（projects/simulation/，成熟）：common/ 7 模块 + params.py（TL-26 制度化）+ explore/ 模式（n1/mcs 先例）。**缺口**：M-APSK 调制 + DA ML/NDA-ML/Gardner TED/FOE 估计器 + B11/B7 参数族。

## 下一步干什么（对话 1 三步，守 3 步上限）

### 步骤 1：报到 + 框架文件重读

报到（session-governance Trigger 1）+ 读：
- `.sessions/2026-07-06-step4a-mve-execution/topic-index.md`（不变量 10 条 + 范围边界 + 组织方案）
- `stages/gw-feasibility.md` §D 维度 D MVE 8 步（含 FR-20 参数溯源 / FR-21 oracle 上界前置 / FR-11 架构摘要 / FR-14/15 baseline 对照）
- `thesis-lessons.md` TL-20（先建理论预期）/ TL-25（起飞检查单 6 条）/ TL-26（参数溯源）/ TL-27（oracle 上界前置）/ TL-13（共用信道实现）/ TL-24（不引用旧代码）
- `projects/simulation/explore/n1-pcs-gain/N1-MVE-SPEC.md`（MVE-SPEC 模板参照，9 节结构）
- `projects/simulation/common/__init__.py` + `params.py` 头部（基建现状）

### 步骤 2：基建增量扩充（派子 agent 并行 + 主线整合）

> 守 TL-13：扩 `_channel/_modulation/_recovery` 都基于现有 common，不自建。

**子 agent A（≤15 分钟）：扩 `_modulation.py` + `_recovery.py`**
- `_modulation.py` 加 M-APSK：
  - 8PSK + Gray 映射 + `resolve_8psk`
  - (8,8)-16APSK（B11 锚调制，两个环 8+8 点）+ Gray 映射 + `resolve_m16apsk`
  - 可选：32APSK / 64APSK（B3 联合估计扩展备用）
  - 每个调制加 `*_mod` / `*_demod` / `ber_count_*` / `resolve_*`，对齐 QPSK/16-QAM 接口
- `_recovery.py` 加估计器：
  - **DA ML**（B11 baseline，单 pilot 符号 decision-aided，从 B11 论文行 181 推导）
  - **NDA-ML**（B11 锚方法，升 M₀ 次幂盲去调制 + 单正弦 freq+phase ML 闭式，从 B11 论文 Wang[13] 框架推导）
  - **Gardner TED**（B7 锚方法，1986 经典 + 双候选+TED2 判决，从 B7 OFC 2026 论文推导）
  - **FOE**（B7 baseline PSA FOE 的复用接口，如 `_recovery.fft_foe` 已有则只补 PSA 版本）

**子 agent B（≤15 分钟）：扩 `params.py`**
- 加 B11 参数族：CLW 500kHz（B11 锚行 143）/ 7% HD-FEC 阈值 / 25 GBaud（B11 行 143）/ M₀ 次幂参数
- 加 B7 参数族：Doppler range 0-23GHz（B7 OFC）/ LEO Doppler rate（参考 Paillier / sat.1553）/ OSNR 10dB 工作点
- 加 B3 参数族：4 支路分集配置（jphot+oe）/ 多孔径阵列配置（待 B3 架构决策）
- 每个参数全标 source_type + source + audit_flag（TL-26，参考现有 params.py 风格）

**主线**：扩 `_channel.py` 加 `generate_shared_realization_apsk`（含 CLW 扩展 + FEC 阈值标记），不重写 `generate_shared_realization`（保留兼容）

### 步骤 3：B11 oracle CRB 推导 + 数值验证（派子 agent，≤15 分钟）

> 守 TL-27 / FR-21：<0.5dB 直接 Kill B11 不跑 MVE（省时间），≥0.5dB 才写 B11-MVE-SPEC.md。

**派子 agent**：
- 推导星地湍流信道（Gamma-Gamma 强湍 + Wiener phase noise + LEO Doppler）下，NDA-ML vs DA ML 的 CRB 下界
- 参考 B11 论文 Wang[13] ML 框架 + Gardner TED CRB 经典推导
- 若解析不可推 → 降级数值上界（蒙特卡洛 N≥100000，避免 S014 N=20000 虚高教训）
- 输出 `explore/b11-nda-ml-sto-cpe/_crb_lower_bound.py` + `_crb_results.json`
- 子 agent 返回 ≤500 词摘要：①CRB 公式或数值方法 ②关键 (turb, SNR) 点的 CRB 差 dB ③判定建议（<0.5dB Kill / ≥0.5dB 进 MVE）④偏离 TL-20 预期的点（如有）

**主线整合**：
- CRB <0.5dB → Kill B11，主线建议转 B7（写 H002 交接）
- CRB ≥0.5dB → 写 `explore/b11-nda-ml-sto-cpe/B11-MVE-SPEC.md`（仿 N1-MVE-SPEC.md 9 节模板，含理论预期表 TL-20 + baseline 设计 FR-14/15 + pass/fail 标准 + 扫描设计 + AIR/BER 计算 + 执行约束）+ 写 H002 交接对话 2 跑 B11 MVE

## 纪律（和下一步直接相关的约束）

1. **profile 第 8 次"急于推进"防线**：每候选必须先算 CRB 下界，<0.5dB 砍不跑 MVE。**禁"先跑起来再说"跳过 oracle 上界前置**
2. **TL-26 参数溯源强制**：params.py 每个新参数全标 source（B11/B7 锚论文 / Paillier / sat.1553 / Fernandes），禁"为了让方法有用"拍参数
3. **TL-13 共用同一信道**：B11/B7/B3 从 `common/_channel.py` 导入，禁自建
4. **TL-20 先建理论预期**：B11-MVE-SPEC.md §2 必填理论预期表（每湍流等级预期 dB + 量化锚点 + 偏离即停查代码）
5. **TL-23 验证完再写文档**：CRB 出 +2dB 先别写进论文，先核查物理前提
6. **5 个口径警示**（切法地图 §3.3 继承）：dB 引用全带条件——B11 +2dB 仅 (8,8)-16APSK + 仿真未建模 FSO / B7 0.6dB @ BER 2e-2 + 1.9×范围 / B3 +2~3dB 强湍 4 支路
7. **D005 务实路线 + 会议门槛放宽**：Go 判据=赢传统 baseline；纯仿真+鲁棒性 dB/范围/绝对指标/同族 dB 都算够格；FR-21 降为参考不卡死（但连传统 baseline 都赢不了仍不行）
8. **切法地图是参照系不是答案**：B11 是稀池 1 细分独占赛道（独占+cited-by 1+75%"既有方法失效"叙事），引用模式不搬"切法地图说这个好"

## 接口变更（如有代码改动）

```yaml
# common/_modulation.py 新增（接口对齐 QPSK/16-QAM）
- m_apsk_mod(bits, format='8psk'|'(8,8)-16apsk'|'32apsk')
- m_apsk_demod(s, format)
- ber_count_m_apsk(tx_bits, rx, format)
- resolve_m_apsk(rx, tx_bits, format)

# common/_recovery.py 新增
- da_ml_recovery(rx, pilot_sym, mod)              # B11 baseline
- nda_ml_recovery(rx, M0, mod)                    # B11 锚方法
- gardner_ted_recovery(rx, doppler_range, mod)    # B7 锚方法
- psa_foe_recovery(rx, ...):                      # B7 baseline（如 fft_foe 不够）

# common/_channel.py 新增
- generate_shared_realization_apsk(Ns, gamma_bar, turb_name, f_dot, clw, fec_threshold, seed)

# params.py 新增（B11/B7/B3 参数族，全标 source）
- B11Params (CLW, HD_FEC_THRESHOLD, BAUD_RATE, M0_POWER)
- B7Params (DOPPLER_RANGE, LEO_DOPPLER_RATE, OSNR_WORKING_POINT)
- B3Params (NUM_BRANCHES_DIVERSITY, ARRAY_CONFIG)  # 待 B3 架构决策
```

## 失败数据附录（如涉及路线失败）

无（首对话，未跑 MVE）

## 已知债务（如原则与现实有差距）

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| ao.581648（B10-Q3 全文）缺 | FR-26 证据链 | 待下载 | B10 进 MVE 才触发（本轮不补）|
| B11 仿真未建模 FSO（行 33 假设已补偿）| FR-18 竞争格局 | 本轮 MVE 核心验证项 | 对话 2 跑 B11 MVE 时闭合 |
| B3 多孔径阵列 vs 单链路架构 | A1 归属 + FR-04 保真度 | 待 B3 架构决策 | 对话 3 触发 |

## 验证阈值（如涉及验证体系）

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|--------|----------|---------|-----------|
| B11 CRB 下界 | NDA-ML vs DA ML ≥ 0.5 dB @ 强湍 | FR-21 + TL-27 | 未跑 |
| B11 MVE | NDA-ML > DA ML + 信号方向一致 + 达同门 2-4dB 区间下沿 | D005 + FR-14/15 | 未跑 |
| B11 物理前提 | 升 M₀ 次幂去调制不依赖判决 → 高星座密度不错误传播 | TL-22 先查物理前提 | 未跑 |

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落（10 条）
- [ ] 已验证本文件中的至少 3 条关键事实声称：
  - [ ] B11 锚论文行 33 假设湍流/Doppler 已补偿（核查 `papers/_read_notes/_B11-nda-ml-sto-cpe-increment.md` 或 content.md）
  - [ ] common/ 7 模块清单（核查 `projects/simulation/common/__init__.py`）
  - [ ] explore/n1-pcs-gain/N1-MVE-SPEC.md 9 节结构（核查模板）
- [ ] 已检查 _registry.yaml 中本专题的 depends_on（2026-06-20-problem-driven-redirection + 切法地图 + 精读沉淀 3 个依赖）
- [ ] 已确认当前范围未违反"明确不含"（不回头救 6 次 Kill / 不改框架 / 不跳框架 / 不污染 common）

## 下一轮

**对话 2**（视对话 1 结果）：
- 若 B11 CRB ≥0.5dB → 跑 B11 星地湍流迁移 MVE（守 TL-20 先建理论预期 + TL-26 参数溯源 + FR-18 竞争格局 + FR-12 MVE→Formal 架构差异）
- 若 B11 CRB <0.5dB → Kill B11，转 B7 全流程（CRB + MVE，机制正交，OFC 2026 已发 baseline PSA FOE 搬星地湍流 + LEO Doppler rate）

**对话 3**（最后）：B3 架构决策（多孔径阵列 vs 单链路工程可行性查证）+ 视情况跑 B3 MVE
