"""
各开放平台 SDK 封装包。

每个平台（如高德、美团）在此目录下拥有独立的子包，负责处理鉴权、签名、
请求构造和响应解析等细节。
"""

from __future__ import annotations

__all__ = [
    "gaode",
    "meituan",
]

