"""
高德 IP 定位示例工具。

该工具演示了从 MCP 工具到平台客户端再到配置的完整调用链路，
并在缺失 API Key 时给出明确提示。
"""

from __future__ import annotations

from typing import Any

from mcp_service.core.config import get_app_config
from mcp_service.core.errors import MissingConfigError
from mcp_service.core.mcp_adapter import mcp
from mcp_service.platforms.gaode import GaodeClient


@mcp.tool
async def gaode_ip_geolocation(ip: str) -> dict[str, Any]:
    """
    使用高德开放平台根据 IP 地址获取位置信息（示例）。

    :param ip: 需要查询的 IP 地址
    :return: 位置信息结果（来自高德 IP 定位接口）
    :raises MissingConfigError: 当缺少高德相关配置（如 app_key）时抛出
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
    return await client.ip_geolocation(ip)

