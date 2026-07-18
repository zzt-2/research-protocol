#!/usr/bin/env python3
"""Fix bold patterns and --- setext heading issues in kaiti-report.md."""
import re

with open('毕设/开题报告/kaiti-report.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove standalone --- separators (they cause setext headings or ugly HRs)
#    Replace with blank line. Match: blank? + --- + blank?
content = re.sub(r'\n*^---$\n*', '\n\n', content, flags=re.MULTILINE)

# 2. Numbered sub-headings (bold → numbered)
numbered = [
    ('**前馈方法失效机制分析。**', '（1）前馈方法失效机制分析。'),
    ('**反馈方法失效机制分析。**', '（2）反馈方法失效机制分析。'),
    ('**前馈与反馈方法的本质差异。**', '（3）前馈与反馈方法的本质差异。'),
    ('**关键参数敏感性分析。**', '（4）关键参数敏感性分析。'),
    ('**方向一：同步方法分析与设计准则（拟研究）。**', '（1）同步方法分析与设计准则（拟研究）。'),
    ('**方向二：参数设计方法（拟研究）。**', '（2）参数设计方法（拟研究）。'),
    ('**方向三：跨模块联合处理方法探索（拟探索）。**', '（3）跨模块联合处理方法探索（拟探索）。'),
    ('**理论可行性。**', '（1）理论可行性。'),
    ('**方法与数据可行性。**', '（2）方法与数据可行性。'),
    ('**初步验证结果。**', '（3）初步验证结果。'),
    ('**风险分析与应对。**', '（4）风险分析与应对。'),
    ('**实验一：信道估计方法性能对比**', '（1）实验一：信道估计方法性能对比'),
    ('**实验二：估计误差对载波同步的级联影响**', '（2）实验二：估计误差对载波同步的级联影响'),
    ('**实验三：调制格式灵敏度对比（拟开展）**', '（3）实验三：调制格式灵敏度对比（拟开展）'),
    ('**实验四：系统性载波同步性能分析**', '（4）实验四：系统性载波同步性能分析'),
    ('**实验五：参数敏感性扫描**', '（5）实验五：参数敏感性扫描'),
    ('**实验六：频偏估计（Frequency Offset Estimation, FOE）+载波相位恢复（Carrier Phase Recovery, CPR）组合方案验证（消融实验）**', '（6）实验六：FOE+CPR 组合方案验证（消融实验）'),
    ('**实验七：综合性能验证**', '（7）实验七：综合性能验证'),
    ('**实验八：方法探索验证（拟根据选定方向设计）**', '（8）实验八：方法探索验证（拟根据选定方向设计）'),
]
for old, new in numbered:
    content = content.replace(old, new)

# 3. Remove bold from list items / method names / table captions
strip = [
    '**弱湍流条件**', '**中等湍流条件**', '**强湍流条件**',
    '**Viterbi-Viterbi（VV）算法**',
    '**盲相位搜索（Blind Phase Search, BPS）算法**',
    '**二阶数字锁相环（Digital Phase-Locked Loop, DPLL）**',
    '**表 1**', '**表 2**',
    '**表 3-1 仿真参数体系**', '**表 3-2 LEO 星地链路典型参数**',
    '**合计**',
]
for s in strip:
    content = content.replace(s, s.replace('**', ''))

# 4. Catch any remaining **bold** → strip (safety net)
remaining = re.findall(r'\*\*([^*]+)\*\*', content)
if remaining:
    print(f"WARNING: {len(remaining)} remaining bold patterns: {remaining[:5]}...")

# Clean up excessive blank lines (max 2 consecutive)
content = re.sub(r'\n{3,}', '\n\n', content)

with open('毕设/开题报告/kaiti-report.md', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done: fixed bold patterns and --- separators")
