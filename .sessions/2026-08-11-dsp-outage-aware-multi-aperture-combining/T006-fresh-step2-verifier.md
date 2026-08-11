# T006：fresh-context Step 2 verifier

> 2026-08-11 | 独立只读验证 | 上限 15 分钟

## 目标

独立核查 GW Step 2 acquisition 的 identity/hash/lines/coverage/terminal/scope；不得依赖执行者口头结论。

## 必读

- `stages/gw-acquire.md`
- `.sessions/2026-08-11-dsp-outage-aware-multi-aperture-combining/topic-index.md`
- `.sessions/2026-08-11-dsp-outage-aware-multi-aperture-combining/decisions.md` D002
- `.sessions/2026-08-11-dsp-outage-aware-multi-aperture-combining/R002-step2-acquisition-coverage.md`
- `.sessions/2026-08-11-dsp-outage-aware-multi-aperture-combining/R003-step2-acquisition-receipt.md`
- `projects/thesis-fso/master-state.md` 顶部 control bridge/GW table

## 独立检查

1. 对四篇 claimed qualified fulltext 重新计算 source/content SHA-256、bytes、总行/非空有效行；核标题/DOI/反爬文本/U+FFFD 是否支持 qualified。
2. 对五篇 claimed unavailable 检查 canonical/worktree/shared-root/downloads/manual；参考文献命中、abstract、read-note 不算全文。
3. 复算 targeted qualified=`4/9`、optical CORE=`2/5`；ICCC 与 JPHOT 2020 不得替代 optical CORE。
4. P0 必须仍是 fulltext unavailable；如发现可验证 source/content，立即 P0 报错并停止接受 terminal。
5. 检查 R002/R003/topic-index/master-state/registry 在 terminal 与 Step3=`NOT_AUTHORIZED` 上一致。
6. 扫描本轮 diff：不得出现完整 input-trigger-action-output、collision verdict、Q#、Go/Kill、METHOD_SIGNAL、实现/仿真/b3 repair。
7. 检查 git staging 为空，且 unrelated dirty files/p05/coded artifacts 未被本轮改写或纳入范围。

## 输出

只返回：

- verdict=`PASS` 或 `FAIL`
- P0/P1/P2 blocker counts
- identity/hash/lines/coverage 核验摘要
- scope/terminal 核验摘要
- 若 FAIL，列精确 file:line 与最小修复建议

不得修改文件、下载、转换、精读方法或进入 Step 3。
