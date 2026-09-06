# T086 Ch4 方法族生产冻结独立验收

> 2026-08-30 | 独立只读验收 | 未运行任何仿真

## 结论

**P0/P1/P2 = 0/0/3，终态：`CH4_FAMILY_PRODUCTION_FREEZE_READY`。**

T086 的 development tuning、结构 smoke 记录和 scientific manifest 冻结满足任务合同。最终 scientific manifest 的现场 SHA-256 为：

`417f334844f9092b02bab5d6478381ae7a57e2ff9b4a385ba37707f601521079`

该结论只表示 T086 冻结准备就绪；它不把 development 数字升级为论文证据，也不授权跳过 T087 的 runner/reducer/tests TDD、execution lock 和首个 formal cell 前的双锁校验。

## 验收边界

- 读取并核对 T086 任务、step-086 worker log、四个 tuning artifacts、scientific schema、最终 scientific manifest 及相关实现/测试。
- fresh 运行聚焦测试、隔离 `py_compile`、task-control、scope/history/diff 检查。
- 使用仅依赖 Python 标准库的独立脚本直接读取 raw，未导入项目 reducer，重算 census、全部 12 个 tau、全部 objective 和 development terminal。
- 未运行 ID20999、ID21999、canonical tuning 或任何 formal production；未改实现、治理、历史产物或论文正文。

## Fresh 验证证据

| 项目 | 现场结果 | 判定 |
|---|---|---|
| focused tests | `27 passed in 2.12s` | PASS |
| 六个 T086 Python 文件 `py_compile` | `PY_COMPILE_PASS 6`；pyc 写入系统临时目录 | PASS |
| task-control validator | `PASS`，T086 对齐 CP027 / epoch 27 | PASS |
| `git diff --check` | exit 0；仅出现既有 LF/CRLF 提示 | PASS |
| 禁止修改项 | `production_core.py`、`common/_modulation.py`、`scaled_unitary.py` 与 T085 manifest/raw/receipt 均无 diff | PASS |
| T085 历史 SHA | `d3ed6c7d…18fde` / `4ef32e16…33ed` / `7ad0d5b8…91c36`，与 T086 manifest 完全一致 | PASS |
| 独立 raw-only 复算 | `96 / 1152 / 8064`；最大 objective 差 `0.0` | PASS |
| 独立终态复算 | `CH4_FAMILY_PRODUCTION_FREEZE_READY` | PASS |

## 谱系与 12-tau 冻结

四件 tuning artifact 的现场 SHA 与 receipt、最终 scientific manifest 三方一致：

| Artifact | SHA-256 |
|---|---|
| tuning manifest | `e35c418d176904b4048fe1b83fe22865e01223f51017953a6443776b8a6a312a` |
| tuning raw | `00161c4838a7543878fb191b667935608a242bbdc8ba2849dec4d324113fa315` |
| tuning aggregate | `9af3b3af134656863b6a39f8e2d927274d9a82fe0548c95e4dd49429da531378` |
| tuning receipt | `afa9189499501a59d65fc549546dd7b88985555c38918cc9cc6b85dba147e2fc` |

receipt 中 runner、reducer core、reducer entry、tests、params、production core、common demapper、scaled-unitary 的登记 SHA 均与当前文件一致；`receipt_inputs_sha256` 也从 aggregate 的 decision、tau map 和 census 独立重建一致。

独立 raw-only 复算所得 tau 恰为：

| Scene | Np=2 | Np=4 | Np=8 | Np=16 |
|---|---:|---:|---:|---:|
| weak | 1.0 | 1.0 | 1.0 | 1.0 |
| moderate | 0.5 | 1.0 | 1.0 | 1.0 |
| strong | 1.0 | 1.0 | 1.0 | 1.0 |

该 map 与 aggregate、receipt、scientific manifest 顶层字段及 tuning lineage 全部相同。复算同时确认 tuned B2 未满足“全部 12 cell 同时不劣于 C4/B3 且至少一处严格更优”的 development stop，因此继续保持 READY，而不是 `TUNED_BASELINE_DOMINATES_DEVELOPMENT`。这不构成 C4/B3 的正式科学胜负结论。

## Scientific manifest 合同核验

