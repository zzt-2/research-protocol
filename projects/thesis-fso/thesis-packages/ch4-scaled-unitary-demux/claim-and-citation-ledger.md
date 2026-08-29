# Claim and citation ledger

## 1. 允许主张

| Claim ID | 允许表述 | 承重证据 | 披露条件 |
|---|---|---|---|
| C01 | 将经典 scaled-unitary/Procrustes 结构估计迁移到短 balanced-pilot DP-(8,8)-16APSK 星地相干偏振解复用 | D052；Step4a paper feasibility | 明示是 classical migration，不称新原子 |
| C02 | 在冻结 strict scaled-unitary 目标场景与同 pilot 开销下，C4 相对 B2 取得四格 `7.37%/2.62%/8.38%/5.06%` 的 BER 相对降幅 | raw-only CSV；V027 | 四格全部展示；metric 定义一致 |
| C03 | 两个 Np=2 cell 合并后，B2/C4 BER=`0.06076145/0.05608821`，paired CI=`[-0.00686385,-0.00282661]` | raw-only pooled row；D052/V027 | 说明 128 paired windows 与 pooled 定义 |
| C04 | C4 与冻结 B2 使用相同 `UV^H`，性能差异只支持公共尺度估计的有限作用 | `development.py:154-169` | B2 `tau=1` 必须同步披露 |
| C05 | deployable C4 只使用接收机可见的 pilots/payload observations | `development.py:125-182`；V027 truth firewall | O1 明确标 oracle，truth 仅用于评分 |

## 2. 必须披露

- B2 是 primary 且最强廉价对手，`tau=1`；不能只用 B0 突出 C4。
- B2 与 C4 共用 `UV^H`；C4 不产生“更好的偏振旋转”证据。
- 场景为 static memoryless `H=gQ`、common scalar Gamma–Gamma、equal circular AWGN；无 PDL/PMD/FIR/时变 SOP/CFO/CPR/LDPC。
- `rho=s1/s2` 只作 receiver-visible diagnostic；没有运行时阈值或 guard。
- O1 读取 true channel，只是离线 oracle。
- 四格均展示；结果图纵轴从 0 起，不通过裁轴放大差异。

## 3. 可省略的内部历史

以下内容不影响公平性、方法身份、metric 或当前有限 claim，可从正式主叙事省略：已停的 C4-2、无关候选失败、development 试探细节、全仓范围外 collection errors。provenance 附录可保留 development→confirmation 的冻结关系，但不把失败史写入方法动机。

## 4. 禁止主张

- “提出了新的偏振旋转/新的 Procrustes 或 polar estimator”。
- “首次”“SOTA”“全面优于近期强方法”或“适用于任意偏振信道”。
- PDL、PMD、FIR、时变 SOP、CFO、CPR、LDPC 已由本 confirmation 验证。
- `rho` 已构成可靠在线 gate 或 near-unitary 自适应方法。
- O1 是可部署 baseline，或 pooled Np=2 是独立第五格。
- 完整论文正文、完整论文实验或全编码链已经完成。

## 5. 引用候选与精确指针

| 用途 | 候选来源 | 当前证据层级 | 使用方式/限制 |
|---|---|---|---|
| 短训练、2×2 unitary/SU(2) demux 通信邻居 | Roudas et al., JLT 2010, DOI `10.1109/JLT.2009.2035526`；`papers/doi/10.1109_jlt.2009.2035526/content.md:1289-1299,601,877-879,3263-3265` | 全文精读 | 支撑邻域与边界；不声称其已给出本完整 recipe |
| Jones/unitary、PDL/PMD 与 2×2 DSP 背景 | Kikuchi, ELEX 2011, DOI `10.1587/ELEX.8.1642`；`papers/doi/10.1587_elex.8.1642/content.md:273-331` | 全文精读 | 支撑系统背景与失配边界 |
| data-aided Kabsch/unitary estimator 强邻居 | *Capacity Bounds Under Imperfect Polarization Tracking*, TCOM 2022, DOI `10.1109/TCOMM.2022.3206803` | title+abstract，全文未读 | 正式引用前需核对全文对应公式；当前只作候选，不承重 exact recipe |
| Procrustes/polar/scaled matrix-nearness 经典原子 | Schönemann 1966；Higham 1986；Eldar–Forney 2002 | 前两者经典 authority；后者摘要级 | 支撑“原子是经典的”；正式 bib 与 exact claim 仍需写作时核对 |

完整引用身份审计与 collision ledger：`projects/thesis-fso/polarization-demux-groundwork/step3-5-c4-1-exact-recipe-closure.md:96-132`。
