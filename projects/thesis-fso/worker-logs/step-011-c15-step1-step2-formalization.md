# Step 011 — C15 Step 1–2 formalization

> 执行日期：2026-07-27（任务书路径日期保持 2026-07-26）
> 执行边界：只执行 T011 §2.1 与 §2.2；未执行 Step 2 acquire。

## Status

- task_control: PASS
- final_status: BLOCKED_SEARCH_COVERAGE
- formal_science_disposition: BLOCKED_SEARCH_COVERAGE
- mission_method_delta: NONE
- simulation_or_seed_run: false
- step1_state: BLOCKED_BEFORE_ACQUISITION_POOL
- step2_state: NOT_STARTED

阻断原因不是候选总量：7 个 archive 合并去重后有 53 条，49/53
（92.5%）被工具标为 `published`。硬阻断是：

1. 53 条保留结果的实际 `source_api` 全部为 `openalex`，未达到 ≥3 个实际来源；
2. S2 每次均被 rate-limit；SerpAPI/Tavily/Firecrawl/Exa 因无 API key 跳过；
3. staged optical、normalized cost、canonical lineage 三组定向检索保留结果均为
   0；FSO task-fit 仅保留 1 篇泛 ML/DL optical survey，不能支撑 task-fit；
4. 因硬门失败，未给原 archive 批量写入 `priority/priority_reason`，未创建
   `c15-step1-acquisition-pool.json`，也未进入 Step 2。

这不是 C15 的科学 negative、Kill 或方法判断，只是 Step 1 检索覆盖阻断。

## Exact commands and exits

### 起飞门

```powershell
python C:\Users\zzt\.agents\skills\research-direction-lab\scripts\validate_task_control.py --repo-root . .sessions\2026-07-23-research-direction-lab-longitudinal-test\T011-c15-step1-step2-formalization.md
```

- exit: `0`
- stdout: `PASS`
- 起飞前 `git status --short`: 空
- formal owner: `.sessions/2026-07-06-step4a-mve-execution/decisions.md#D023`
  存在且 active
- live owner: `.sessions/2026-07-23-research-direction-lab-longitudinal-test/decisions.md#D012`
  存在且 active
- `rdl-t010-closure` (`b72bf08d8757af7af06cfdc545d729ddd12518a2`) 是当前
  HEAD `700864d` 的祖先
- 未发现 `projects/simulation`、MVE 或 seed 进程

### Step 1 search

以下 7 条命令均逐字来自 T011，全部 exit `0`：

```powershell
wsl bash -lc "cd /mnt/d/code/study/research-protocol/.worktrees/rdl-method-production-v2/tools && mkdir -p ../search-archive/2026-07-26 && sed 's/\r$//' search | bash -s -- 'blind equalization square QAM constant modulus multimodulus' --mode academic --preset problem-driven --max-per-source 20 --top 40 -o ../search-archive/2026-07-26/c15-broad-cma-mma.json"
wsl bash -lc "cd /mnt/d/code/study/research-protocol/.worktrees/rdl-method-production-v2/tools && sed 's/\r$//' search | bash -s -- 'reduced constellation equalization Sato algorithm square QAM' --mode academic --preset problem-driven --max-per-source 20 --top 40 -o ../search-archive/2026-07-26/c15-broad-rca-sato.json"
wsl bash -lc "cd /mnt/d/code/study/research-protocol/.worktrees/rdl-method-production-v2/tools && sed 's/\r$//' search | bash -s -- 'radius directed equalization RDE coherent optical PM-16QAM' --mode academic --preset problem-driven --max-per-source 20 --top 40 -o ../search-archive/2026-07-26/c15-broad-rde-optical.json"
wsl bash -lc "cd /mnt/d/code/study/research-protocol/.worktrees/rdl-method-production-v2/tools && sed 's/\r$//' search | bash -s -- 'CMA RDE MMA staged blind equalization coherent optical 16QAM' --mode academic --preset comparison --max-per-source 20 --top 40 -o ../search-archive/2026-07-26/c15-deep-staged-optical.json"
wsl bash -lc "cd /mnt/d/code/study/research-protocol/.worktrees/rdl-method-production-v2/tools && sed 's/\r$//' search | bash -s -- 'free space optical turbulence adaptive blind equalization CMA RDE' --mode academic --preset comparison --max-per-source 20 --top 40 -o ../search-archive/2026-07-26/c15-deep-fso-taskfit.json"
wsl bash -lc "cd /mnt/d/code/study/research-protocol/.worktrees/rdl-method-production-v2/tools && sed 's/\r$//' search | bash -s -- 'normalized variable step CMA confidence weighted blind equalization square QAM' --mode academic --preset comparison --max-per-source 20 --top 40 -o ../search-archive/2026-07-26/c15-deep-normalized-cost.json"
wsl bash -lc "cd /mnt/d/code/study/research-protocol/.worktrees/rdl-method-production-v2/tools && sed 's/\r$//' search | bash -s -- 'reduced constellation algorithm radius directed equalizer multimodulus canonical' --mode academic --preset comparison --max-per-source 20 --top 40 -o ../search-archive/2026-07-26/c15-deep-lineage.json"
```

