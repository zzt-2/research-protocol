# Verifications — Ch4 参考方法扩展

## V001: 防偏合同与 Skill 最小补丁独立验收

> date: 2026-08-08
> 关联：S001 / D001 / 旧专题 D041
> 结论：PASS

### 验证范围

Fresh-context verifier 独立检查 12 项：Skill 最小补丁、supporting leftovers 禁止重包装、cheap alternative 比较纪律、基础设施预算门、每对象两包与两对象停机条件、旧专题 dormant 且无 S020、新专题治理结构、H001 恢复边界、registry 血缘、p05 日志隔离、Skill repo/user 同步及 `git diff --check`。

### 结果

- 12/12 PASS；P0/P1/P2 = 0/0/0。
- Skill 完整回归：`116 passed, 1 skipped`。
- repo/user Skill：104/104 个非缓存文件 SHA256 byte-identical。
- 旧 system 专题 S### 数量保持 19；不存在 S020。
- registry YAML 可解析；旧专题 `dormant`、新专题 `active`，依赖 slug 均存在。
- 下一轮被限制为最多 3 个对象、至多 1 个推荐，不检索、不进入 GW、不实现、不仿真。
- 四个既有 `p05_run*.log` 未跟踪、未暂存、未进入 diff；因其从未受 Git 跟踪，Git 只能直接证明本补丁未纳入它们。
- `git diff --check` exit 0；仅有 Windows 行尾提示。

### 裁决

防偏合同、恢复入口与 Skill 三条通用规则可以进入使用；无修复项。
