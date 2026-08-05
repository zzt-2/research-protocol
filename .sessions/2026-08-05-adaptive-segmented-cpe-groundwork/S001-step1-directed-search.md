# [S001] C3 Step 1 定向检索

> 2026-08-06 | Groundwork Step 1 | closed

## 目标

在最多 4 组新增 query 内，关闭近期 task-matched fixed-granularity baseline、直接 adaptive-segmentation
竞品、物理前提与四判据问题门；只有 Q# 存活才允许进入 Step 2。

## 记录

### 启动恢复

- P1 已由 D005/V005/H003 关闭：`RECENT_BASELINE_UNAVAILABLE / SUPPORTING_ONLY`；禁止改名重开。
- registry 查重未发现同方向 active/dormant C3 专题，故按用户指定路径建立本专题。
- 历史动作碰撞：`D-011` 与 inventory `a1_adaptive_segmented_cpe` 已测试同一
  `current-window proxy → choose K → segmented NDA CPE` 动作。旧结果为 adaptive-J4 退化 always-K16、
  gain=0.000 dB、0/8 显著胜；主流 10–80 kHz 物理区间内增量不成立。该证据作为本轮 Step 1
  `PHYSICAL_PREMISE_UNSUPPORTED` 的前置反证，不作 Step 4a 复跑授权。

### 检索执行

已完成 4/4 组新增 query。raw=187、组内 dedup=179、final=151、跨组 dedup=140；逐条 AI 标注见
四个 `search-archive/2026-08-06/c3-q*.json`，综合见 R001。

### Step 1 terminal

`PHYSICAL_PREMISE_UNSUPPORTED`。近期合法 fixed-window baseline 存在，外部同信息同动作竞品未发现；
但新增文献没有满足历史 D-011/inventory 的 reopen condition。无四判据全 PASS Q#，Step 2 未授权。

## 决策引用

- D001：本专题只做 bounded Step 1；Step 2 条件式；历史同动作否决继续有效（新建）。
- D002：C3 在 Step 1 触发 `PHYSICAL_PREMISE_UNSUPPORTED`，关闭并返回上游轮换（新建）。

## 范围确认

- 本轮是否在 scope boundary 内：是。

## 后续

返回上游 RDL，选择机制不同且具备近期合法 baseline 的新候选；不在本专题改名重开 C3。
