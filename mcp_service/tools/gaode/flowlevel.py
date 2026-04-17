"""
高德 Web 服务 API 流量限制说明工具。

该工具不会实时访问外部网络，而是返回一份包含：
- 官方流量限制文档链接；
- 文档最后更新时间；
- 控制台中查看当前应用配额/QPS 的入口说明；
- 若干通用注意事项。
"""

from __future__ import annotations

from typing import Any, Dict

from mcp_service.core.mcp_adapter import mcp
from mcp_service.platforms.gaode.metadata import get_flowlevel_info


@mcp.tool
async def gaode_flowlevel() -> Dict[str, Any]:
    """
    查询高德 Web 服务 API 的流量限制说明与官方文档链接。

    返回内容包含：
    - doc_url: 官方流量限制说明文档链接；
    - last_update: 文档标注的最后更新时间（字符串形式）；
    - summary: 简要中文说明；
    - how_to_check_quota: 在控制台查看当前配额/QPS 的入口说明；
    - notes: 若干注意事项。

    实际生效的配额与 QPS 以高德开放平台控制台显示为准。
    """

    return get_flowlevel_info()


__all__ = [
    "gaode_flowlevel",
]

