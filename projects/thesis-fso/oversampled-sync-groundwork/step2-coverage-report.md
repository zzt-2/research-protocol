# GW Step 2：全文获取与覆盖面报告

> 日期：2026-08-06
> 边界：通过项目 `tools/download` 做有界获取，并复用两份证据根中的已有合法全文；不进入 Step 3。

## 1. CORE 获取清单

| CORE | 身份与角色 | 本地来源 / provenance | content SHA256 | 行数 | 非拦截页 |
|---|---|---|---|---:|---|
| Tang et al., 2022, *Symmetric Training Sequence-Based Carrier Frequency Offset Estimation Scheme for Coherent Free-Space Optical Communication*, DOI `10.1109/JPHOT.2022.3161795` | CFSO frame positioning + CFO acquisition；Q1 直接基线 | 证据 worktree `papers/doi/10.1109_jphot.2022.3161795/`；题名/DOI由 `content.md` 核对。`metadata.json` 虽为 `all_failed`，但目录已有 PDF 与 278 行正文，故保留 provenance 不一致警告 | `db526ba5e1787efbd05034bd7759e5ccc4ddca34311c979a35464176db40fb69` | 278 | PASS |
| Paillier et al., 2020, *Space-Ground Coherent Optical Links: Ground Receiver Performance With Adaptive Optics and Digital Phase-Locked Loop*, DOI `10.1109/JLT.2020.3003561`, arXiv `1911.11851` | turbulence + AGC/DPLL carrier maintenance；Q2 基线/物理源 | 证据 worktree `papers/doi/10.1109_jlt.2020.3003561/`；`metadata.json`: `success`, `arxiv_latex` | `52c1845701fb0fb388b9a359492c6ec77ce4fda34f8e8f405858449541a21e5f` | 244 | PASS |
| Wang et al., 2023, *Carrier FOE Scheme Based on FSTS in Spatial Diversity PM Coherent FSO Communication*, DOI `10.1109/JPHOT.2023.3265847` | integrated FS+FOE；Q1 强近邻 | 主根复用 `D:/code/study/research-protocol/papers/doi/10.1109_jphot.2023.3265847/`；`metadata.json`: `success`, `firecrawl_scrape` | `e30a66fe650ff065c65746943b52cc48afc0476900f90421febd1f9b5d351a9f` | 455 | PASS |
| Wang et al., 2024, *Enhanced frame synchronization and carrier recovery in coherent FSO communication: a pseudo-random and cyclic QPSK approach*, DOI `10.1364/OE.520452` | FS + two-stage FOE/carrier recovery；Q1 最强同场景近邻 | 主根复用 `D:/code/study/research-protocol/papers/doi/10.1364_oe.520452/`；`metadata.json`: `success`, `firecrawl_scrape` | `49a7fd02db0a2758e3998c678f56190fbaa9d029d4cba346320a8e94f8193edd` | 891 | PASS（首部有登录提示，但正文、摘要、方法与参考文献均存在） |
| Valjus et al., 2025, *Review and Analysis of Digital Signal Processing Algorithms for Coherent Optical Satellite Links*, DOI `10.1002/sat.1553` | satellite DSP 综述；timing/carrier/equalization 物理与 baseline 入口 | 主根复用 `D:/code/study/research-protocol/papers/doi/10.1002_sat.1553/`；`metadata.json`: `success`, `firecrawl_scrape` | `b40962d6e9f8c35e5f38dc2ce77aeefd93c4b4fba850d52c7dead95a463a7d0a` | 1582 | PASS |
| Le Bidan et al., 2023, *Frame format and DSP receiver design for a 56-GBaud GEO DP-QPSK coherent optical feeder link*, DOI `10.1109/ICSOS59710.2023.10490279` | 2-sps GEO receiver、coarse CFO、block timing recovery；Q1/Q2 系统参数与顺序链基线 | 主根复用 `D:/code/study/research-protocol/papers/doi/10.1109_icsos59710.2023.10490279/`；`metadata.json`: `success`, `firecrawl_scrape` | `70b0277f55c2207ff74085e4cd6ab2e571a823841ece1091dcd9002163d5927b` | 873 | PASS |
| Sun et al., 2025, *Preamble Design for Joint Frame Synchronization, Frequency Offset Estimation, and Channel Estimation in Upstream Burst-Mode Detection of Coherent PON*, DOI `10.1109/JLT.2025.3533197`, arXiv `2409.14400` | 最接近的 clock/frame/FOE 直接竞品；Step 2 角色 5 | 证据 worktree `papers/arxiv/2409.14400/`；Crossref DOI 与官方 arXiv 题名/作者核对，`metadata.json`: `success`, `arxiv_pdf` | `73b2623b7d39199e31c801694dc78bfbc36fe5726ed5f5e28aa172bb525ccc81` | 466 | PASS |

