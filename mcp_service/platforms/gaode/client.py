"""
高德开放平台客户端。

当前实现主要用于演示配置加载和调用链路，具体 API 调用逻辑可在后续迭代中补充。
"""

from __future__ import annotations

from typing import Any

from mcp_service.core.config import GaodeConfig
from mcp_service.core.errors import ConfigError
from mcp_service.infra.http_client import AsyncBaseApiClient


class GaodeClient(AsyncBaseApiClient):
    """
    高德开放平台客户端封装。
    """

    def __init__(self, config: GaodeConfig) -> None:
        """
        初始化客户端。

        :param config: 高德平台配置
        :raises ConfigError: 当平台未启用时抛出
        """

        if not config.enabled:
            raise ConfigError("高德平台当前未启用，请在配置中将 gaode.enabled 设置为 true。")

        self._config = config
        super().__init__(base_url=config.base_url)

    async def ip_geolocation(self, ip: str) -> dict[str, Any]:
        """
        根据 IP 地址获取位置信息。

        当前使用高德开放平台 IP 定位接口：
        https://restapi.amap.com/v3/ip

        :param ip: 需要查询的 IP 地址
        :return: 高德返回的 JSON 数据（原样透传，并附带 provider 字段）
        """

        params: dict[str, Any] = {
            "key": self._config.app_key,
            "ip": ip,
        }

        data = await self._request_json(
            method="GET",
            path="/v3/ip",
            params=params,
        )

        if isinstance(data, dict):
            data.setdefault("provider", "gaode")
            data.setdefault("api", "ip")
            data.setdefault("ip", ip)

        return data

    async def geocode(self, address: str, city: str | None = None) -> dict[str, Any]:
        """
        地理编码：将详细地址转换为经纬度。

        接口文档：
        https://lbs.amap.com/api/webservice/guide/api/georegeo
        使用路径 /v3/geocode/geo。
        """

        params: dict[str, Any] = {
            "key": self._config.app_key,
            "address": address,
        }
        if city:
            params["city"] = city

        data = await self._request_json(
            method="GET",
            path="/v3/geocode/geo",
            params=params,
        )

        if isinstance(data, dict):
            data.setdefault("provider", "gaode")
            data.setdefault("api", "geocode")

        return data

    async def regeocode(self, location: str, radius: int | None = None) -> dict[str, Any]:
        """
        逆地理编码：根据经纬度获取结构化地址信息。

        :param location: \"lng,lat\" 格式的经纬度字符串（GCJ-02）
        :param radius: 查询半径，单位米（可选）
        """

        params: dict[str, Any] = {
            "key": self._config.app_key,
            "location": location,
        }
        if radius is not None:
            params["radius"] = radius

        data = await self._request_json(
            method="GET",
            path="/v3/geocode/regeo",
            params=params,
        )

        if isinstance(data, dict):
            data.setdefault("provider", "gaode")
            data.setdefault("api", "regeocode")

        return data

    async def direction_driving(self, origin: str, destination: str, **kwargs: Any) -> dict[str, Any]:
        """
        驾车路径规划。

        :param origin: 起点经纬度，\"lng,lat\" 格式
        :param destination: 终点经纬度，\"lng,lat\" 格式
        :param kwargs: 其他可选参数（如 strategy、waypoints 等），直接透传给高德
        """

        params: dict[str, Any] = {
            "key": self._config.app_key,
            "origin": origin,
            "destination": destination,
        }
        params.update(kwargs)

        data = await self._request_json(
            method="GET",
            path="/v3/direction/driving",
            params=params,
        )

        if isinstance(data, dict):
            data.setdefault("provider", "gaode")
            data.setdefault("api", "direction_driving")

        return data

    async def direction_walking(self, origin: str, destination: str, **kwargs: Any) -> dict[str, Any]:
        """
        步行路径规划。

        :param origin: 起点经纬度，\"lng,lat\" 格式
        :param destination: 终点经纬度，\"lng,lat\" 格式
        :param kwargs: 其他可选参数，直接透传给高德
        """

        params: dict[str, Any] = {
            "key": self._config.app_key,
            "origin": origin,
            "destination": destination,
        }
        params.update(kwargs)

        data = await self._request_json(
            method="GET",
            path="/v3/direction/walking",
            params=params,
        )

        if isinstance(data, dict):
            data.setdefault("provider", "gaode")
            data.setdefault("api", "direction_walking")

        return data

    async def traffic_status_rectangle(self, rectangle: str) -> dict[str, Any]:
        """
        矩形区域交通态势查询。

        :param rectangle: 左上和右下顶点经纬度，\"lng1,lat1;lng2,lat2\" 格式
        """

        params: dict[str, Any] = {
            "key": self._config.app_key,
            "rectangle": rectangle,
        }

        data = await self._request_json(
            method="GET",
            path="/v3/traffic/status/rectangle",
            params=params,
        )

        if isinstance(data, dict):
            data.setdefault("provider", "gaode")
            data.setdefault("api", "traffic_status_rectangle")

        return data

    async def weather_info(self, city: str, extensions: str = "base") -> dict[str, Any]:
        """
        天气查询。

        :param city: 城市编码或名称
        :param extensions: base 为实时天气，all 为预报天气
        """

        params: dict[str, Any] = {
            "key": self._config.app_key,
            "city": city,
            "extensions": extensions,
        }

        data = await self._request_json(
            method="GET",
            path="/v3/weather/weatherInfo",
            params=params,
        )

        if isinstance(data, dict):
            data.setdefault("provider", "gaode")
            data.setdefault("api", "weather_info")

        return data


