# Q1 Step 4a Preflight Independent Verifier Report

> 2026-08-07 | 独立只读复验（唯一新增文件为本报告）
> **Verdict: PASS**
> **Blockers: 0**

## 0. 结论先行

当前 `STEP4A_PREFLIGHT_EVIDENCE_GAP` 是合法且保守的终态；工作树没有把 preflight 写成 Go、
Conditional Go、METHOD_SIGNAL 或已执行维度 D。formal、RDL、master-state 与 registry 的科学状态一致。
首次复验提出的 5 个 blocker 均已按最小范围闭合，smoke 合同已具备后续“用户批准后再派执行”的
确定性语义；本次复验未发现新 blocker。结论为 **PASS**。

## 1. 首次复验 5 项修复闭合

### B1 — PASS：A0 §5 负面证据边界已显式登记

- 框架要求主动搜索“方法名 + 领域 + limitation/challenge/failure/unsuccessful”，找到失败报告则解释条件差异；
  完全找不到也须结合跨域先例判断（`stages/gw-feasibility.md:75-78`）。
- 修订后明确记录：既有 Step 3/3.5 只做 collision/coverage，不等价于负面检索；本项为
  `EVIDENCE_GAP`，不能声称“没有失败报告”或 A0 全通过；若 smoke 获批，执行前只允许先复用本地证据
  做有界核查（`projects/thesis-fso/oversampled-sync-groundwork/step4a-preflight-discussion.md:91-95`）。
- 该处理与当前整体 `EVIDENCE_GAP` 一致，闭合的是“证据边界遗漏”，不是伪造负面搜索已完成。

### B2 — PASS：复增益 nuisance 参数化已去冗余

- 修订后只保留 \(\alpha\in\mathbb C\)，由其同时吸收未知幅度和常相位；模型不再出现独立
  \(\phi_0\)（`step4a-preflight-discussion.md:32-47`）。
- FIM 方案明确以 \(x,jx\) 张成复 \(\alpha\) nuisance tangent space，\(P_\perp\) 投影到其正交补
  （同文件 `:108-113`）。参数化与投影职责自洽。

### B3 — PASS：B1/C 严格等价合同已冻结

- information contract 已新增共同 hypothesis grid、profiled GLRT、observation window/normalization、
  deterministic tie-break 与 refinement stop rule（`step4a-preflight-discussion.md:209-234`）。
- 等价只允许在候选集合、复 \(\alpha\) profiling、score、window、padding、normalization、tie-break
  完全相同且 B1 全局遍历三元候选时成立；连续 refinement 被隔离为扩展切片
  （同文件 `:238-242`）。原先“仅 timing bank 即等价”的歧义已消除。

### B4 — PASS：唯一主指标及分子分母已可执行

- 唯一主维度已改为 `wrong-basin false-lock rate`；所有 cell 含前导且四法必须输出估计，故
  `miss=N/A`，不混入主指标（`step4a-preflight-discussion.md:125-134`）。
- grid-only 与 refinement 切片分别冻结成功判据；分母是全部 preamble-present paired cells，
  `acquisition_success=1-R_FL`，并给出 \(G_C\) 与 B1/B2 coverage 公式及零分母处理
  （同文件 `:199-207`）。口径可确定性复算。

### B5 — PASS：D010 critic 指针已改为真实独立报告

- D010 现已直接引用本独立 verifier report，不再把 S002 冒充 verifier
  （`.sessions/2026-08-06-oversampled-coherent-sync-groundwork/decisions.md:372-379`）。
- topic-index 继续把 V007/H004 保留为后续收口动作，没有预写 V007 PASS
  （`.sessions/2026-08-06-oversampled-coherent-sync-groundwork/topic-index.md:112-136`）。

## 2. 九项核验结果

### 2.1 A0 §0 与 B0/B1/B2/C 身份 — PASS

- Q1 的 M-C-A 与四判据入口已明确，且 B0 被纠正为 evidence-faithful coarse-CFO-first 强链
  （`step4a-preflight-discussion.md:9-28`）。
