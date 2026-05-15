"""Baseline 评估框架 — 统一接口和注册表。"""

from .base import Baseline, BaselineSuite, RandomBaseline, GreedyBaseline

__all__ = [
    "Baseline",
    "BaselineSuite",
    "RandomBaseline",
    "GreedyBaseline",
]
