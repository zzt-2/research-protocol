# Verifications — Adaptive Intra-Window Segmented CPE Groundwork

## V001: fresh-context Step 1 terminal 与控制面终验

> date: 2026-08-06
> 关联：S001 / D002

### 验证项

- [x] P1 acceptance repair：P1 topic 相对起点 diff=0；topic/registry/master 一致为
  `closed / RECENT_BASELINE_UNAVAILABLE / SUPPORTING_ONLY / 禁改名重开`。
- [x] RDL current control：D026 / CP007 / epoch 19 / `CANDIDATE_ROTATION_REQUIRED` 一致；stale grep=0。
- [x] 检索统计：四 JSON final=50/30/37/34→151，跨组 unique=140；优先级 8/7/20/36/69，
  published/unknown=77/63；151/151 均有 priority/reason；四 SHA256 与 receipt 匹配。
- [x] baseline/竞品：两篇 JLT DOI 均存在且 abstract 支持 fixed-window blind CPE baseline 角色；
  Photonics 2022 是 EKF-PC 跨 SNR 参数联合优化，不是同信息同动作的在线 K 选择。
- [x] 历史 exact-action：inventory/D-011 支持 gain=0、0/8、71%、`rho=0.361`、VV 反超
  14%/68% 与 10–80 kHz 有限样本边界；terminal 仅限冻结 C3 条件。
- [x] Step 2/范围：papers/code diff=0、无新增论文；Step 2=0/0 且因 gate stop 未执行；
  Step 3/3.5/4a/实现/仿真均未发生。
- [x] 治理：topic-index/S001/R001/D001–D002/H001/voice 齐全；master/literature notes 一致；
  registry 可解析为 57 topics，C3 三项依赖均存在，`conflicts=[]`。
- [x] Git 边界：`git diff --check c794d152` exit 0；暂存区为空；tracked pycache clean；四个
  `p05_run*.log` 仍为 `??`、mtime 保持 2026-07-30、未进 index。

### 证据

fresh-context verifier 独立只读复算摘要：

```text
final = 50 + 30 + 37 + 34 = 151
cross-query dedup = 140
priority = must-read 8 / recommended 7 / backup 20 / to-confirm 36 / excluded 69
publication = published 77 / unknown 63
annotations = 151/151 non-empty
registry = 57 topics; C3 depends_on all exist; conflicts=[]
git diff --check c794d152 = exit 0
staged_count = 0
tracked litsearch pycache dirty = 0
p05 logs = four untracked files; index entries = 0
```

证据边界：raw=187 与 query-dedup=179 来自 `tools/search` executor stdout lineage，final JSON 无法独立
重算这两个中间阶段；receipt 已明确披露。10–80 kHz 来自有限实测样本，不能泛化为全领域；“offline”
竞品判断仍是 abstract 级推断，不是全文裁决。

### 结论

PASS