命令退出码依次为：

| query | exit |
|---|---:|
| c15-broad-cma-mma | 0 |
| c15-broad-rca-sato | 0 |
| c15-broad-rde-optical | 0 |
| c15-deep-staged-optical | 0 |
| c15-deep-fso-taskfit | 0 |
| c15-deep-normalized-cost | 0 |
| c15-deep-lineage | 0 |

## Step 1 search audit

### Query families and archive paths

| query family | archive | OpenAlex raw | retained | other actual sources |
|---|---|---:|---:|---|
| CMA/MMA broad | `search-archive/2026-07-26/c15-broad-cma-mma.json` | 20 | 20 | 0 |
| RCA/Sato broad | `search-archive/2026-07-26/c15-broad-rca-sato.json` | 20 | 16 | 0 |
| RDE/coherent optical broad | `search-archive/2026-07-26/c15-broad-rde-optical.json` | 20 | 19 | 0 |
| staged optical deep | `search-archive/2026-07-26/c15-deep-staged-optical.json` | 0 | 0 | 0 |
| FSO/task-fit deep | `search-archive/2026-07-26/c15-deep-fso-taskfit.json` | 1 | 1 | 0 |
| normalized/variable-step deep | `search-archive/2026-07-26/c15-deep-normalized-cost.json` | 3 | 0 | 0 |
| RCA/RDE/MMA lineage deep | `search-archive/2026-07-26/c15-deep-lineage.json` | 0 | 0 | 0 |

`top.sources` 是工具计划请求的来源列表，不能当实际覆盖。实际来源以每条结果的
`source_api` 和 stdout 为准：

- OpenAlex：原始返回依次为 `20, 20, 20, 0, 1, 3, 0`；过滤后为
  `20, 16, 19, 0, 1, 0, 0`。
- S2：7 组均发起请求，`--max-per-source 20`，但均因 rate-limit 返回 0。
- SerpAPI：无 API key，返回 0。
- Tavily：前三组启用但无 API key，返回 0；comparison preset 未启用。
- Firecrawl：前三组启用但无 API key，返回 0；comparison preset 未启用。
- Exa：无 API key，返回 0。

### Archive integrity

| archive | SHA-256 |
|---|---|
| `c15-broad-cma-mma.json` | `62045470d3b3be38defd01782cfc5ead83b41df19ea097d3f6d5a0fefaf2dfa4` |
| `c15-broad-rca-sato.json` | `fa001ebcbb1eadd10aebb3d72d6d4a65bfe34cc6c59fee9ae93cb5a7f3c8ae43` |
| `c15-broad-rde-optical.json` | `419919d1f6b7ba7ffe561943d7d283ed0cd4c89a93ca37da87295ba41f75580c` |
| `c15-deep-fso-taskfit.json` | `04c512679f0a5651f52e2f29c6494e40ae8c36dbab0b2e3212b85ba1ca61ba34` |
| `c15-deep-lineage.json` | `38a09717b419b7fb84dcbe78a22012e5488b3343135cc66068dd8c9070a2540d` |
| `c15-deep-normalized-cost.json` | `740860aa6f543844c9b5abe45c3c412cbe6a00dbef64d4515f3375ccda8d3cca` |
| `c15-deep-staged-optical.json` | `27af40b53dd7dd8f6b45103bc7e6743d1cb6c8c6494894652fcbb32cf9636950` |

工具同时自动生成了 7 个
`search-archive/2026-07-27/<query-slug>.json` 和一个孤立的
`search-archive/_index/all-papers.jsonl`。逐项验证表明：

