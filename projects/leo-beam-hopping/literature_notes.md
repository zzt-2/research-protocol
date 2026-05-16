# Literature Notes

## 方向概述
LEO 多波束卫星波束跳变调度——利用 GNN 建模小区间空间干扰图结构，替代 MA-DRL 的独立 agent 假设。

## 检索来源
- 一轮检索: `search-archive/2026-05-16/leo-satellite-spectrum-sharing-*.json`, `satellite-frequency-allocation-*.json`
- 二轮深搜: `search-archive/2026-05-16/leo-satellite-beam-hopping-*.json`, `satellite-beam-hopping-*.json`, `hts-beam-hopping-*.json`, `leo-satellite-time-slot-allocation-*.json`

## 关键发现
- GNN+Beam Hopping: 0/119 完全空白，首创性最强
- MA-DRL 占主导（52%），但 >40 小区时收敛困难（已确认痛点）
- 详见 `.session/direction-scouting/LOG-001-candidates.md`

## 精读笔记
