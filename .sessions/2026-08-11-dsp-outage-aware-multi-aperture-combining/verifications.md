# 验证记录

## V001：GW Step 1 检索与 collision 综合终验

- 日期：2026-08-11
- 关联：S001 / D001 / R001 / T003
- 验证方：fresh-context child verifier（与作者/两路初筛分离）
- 状态：PASS
- 严重度：P0/P1/P2=`0/0/0`

### 验证对象

- q1–q6 原始 JSON、search receipt、27-entry candidate/collision matrix。
- R001 synthesis、provenance receipt、topic/decision/master-state 控制面。
- registry/master-state/topic diff 与 Step 1 scope。

### 验证结果

| 组 | 结论 | 独立证据 |
|---|---|---|
| A counts/sources | PASS | `0+18+50+48+22+31=169`；DOI/title unique=`157`；matrix 27、24 formal+3 unknown、8 must-read；贡献源仅 S2/OA/Tavily。 |
| B identity/provenance | PASS | 2019 行 10860 SHA=`9c35292e...651e4e8`；Geisler 行 15493 SHA=`3d26dd2f...7bddfab4`；Johst/Wang 边界与 OFC 错配隔离成立。 |
| C collision/terminal | PASS | hard 与宽泛 soft 先例已降 comparator/neighbor；2019 direct exact=`UNRESOLVED`；未写 novelty PASS；terminal 被接受。 |
| D scope/diff | PASS | Step 2=`NOT_AUTHORIZED`；未下载、精读、实现、仿真、smoke 或修改 b3/coded topic。 |

### 失败与修复血缘

第一次 fresh 终验为 `FAIL 0/1/1`：专题未绑定既有全局索引的 2019/Geisler 记录，且 receipt 残留“26 项”。唯一窄修新增 provenance receipt、绑定两行哈希并修为 27；未新增 query。第二个 fresh context 在最终文件上给出 `PASS 0/0/0`。

### 结论

`STEP1_PASS_READY_FOR_STEP2_CONFIRMATION`。该结论只接收 Step 1 检索质量和后续获取必要性；Q#、Go/Kill、METHOD_SIGNAL、method/thesis delta 均未产生。

## V002：GW Step 2 acquisition 与 coverage 终验

- 日期：2026-08-11
- 关联：S002 / D002 / R002 / R003 / T006
- 验证方：fresh-context child verifier（与获取/转换执行分离）
- 状态：PASS
- 严重度：P0/P1/P2=`0/0/0`

### 验证对象

- 四篇 claimed qualified 的 canonical/shared-root source/content 与 metadata。
- 五篇 claimed unavailable 在 worktree、共享根、canonical DOI、downloads/manual 的可验证资产。
- R002/R003/topic-index/master-state/registry 的 coverage 数字、terminal 与 scope。
- 本轮 diff、git staging 与 unrelated dirty files 的隔离。

### 验证结果

| 组 | 结论 | 独立证据 |
|---|---|---|
| A identity/hash/lines | PASS | WiSEE 2024、Wang 2023、ICCC 2022、JPHOT 2020 的 bytes/SHA/总行/非空有效行与 R003 全部一致；标题/DOI 闭合。 |
| B content quality | PASS | 四篇反爬文本命中 0；前三篇 U+FFFD=0；JPHOT 2020 的 39 个替换符仅分布在 18 行公式符号，未构成大面积乱码。 |
| C unavailable/coverage | PASS | 五篇均无 target source/content；P0 仍 unavailable。targeted qualified=`4/9`，optical CORE=`2/5`，ICCC/JPHOT 2020 未被计入 CORE。 |
| D terminal/control plane | PASS | R002/R003/topic/master/registry 一致：`STEP2_BLOCKED_CRITICAL_DIRECT_COMPETITOR_FULLTEXT`；Step 3=`NOT_AUTHORIZED`。 |
| E scope/diff | PASS | 无正向动作签名、碰撞裁决或后续科学门产出；无实现/仿真/b3 repair；staging 为空，unrelated dirty files 未纳入。 |

### 结论

接受 Step 2 acquisition/coverage 终态。下一合法动作只有用户手动补 P0 后重跑 Step 2 gate，或用户显式接受 coverage/claim limitation 并另行授权 Step 3；当前不得继续。
