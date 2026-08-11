# Task Brief: GW Step 1 fresh-context 独立终验

> 来源: S001 | 产出位置: 回传主线程，不写文件
> 日期: 2026-08-11
> 唯一文档: 本任务书 + 本专题文件 + q1–q6 JSON + git diff

## 0. TL;DR

在 fresh context 中独立验证 Step 1 的计数、来源质量、语义分类、collision 措辞和 scope；不得继承作者结论。

最高纪律：只读；不联网、不下载、不全文精读、不实现、不仿真、不改文件。任何 exact-collision 或 terminal 结论必须从现有摘要/元数据证据推出。

## 1. 背景

作者 provisional terminal 为 `STEP1_PASS_READY_FOR_STEP2_CONFIRMATION`。2019 Optics Communications adaptive digital combining 被标为最近 direct competitor 且 collision=`UNRESOLVED`；hard admission 和宽泛 soft MRC 已降为 comparator/neighbor。终验需要独立接受或否决，不做措辞润色式自审。

## 2. 任务详情

### 2.1 必读

- 本专题 `topic-index.md`、`S001-step1-search.md`、`decisions.md`、`R001-step1-synthesis.md`
- `step1-search-receipt.md`、`step1-candidate-collision-matrix.md`
- q1–q6 JSON
- `projects/thesis-fso/master-state.md` 当前控制面桥接
- `git diff --` 上述文件与 `.sessions/_registry.yaml`

### 2.2 独立检查

1. query≤6、round≤2；返回量、去重 157、candidate 27、formal 24、must-read 8 是否可复算。
2. contributing sources 是否确为 S2/OpenAlex/Tavily 三个；0 贡献源未被计入。
3. 27 行是否逐条有 semantic class；formal/unknown 口径是否自洽。
4. Johst/Wang/Geisler/2019 closest competitor identity/provenance 是否诚实；已知索引摘要错配是否被隔离。
5. collision 措辞是否正确区分 hard exact、broad-soft neighbor、2019 direct unresolved；是否错误写成 novelty PASS。
6. 是否越界下载、精读、实现、仿真、smoke、修 b3/coded topic，或把 Step 2 标为已授权。
7. terminal 是否只能落在三个允许值之一，并与证据一致。

### 2.3 产出格式

- verdict：`PASS` 或 `FAIL`
- P0/P1/P2 计数
- A counts/sources；B identity/provenance；C collision/terminal；D scope/diff，各给 PASS/FAIL 与证据
- 若 FAIL，只列可操作 blocker；若 PASS，明确 accepted terminal

## 3. 已知陷阱

- 不能把 169 raw 当 unique；不能把工具的 publication_status 自动标签当正式身份。
- 不能因摘要未出现 validity 一词就判 2019 competitor non-exact。
- 不能把 Step 1 PASS 写成问题四判据、方法或论文贡献。

## 4. 验收

- [ ] 所有计数独立复算。
- [ ] collision 与 scope 逐项核验。
- [ ] 返回内容足以直接写 V001。

## 附：产出回传位置

直接回传主线程，限 1200 中文字。
