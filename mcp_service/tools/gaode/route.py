"""
高德路径规划相关工具。
"""

from __future__ import annotations

from typing import Any, Dict

from mcp_service.core.config import get_app_config
from mcp_service.core.errors import MissingConfigError
from mcp_service.core.mcp_adapter import mcp
from mcp_service.platforms.gaode import GaodeClient


def _require_gaode_config() -> GaodeClient:
    """
    获取带配置校验的 GaodeClient 实例。
    """

    app_config = get_app_config()
    gaode_cfg = app_config.gaode

    if not gaode_cfg.app_key:
        raise MissingConfigError(
            platform="高德",
            field="app_key",
            hint="环境变量 GAODE_API_KEY 或配置文件 gaode.app_key",
        )

    return GaodeClient(gaode_cfg)


@mcp.tool
async def gaode_route_driving(
    origin_lng: float,
    origin_lat: float,
    dest_lng: float,
    dest_lat: float,
) -> Dict[str, Any]:
    """
    使用高德驾车路径规划接口获取从起点到终点的驾车路线。

    :param origin_lng: 起点经度（GCJ-02）
    :param origin_lat: 起点纬度（GCJ-02）
    :param dest_lng: 终点经度（GCJ-02）
    :param dest_lat: 终点纬度（GCJ-02）
    :return: 高德返回的 JSON 结果。
    """

    client = _require_gaode_config()
    origin = f"{origin_lng},{origin_lat}"
    destination = f"{dest_lng},{dest_lat}"
    return await client.direction_driving(origin=origin, destination=destination)


@mcp.tool
async def gaode_route_walking(
    origin_lng: float,
    origin_lat: float,
    dest_lng: float,
    dest_lat: float,
) -> Dict[str, Any]:
    """
    使用高德步行路径规划接口获取从起点到终点的步行路线。

    :param origin_lng: 起点经度（GCJ-02）
    :param origin_lat: 起点纬度（GCJ-02）
    :param dest_lng: 终点经度（GCJ-02）
    :param dest_lat: 终点纬度（GCJ-02）
    :return: 高德返回的 JSON 结果。
    """

    client = _require_gaode_config()
    origin = f"{origin_lng},{origin_lat}"
    destination = f"{dest_lng},{dest_lat}"
    return await client.direction_walking(origin=origin, destination=destination)


__all__ = [
    "gaode_route_driving",
    "gaode_route_walking",
]

