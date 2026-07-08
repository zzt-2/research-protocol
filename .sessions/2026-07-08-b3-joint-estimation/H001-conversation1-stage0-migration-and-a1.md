# Handoff: 对话 1 — 阶段 0.1-0.6 前置规约（4 支路迁移验证 + A1 归属 + 架构 + 公平对照 + 参数 + 文件）

> 来源: S001 | 交接目标: 新工作对话执行阶段 0.1-0.6
> 日期: 2026-07-08

## 到哪了（状态）

主控对话开题完成（D001），阶段 0 六项规约设计完成。**未写代码，未进 sandbox**。

**关键风险（工作对话首验证）**：
- B3-Q2 +2~3dB 是 4 支路 MRC 强湍下的，**单支路只有 ~1dB**
- **星地单孔径终端难以堆叠多望远镜**（jphot 笔记 L56）
- "星地多孔径阵列接收"是 S031 假设，**未验证**

→ **阶段 0.1 = 验证星地多孔径阵列是否真实工程场景 + FR-21 单链路 CRB 上界前置**。

## 不要做什么

1. **不要跳过 4 支路迁移验证直接跑 MVE**：星地单孔径难堆叠多望远镜，单链路 dB 砍半，直接跑可能在错误场景下测
2. **不要跳阶段 0 直接写代码**
3. **不要走环路 TF 联合建模**：前馈开环不撞 D006，环路 TF 撞转 B3-Q3
4. **不要忽视 A1 归属**：jphot+oe BUPT 课题组已完成 FS+FOE+MRC 联合，B3-Q2 增量要查清
5. **不要自建信道**：从 common/_channel.py 导入，多支路扩展在 explore 做
6. **不要污染 common**

## 必读（按优先级）

1. **本 H001 + topic-index**（15 不变量，重点 11/12/13/14/15 B3-Q2 特殊）
2. **S001** 开题 + 复用基建盘点
3. **B3-Q2 详评**：
   - `papers/_read_notes/_B3-subsystem-coordination-increment.md` L32,74-76,77,85（M-C-A + A1 + D006 边界）
   - `papers/_read_notes/10.1109_jphot.2023.3265847.md` L17,56（4 支路场景 + 星地迁移风险）
   - `papers/_read_notes/10.1364_oe.520452.md` L16,51（BUPT 课题组姊妹工作）
   - `.sessions/2026-07-05-carrier-sync-v2-cut-pattern/_cut-b1b2b3-verify.md` L258-291（dB 出处核验）
   - `.sessions/2026-07-05-carrier-sync-v2-cut-pattern/_cut-map-final.md` L25,41,55（饱和池联合建模）
   - `.sessions/2026-06-20-problem-driven-redirection/S031-step4a-priority-and-go-kill-top5.md` L33-39,161-169,213（Conditional Go + 旋钮 + 不建议先试）
4. **复用基建**：`projects/simulation/common/_recovery.py`（fft_foe/vv_cpr/bps_cpr/da_ml 等单支路估计器）
5. **sim-preflight v1.3.0**：rules/mve-validation.md V1-V6 + rules/interrupt.md 10-12 + SKILL.md §1.6 C6-C8
6. **框架文件**：stages/gw-feasibility.md §D + thesis-lessons TL-13/20/26/27
7. **上游决策链**：`.sessions/2026-06-20-problem-driven-redirection/decisions.md` D005/D006/D017/D018
8. **导师标准**：`.sessions/2026-07-08-b3-joint-estimation/voice.md`（"特长场景"标准）
9. **B2 Kill 教训**：`.sessions/2026-07-08-b2-fade-freeze-pilot-fallback/decisions.md` D004/K001（前馈化测度失效 + 造问题 vs 真实场景）

## 下一步干什么（对话 1 = 阶段 0.1-0.6，不写代码）

### 步骤 1：报到 + 重读关键文件

报到（session-governance Trigger 1）+ 读必读清单 1-9。

### 步骤 2：阶段 0.1 星地多孔径阵列场景验证 + 单链路 CRB 上界（B3-Q2 最高优先）

> INVARIANT 11（B3-Q2 特殊）+ FR-21 oracle 上界前置。

**0.1a 星地多孔径阵列场景验证**（派子 agent，≤15 分钟）：
- 查文献：星地多孔径阵列接收（AO 校正后分集）是否真实工程场景？有没有论文做过？
- 查 jphot 笔记 L56 "星地单孔径终端难以堆叠多望远镜"的具体语境——是绝对不行还是工程挑战？
- 查 sat.1553 综述是否提星地分集接收
- 查 AO（自适应光学）校正后多孔径分集的工程可行性

