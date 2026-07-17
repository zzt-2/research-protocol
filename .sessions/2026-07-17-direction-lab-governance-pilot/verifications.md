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
