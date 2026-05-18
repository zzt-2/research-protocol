# 新对话提示词：新研究方向检索

## 任务

为用户的研究寻找**第二个**可行方向。执行 Groundwork Step 1（文献检索 + 方向初筛），产出候选方向列表供用户选择。

## 背景

用户已有一个在研项目（leo-mega-constellation-gnn-routing，GNN size generalization for LEO routing，已进入 Execute 阶段），现在想并行开第二个方向。导师给的总方向是"**LEO 卫星链路**"。

### 已完成的搜索资产（可直接复用）

2026-05-13 已做过大规模卫星通信领域检索（6 组关键词、180+ 候选、5 个子方向），存档在 `search-archive/2026-05-13/` 下。`.session/DIRECTION-CANDIDATES.md` 中有完整的方向分析和排序。

### 已占用/排除的方向

| 方向 | 状态 | 理由 |
|------|------|------|
| GNN-based LEO routing | **已完成**（leo-mega-constellation-gnn-routing，Execute 阶段） | 当前主项目 |
| LEO handover + DRL | **已完成**（leo-ntn-handover-drl） | 50+ 篇，过度饱和 |
| RIS phase shift + DRL | **已完成**（ris-phase-drl） | 当前活跃项目 |
| ISL ACM prediction | **负面结果**（isl-acm-prediction） | ISL 信道太确定性，DL 无优势 |
| Grant-free RA for satellite IoT | **排除** | 5 年 1700+ 篇，红海 |
| HGAT satellite DAG offloading | **已完成**（hgat-satellite-dag-offloading） | 边缘计算卸载 |
| AI-driven beam hopping (方向 2) | **候选**，未深入 | 论文密度中等，与导师方向高关联 |
| NTN-terrestrial integration (方向 3) | **候选**，未深入 | 竞争激烈（200 篇/年），需收窄 |

### 第二个方向的选择标准

1. **与导师"LEO 卫星链路"方向相关**（高优先）
2. **与第一个项目（网络层路由）形成互补**，不是简单重复（如不同协议层、不同技术路线）
3. **仿真负担可控**：纯 Python 可实现，不需要 NS-3/STK 等重型工具
4. **蓝海或有明确空白**：论文密度不过高，有可发表的创新空间
5. **与已有项目不冲突**：不与 leo-gnn-routing / ris-phase-drl / leo-ntn-handover 重叠

## 执行步骤

### Step 0：读框架文件（必须）

1. `stages/groundwork.md` — Step 1 部分
2. `stages/gw-search.md` — 检索操作规范（完整读取）
3. `domain-comms.md` — 通信领域定制
4. `tools-guide.md` §1-2 — 工具使用

### Step 1：评估现有搜索资产

读 `.session/DIRECTION-CANDIDATES.md`，评估：
- 方向 2（beam hopping）和方向 3（NTN）是否仍然可行
- 现有搜索数据的覆盖度是否足够（按 gw-search.md 复用规则检查）
- 是否需要新的搜索角度

### Step 2：补充检索（如需要）

如果现有搜索覆盖不足，或想探索全新子方向，用 `tools/search` 做补充检索。可能的新角度包括（但不限于）：

- LEO 卫星星间链路（ISL）相关的**其他**网络层/链路层问题（路由已做，其他？）
- LEO 星座中的**拓扑优化**（非路由，如 ISL 调度/连接管理）
- LEO 卫星的**功率控制/功率分配**问题
- **卫星边缘计算**（与 hgat 项目不同角度，如联邦学习、任务调度）
- **卫星网络安全**（抗毁/加密/入侵检测）
- **LEO 星座的频谱共享/干扰管理**
- **6G NTN 标准化**中的具体技术问题（3GPP Rel-18/19 相关）

检索存档到 `search-archive/2026-05-15/`。

### Step 3：方向分析和推荐

产出 ≥2 个候选方向的详细分析（格式参考 `.session/DIRECTION-CANDIDATES.md`），每个方向包含：
- 核心问题（1-2 句）
- 与导师方向关联度（高/中/低）
- 论文密度和趋势（蓝海/中等/红海）
- 创新空间（≥2 个具体创新点）
- 最小可发表单元（MVP）
- 代表文献（3-5 篇）
- 与已有项目的关系（互补/重叠/独立）

最终给出推荐排序和理由。

### Step 4：等待用户选择

列出候选方向后，**等待用户确认**选定方向，不要自动进入 Step 2-3（论文获取）。

## 约束

- 检索用 `tools/search`，不用通用 web search
- 工具调用从项目根目录：`cd /mnt/d/code/study/research-protocol && ...`
- 路径合规：检索存 `search-archive/`，不乱建目录
- 子 agent 最多 3 个并发
- 不要重复已有项目的方向
