# [S013] Ch3 (leo-congestion-routing) 完整终审

> 2026-05-26 | Phase 5 | 完成
> 对话13，执行 H003 handoff

## 目标

对 leo-congestion-routing 执行与 Ch1/Ch2 同等标准的完整终审（对标 S001-S011），覆盖竞品+方法论+技术+数据+统计+合规。

## 记录

### Phase 1: 竞品 + 方法论 + 跨章叙事（3 子 agent）

**1a 竞品检索验证**
- 空白 1"故障弹性+跨规模泛化"：**仍为空**（TELGEN 有泛化无故障，GNN-ASSSP 有故障无泛化）
- 空白 2"GNN per-flow K-path + LEO 时变"：**仍为空**（所有竞品为 per-path splitting/per-hop/per-edge weight）
- 空白 3"在线 DRL + Walker-Delta 族内泛化"：**部分满足**（DTAR/GRLR 覆盖部分），需收窄为"per-flow K-path + 跨规模"
- TELGEN/DTAR/DeepLaDu 差异化：**PASS**
- GMR/GNN-ASSSP：**PASS（有条件）**——缺 paper-materials 对比表
- **2 篇待获取论文**（DPR/Wang 2026）：中等风险，需 abstract 验证

**1c 方法论精读**
- 合规评分：**7.5/10**
- 故障测试（E08+E12）：**超出标准**（领域最佳）
- Baseline 3 个：领域下限（中位数 4），DTAR/GMR 降级理由充分
- E2E delay 作为主指标：11/17 论文使用，**最高共识度**
- 需补：baseline 论证段落、bootstrap CI（跨章一致性）

**3d 跨章叙事隔离**
- 隔离充分性：**STRONG**
- 贡献机制零重叠：Ch1=无故障+SL，Ch3=故障弹性+DRL
- 方法四维根本不同：学习范式、决策粒度、图模型、PE 机制
- E02 诚实报告（GNN/ECMP=1.018，ECMP 略优）反而强化叙事
- 元分析框架"探索性分化"下互补：简单架构擅长泛化 vs 复杂注意力擅长故障响应

### Phase 2: 技术 + 公式（3 子 agent）

**5a 仿真参数审查**
- 0 CRITICAL, 0 HIGH
- 2 MEDIUM: M/M/1 假设需在 limitations 补充；data-flow.md 封顶值 1e6→100.0
- 4 LOW: 死参数 isl_bandwidth_mhz、极地间隙 >=/> 描述、surge 文档不一致
- 星座参数合理：550km/86.4°/polar gap 70° 均有文献支撑

**5b 公式指标审查**
- 1 CRITICAL: **M/M/1 物理模型声称不准确**——实际是确定性逐流路由，`1/(1-util)` 应定位为拥塞惩罚权重而非物理排队延迟
- 2 HIGH:
  - 节点特征文档 vs 代码不匹配（data-flow.md 列 7 列 vs env.py 实现 7 列但列名/内容不同）
  - ECMP 种子人为划分（单次运行切分），Wilcoxon N=3 无意义
- 3 MEDIUM: Table 1 vs Table 4 数据不一致（E01@8% vs E08@8%）、delay 计算语义、delay 无跨 seed std
- 2 LOW: PathScoringHead 用 node embedding 非 edge embedding、MLU std ddof

**5c 跨章公式一致性**
- **核心发现：S011 的 18 项修正是针对旧 Ch3(hgat)**，当前 Ch3 需重新基线化
- Shannon/FSPL：Ch3 **不使用**（固定容量 10Gbps），与 Ch1/Ch2 物理层模型根本不同
- 轨道倾角：Ch3=86.4° vs Ch1/Ch2=53°，**有意设计**（近极轨产生极地间隙）
- 轨道高度：550km 三章统一
- 符号冲突：Ch3 缺 `06_formulas_symbols.md`，需创建并采用 S011 统一建议

### Phase 3: 数据 + 统计 + 合规（3 子 agent）