七篇均超过 50 行并含可辨识正文。可用源文件 SHA256：Tang PDF `e7d281a30fc15ebfc4ad20ac80985fd627c7b3fcc70e40e7bafb41231ddad1ce`；Paillier tar.gz `439f80ace73dc7dfa3ae7628f7dd054b485c1ff2df02107d535aa254e7c0fa6b`；GEO PDF `0a2bd126de429c06845df40979678790ea66c7572d49b1072e03250f5643f67e`；JLT 2025 arXiv PDF `601cbe1cbedffbe904551e64f19b5bf0259266c4d10d5b896bc8b846b4ecc443`。其余三篇本地记录只有 `content.md` 与 metadata，因此不虚构原始源文件哈希。

## 2. 获取动作、止损与覆盖判断

首轮对 7 个 DOI 运行项目 `tools/download` 的单条自动获取管线：Paillier 2020 通过
`arxiv_latex` 成功；Gu 2019、Wang 2023、OE 2024、卫星综述、OE 2022 与 JLT 2025 返回
`all_failed`。失败项没有开启第二、第三条手工路径，因此均未超过“三路径止损”上限。随后只对本地共享
论文库做复用核验：Wang 2023、OE 2024 与卫星综述已有合法全文；GEO 2023 作为系统参数与顺序链
补充 CORE。独立 verifier 指出角色 5 仍缺失后，对两个最近竞品执行定向三轮止损：JLT 2025 在第二轮
找到并核验官方 arXiv `2409.14400`，因此停止；JOCN 2026 的 DOI 自动管线、官方 arXiv 精确题名检索、
Optica 官方获取页三轮均失败，保留高风险覆盖缺口，不以摘要顶替全文。完整路径见
`direct-competitor-acquisition-receipt.json`。

- Gu 2019 timing baseline，DOI `10.1109/JPHOT.2019.2956086`：证据 worktree 仅有 `metadata.json`，状态 `failed/all_failed`，无全文。
- Optics Express 2022 timing-phase detector，DOI `10.1364/OE.447448`：仅有 `failed/all_failed` metadata，无全文。
- JOCN 2026 single-preamble direct competitor，DOI `10.1364/JOCN.587273`：三轮止损后仍无合法全文；
  官方摘要所示 clock/frame/FOE 动作形成 `UNRESOLVED_HIGH_RISK`，不得据摘要作 exact collision 或新颖性裁决。
- Gu 2019 与 OE 2022 两条未获取记录只保留自动管线终态 `all_failed`；每篇仅执行 1 条项目工具路径，未追加手工绕过，
  因而在三路径上限内止损。工具内部通道不是三次独立人工获取承诺，receipt 不虚构逐通道成功/失败明细。

覆盖面已达到用户确认门：7 篇 CORE 同时覆盖 timing baseline 入口、FS+CFO 强近邻、2-sps GEO DSP 链、卫星参数综述、turbulence+DPLL，以及最接近的 clock/frame/FOE 直接竞品。未获取的 Gu/OE timing 全文与 JOCN 2026 继续列为用户确认项，不用摘要替代全文。

## 3. Q1 / Q2 碰撞与物理审计

- **Q1：强近邻存在，但当前未发现同信息—同动作—同任务 collision。** Tang 在正文中明确以 `one sample per symbol` 进入 carrier recovery；Wang 2023 的 FSTS 同样以 1 sps 实现 FS+FOE；OE 2024 的后续 FOE 采样率等于符号率。GEO 2023 虽采用 2 sps、coarse CFO 与 timing recovery，但为顺序/block-wise DSP 链。JLT 2025 已占用“一个 burst preamble 支持 clock/frame/frequency acquisition”的泛化表述，但全文动作是 TS-A/Godard clock recovery 与 TS-B frame/FOE 的顺序、分区处理，无 SCO。现有 CORE 因而没有闭合相同的 sample-level fractional timing + frame + CFO 联合搜索/更新。JOCN 2026 官方摘要更接近同一 preamble 三动作，但全文未获取，保持高风险缺口。这只是 Step 2 覆盖判断，不是新颖性结论。
- **Q2：物理动机成立，量化缺口保留。** 卫星 DSP 综述把 timing recovery 与 carrier synchronization列为必要子系统，并说明 timing loop需连续调整采样相位/频率；Paillier 2020证明 turbulence 下 AGC+DPLL carrier tracking 是真实任务；GEO 2023提供 2-sps timing/CFO 顺序链。但当前 CORE 尚未给出 GG fade + SCO 下 timing/carrier 双环共同失锁、恢复时间或联合状态机增益的量化证据。因此不得把 Q2 写成已确认问题，也不得拍 SCO/fade/reacquisition 参数。

## 4. Step 2 终态

`STEP2_READY_FOR_USER_CONFIRMATION`

下一合法动作仅为：由用户确认 CORE 覆盖面，或指定补充/替换文献。未经确认不得进入 Step 3、Step 3.5、Step 4a、方法设计、代码或仿真。
