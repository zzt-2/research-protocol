# [S080] Pilot-Jones complex-Jones/PMD/PDL 模型充分性救活大包（T003）

> 2026-07-23 | GW Step 4a (model-sufficiency salvage) | 状态: 完成
> 来源: T003 / formal D063 / S079 续接

## 目标

回答 D063 授权的 bounded 问题：物理上更充分的 complex Jones / PMD / PDL 信道，
是否重新产生一个最强任务适配传统 baseline（B3）无法关闭、且可形成方法的
Pilot-Jones 问题？前置门通过时同包完成有界 MVE；不进 Step 5/Contract/Execute。

## 记录

**Phase 0 基线与 T002 amendment**：HEAD `68c1fd8`，T002 commit `0b642e9`。独立
raw 重算确认 P/B1 win-tie-loss = **0/6/4**（contract 残留 `0/7/3` 是 stale-count
文档缺陷，记录不回写）；`B1/O=1.19` 是 BER ratio 非 0.5dB，第二条 FR-21 门降为
diagnostic。V037 对 V036 的 claim-scope 修正接收（numeric/code integrity PASS，
全量 integrity PARTIAL）。protected paths 4 个 + T002 contract/result 全 byte-
unchanged。

**Phase 1 物理证据**（`model-evidence.yaml`）：DGD ≤6ps = 1.5% T_S（Valjus 2025
sat.1553 ref[76]）→ 2.5GBaud 下 memoryless；component PDL <1dB → cond<1.12；
RSOP ≤600krad/s → 块内 Jones 恒定。PMD/PDL 是 component/fiber 损伤非大气。
物理门：verified range 低于 memory/conditioning 阈值，但 task-matched baseline
fully-covered 条件不成立（4 篇 BLOCKED）→ 建模型梯让经验 headroom 裁决。

**Phase 2 模型梯**（`complex_jones_channel.py`）：M0/M1/M2/M3/M4 在 canonical
generator 之上叠加块常数损伤，保留 shared-noise 契约。`run_salvage.py --mode
theory` → **8/8 limiting-case tests PASS**（M0 byte-兼容；M1 cond=1 酉；M2 cond
精确匹配 PDL-dB 3.5/6/9.5dB；M3 dgd=0 memoryless / dgd=80ps 有 memory；M2 无噪
声可恢复）。

**Phase 3 指标/阈值纠偏**：主指标 `fixed_label_ber`（nocma 变体隔离 Jones 估计
质量与 CMA 主动分量；CMA 变体并报）；BER→Q² 冻结公式 `Q=sqrt(2)·erfcinv(2·BER)`、
`Q²_dB=20·log10(Q)`，BER=0→0.5/N_eval 上界，BER≥0.5→None，BER ratio≠dB（修复 T002
缺陷）。Go 对手 = task-matched B3（M2 用 whitening，M3 用 tapped）。

**Phase 3 headroom 门（决定性结构发现）**：在 α=2.0/β=1.0/17dB 最 P-favorable
条件下，B3-vs-oracle headroom **不随损伤强度增长**——PDL 0→9.5dB（cond 1→3.6）
headroom 与 M0 deep-fade-only control 完全相同（delta=0.0）；PMD 40→160ps 不单调
增长。残余 headroom 来自深衰落+噪声，非 PDL/PMD 结构。verified range（PDL 1dB/
DGD 6ps）信道近酉/memoryless，B3≈oracle≈M0。

**Phase 4 方法候选**：P1 energy-weighted LS（机制独立于固定 EMA 与事后正则）。
P1 vs task-matched B3 全 cell 不胜（M2 6dB 0/2/3；M3 160ps 0/0/5）。

**Phase 5 双审查**：Integrity 独立重算 PASS（SHA 链全 MATCH、raw→aggregate bit-
exact、seeds disjoint、protected unchanged、13/13 tests PASS）。Science critic 8
项攻击（光纤换皮/稻草人/B3 调参/P1 别名/oracle 偷做/stress-only/4 篇债）均
survive。verdict 稳健。

**anomaly（TL-22 触发并修复）**：执行中发现 memoryless oracle 反常地比 B3 差——
根因是 oracle 只逆 J_b 不逆 SOP 旋转 R(theta)，而可部署 LS 联合估计 J_b@R(theta)。
component-level trace 定位、修复（derotate_oracle 现同时逆 J_b 和 R(-theta)）、
回归测试守护。M4（PDL+PMD 联合）因 FDE oracle 需联合信道求解器而排除出 headroom
表（scope 限制非 confound；M2/M3 已覆盖决定轴）。

## 决策引用

- D063：接收 T002 局部 Kill + 授权 complex-model salvage（**继承，未新建**）
- 无新建 D###（provisional verdict 待主控验收；不新建 D064，不进 Step 5）

## 范围确认

- 本轮是否在 scope boundary 内：**是**（D063 授权的 model-sufficiency salvage，
  止于 provisional verdict；未进 Step 5/Contract/Execute，未改 protected/Skill/
  controller，未 push）

## 后续

- **Provisional verdict = `PIVOT_MODEL_NOT_JUSTIFIED`**（允许枚举）：complex Jones/
  PMD/PDL 模型升级不在 2.5GBaud / 64–100 sym block 下重新产生方法级 Pilot-Jones
  gap；B3 关闭 headroom，残余是深衰落+噪声 floor。
- Pilot-Jones family **不在本轴关闭**，仍 `PILOT_JONES_FAMILY_UNRESOLVED`，等待
  真正新轴（如 verified DGD≫T_S 频选信道，或 sub-symbol 块变 Jones）。
- T002 的 `UNITARY_REAL_ROTATION_MCA_KILLED` 扩展为：即便 richer（非酉/memory）
  Jones，B3 仍关闭 headroom。
- 待主控验收 provisional verdict；4 篇 D056 全文继续 BLOCKED；OE2021 一阶 PMD
  provenance 标 unverified 债务。
- 不复活 Scout/P03，不改 protected history。