- population：formal IDs 精确为 `30000..30127`，128 个 `latent_id` clusters；与 T085、tuning smoke、canonical tuning、structure smoke 分区零重叠。
- grid：SNR 固定为 `5:2:41 dB`；moderate 的 Np=2/4/8/16、weak/strong 的 Np=2 均为完整曲线。
- signal：4096 payload symbols/polarization、`DP-(8,8)-16APSK`、post-demux/pre-Ch3-CPR/uncoded pre-FEC BER、工程参考 BER `3.8e-3` 均已冻结。
- mismatch：moderate/Np2/25 dB，delta=`0/0.05/0.10/0.20/0.30/0.40`；公式、Q/R/g component usage 与 `mismatch_left` 不消费规则完整。delta=0 明确为主 cell 的 exact reference、不得重复 observations/rows；聚焦测试已覆盖 H0 与三类 observation hash exact identity。
- statistics：whole-curve PCG64 seed `2026083007`、5000 resamples、至少 4500 个有效 gain crossings；cell-level PCG64 seed `2026083008`、5000 resamples、仅同一 scene/Np 内 128 paired clusters。
- grade：A/B/C/F 与 `CH4_FORMAL_INVALID` 分离；A/B 才进入章节定稿，C/F 返回论文结构讨论。
- execution interface：状态为 `PENDING_T087_IMPLEMENTATION`；future runner/reducer/tests hash 值为 `null`；首个 formal cell 前必须绑定 exact scientific-manifest SHA、runner、reducer、tests、base commit 和 environment snapshot。

scientific schema 的现场 SHA 为 `74a5f61408a16a7874eb73ac00b2ea5cd9144f8b9212b930a368274e5a8493ee`，与最终 manifest 绑定值一致。params SHA、weak/moderate/strong 的 resolved `(alpha,beta)` 及三项 frozen code SHA 也均与现场文件一致。

## Scope 与历史不可变性

T086 实现产物均位于任务允许的仿真 seam 和 worker log 路径；本独立验收新增的只有本报告。当前 worktree 另有同一长期 campaign 的既有改动，因此 scope 判断以 T086 文件清单、禁止修改项定向 diff 和历史 SHA 三者交叉完成，而不是把整个脏 worktree 误当成 T086 单任务 diff。

结构 smoke 的 raw/receipt 仅在 worker log 记录的 OS 临时目录产生；仓库和当前 Git worktree 中没有 smoke artifact。日志记录 terminal=`STRUCTURE_SMOKE_PASS`、10 个实际 cells、1 个 delta-zero reference、50 个 arm rows，以及 delta-zero exact identity。由于本轮禁止仿真，独立验收不重跑该 smoke，只以 frozen tests、实现静态检查和留存日志验收其结构合同。

## 非阻断 P2（保留，不隐去）

1. **最终 freeze CLI 不会再次逐项校验 receipt 中 reducer core、reducer entry 与 tests 的当前 SHA。** 本次独立验收已逐项核为一致，且最终 manifest 绑定了完整 receipt SHA；因此当前产物有效。后续若这些辅助文件变化，仅依靠 freeze CLI 本身不能提示 receipt 内的辅助审计绑定已陈旧。
2. **smoke 输出目录护栏只拒绝当前 repository/worktree 根之内的路径。** 它不能识别其他 sibling worktree 是否属于同一 Git 仓库。本次两个 smoke 的记录路径均为 OS temp，且未发现 tracked smoke 污染，故不影响本次结论。
3. **aggregate 与 receipt 采用两个顺序 `os.replace`，不是跨文件事务。** 若首次发布时 aggregate replace 成功而 receipt replace 失败，会留下半发布状态，需要人工恢复。当前两文件均已完整存在、SHA/内容/谱系一致，因此这是历史故障恢复风险，不是当前科学产物错误。

以上三项均未吸收承重科学结论，也不改变 T086 的 READY 终态；应在 T087 execution lock 中继续 fail closed，而不应据此重跑 T086 development 数据。

## 最终判定

- P0：0
- P1：0
- P2：3
- Artifact validity：PASS
- T086 terminal：`CH4_FAMILY_PRODUCTION_FREEZE_READY`
- Formal production：仍未执行；须由后续独立授权和 T087 execution lock 开放
