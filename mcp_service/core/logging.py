"""
日志初始化模块。

提供统一的日志配置入口，避免在各个模块中重复配置 logging。
"""

from __future__ import annotations

import logging
from logging import Logger


def setup_logging(level: str = "INFO") -> None:
    """
    初始化基础日志配置。

    :param level: 日志级别名称，例如 "DEBUG"、"INFO"
    """

    numeric_level = getattr(logging, level.upper(), logging.INFO)
    logging.basicConfig(
        level=numeric_level,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    )


def get_logger(name: str) -> Logger:
    """
    获取指定名称的 logger。

    :param name: 日志记录器名称
    :return: 对应的 Logger 实例
    """

    return logging.getLogger(name)

