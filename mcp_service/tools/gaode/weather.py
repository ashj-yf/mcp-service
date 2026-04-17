"""
高德天气查询相关工具。
"""

from __future__ import annotations

from typing import Any, Dict

from mcp_service.core.config import get_app_config
from mcp_service.core.errors import MissingConfigError
from mcp_service.core.mcp_adapter import mcp
from mcp_service.platforms.gaode import GaodeClient


@mcp.tool
async def gaode_weather(city: str, forecast: bool = False) -> Dict[str, Any]:
    """
    查询指定城市的天气信息。

    :param city: 城市名称或行政区代码。
    :param forecast: 是否查询预报天气；False 为实时天气（base），True 为预报天气（all）。
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

    extensions = "all" if forecast else "base"
    client = GaodeClient(gaode_cfg)
    return await client.weather_info(city=city, extensions=extensions)


__all__ = [
    "gaode_weather",
]

