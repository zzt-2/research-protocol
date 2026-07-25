# [S082] Pilot-Jones T005 接收与局部路线收口

> 2026-07-25 | GW Step 4a 接收验收 | 状态：SCOPED_AXIS_KILLED

## 目标

独立接收 T005，区分科学裁决与证据完整性，并决定是否继续投资 Pilot-Jones。

## 记录

T005 commit `8f7dd0d323c8c35c47842ed34e6f68e9d4e9d4b3` 的边界正确：
只新增 temporal-adjudication source/result/test/worker-log，protected/formal/shared
文件未改。120 validation + 120 test raw rows可逐行重算，8 个 primary cells 的
impairment-added headroom 最大 point `0.0804126817 dB`、最大 CI upper
`0.2371961896 dB`，全部低于 0.5 dB。12 个 B* 选择均可由 raw 重算，8 个 source SHA
与 contract SHA 均匹配，跨 `PYTHONHASHSEED=1/999` fingerprint 一致。

发现两项完整性缺口：

1. contract 预注册 M3 noiseless recovery `1e-10`，实现/测试却把带 MMSE 正则的
   `reference_m3` 以 `<1e-4` 判 PASS，实际误差约 `1e-6`；
2. Windows 默认 GBK 下 3 tests 因未显式 UTF-8 失败；`PYTHONUTF8=1` 下 17/17 PASS。

主控另用 `H(f)^H` 真精确逆重算所有 40 个 M3 test realizations：`H^H H-I` 最大残差
`1.4433e-15`，无噪恢复误差 `1.1310e-15`，与 stored MMSE reference 的 BER
40/40 一致。因此完整性仍为 PARTIAL，但科学裁决不受影响。

## 决策引用

- D066：接收局部 component rescue axis Kill，Pilot-Jones 退出当前 carrier（新建）

## 范围确认

- 本轮是否在 scope boundary 内：是。只裁决 T005 与当前 Step 4a 路线，不关闭
  4 篇全文债覆盖的整个 family，不进入 Step 5。

## 后续

不再修 Pilot-Jones 或寻找其新方法。保留局部负面、semantic-smoke 与 exact-inverse
审计材料；前台 carrier 转到 step4a-mve-execution 的 B10/B12 高阶 CPR 组合方法。