- B0/B1/B2/C 均列出 receiver-visible input、objective、action/output、搜索维度、复杂度和结构身份；
  C 的增量被严格限制为共同 likelihood、无中间硬判决、利用交叉项/全局 margin
  （同文件 `:61-72`）。
- A′/A/B 矩阵覆盖 false-lock、reliability、RMSE、complexity、overhead，且不把 novelty 当可行性
  （同文件 `:147-162`）。
- A0 §5 的未完成事实已显式降为 `EVIDENCE_GAP`，未被误写成 A0 全通过；当前 terminal 与执行前补查门一致。

### 2.2 离散模型与非可分/等价判断 — PASS

- \(d\) 改变截窗、\(\tau\) 改变过采样脉冲、\(\nu\) 改变同一索引相位，因此一般 score 不可写成三个
  独立一维函数；在 coarse CFO 足够准、相关峰近理想、guard 消边界或交叉项很小时可近似可分，判断自洽
  （`step4a-preflight-discussion.md:30-59`）。
- B1/C 等价是“可能、条件式”而非既成事实；严格候选集/score/profiling/tie-break 条件现已冻结。

### 2.3 Identifiability / FIM / Hessian / ambiguity — PASS

- 已覆盖 frame–fractional 等价类、CFO alias、周期前导多峰、短前导 timing 信息弱与近似正交退化
  （`step4a-preflight-discussion.md:97-106`）。
- 局部 FIM/Hessian 只负责正确 frame basin，离散 ambiguity top-1/top-2 margin 与错误峰连通区负责
  全局 false lock，职责分工正确（同文件 `:108-113`）。
- 复 \(\alpha\) nuisance tangent 与 \(P_\perp\) 已明确，参数化闭合。

### 2.4 唯一主贡献 — PASS

- `wrong-basin false-lock rate` 是唯一主要贡献；complexity、RMSE、SNR、overhead 均未并列包装
  （`step4a-preflight-discussion.md:125-134,147-155`）。
- `miss=N/A`，成功口径与 false-lock 严格互补，分子分母和改善/覆盖公式均已冻结。

### 2.5 四个空白零假设与 JOCN ceiling — PASS

- 四个零假设均逐项列为未反驳/部分受支持，且明确“未发现 exact action”不反驳任何零假设
  （`step4a-preflight-discussion.md:136-145`）。
- JOCN 只限制 exact-action novelty/“首次”措辞，不作为 negative collision 或可行性证据；允许措辞上限
  被压到 bounded coupled acquisition rule（同文件 `:9-14,160-162`）。

### 2.6 ≤1 天 semantic smoke 合同与未执行边界 — PASS

- 已有同一 sample array 的 paired realization、四法 identity、B0/B1/B2/C-oracle、truth-scoring 隔离、
  hidden-truth metamorphic check、参数来源等级、真实 MAC/FFT/Farrow/score/wall-time 计数与预注册裁决
  （`step4a-preflight-discussion.md:164-265`）。
- `C-oracle` 被限定为 visible-only global optimum，不读取真值（同文件 `:177-185`）。
- 参数缺口诚实保留：fractional/frame 是 sentinel，SNR 执行前补来源或标 diagnostic sentinel
  （同文件 `:244-254`）。
- 共同搜索合同与主指标口径已闭合；是否执行仍须用户另行批准。
- 工作树修改只有治理/研究文档；`common/`、`params.py`、旧实验、Skill 均无 diff。四个 `p05_run*.log`
  是未跟踪旧文件，mtime 为 2026-07-30，当前 diff 为 0；未发现本轮运行痕迹（命令证据见 §4）。

### 2.7 Terminal 与无 Go/Conditional Go — PASS

