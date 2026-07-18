# [S063] Pilot Jones derotation 扩展验证预注册

> 2026-07-16 | E 族扩展验证 | 状态：运行中

## 目标

验证 S062 的正信号是否跨 seed、SOP rate 和 pilot 开销稳定，决定是否形成正式晋级候选。

## 记录

预注册网格：N=100k；seeds41–48；SOP rates=`4e-6/8e-6/1e-5`；pilot counts=`2/4/6`（3.125%/6.25%/9.375%）。每 cell 保留 baseline/naive/derotation 三臂、same-realization fingerprint、shared data mask、source/config SHA。

判据：failure cells derotation 相对 baseline fixed BER 改善≥50%；clean cells不退化；overhead≤10%；至少一个 pilot-count 在新 seeds/rates 稳定。若主网格耗时，先保存 4-pilot 主臂 checkpoint，再补2/6敏感性，不允许丢过程。

## 决策引用

- D052：短集成 feasible，准入扩展验证。

## 范围确认

- 本轮是否在 scope boundary 内：是。

## 后续

结果完成后独立审查；满足门槛才立正式晋级候选，否则回候选地图换族。
