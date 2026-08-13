# Task Brief: 工程、复杂度与硬件资产全量普查

> 来源: S021 | 产出位置: 仅回传主线程，不写文件
> 日期: 2026-08-13
> 唯一文档: 本任务书 + 仓库只读文件/可读 git 历史

## 0. TL;DR（执行方先读）

只读扫描 thesis-fso 中的工程优化、计算共享、条件执行、定点、编码接收、testbed、FPGA/HLS/RTL/架构与部署材料，判断哪些能独立命名或组合成硕士工程方法。禁止运行实验/综合、联网、补 Groundwork、新建方向或修改文件。

## 1. 背景

D031 不要求每个方法都是新科学主算法。调度、校准、计算图替换、共享计算、固定点、资源/时延优化和场景迁移均可成为硕士方法，只要动作真实、baseline 正确、结果/代价可计量。已知更强替代只限制 claim，不自动 Kill。不能把仅有框图、接口 smoke 或软件调用减少冒充已有 FPGA/PPA 证据。

## 2. 任务详情

1. 扫描 direction-lab harvest/atlas、worker-logs/results、实现/验证材料、FPGA 专题与必要 git 历史。
2. 重点但不限于 select-before-execute、P1-M0、P10、fixed-point/Q、coded receiver、shared architecture、FPGA/testbed。
3. 每项返回：真实输入—动作—输出；软件/硬件身份；已有数字与 baseline；最窄可写命题；独立成章所需身份是否已经存在（不是要求补实验）；D031 身份。
4. 同时寻找此前未进入 P 系列编号、但已有实现和计量证据的工程资产。

## 3. 已知陷阱

- 软件 caller reduction 不等于 FPGA 资源节省；无 RTL/HLS/PPA 时必须明确 ceiling。
- 纯接口、verifier、bit-exact consistency、bugfix 不能单独冒充方法，但可与真实动作链组合。
- 不因“不够原创”否决真实工程动作；也不创造尚不存在的硬件问题或结果。
- 时间上限 15 分钟，优先覆盖广度与别名去重。

## 4. 验收与回传格式

回传紧凑 Markdown：覆盖范围；工程资产总表；Top 10 可命名/可组合项；只有支撑价值的组件；明确缺乏实际证据的硬件声称；与 T016/T017 的别名。每项给真实路径，不给执行任务建议。
