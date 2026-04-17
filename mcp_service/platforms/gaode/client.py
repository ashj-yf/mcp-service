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
        根据 IP 地址获取位置信息的示例方法。

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

        # 附加一些上下文字段，便于调用方识别来源。
        if isinstance(data, dict):
            data.setdefault("provider", "gaode")
            data.setdefault("ip", ip)

        return data