**7a 数据溯源**
- Tables 1-8 核心数字与 JSON **全部吻合**（~100 个数据点）
- 1 CRITICAL: **E02 vs E08@0% 数据矛盾**
  - E02 (GNN/ECMP=1.018) vs E08@0% (GNN/ECMP=0.931)——同一条件（0%故障），不同实验轮次
  - 叙事依赖两者得出相反结论："无故障 GNN 约等于 ECMP" vs "0%故障 GNN 优于 ECMP"
- 1 HIGH: E01@8% GNN MLU=1.378 vs E08@8% GNN MLU=1.335——E08 为单 seed 扫描，需说明
- 其余为 MEDIUM/LOW（四舍五入、注释澄清等）

**7f 统计补充**
- stat_tests.py 代码已就绪，**已执行**生成 `stat_tests.json`
- 结果：GNN vs ECMP MLU **不显著** (p=0.26, d=-0.16)；GNN vs MLP **显著** (p<0.001, d=-0.52)
- **E2E delay -20% 是主指标**，MLU 改善有限(4%)但 delay 改善显著
- Wilcoxon N=3 无意义（p=0.25 for all），不应报告

**7e 合规检查**
- **6/8 PASS, 2/8 PARTIAL, 0/8 FAIL**
- vs 旧 Ch3(hgat) S008 基准 2/8 PASS：**显著改善**
- PARTIAL 项：(1) Baseline 数量 3 vs 标准 5-8；(2) 训练详情缺收敛标准+时间不一致
- 强项：统计报告超标、故障测试超标、泛化诚实报告、新颖性论证充分

## 决策引用

- 无新决策。本 session 为只读审查 + stat_tests.json 生成。

## 范围确认

- 本轮在 scope boundary 内：是

## 后续

### P0（写作前必须修复）

| # | 问题 | 修复 | 来源 |
|---|------|------|------|
| 1 | M/M/1 物理模型声称不准确 | 重写为"拥塞惩罚权重"定位 | P2-5b |
| 2 | E02 vs E08@0% 数据矛盾 | 统一数据源或明确说明实验差异 | P3-7a |
| 3 | 节点特征文档 vs 代码不匹配 | 更新 data-flow.md 节点特征表 | P2-5b |
| 4 | data-flow.md 封顶值 1e6→100.0 | 修正 | P2-5a |

### P1（建议补充）

| # | 问题 | 修复 | 来源 |
|---|------|------|------|
| 5 | GMR/GNN-ASSSP 缺对比表 | 补充到 paper-materials | P1-1a |
| 6 | Baseline 公平性声明 | 段落说明共享 PPO 框架 | P3-7e |
| 7 | 训练配置表 | 添加 lr/batch/clip/gamma/lambda 表 | P3-7e |
| 8 | GNN vs ECMP MLU 不显著 | 论文中如实报告，强调 delay 指标 | P3-7f |
| 9 | Wilcoxon N=3 无意义 | 不报告或标注局限性 | P2-5b |
| 10 | 创建 06_formulas_symbols.md | 采用 S011 统一符号 | P2-5c |
| 11 | 2 篇待获取论文 DPR/Wang 2026 | 至少获取 abstract 验证 | P1-1a |

### P2（可选增强）

| # | 问题 | 来源 |
|---|------|------|
| 12 | Ch3 章间过渡句（S004 建议） | P1-3d |
| 13 | 绪论 Ch1/Ch3 分工表 | P1-3d |
| 14 | M/M/1 limitations 承认（非泊松到达） | P1-1c |
| 15 | E10/E11 消融单 seed 脚注 | P1-1c |
| 16 | Ch1 断链性质说明（确定性 vs 随机故障） | P1-3d |
| 17 | 跨章星座参数比较表（86.4° vs 53°） | P2-5c |

### 写作阶段待做

- 图表生成（Fig 1-7，paper-materials §6 已规划）
- stat_tests 结果整合到 Table 1
- Delay 跨 seed std 报告
