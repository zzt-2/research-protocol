# Handoff: Ch4 reference-method 入口选择

> 来源: S001 | 交接目标: 在下一对话比较最多 3 个 research object / reference baseline，选出至多 1 个正式入口
> 日期: 2026-08-08

---

## 已完成边界

旧 RDL system 专题已停止继续膨胀并转 dormant。新专题已冻结 reference-method extension 合同：Ch4 必须从可复现 baseline、observed defect、one deployable action 与 fair comparator 出发；P1、decoder-feedback 基建和 supporting 反复包装均不在当前入口。

## 不要做什么

- 每轮先回答 topic-index 的防偏三问；答案不支持方法产出时立即停止行政扩展。
- 廉价替代进入 comparator，不凭想象预杀；exact existing-action collision 才可在入口期拒绝。
- 基础设施工作量只作投资预算；3–7 天预算只给入口门通过的单一胜者。
- `SUPPORTING_ONLY` / `REJECT` 不能关闭 Ch4，也不能触发同资产再包装。
- 下一轮只选入口，不越级进入 GW、实现或仿真。

## 必读

1. `.sessions/2026-08-08-ch4-reference-method-extension/topic-index.md`
2. `.sessions/2026-08-08-ch4-reference-method-extension/decisions.md` 的 D001
3. `.agents/skills/research-direction-lab/references/method-production.md` 的 `Reference-method extension lane`

## 接口变更（如有代码改动）

无代码改动。

## 失败数据附录（如涉及路线失败）

无；旧路线的失败数据继续由 dormant RDL system 专题持有，本 handoff 不复制。

## 已知债务（如原则与现实有差距）

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|---|---|---|---|
| 具体 reference baseline 尚未选择 | 只给单一胜者投入重资源 | PENDING | 下一对话完成最多 3 个对象的入口比较 |

## 验证阈值（如涉及验证体系）

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|---|---|---|---|
| 入口选择 | 至多 3 个对象、推荐至多 1 个，且不启动检索/实现/仿真 | D001 | 首次执行，暂无 |

---

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落
- [ ] 已验证本文件中的至少 3 条关键事实声称
  - 声称1: 旧 RDL system 专题已 dormant → [PASS/FAIL + registry 证据]
  - 声称2: 新专题当前只授权入口选择 → [PASS/FAIL + topic-index/D001 证据]
  - 声称3: P1 与 decoder-feedback 不在当前入口 → [PASS/FAIL + topic-index 明确不含证据]
- [ ] 已检查 _registry.yaml 中本专题的 depends_on 和 conflicts_with
- [ ] 已确认当前范围未违反“明确不含”

## 下一轮

先完成上述接收方验证，再利用已有论文、代码和历史 inventory 比较最多 3 个 research object / reference baseline。只形成入口收据与至多 1 个推荐对象；本轮不直接检索、实现或仿真。