- 三个科学终态仅为 `STEP4A_PREFLIGHT_KILL_OR_PIVOT`、
  `STEP4A_PREFLIGHT_RECOMMEND_MICRO_MVE`、`STEP4A_PREFLIGHT_EVIDENCE_GAP`
  （`step4a-preflight-discussion.md:256-265`）。`SEMANTIC_INVALID` 明确是不作科学终态的合同修复门
  （同文件 `:258-259`）。
- 当前终态是 `EVIDENCE_GAP`，未授权脚本/MVE/testbed，明确禁止 Go/Conditional Go
  （同文件 `:267-277`）。

### 2.8 formal / RDL / master / registry 状态 — PASS

- formal topic closed、D 未执行、等待用户批准 smoke（formal topic-index `:132-136`）。
- D033/CP016 同为 `EVIDENCE_GAP`、`mission_method_delta=NONE`、等待用户决定，未授权执行
  （RDL `decisions.md:1161-1187`; `mission-log.md:240-253`）。
- RDL control epoch 29 指向 formal D010，allowed action 只有用户决定/closeout verification，明确禁止
  未授权 smoke 与实现仿真（RDL `topic-index.md:3-26`）。
- master-state 同样记录维度 D 未执行、无 Go/Conditional Go（`projects/thesis-fso/master-state.md:30-52`）。
- registry 中 RDL 为 active、formal 为 closed，两者都记录同一 EVIDENCE_GAP 与下一动作
  （`.sessions/_registry.yaml:29-59`）。

### 2.9 Diff / YAML / status / push — PASS（本地可证范围）

- `git diff --check` 退出 0。
- `_registry.yaml`、master frontmatter、RDL control fenced YAML、smoke information contract 均经
  `yaml.safe_load` 解析通过。
- `git diff --name-status` 不含 `projects/simulation/common/`、`projects/simulation/params.py`、
  `.agents/skills/`、旧实验或 `p05_run*.log`；保护边界亦写入 formal topic-index `:36-43`。
- 当前分支无 upstream，`refs/remotes` 无包含 HEAD 的 ref，本地 reflog 只有 commit/checkout 事件；在禁止
  网络的约束下未发现 push 证据。该结论仅限本地 Git 证据，不声称远端网络级不可证明的绝对否定。

## 3. 逐项验收表

| 项目 | 结果 | Blocker |
|---|---|---|
| A0§0、B0/B1/B2/C 六字段与结构增量 | PASS | 0 |
| 离散模型、一般非可分、条件式离散等价 | PASS | 0 |
| identifiability / FIM / Hessian / ambiguity | PASS | 0 |
| wrong-basin false-lock 唯一主贡献 | PASS | 0 |
| 四零假设与 JOCN claim ceiling | PASS | 0 |
| ≤1 天 smoke 合同与未运行边界 | PASS | 0 |
| 三科学终态、当前 EVIDENCE_GAP、无 Go | PASS | 0 |
| formal/RDL/master/registry 状态 | PASS | 0 |
| diff/YAML/status/protected/push 本地证据 | PASS | 0 |

## 4. 确定性检查记录

```text
git diff --check
  exit 0

yaml.safe_load
  registry PASS
  master-frontmatter PASS
  rdl-control PASS
  information-contract PASS

git status --short --branch
  8 个 tracked 文档修改；S002 与 step4a-preflight-discussion.md 为新文件；
  四个 p05_run*.log 为 2026-07-30 旧未跟踪文件；无代码/参数/Skill 修改。

git diff -- projects/simulation/common projects/simulation/params.py .agents/skills p05_run*.log
  空输出

git for-each-ref --contains HEAD refs/remotes
  空输出
```

## 5. 最终裁决

**PASS，0 blockers。** 当前 `STEP4A_PREFLIGHT_EVIDENCE_GAP` 可保留。该 PASS 只证明 preflight 分析、
smoke 合同与跨文件状态一致，不代表维度 D 已执行、Q1 已 Go 或用户已批准 smoke。下一合法动作仍只是
用户审阅并决定是否授权；未授权前不得派执行 T、运行脚本或写 Go/Conditional Go。
