"""
MCP 服务启动入口。

该模块负责：
1. 解析命令行参数；
2. 加载并注入应用配置；
3. 初始化日志；
4. 注册所有工具模块；
5. 调用 FastMCP 的运行入口。
"""

from __future__ import annotations

import argparse
from typing import Sequence

from mcp_service.core.config import (
    AppConfig,
    load_config,
    set_app_config,
    validate_config,
)
from mcp_service.core.logging import setup_logging, get_logger
from mcp_service.core.mcp_adapter import mcp


logger = get_logger(__name__)


def _parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """
    解析命令行参数。

    :param argv: 可选的参数列表，默认从 sys.argv 读取
    :return: 解析后的命名空间对象
    """

    parser = argparse.ArgumentParser(
        prog="mcp-service",
        description="多开放平台 MCP 服务。",
    )
    parser.add_argument(
        "--config",
        dest="config_path",
        help="配置文件路径（YAML），未指定时可使用环境变量 CONFIG_PATH。",
    )
    parser.add_argument(
        "--env",
        dest="env",
        help="运行环境标识，例如 dev、prod；优先级高于配置文件与 APP_ENV 环境变量。",
    )
    parser.add_argument(
        "--port",
        dest="port",
        type=int,
        help="服务监听端口，优先级高于配置文件与 APP_PORT 环境变量。",
    )

    return parser.parse_args(list(argv) if argv is not None else None)


def _init_app_config(args: argparse.Namespace) -> AppConfig:
    """
    根据命令行参数与环境变量加载并初始化应用配置。

    :param args: 命令行参数解析结果
    :return: 初始化完成的 AppConfig 实例
    """

    config = load_config(
        config_path=args.config_path,
        env_override=args.env,
        port_override=args.port,
    )
    setup_logging(config.log_level)
    set_app_config(config)
    validate_config(config)

    logger.info(
        "应用配置已加载: env=%s, port=%s, log_level=%s",
        config.env,
        config.port,
        config.log_level,
    )

    return config


def _register_tools() -> None:
    """
    导入并注册所有 MCP 工具。

    通过简单的模块导入触发 `@mcp.tool` 装饰器的执行。
    """

    # 高德相关工具
    from mcp_service.tools import gaode as _gaode_tools  # noqa: F401

    # 预留美团等其他平台工具的导入位置
    # from mcp_service.tools import meituan as _meituan_tools  # noqa: F401


def main(argv: Sequence[str] | None = None) -> None:
    """
    MCP 服务主入口。

    :param argv: 可选命令行参数列表
    """

    args = _parse_args(argv)
    _init_app_config(args)
    _register_tools()

    # FastMCP 默认通过 STDIO 运行，适用于 MCP 客户端集成。
    logger.info("启动 MCP 服务...")
    mcp.run()


if __name__ == "__main__":
    main()

