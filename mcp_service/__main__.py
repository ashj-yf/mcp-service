"""
`python -m mcp_service` 入口模块。

等效于在命令行执行 `mcp-service`。
"""

from __future__ import annotations

from .server import main


def _run() -> None:
    """
    执行服务启动逻辑。
    """

    main()


if __name__ == "__main__":
    _run()