- 7 个自动副本分别与显式 `-o` 文件有相同 query、sources、total、timestamp 和
  results；原始 SHA 不同仅由序列化/换行造成；
- 孤立 index 恰有本轮 53 个唯一结果，不是任务指定的共享主仓索引；
- 这些路径均在本轮命令后新建。

为遵守 T011“不得在 worktree 内另建孤立索引”与只保留确定路径的约束，已删除
上述 8 个精确文件及两个删除后为空的精确目录；未泛删任何目录。搜索导入还改写了
5 个 tracked `.pyc`，已从当前 HEAD 的精确 blob 机械恢复，逐项
`git hash-object == git rev-parse HEAD:<path>`。清理后、写本日志前
`git status --short --untracked-files=all` 为空。

### Deduplicated coverage statistics

- archive retained rows: `56`
- DOI 优先、否则 normalized title 去重后：`53`
- 重复唯一项：`3`
- actual sources: `1`（OpenAlex）
- publication status: `published=49`, `preprint=3`, `unknown=1`
- published ratio: `49/53 = 92.5%`
- metadata 可见机制路线：
  - CMA/MCMA/MMA/dual-mode/variable-step blind-equalization cost/update；
  - RDE / coherent-optical high-order QAM；
  - staged MMA→decision-directed；
- direct coherent-FSO/turbulence task-fit route：`0` 个有效命中；
- canonical Sato 1975、Godard 1980、Yang/Werner/Dumont 2002 的精确 canonical
  记录：本轮定向检索未闭合。

数量与 published ratio 只是诊断信息；由于实际来源仅 1，不能宣布 Step 1 PASS。

### Candidate table

下表是阻断前基于 title + abstract + venue + year + citations +
publication_status 的**诊断 shortlist**，不是可下载 acquisition pool；priority
未回写 archive。

| id / archive | title | year/venue | DOI/arXiv | source | route | provisional priority | reason |
|---|---|---|---|---|---|---|---|
| L003 / broad-cma-mma | New algorithms for blind equalization and blind source separation/phase recovery | 2002 / UPenn Scholarly Commons | 无 | OpenAlex | RCA/CMA/MMA/SCA lineage | 必读候选 | abstract 明示讨论 RCA/CMA/MMA 关系，但 venue/版本/正式论文身份未闭合 |
| L005 / broad-cma-mma | A regional multimodulus algorithm for blind equalization of QAM signals: Introduction and steady-state analysis | 2012 / Signal Processing | 10.1016/j.sigpro.2012.04.010 | OpenAlex | regional MMA | 必读候选 | 直接命中 QAM blind-equalization cost；abstract 缺失，必须全文核验 |
| L011 / broad-rde-optical | Modified radius directed equaliser for high order QAM | 2015 / ECOC | 10.1109/ecoc.2015.7341620 | OpenAlex | RDE / dynamic coherent QAM | 必读候选 | abstract 报告 DP-64/256QAM 动态信道；是 RDE comparator 候选 |
| L014 / broad-cma-mma | Optimized blind equalization for probabilistically shaped high-order QAM signals | 2022 / Chinese Optics Letters | 10.3788/col202220.080601 | OpenAlex | coherent-optical radius tracking | 必读候选 | 近年 coherent optical、明确指出传统 blind equalization 对半径/分布敏感 |
| L002 / broad-rca-sato | High-Order-QAM Source Equalization for Cognitive Communication Systems | 2024 / IEEE TCCN | 10.1109/tccn.2024.3522574 | OpenAlex | MMA→soft-DD staged | 必读候选 | 近年正式 staged-chain 方法，但不是 optical/FSO |
| L001 / broad-cma-mma | Robust Blind Equalization for NB-IoT Driven by QAM Signals | 2024 / IEEE IoT-J | 10.1109/jiot.2024.3374553 | OpenAlex | MCMA/GMCMA | 建议读候选 | 正式、近年、高阶 QAM cost 问题直接；场景为 NB-IoT |
| L004 / broad-cma-mma | A Novel Dual Mode Decision Directed Multimodulus Algorithm | 2021 / FAIA | 10.3233/faia210430 | OpenAlex | MMA→DD switch | 建议读候选 | 16-QAM staged switching；venue 与 task-fit 需核验 |
| L009 / broad-cma-mma | New Variable Step-Size Blind Equalization Based on Modified CMA | 2012 / IJMLC | 10.7763/ijmlc.2012.v2.85 | OpenAlex | variable-step MCMA | 建议读候选 | 直接命中 normalized/step-size mechanism，但非 optical |
| L012 / broad-cma-mma | New hybrid adaptive blind equalization algorithms for QAM signals | 2009 / ICASSP | 10.1109/icassp.2009.4960207 | OpenAlex | CMA + penalty hybrid | 建议读候选 | cost hybrid lineage 候选 |
| L013 / broad-cma-mma | A Simplified CMA for Blind Recovery of MIMO QAM and PSK Signals | 2007 / EURASIP JWCN | 10.1155/2007/90401 | OpenAlex | simplified CMA | 建议读候选 | MIMO QAM cost/complexity comparator 候选 |
| L017 / broad-cma-mma | An Analytical Multimodulus Algorithm for Blind Demodulation in a Time-Varying MIMO Channel Context | 2010 / IJDMB | 10.1155/2010/307927 | OpenAlex | analytical MMA / dynamics | 建议读候选 | 动态 MIMO route，但非 optical |

