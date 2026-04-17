"""
HTTP 客户端与请求基类封装。

为各开放平台客户端提供统一的 HTTP 请求能力和错误封装。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

import httpx

from mcp_service.core.errors import AppError
from mcp_service.core.logging import get_logger


logger = get_logger(__name__)


class HttpError(AppError):
    """
    HTTP 请求相关错误。
    """


@dataclass(slots=True)
class HttpRequest:
    """
    HTTP 请求数据结构。
    """

    method: str
    url: str
    params: dict[str, Any] | None = None
    headers: dict[str, str] | None = None
    timeout: float | None = None


class AsyncHttpClient:
    """
    基于 httpx 的异步 HTTP 客户端封装。
    """

    def __init__(self, timeout: float = 10.0) -> None:
        """
        初始化异步 HTTP 客户端。

        :param timeout: 默认请求超时时间（秒）
        """

        self._timeout = timeout
        self._client = httpx.AsyncClient(timeout=timeout)

    async def request_json(self, request: HttpRequest) -> dict[str, Any]:
        """
        发送异步 HTTP 请求并解析 JSON 响应。

        :param request: 请求参数
        :return: 解析后的 JSON 对象
        :raises HttpError: 网络错误、状态码异常或 JSON 解析失败时抛出
        """

        timeout = request.timeout or self._timeout
        try:
            response = await self._client.request(
                method=request.method.upper(),
                url=request.url,
                params=request.params,
                headers=request.headers,
                timeout=timeout,
            )
        except httpx.HTTPError as exc:  # pragma: no cover - 网络错误依赖运行环境
            logger.error("异步 HTTP 请求失败: %s %s - %s", request.method, request.url, exc)
            raise HttpError(f"HTTP 请求失败: {exc}") from exc

        logger.debug(
            "异步 HTTP 响应: %s %s -> %s",
            request.method,
            request.url,
            response.status_code,
        )

        if response.status_code >= 400:
            snippet = response.text[:512]
            raise HttpError(
                f"HTTP 响应状态码异常: {response.status_code}; 响应片段: {snippet}",
            )

        try:
            data = response.json()
        except ValueError as exc:
            snippet = response.text[:512]
            logger.error("响应体非 JSON: %s", snippet)
            raise HttpError("HTTP 响应体不是有效的 JSON。") from exc

        return data


class AsyncBaseApiClient:
    """
    异步开放平台客户端基类。

    使用 AsyncHttpClient 提供异步 JSON 请求能力。
    """

    def __init__(self, base_url: str, http_client: AsyncHttpClient | None = None) -> None:
        """
        初始化异步基础客户端。

        :param base_url: 平台基础 URL，例如 https://restapi.amap.com
        :param http_client: 可选的自定义 AsyncHttpClient 实例
        """

        self._base_url = base_url.rstrip("/")
        self._http = http_client or _get_default_async_http_client()

    def _build_url(self, path: str) -> str:
        """
        构造完整 URL。

        :param path: 路径部分，例如 /v3/ip
        :return: 完整 URL
        """

        return f"{self._base_url}/{path.lstrip('/')}"

    async def _request_json(
        self,
        method: str,
        path: str,
        params: Mapping[str, Any] | None = None,
        headers: Mapping[str, str] | None = None,
        timeout: float | None = None,
    ) -> dict[str, Any]:
        """
        发送异步 JSON 请求的便捷方法。

        :param method: HTTP 方法，例如 GET/POST
        :param path: 路径部分，例如 /v3/ip
        :param params: 查询参数
        :param headers: 额外请求头
        :param timeout: 可选超时时间（秒）
        :return: 解析后的 JSON 响应
        """

        url = self._build_url(path)
        request = HttpRequest(
            method=method,
            url=url,
            params=dict(params) if params is not None else None,
            headers=dict(headers) if headers is not None else None,
            timeout=timeout,
        )
        return await self._http.request_json(request)


_DEFAULT_ASYNC_HTTP_CLIENT: AsyncHttpClient | None = None


def _get_default_async_http_client() -> AsyncHttpClient:
    """
    获取默认的 AsyncHttpClient 实例（懒初始化的单例）。
    """

    global _DEFAULT_ASYNC_HTTP_CLIENT
    if _DEFAULT_ASYNC_HTTP_CLIENT is None:
        _DEFAULT_ASYNC_HTTP_CLIENT = AsyncHttpClient()

    return _DEFAULT_ASYNC_HTTP_CLIENT


__all__ = [
    "HttpRequest",
    "AsyncHttpClient",
    "HttpError",
    "AsyncBaseApiClient",
]

