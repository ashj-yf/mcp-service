"""
FastMCP 适配模块。

创建并暴露全局 FastMCP 应用实例，供各个工具模块注册工具与资源。
"""

from __future__ import annotations

from fastmcp import FastMCP


mcp = FastMCP(name="MCP Multi Platform Service")
"""
全局 FastMCP 应用实例。

所有工具应通过 `@mcp.tool` 装饰器进行注册。
"""


__all__ = [
    "mcp",
]

