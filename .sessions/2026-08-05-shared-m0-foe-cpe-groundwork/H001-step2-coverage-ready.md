# Handoff: P1 Shared M0-Power FOE–CPE GW Step 1–2 完成，覆盖面已验收

> 来源: S001（含 acceptance repair 续接）| 交接目标: 新对话显式授权后执行 Step 3 精读
> 文件名: H001-step2-coverage-ready.md
> 日期: 2026-08-05

## 到哪了（状态）

T008 已完成 GW Step 1 检索 + Step 2 全文获取/覆盖面门，并完成 T008 acceptance repair
（V001 PARTIAL → V002 PASS），terminal = **`STEP2_ACCEPTED_READY_FOR_STEP3`**。
P1 当前层级仍是 `THESIS_ENGINEERING_COMPONENT` 设计候选（D024），不是 METHOD_SIGNAL。

- Step 1 ✅：**raw=100 → dedup=97** 去重候选。4 查询通道均被调用，实际贡献候选的 API 源只有
  3 类（Semantic Scholar / OpenAlex / SerpAPI-scholar），**Exa 贡献 0**；publication_status =
  published 59 / unknown 36 / preprint 2；**可直接证明的正式发表率下限 = 59/97 = 60.8%**
  （通过 ≥50% 门；unknown 不计入分母）。3 语义类全覆盖，必读 ≥12。初筛矩阵在
  `search-archive/2026-08-05/_p1-competitor-shortlist.md`（metadata/abstract 级）。
- Step 2 ✅（已验收）：**12 篇合格全文**（identity/≥50 行/SHA256 全过，V002 复核 12/12），含
  2 篇 HIGH★ 直接竞品（CSNDSP 2014 method-level、udWDM-PON 2018 implementation-level）。
  原"2 篇最高优先竞品在 IEEE paywall 后"的系统性偏差已由 blit 第三轮消除。receipt 在
  `search-archive/2026-08-05/_step2_receipt.json`，覆盖面报告在
  `projects/thesis-fso/shared-m0-foe-cpe-groundwork/step2-coverage-report.md`。
- 剩余失败项：Optica/SPIE/MDPI 为主（中等/低相关），类别已有覆盖，非阻塞。

## 下一步干什么

**Step 3 不自动开始，需用户在新对话显式授权**：
1. 用户授权 → 开新对话执行 Step 3 精读（读 12 篇 content.md 中 Step 2 标定的必读子集，按 gw-read
   模板提取，关闭 topic-index 未决项 ①②③）。**Step 3 启动前必读 `stages/gw-read.md`**。

新对话第一步：读本专题 `topic-index.md`（不变量 + 未决项）+ `step2-coverage-report.md`，再读
`stages/gw-read.md`（Step 3 职责文件，**转步骤必须先读**）。

## 纪律（和下一步直接相关的约束）

1. **Step 3 未授权前禁读全文下方法/数据流/竞品结论**；本轮 coverage report 的"与 P1 关系"列仅复用
   Step 1 metadata 标注 + 首行 abstract 关键短语。
2. **P1 不是 METHOD_SIGNAL**；Step 3 精读要关闭"共享图是否已被传统实现吸收""是否还有可区分工程
   claim"——关闭前不得宣称新颖/有效/能成章。**"metadata 级未发现明确覆盖"不得当作新颖性证据**。
3. **对手默认 = 传统未优化 baseline**（FR-25），不是 oracle 上界；FR-21 只在 Step 3 走完 + 判据 A
   成立后才触发。
4. **不修改 NDA-ML 估计器统计**（触发既有 `NDA_ML_BODY_REOPEN`，不属于本候选）。
5. 主线程禁 WebSearch/WebReader；全文精读走子 agent（gw-read）。

---
## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落（M/C/A 冻结 + P1 层级 + 廉价吸收判据 + 覆盖面门 + NDA_ML_BODY_REOPEN 边界）
- [ ] 已验证本文件中的至少 3 条关键事实声称：
  - [ ] 12 篇合格全文存在且 ≥50 行（验证：`wc -l papers/doi/{12 dirs}/content.md`）
  - [ ] receipt 中 12 个 SHA256 可复核（验证：`sha256sum papers/doi/*/source.pdf` 对 `_step2_receipt.json`）
  - [ ] 统计口径 = raw 100 / dedup 97 / 3 API 源（Exa=0）/ published 59 → 下限 60.8%（验证：读 `_r1_merged_shortlist.json`）
- [ ] 已检查 _registry.yaml 中本专题（`2026-08-05-shared-m0-foe-cpe-groundwork`）的 depends_on（system 专题 D024 + problem-driven-redirection），无冲突
- [ ] 已确认当前范围未违反"明确不含"（Step 3 未授权、不实现、不仿真、不改 Skill/common/params、不重开旧 campaign）

## 失败数据附录

| 项 | 数据 |
|---|---|
| Step 2 获取成功率（修订） | 12 篇合格 / 高优先池 ~14 → ~86%（blit 第三轮补取 7 篇 IEEE 后） |
| 初版失败数据（已过时） | 初版仅 5 篇，2 篇 HIGH★ 在 IEEE paywall 后（用户纠正后由 blit 补取）——已修复，当前为 12 篇含 2 篇 HIGH★ 直接竞品 |
| 剩余失败 | Optica/SPIE/MDPI 为主（中等/低相关），类别已有覆盖 |
| 教训 | blit 是 IEEE 校园网有效第三轮通道；凭 `--help` 推断跳过实测 = TL-33 自欺式核查 |

## 已知债务

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| blit 取的 7 篇 metadata.json 仍是"failed"记录 | 身份可审计 | content.md 首行 + SHA256 已逐篇人工核验；blit meta 在 downloads/ | Step 3 前可重生成 metadata.json（非阻塞） |
| Optica/SPIE/MDPI 剩余失败项 | Step 2 应覆盖直接竞品 | 类别已有合格全文覆盖 | 视 Step 3 需要补取（非阻塞） |

## 验证阈值

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|--------|----------|---------|-----------|
| Step 1 检索门槛 | 去重 ≥20 / ≥3 源 / 必读 ≥5 / 正式发表率下限 ≥50% / ≥2 路线 | gw-search.md | 本轮 dedup=97/3源/≥12/下限 60.8%/3类 ✅ |
| Step 2 全文质量 | ≥5 篇 identity+≥50行+SHA256 | gw-acquire.md | 本轮 12/12 ✅（V002 复核） |
| Step 2 覆盖面门 | terminal ∈ {ACCEPTED_READY_FOR_STEP3, BLOCKED} | T008 §5 + acceptance repair | STEP2_ACCEPTED_READY_FOR_STEP3（V002 PASS） |

## 下一轮

开新对话执行 Step 3 精读（需用户显式授权）。**Step 3 启动前必须先读 `stages/gw-read.md`**。