**0.1b FR-21 单链路 CRB 上界前置**（派子 agent，≤15 分钟）：
- 算单链路（无分集）强湍下联合估计 vs 分立管线的 CRB 下界
- <0.5dB 直接砍（FR-21 降级为参考但 B3-Q2 单链路 dB 砍半后可能不够格，这个前置门控保留）
- 如果单链路 CRB ≥0.5dB，B3-Q2 单链路场景仍可考虑

**判定门控**：
- 星地多孔径阵列是真实工程场景 + 单链路 CRB ≥0.5dB → B3-Q2 特长场景成立，进 0.2
- 星地多孔径阵列不是真实场景 + 单链路 CRB <0.5dB → **B3-Q2 转 Kill**（特长场景不成立）
- 星地多孔径阵列是真实场景但单链路 CRB <0.5dB → B3-Q2 限定多孔径阵列场景，单链路不测
- 输出 `explore/b3-joint-estimation/_diversity_migration_validation.md`

### 步骤 3：阶段 0.2-0.6（主线定）

**0.2 A1 归属核查**（INVARIANT 12）：
- 查 BUPT 课题组（Liqian Wang 等）是否已发星地分集续作
- 查 B3-Q2 相对 jphot+oe 的增量够 D005 够格吗（纯迁移型可能不够）
- 输出 `explore/b3-joint-estimation/_a1_attribution_audit.md`

**0.3 架构定性**（INVARIANT 13 + D006）：
- 前馈开环（一套 TS 同时估 FS+FOE+CPE）不撞 D006
- 环路 TF 联合建模则撞 D006 转 B3-Q3
- 建议前馈开环
- 输出 `explore/b3-joint-estimation/_architecture_decision.md`

**0.4 公平对照框架**：
- baseline=分立 FOE+CPE+RSOP 管线（每支路独立 DSP）
- fair gain @ HD-FEC 3.8e-3
- 4 支路 vs 单链路双场景（如果 0.1 验证两者都可行）
- 输出 `explore/b3-joint-estimation/_fair_comparison_framework.md`

**0.5 参数真相源前置**：
- 4 支路分集参数：望远镜口径 0.2m / 间距 > 空间相干长度 / Cn²=1e-14（jphot 锚）
- 调制格式（4-QAM / 16-QAM）
- 全标 source + 读原文数值
- 输出 B3Params 草稿

**0.6 文件组织规约**：
- `explore/b3-joint-estimation/` 目录
- MRC 合并器 / 帧同步 / 多支路管线接口定义
- 多望远镜信道扩展接口

## 纪律

1. **profile 第 9 次防线 + INVARIANT 6**：阶段 0 六项规约全做完才进 sandbox
2. **INVARIANT 11 4 支路迁移首验证**（B3-Q2 特殊）：0.1 必须验证星地多孔径阵列 + 单链路 CRB
3. **INVARIANT 12 A1 归属前置**（B3-Q2 特殊）：jphot+oe 已做联合，B3-Q2 增量要查清
4. **INVARIANT 13 D006 边界**（B3-Q2 特殊）：前馈开环不撞，环路 TF 撞转 B3-Q3
5. **INVARIANT 14 代码基建新增**（B3-Q2 特殊）：MRC+帧同步+多支路管线需新建
6. **INVARIANT 15 导师"特长场景"标准**：B3-Q2 特长场景必须真实工程场景
7. **sim-preflight v1.3.0 C6-C8 + V1-V6**
8. **TL-26 参数溯源 + 读原文数值**
9. **TL-13 共用同一信道**

## 接收方验证

- [ ] 已读取 topic-index 15 不变量（重点 11/12/13/14/15 B3-Q2 特殊）
- [ ] 已验证 3 条关键事实声称：
  - [ ] B3-Q2 +2~3dB 是 4 支路 MRC 强湍，单支路 ~1dB（核查 `_cut-b1b2b3-verify.md:258-291`）
  - [ ] 星地单孔径终端难以堆叠多望远镜（核查 jphot 笔记 L56）
  - [ ] jphot+oe BUPT 课题组已完成 FS+FOE+MRC 联合（核查 `_B3-...md:32,76`）
- [ ] 已检查 _registry.yaml 中本专题 depends_on
- [ ] 已确认当前范围未违反"明确不含"

## 下一轮

**对话 2**（阶段 0.1-0.6 完成后）：
- 阶段 1 sandbox（联合估计 vs 分立管线三方对照）
- 多望远镜信道 + MRC 合并器 + 帧同步实现
- sandbox 发现联合估计打不过分立管线 → 红线警报

**对话 3**（sandbox 通过后）：
- 阶段 2 TL-20 理论预期表 + 阶段 3 MVE + consistency
