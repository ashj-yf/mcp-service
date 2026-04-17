"""
高德开放平台静态元数据。

当前仅封装 Web 服务 API 的流量限制说明入口信息，避免在运行期依赖外网抓取。
"""

from __future__ import annotations

from typing import Any, Dict


def get_flowlevel_info() -> Dict[str, Any]:
    """
    获取高德 Web 服务 API 流量限制说明的关键信息。

    返回结果不会包含具体的配额数值（这些会随时间调整），而是提供：

    - 官方文档链接；
    - 官方标注的最后更新时间；
    - 流量/配额信息的总体说明；
    - 在控制台中查看当前应用配额与 QPS 的入口路径；
    - 重要注意事项。
    """

    return {
        "provider": "gaode",
        "doc_url": "https://lbs.amap.com/api/webservice/guide/tools/flowlevel",
        "last_update": "2024-07-15",
        "summary": (
            "高德 Web 服务 API 的流量限制（调用配额与 QPS）说明文档。"
            "基础服务调用配额请参考高德开放平台定价页中的“基础服务配额说明”，"
            "具体 QPS 与配额上限需在控制台的流量分析/配额管理页面查看。"
        ),
        "how_to_check_quota": (
            "登录高德开放平台控制台，在“流量分析 -> 配额管理”页面查看当前应用的 QPS "
            "和调用配额等详细限制信息。"
        ),
        "notes": [
            "文档中的配额示例仅供参考，实际生效的配额以控制台显示为准。",
            "不同产品线和套餐可能有不同的配额与 QPS 限制，请结合定价页与控制台信息一起查看。",
        ],
    }


__all__ = [
    "get_flowlevel_info",
]

