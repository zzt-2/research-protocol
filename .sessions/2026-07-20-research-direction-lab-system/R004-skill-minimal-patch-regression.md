# [R004] Research Direction Lab Skill 最小 patch 与历史回归

> 2026-08-02 | 关联：D020 / H003

## 调研问题

真实长程 campaign 收口后，现有 Skill 是否需要且仅需要补强 executable semantic gates、contribution tiers 与 lightweight persistence；这些补强能否通过修改前后的同源六案例盲测证明，而不改科学裁决或引入第四类机制。

## 发现

1. 接收 H003 后核验：longitudinal campaign 已 dormant；accepted valid=7；`METHOD_SIGNAL=0`；P11 runner 标签为 9/11/13/15 dB，但 generator 实际使用固定 20 dB；registry 无 scope 冲突。
2. 修改前 canonical Skill 共 60 个非缓存文件，权威 RED baseline 固定为 Git object `53085bb5d1b7cc3e759e62af5c55397979402acc`，按 `baseline-manifest.md` 算法可复算 bundle SHA256 `fbd44ac762114e54f2f6fae90226487ff0748a43c1fa6e8ba57ff9b521274a87`。早期 ad-hoc capture `91f306ef72b54dc883b52a9683629b4dff54a0f6ce985d22bd34c33e3822f1ab` 未记录序列化算法，只保留为历史记录，不作审计身份。六组 fresh-context RED 中，Case 1 真实失败：旧 Skill 在缺 caller action trace、scale decomposition 和 invariant downstream evaluation 时仍使用“机制信号很强”“实现边界基本合理”等表述；Case 2–6 已能发现各自历史问题，因此是防回归基线，不伪造为失败。
3. 最小实现只修改现有 evidence/method/harvest/long-horizon owner、既有 receipt validator 及测试：五门 executable contract fail-close；三层贡献合同与 B 级工程入口；topic-index/mission-log/detail 三层持久化；receipt hash/chronology/seed ledger fail-close。
4. GREEN 六案均阻止错误晋级或 campaign closure；Case 6 同时保留真实 B 级工程组件入口且不制造 P12。Case 1 首轮 GREEN 暴露 scale/normalization 分解表达不足，经一次 RED→GREEN refactor 后，明确要求 invariant downstream evaluation 与 evaluator-sensitivity decomposition；未继续堆规则。
5. 行为原始输出与逐案对照保存在 `.agents/skills/research-direction-lab/tests/forward/runs/historical-minimal-patch/`。未启动 AMC、未运行科学仿真、未修改 P07–P11/G1 科学资产、formal owner 或其他 Skill。

## 结论

三类 patch 均有历史根因或真实 RED 证据，且可在不扩 controller、不改 `SKILL.md` 触发描述、不写入项目专属状态的前提下闭合。旧 Skill 并非六案全败；本轮证据是“一项真实新增失效 + 五项历史防回归”，应如实保留。

## 对决策的影响

支持 D020 采用且只采用三类最小 patch；V014 负责记录自动化、fresh-context、独立 verifier 与 canonical/runtime 同步的最终证据。
