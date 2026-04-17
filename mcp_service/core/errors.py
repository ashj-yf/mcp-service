"""
错误类型定义。

对外暴露统一的异常层次结构，便于在 MCP 层进行一致的错误处理与展示。
"""

from __future__ import annotations


class AppError(Exception):
    """
    应用运行时错误基类。

    所有自定义异常都应继承自该类，便于统一捕获和分类处理。
    """


class ConfigError(AppError):
    """
    配置相关错误。

    在解析配置文件、环境变量或访问配置对象时出现问题时抛出。
    """


class MissingConfigError(ConfigError):
    """
    缺少必要配置（例如 API Key、Secret 等）时抛出。
    """

    def __init__(self, platform: str, field: str, hint: str | None = None) -> None:
        """
        初始化缺失配置错误。

        :param platform: 平台名称，例如 "高德"、"美团"
        :param field: 缺失字段名称，例如 "app_key"、"app_secret"
        :param hint: 可选的配置提示信息，例如环境变量名或配置路径说明
        """

        message = f"{platform} 平台缺少必要配置: {field}"
        if hint:
            message = f"{message}；请通过 {hint} 进行配置。"

        super().__init__(message)
        self.platform = platform
        self.field = field
        self.hint = hint

