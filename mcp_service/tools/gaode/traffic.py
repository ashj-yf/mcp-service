"""
高德交通态势相关工具。
"""

from __future__ import annotations

from typing import Any, Dict

from mcp_service.core.config import get_app_config
from mcp_service.core.errors import MissingConfigError
from mcp_service.core.mcp_adapter import mcp
from mcp_service.platforms.gaode import GaodeClient


@mcp.tool
async def gaode_traffic_rectangle(rectangle: str) -> Dict[str, Any]:
    """
    查询矩形区域的交通态势信息。

    :param rectangle: 矩形区域，格式为 \"lng1,lat1;lng2,lat2\"，分别为左上角和右下角经纬度（GCJ-02）。
    :return: 高德返回的 JSON 结果。
    :raises MissingConfigError: 当缺少高德 app_key 时抛出。
    """

    app_config = get_app_config()
    gaode_cfg = app_config.gaode

    if not gaode_cfg.app_key:
        raise MissingConfigError(
            platform="高德",
            field="app_key",
            hint="环境变量 GAODE_API_KEY 或配置文件 gaode.app_key",
        )

    client = GaodeClient(gaode_cfg)
    return await client.traffic_status_rectangle(rectangle=rectangle)


__all__ = [
    "gaode_traffic_rectangle",
]

