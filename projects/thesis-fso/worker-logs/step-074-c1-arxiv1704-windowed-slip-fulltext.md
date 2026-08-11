# Step 074 — arXiv 1704.04618 windowed slip fulltext attempt

> 2026-08-09 | T028 / CP009 / Groundwork Step 3.5 | `UNRESOLVED_FULLTEXT`

## 1. Control 与范围

- 唯一工作树：`D:/code/study/research-protocol/.worktrees/rdl-method-production-v2`。
- Fresh validator：`PYTHONDONTWRITEBYTECODE=1 python .agents/skills/research-direction-lab/scripts/validate_task_control.py .sessions/2026-08-09-coded-decoder-feedback-groundwork/T028-c1-arxiv1704-windowed-slip-fulltext.md` → `PASS`。
- 已读 task、gw-acquire/gw-read/gw-supplement、topic-index、D008、step-067、ICTON 2016 read note、RDL long-horizon control；本包只执行 `FULLTEXT_READ`。
- 未改中央 owner/治理/代码，未运行实验，未 stage/commit/push。

## 2. Identity 与 acquisition receipts

| 项目 | Receipt / result |
|---|---|
| official identity | arXiv API receipt=`1704.04618v1`，2017-04-15；标题 *Advances in Detection and Error Correction for Coherent Optical Communications: Regular, Irregular, and Spatially Coupled LDPC Code Designs*；authors=Laurent Schmalen / Stephan ten Brink / Andreas Leven |
| DOI mapping | S2/OpenAlex把该 chapter映射到 book DOI `10.1002/9781119078289`；official arXiv receipt无 DOI，故不把 book DOI冒充 exact chapter DOI |
| dry run | `tools/download --arxiv 1704.04618 --dry-run` → normalized target `papers/arxiv/1704.04618` |
| actual attempt | 244 s timeout；留下532480-byte截断 PDF；Poppler xref/endstream/trailer全失败，质量门 FAIL |
| safe cleanup | 确认损坏文件位于 exact paper dir且停止增长后，仅删除该 corrupt `source.pdf` |
| forced retry | `tools/download --arxiv 1704.04618 --force --quality fast`；等待终止后子进程仍写入，最终按时间门停止于1941762 bytes；Poppler仍报告xref/endstream错误，SHA256=`39B485F8CF10CA64863F44FC9A7FE9A200F02D2E7E2DA8B73C9AAFF6E4687E63`；记录后删除损坏PDF，`metadata.json=all_failed` |
| late completion anomaly | 主控止损后后台下载/转换进程才落下 title-matched `content.md` 1289行与success metadata；本 T 未再扩展精读，故不伪造 `FULLTEXT_READ`；保留正文供后续 fresh read |

## 3. Evidence-backed facts（9 条）

1. Identity由官方 arXiv v1 receipt确认；正文在止损后late-arrive，但本 T 未完成全文精读。
2. 摘要讨论 QPSK differential coding与phase slips对information rate/capacity的影响。
3. 摘要把 differential loss归因于simplified differential detection/decoding，而非 differential coding必然损失。
4. 摘要明确声称 modified differential decoder accounts for phase slips，并据此设计 LDPC codes。
5. 摘要明确声称 LDPC/SC-LDPC用于 iterative differential demodulation/decoding。
6. “windowed”在摘要中修饰 SC-LDPC decoder；没有 slip flag、boundary、segment/suffix action或 selective re-decode证据。
7. window length/latency/iterations、clean behavior、fallback、slip metric与实验全部 `UNKNOWN_FULLTEXT`。
8. ICTON 2016是不同作者/题名/ID；其全文改 layered LDPC schedule与stop，且DD不建模 slip；不能把两篇合并计数或称直接扩展。
9. Collision=`UNRESOLVED_FULLTEXT`；缺全文不得裁 exact，也不得降格为 partial/neighbor/no collision。

## 4. 八字段

| 字段 | 可承重结论 |
|---|---|
| input | differential coherent QPSK observations + LDPC/SC-LDPC messages（abstract） |
| trigger | iterative loop；event trigger `UNKNOWN_FULLTEXT` |
| localization | SC-LDPC window stated；slip boundary `UNKNOWN_FULLTEXT` |
| candidate/correction action | modified DD accounts for slips；state/metric/local action `UNKNOWN_FULLTEXT` |
| decoder interaction | iterative DD + LDPC/SC-LDPC（abstract） |
| fallback | `UNKNOWN_FULLTEXT` |
| complexity/latency budget | only qualitative “very simple windowed decoder”；numbers `UNKNOWN_FULLTEXT` |
| output | decoded data；boundary/local repair output `UNKNOWN_FULLTEXT` |

## 5. Window / ICTON adjudication / claim ceiling

- Window verdict：`WINDOWED_SC_LDPC_GRAPH_SCHEDULE_STATED / LOCAL_REPAIR_NOT_ESTABLISHED`。抽象层不能把 code-graph window等同于 slip-aligned affected segment/suffix，也不能据此断言全文没有该机制。
- ICTON relation：`DISTINCT_IDENTITY / MECHANISM_DISTINCT_AT_AVAILABLE_EVIDENCE / EXPLICIT_LINEAGE_UNVERIFIED`。arXiv摘要改 differential metric/code design；ICTON全文改LDPC schedule与全码字停止。
- Claim ceiling：只能保留为 exact-chain acquisition debt；不得写 Q1新颖、无碰撞、已被碰撞或 Step 4a可进入。

## 6. Protection

- p05未修改；fresh终验4个冻结SHA256=`4/4 MATCH`。
- Git staging fresh终验=`EMPTY`；并发 dirty/untracked未清理、未归因。
- 保留 late-arrived `content.md`（1289行）与success `metadata.json`，供后续 fresh read；已终止任务专属下载进程。`source.pdf` 因止损时 Poppler corruption receipt被删除；本 T 不把转换文件存在伪称为已完成全文裁决。

`UNRESOLVED_FULLTEXT`
