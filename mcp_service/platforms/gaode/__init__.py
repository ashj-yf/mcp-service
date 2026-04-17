"""
高德开放平台封装。

该子包负责与高德开放平台的交互，包括请求签名、URL 构造以及响应解析。
"""

from __future__ import annotations

from .client import GaodeClient

__all__ = [
    "GaodeClient",
]