### Directional deep-search results

两个预设子方向及其至少两组检索本应为：

1. coherent-optical comparator/staged chain：
   - `radius directed equalization RDE coherent optical PM-16QAM`：19 retained；
   - `CMA RDE MMA staged blind equalization coherent optical 16QAM`：0 retained；
   - `reduced constellation algorithm radius directed equalizer multimodulus canonical`：
     0 retained。
2. dynamic/normalized/FSO task fit：
   - `free space optical turbulence adaptive blind equalization CMA RDE`：1 retained，
     但为泛 ML/DL optical survey；
   - `normalized variable step CMA confidence weighted blind equalization square QAM`：
     0 retained；
   - CMA/MMA broad 中仅有若干非 optical variable-step/dynamic MIMO 条目。

因此不能在 metadata 层确认“创新空白不是初始漏召”。当前的 0/1 命中既可能表示
真实 task-fit 缺口，也可能只是单源覆盖不足；在三源门未过时不能选择其中一种解释。

### Excluded false positives

以下是明确不能进入后续 acquisition pool 的代表性假阳性/任务错配：

| title | exclusion reason |
|---|---|
| A Survey on Machine and Deep Learning for Optical Communications | 泛 ML/DL optical survey；abstract 未涉及 FSO turbulence 下 CMA/RDE 盲均衡失效 |
| White Paper on Broadband Connectivity in 6G | 宽带白皮书，不是 blind-equalization cost 或 comparator |
| Optimized LMS algorithm for system identification and noise cancellation | 系统辨识/噪声消除，非本任务盲均衡 |
| Low-Complexity Frequency Offset Estimation for Probabilistically Shaped MQAM Coherent Optical Systems | FOE，不是 blind equalization cost/update |
| A Chromatic Dispersion-Tolerant Frequency Offset Estimation Algorithm Based on Pilot Tone | pilot FOE，不是 C15 comparator |
| Turbo Equalization Techniques Toward Robust PDM 16-QAM Optical Fiber Transmission | turbo equalization，未由 metadata 证明为 CMA/MMA/RDE blind cost lineage |
| Scaling capacity of fiber-optic transmission systems via silicon photonics | 系统容量综述/器件方向，不是算法血缘 |
| Electro-Optical Modulator Requirements for 1 Tb/s per Channel Coherent Systems | 调制器需求，不是盲均衡算法 |

## Terminology and lineage questions

| claim | evidence status | source pointer | unresolved debt |
|---|---|---|---|
| Sato 1975 “reduced constellation” 的精确 cost/update | UNRESOLVED | `c15-broad-rca-sato.json` 与 `c15-deep-lineage.json` 均未命中 canonical record | 需要多源召回与全文 |
| Godard 1980 CMA 的 canonical identity | UNRESOLVED | 7 个 archive 未命中精确 canonical record | 需要 canonical DOI/title/fulltext |
| RCA、CMA 与 MMA 的关系 | ABSTRACT_CANDIDATE_ONLY | `c15-broad-cma-mma.json#results[L003]` | 2002 条目身份/版本未闭合，不能据 abstract 写公式或血缘 |
| regional MMA / dual-mode MMA / staged DD 的差异 | ABSTRACT_CANDIDATES_ONLY | L005/L004/L002（见候选表） | 需全文提取 cost、update、switch gate |
| RDE 在 coherent high-order QAM 的传统 comparator 身份 | ABSTRACT_CANDIDATE_ONLY | `c15-broad-rde-optical.json#results[L011]` | 需 canonical + representative fulltexts |
| FSO turbulence/dynamic polarization 下的 M-C-A 失效 | NO_DIRECT_METADATA_SUPPORT | `c15-deep-fso-taskfit.json` 唯一结果为泛 survey | 单源 0 命中不能证明“不存在” |

