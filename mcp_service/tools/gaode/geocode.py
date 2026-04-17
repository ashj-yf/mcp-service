"""
高德地理/逆地理编码相关工具。
"""

from __future__ import annotations

from typing import Any, Dict

from mcp_service.core.config import get_app_config
from mcp_service.core.errors import MissingConfigError
from mcp_service.core.mcp_adapter import mcp
from mcp_service.platforms.gaode import GaodeClient


@mcp.tool
async def gaode_geocode(address: str, city: str | None = None) -> Dict[str, Any]:
    """
    使用高德地理编码接口将地址转换为经纬度。

    :param address: 详细地址，例如 \"北京市朝阳区阜通东大街6号\"。
    :param city: 可选城市名称或行政区代码，用于提高解析精度。
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
    return await client.geocode(address=address, city=city)


@mcp.tool
async def gaode_regeocode(lng: float, lat: float, radius: int | None = None) -> Dict[str, Any]:
    """
    使用高德逆地理编码接口将经纬度转换为结构化地址。

    :param lng: 经度（GCJ-02 坐标系）。
    :param lat: 纬度（GCJ-02 坐标系）。
    :param radius: 可选查询半径，单位米。
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

    location = f"{lng},{lat}"
    client = GaodeClient(gaode_cfg)
    return await client.regeocode(location=location, radius=radius)


__all__ = [
    "gaode_geocode",
    "gaode_regeocode",
]

