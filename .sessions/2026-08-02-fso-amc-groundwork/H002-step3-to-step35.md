# Handoff: GW Step 3 终态 STEP3_NO_VALID_PROBLEM → Step 3.5 定向补充检索

> 来源: S004 | 交接目标: 下一对话执行 GW Step 3.5 定向补充检索
> 日期: 2026-08-03 | 文件名: H002-step3-to-step35.md

## 到哪了（状态）

GW Step 2 + Step 3 在本轮（S004/D004/V005）一个对话内完成：
- **Step 2**: 用仓库历史全文 Nguyen2024（IEEE TAES 60(5):7498-7509, 2024，Crossref 独立验证 + SHA256 迁移，**非公开 OA** 机构 IEEE Xplore 授权）补到 **5 CORE 全文**（L023/L096/L146/Galijasevic/Nguyen2024）。终态 **STEP2_PASS_WITH_COHERENT_C_FAMILY_BLOCKED**。C 族 L124 仍 BLOCKED，Safi 仍 PROVISIONAL abstract-only。
- **Step 3**: 5 CORE 全文精读（fresh-context 子 agent，14+ 字段 + 7 结构化子表 + 问题提取 + 四判据）+ 3 边界（L075=classification / L165=AO / L090=fixed-STTC）+ 2 abstract（Safi/L124）。**直接竞品矩阵确认无一篇 confirmed 同时覆盖 coherent+GG+coded+uncertainty 四要素**。5 候选 Q# **无一四判据全过** → **终态 STEP3_NO_VALID_PROBLEM**。
- 产出: `projects/thesis-fso/literature_notes_amc.md`（专属 owner，不覆盖 receiver literature_notes）+ 5 `papers/_read_notes/` + `_step2_acquisition_receipt.json`（更新）+ D004/V005/S004/本 H。

## 下一步干什么

**GW Step 3.5 定向补充检索**（glossary"候选全被筛掉时"流程①回扩检索；`stages/gw-supplement.md`）。优先级：
1. **coherent FSO + Gamma-Gamma + adaptive modulation/coding 直接竞品**（确认 L124 之外是否有 confirmed 同时覆盖 coherent+GG+runtime AMC 的工作）。
2. **coherent 检测下 CSI 反馈/预测的 AMC 工作**（coherent γ∝h 的信息度量 vs IM/DD γ∝h²）。
3. **Gamma-Gamma 中/强湍流下 AMC headroom 分析论文**（确认 GG 下 AMC 是否物理成立）。
4. **共同引用基础文献延伸**: Nguyen[9 Perlot/de Cola, 12 Geisler AM+coding coherent LEO 实验, 16 terrestrial rate+power] / L096[12,13 IR-HARQ-SW, 15 pure SW-ARQ] / Galijasevic[8 Nguyen2020 Asilomar, 20 PBRL]。
5. **Safi + L124 全文获取**（用户手动，关键身份闭合）：Safi DOI 10.1109/tvt.2019.2916843（IEEE paywall）/ L124 DOI 10.1364/oe.595557（Optica gold-OA bot-block）。
6. 中文检索 cookie/IP（L050/L206）校园网可用时重试。

Step 3.5 后若仍无 Q# 四判据全过 → 上报用户决策是否调整 C 条件（coherent+GG+coded+sat-ground+uncertainty 五要素锁死）或换子方向。

## 纪律（和下一步直接相关的约束）

1. **FR-22 硬门控**: Step 3 已完成但**无 Q# 全过 → 禁进 Step 4a/MVE/方法设计/仿真**。Step 3.5 是唯一合法下一步。
2. **FR-23 + brief 明示**: rate/power（Nguyen）/ HARQ-rate（L096）/ coding-rate+prediction（Galijasevic）/ robust-MCS（L146）已被覆盖，**禁止重命名为空白**。
3. **D003 约束**: Safi/L124 全文缺失时，**禁据 abstract 推导失效机制**；coherent-C 族（L124）不得过 novelty closure；Safi 邻近切片不得据 abstract 通过。
4. **glossary 空集处置**: 候选全空先回扩检索（Step 3.5）；扩检索后仍空 → 上报用户，**禁 agent 自行放宽 C 条件**（跨阶段决策）。
5. **TL-31/TL-33**: 动笔前必读 decisions.md + thesis-lessons；所有"已读/已确认"必附 file:line/API 证据，不靠联想。

---
## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落（AMC≠receiver campaign / GW 流程强制 / Go-Kill 分离 / 证据链强制）
- [ ] 已验证本文件至少 3 条关键事实声称:
  - Nguyen2024 迁移 SHA256 一致（`sha256sum papers/doi/10.1109_taes.2024.3403809/source.pdf` = b49f5abf…4c95c51）
  - 5 CORE 全文存在（`ls papers/doi/10.1109_{jltaes...}/content.md` 5 篇 ≥ 50 行）
  - literature_notes_amc.md Step 3 终态 = STEP3_NO_VALID_PROBLEM（§7）
- [ ] 已检查 _registry.yaml 本专题 status=active，conflicts_with=[]
- [ ] 已确认当前范围未违反"明确不含"（不进 Step 4a/不设计方法/不跑仿真/不修 Skill/不碰 p05 log）

## 关键事实证据指针（接收方快速核对）

- Nguyen 迁移 + Crossref 验证: `papers/doi/10.1109_taes.2024.3403809/metadata.json` + receipt `Nguyen2024` 条目
- 5 CORE 精读: `papers/_read_notes/{L023_jlt_2023,L096_tvt_2022,L146_jiot_2025,Galijasevic_ojcoms_2024,Nguyen2024_taes}.md`
- 直接竞品矩阵 + Q# 表: `projects/thesis-fso/literature_notes_amc.md` §4 + §6
- Step 3 终态判定: `literature_notes_amc.md` §7
- D004 + V005: `.sessions/2026-08-02-fso-amc-groundwork/{decisions,verifications}.md`