## Step 2 acquisition audit

| title | id | download route | content path | effective lines | title/DOI check | status |
|---|---|---|---|---:|---|---|
| 无 | 无 | 未运行 | 无 | 0 | 未运行 | NOT_STARTED_DUE_TO_STEP1_HARD_GATE |

- 未创建 `search-archive/2026-07-26/c15-step1-acquisition-pool.json`。
- 未执行 `tools/download`、arXiv/author-version 二轮、IEEE/blit 三轮或
  `tools/convert`。
- 未读取任何 `content.md`。

## Coverage gap report

### 成功获取

无。Step 2 未启动。

### 内容质量不达标

无。没有全文质量检查。

### 下载失败

无。没有发起下载。

### 覆盖面分析

- 候选数量和工具标注的正式发表占比达到了数量诊断门；
- actual source coverage 只有 1/3；
- canonical lineage、coherent staged chain、normalized/confidence-weighted route
  的定向搜索均未闭合；
- 没有直接 coherent-FSO/turbulence blind-equalization task-fit metadata；
- 因检索管道缺失而非科学事实，不能将这些缺口解释为文献空白或方法机会。

### 引用质量分析

- 全部保留结果来自 OpenAlex，缺少独立来源交叉验证；
- 部分条目 venue/abstract 缺失，2002 lineage 条目没有 DOI；
- OpenAlex 的 `publication_status` 只能用于筛选，不能替代全文版本核验；
- 本包没有 canonical fulltext，因此不能支撑公式、cost identity、传统 comparator
  或 M-C-A。

### 用户行动项

无技术行动项。executor 不要求用户配置 key、寻找全文或判断候选正确性。主控应在
合法替代项之间判断：进行一次有明确三源恢复证据的 bounded Step 1 retry，或把
C15 记为 local search-coverage blocker 后轮换；两者都不能把本结果算 method
delta。

## Candidate-specific baseline map

| possible claim | shared anchor | task comparator | canonical source | representative uses | task-fit status |
|---|---|---|---|---|---|
| staged/normalized cost 改善高阶 QAM 收敛/稳态误差 | 2×2 high-order-QAM blind equalizer | CMA/MMA/RDE 或 staged chain（待全文裁定） | MISSING | TCCN 2024 staged、COL 2022 PS-QAM、ECOC 2015 RDE（均仅 metadata/abstract） | coherent optical 有候选；FSO 未闭合 |
| 降复杂度且保持 blind recovery | 同一 QAM/MIMO equalizer | canonical CMA | MISSING | EURASIP 2007 simplified CMA（仅 abstract） | 非 optical；迁移合法性未知 |
| dynamic channel 下改进 tracking | time-varying 2×2 channel | conventional CMA/MMA/RDE | MISSING | ECOC 2015 RDE、2010 analytical MMA（仅 abstract） | dynamics 有候选；星地湍流/偏振未闭合 |

## Integrity boundaries

1. C15 全程按 blind equalization cost/update family 处理，未误称 CPR。
2. 未运行仿真、测试矩阵、seed、MVE 或旧 C15 sandbox。
3. 未修改旧 C15 Scout、`.sessions/**`、control、formal owner、mission-log、
   master-state 或 current projections。
4. 未将 title/abstract/search metadata 当全文或 scientific verdict。
5. 未访问 ResearchGate、私有全文或网页抓取。
6. 未创建 acquisition pool，未运行 Step 2。
7. `formal_science_disposition=BLOCKED_SEARCH_COVERAGE` 与
   `mission_method_delta=NONE` 分开记录。

## Next gate

Step 1 因实际来源不足与定向检索空洞被阻断；未到 coverage confirmation，未进入
Step 2，更未进入 Step 3。下一动作由主控基于磁盘证据决定 bounded source-recovery
retry 或轮换，本 executor 不改 control。
