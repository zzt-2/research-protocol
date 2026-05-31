# 状态盘点对话提示词

## 背景
需要全面盘点所有活跃项目的真实状态。用户反馈："之前那几个，说实话都不太乐观"。

**特别关注**：不要只看 handoff 里的乐观结论，要实际检查每个项目的最新文件（代码、结果、decision_log），判断真实健康状况。

## 盘点范围

按 `projects-overview.md` 活跃项目逐一检查：

### 1. leo-mega-constellation-gnn-routing
- 状态：Execute 完成 → 论文素材提取
- 检查点：
  - `projects/leo-mega-constellation-gnn-routing/` 下有什么文件？
  - 结果数据是否存在？实验是否真的跑完了？
  - "论文素材提取"进展如何？有没有实际产出？
  - 距离可发表还有多远？

### 2. leo-ntn-handover-drl
- 状态：Execute 完成 → Contract 叙事转向后重新冻结
- 检查点：
  - "Contract 叙事转向"是什么意思？转向后有没有实际冻结？
  - 实验结果是否支撑新的叙事（size generalization）？
  - GNN 仅 +0.8%，top-K 压缩才是决定性——这个结论对论文发表意味着什么？

### 3. hgat-satellite-dag-offloading
- 状态：GW Stage 7 — 仿真器搭建+Baseline复现
- 检查点：
  - MVE 通过了但"奖励权重η_t=0.5导致E_norm占97.9%需试运行验证"
  - 仿真器搭建到什么程度？有没有实际代码？
  - Baseline 复现进展？

### 4. ris-phase-drl
- 状态：GW Step 4a Go → 待 Step 5 Baseline 选定
- 检查点：
  - "最直接竞争者已撤稿"——这个信息是否可靠？有没有验证过？
  - 从 Go 到现在过了多久？有没有推进？
  - 100 维连续动作空间——实际可行性如何？

## 盘点方法

1. 先读 `projects-overview.md` 了解全局
2. 对每个项目：读最新 handoff → 读 decision_log → 读 results/ 目录 → 判断真实状态
3. 给每个项目一个健康评级：🟢 健康 / 🟡 有风险 / 🔴 严重问题
4. 给出总体判断：现有项目能不能凑出学位论文？缺什么？

## 注意事项
- 规范书面中文
- facts-first：先列事实和发现，再补总结
- 不要粉饰——用户明确说"都不太乐观"，要给出诚实评估
- 归档项目不检查，只看活跃的 4 个
