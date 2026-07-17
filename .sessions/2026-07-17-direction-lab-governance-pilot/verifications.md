# Verification Records — Direction Lab 可遵守性与控制器试运行

## V001: 首版最小控制器 RED/GREEN 与独立复核

> date: 2026-07-17
> 关联：S001

### 验证项

- [x] RED：控制器模块不存在时测试收集失败，补齐包入口后仍因 `controller` 缺失失败。
- [x] GREEN：`python -m pytest projects/simulation/tests/test_direction_lab_controller.py -q` → `9 passed`。
- [x] 行为覆盖：缺 manifest/run_id、未知或 fingerprint 不匹配、BOARD_READY 前 GO/KILL、PARTIAL 晋级、组件变化 STALE、合法 RUN。
- [x] 审计覆盖：合法 RUN 与缺 manifest 拒绝均写入可解析 JSONL；控制器实现统一 `_record` 路径。
- [x] 独立 verifier：复核测试是否触发行为拦截并指出漏测；补测后最终结论 PASS。

### 证据

```text
RED 1: ModuleNotFoundError: No module named 'verify.direction_lab_pilot'
RED 2: ModuleNotFoundError: No module named 'verify.direction_lab_pilot.controller'
GREEN: .........                                                        [100%]
9 passed in 0.30s
manifest PASS
```

独立 verifier 首轮结论为 PARTIAL，具体指出 run_id 缺失、组件 fingerprint 在 RUN 下拒绝及 JSONL 覆盖风险；补测后最终结论为 PASS，确认未见关键行为漏测。

### 结论

PASS

### 后续（FAIL/PARTIAL 时）

无。首轮只覆盖五个硬门，未扩张到其余 schema 或正式研究流程。

## V002: 首轮控制器边界复核

> date: 2026-07-17
> 关联：V001 / S001

### 复核范围

- 独立运行 V001 测试：`9 passed`。
- 查看 HEAD 提交边界：仅包含 pilot 专题文档、manifest、controller 和测试共 7 个文件；未修改 canonical baseline。
- 对未被测试覆盖的动作和字段做黑盒探针。

### 发现

1. `PROMOTE` 缺少 `evidence_status` 时仍可放行；当前实现只拒绝值恰好为 `PARTIAL`，没有拒绝缺失、`NONE` 或未知证据等级。
2. 未知动作名仍可放行；控制器没有动作枚举硬门。
3. `REUSE_RESULT` 的 stale 特殊处理只覆盖 component fingerprint 变化；baseline fingerprint 变化会直接抛错，尚未统一成失效传播记录。
4. 当前测试证明“直接调用控制器时五个门有效”，尚未证明真实运行入口无法绕过控制器，也未覆盖上下文恢复和重复轮次。

### 结论

`PARTIAL`：V001 的单元级硬门 PASS 保留；整体治理 pilot 不得标记为完全 PASS。以上问题进入下一轮，不立即扩展更多 schema。

### 下一步

- 先补动作枚举和证据等级缺失/非法值的 RED 测试；
- 统一 baseline/component 变化的 STALE 处理或明确两者差异；
- 增加一个真实入口 smoke test，证明绕过 controller 的运行会被拦截；
- 再做一次中断恢复和重复违规测试。

## V003: 最小硬门修复与独立复核

> date: 2026-07-17
> 关联：V002 / S001

### 修复内容

- 动作名改为白名单；
- 晋级证据改为显式白名单，缺失或未知值拒绝；
- `sandbox_only` 或缺失 `promotion_allowed=true` 时禁止晋级；
- baseline/component 非 canonical 的正式动作拒绝；历史复用统一返回 `STALE`；
- `execute()` 检查 `blocked/STALE` 后才调用 operation；
- 增加真实 B5 manifest smoke test、双 fingerprint 漂移、非 canonical 复用和审计恢复/重复违规测试。

### 证据

```text
pytest projects/simulation/tests/test_direction_lab_controller.py -q
22 passed in 0.33s
compileall: PASS
git diff --check: PASS（仅 CRLF 提示，无 whitespace error）
```

独立 verifier 复核结论：`PASS`。未发现本轮最小硬门可绕过。

### 结论

PASS（仅针对本轮最小治理边界）。

### 已知债务

manifest 仍由调用方提供，尚无签名或不可变来源绑定。若调用方同时伪造 `sandbox_only=false`、`promotion_allowed=true`、FULL 和匹配 fingerprints，理论上仍可走 PROMOTE。该问题留到正式 registry/manifest schema 阶段，不扩大本轮 pilot。
