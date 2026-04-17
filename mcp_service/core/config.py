"""
配置管理模块。

负责从环境变量与可选配置文件中加载应用配置，并提供统一的访问接口。
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .errors import ConfigError
from .logging import get_logger

try:
    import yaml
except ImportError:  # pragma: no cover - 仅在未安装 PyYAML 时触发
    yaml = None  # type: ignore[assignment]


logger = get_logger(__name__)


@dataclass
class GaodeConfig:
    """
    高德开放平台配置。
    """

    enabled: bool = False
    app_key: str | None = None
    app_secret: str | None = None
    base_url: str = "https://restapi.amap.com"


@dataclass
class MeituanConfig:
    """
    美团开放平台配置。
    """

    enabled: bool = False
    app_key: str | None = None
    app_secret: str | None = None
    base_url: str = "https://api.meituan.com"


@dataclass
class AppConfig:
    """
    应用整体配置。
    """

    env: str = "dev"
    port: int = 8000
    log_level: str = "INFO"
    gaode: GaodeConfig = field(default_factory=GaodeConfig)
    meituan: MeituanConfig = field(default_factory=MeituanConfig)


_APP_CONFIG: AppConfig | None = None


def load_config(
    config_path: str | None = None,
    env_override: str | None = None,
    port_override: int | None = None,
) -> AppConfig:
    """
    从配置文件和环境变量加载应用配置。

    :param config_path: 可选配置文件路径，优先级高于环境变量 CONFIG_PATH
    :param env_override: 可选环境名称覆盖
    :param port_override: 可选端口覆盖
    :return: 构建完成的 AppConfig 对象
    """

    base = AppConfig()

    # 1. 解析配置文件（如存在）
    path = _resolve_config_path(config_path)
    if path is not None and path.is_file():
        file_data = _load_yaml(path)
        _merge_dict_into_config(base, file_data)
    elif path is not None:
        logger.warning("指定的配置文件不存在: %s", path)

    # 2. 环境变量覆盖
    _apply_env_overrides(base)

    # 3. 显式参数覆盖
    if env_override:
        base.env = env_override
    if port_override is not None:
        base.port = port_override

    return base


def set_app_config(config: AppConfig) -> None:
    """
    设置全局应用配置。

    :param config: 已加载的 AppConfig 实例
    """

    global _APP_CONFIG
    _APP_CONFIG = config


def get_app_config() -> AppConfig:
    """
    获取全局应用配置。

    :return: 当前应用配置
    :raises ConfigError: 当配置尚未初始化时抛出
    """

    if _APP_CONFIG is None:
        raise ConfigError("应用配置尚未初始化，请先在启动入口中调用 set_app_config。")

    return _APP_CONFIG


def validate_config(config: AppConfig) -> None:
    """
    对当前配置进行基础校验，在发现潜在问题时输出警告日志。

    - 如果某个平台被标记为启用但缺少关键字段（如 app_key 或 app_secret），
      会在日志中输出 WARNING，提示如何进行配置。

    :param config: 需要校验的应用配置
    """

    if config.gaode.enabled and not config.gaode.app_key:
        logger.warning(
            "高德平台已启用但缺少 app_key，请通过环境变量 GAODE_API_KEY 或 "
            "配置文件中的 gaode.app_key 字段进行配置。",
        )

    if config.meituan.enabled and not config.meituan.app_key:
        logger.warning(
            "美团平台已启用但缺少 app_key，请通过环境变量 MEITUAN_APP_KEY 或 "
            "配置文件中的 meituan.app_key 字段进行配置。",
        )


def _resolve_config_path(config_path: str | None) -> Path | None:
    """
    解析最终的配置文件路径。

    :param config_path: 显式传入的配置路径
    :return: 解析后的 Path 对象或 None
    """

    if config_path:
        return Path(config_path).expanduser()

    env_path = os.getenv("CONFIG_PATH")
    if env_path:
        return Path(env_path).expanduser()

    return None


def _load_yaml(path: Path) -> dict[str, Any]:
    """
    从指定路径加载 YAML 文件。

    :param path: YAML 文件路径
    :return: 解析后的字典
    :raises ConfigError: 当未安装 PyYAML 或解析失败时抛出
    """

    if yaml is None:
        raise ConfigError("未安装 PyYAML，无法解析 YAML 配置文件。")

    try:
        with path.open("r", encoding="utf-8") as fp:
            data = yaml.safe_load(fp) or {}
    except OSError as exc:  # pragma: no cover - IO 错误通常在运行环境中出现
        raise ConfigError(f"读取配置文件失败: {exc}") from exc

    if not isinstance(data, dict):
        raise ConfigError("配置文件根节点必须是字典。")

    return data


def _merge_dict_into_config(config: AppConfig, data: dict[str, Any]) -> None:
    """
    将字典数据合并到 AppConfig 对象中。

    :param config: 目标配置对象
    :param data: 从 YAML 或其他来源读取的原始字典
    """

    if "env" in data and isinstance(data["env"], str):
        config.env = data["env"]

    if "port" in data and isinstance(data["port"], int):
        config.port = data["port"]

    if "log_level" in data and isinstance(data["log_level"], str):
        config.log_level = data["log_level"]

    gaode_data = data.get("gaode")
    if isinstance(gaode_data, dict):
        config.gaode.enabled = bool(gaode_data.get("enabled", config.gaode.enabled))
        if "app_key" in gaode_data:
            config.gaode.app_key = str(gaode_data["app_key"])
        if "app_secret" in gaode_data:
            config.gaode.app_secret = str(gaode_data["app_secret"])
        if "base_url" in gaode_data:
            config.gaode.base_url = str(gaode_data["base_url"])

    meituan_data = data.get("meituan")
    if isinstance(meituan_data, dict):
        config.meituan.enabled = bool(meituan_data.get("enabled", config.meituan.enabled))
        if "app_key" in meituan_data:
            config.meituan.app_key = str(meituan_data["app_key"])
        if "app_secret" in meituan_data:
            config.meituan.app_secret = str(meituan_data["app_secret"])
        if "base_url" in meituan_data:
            config.meituan.base_url = str(meituan_data["base_url"])


def _apply_env_overrides(config: AppConfig) -> None:
    """
    通过环境变量覆盖部分配置字段。

    :param config: 目标配置对象
    """

    env = os.getenv("APP_ENV")
    if env:
        config.env = env

    port = os.getenv("APP_PORT")
    if port and port.isdigit():
        config.port = int(port)

    log_level = os.getenv("LOG_LEVEL")
    if log_level:
        config.log_level = log_level

    gaode_enabled = os.getenv("GAODE_ENABLED")
    if gaode_enabled is not None:
        config.gaode.enabled = gaode_enabled.lower() in {"1", "true", "yes"}

    gaode_key = os.getenv("GAODE_API_KEY")
    if gaode_key:
        config.gaode.app_key = gaode_key

    gaode_secret = os.getenv("GAODE_APP_SECRET")
    if gaode_secret:
        config.gaode.app_secret = gaode_secret

    gaode_base_url = os.getenv("GAODE_BASE_URL")
    if gaode_base_url:
        config.gaode.base_url = gaode_base_url

    meituan_enabled = os.getenv("MEITUAN_ENABLED")
    if meituan_enabled is not None:
        config.meituan.enabled = meituan_enabled.lower() in {"1", "true", "yes"}

    meituan_key = os.getenv("MEITUAN_APP_KEY")
    if meituan_key:
        config.meituan.app_key = meituan_key

    meituan_secret = os.getenv("MEITUAN_APP_SECRET")
    if meituan_secret:
        config.meituan.app_secret = meituan_secret

    meituan_base_url = os.getenv("MEITUAN_BASE_URL")
    if meituan_base_url:
        config.meituan.base_url = meituan_base_url


__all__ = [
    "AppConfig",
    "GaodeConfig",
    "MeituanConfig",
    "load_config",
    "set_app_config",
    "get_app_config",
    "validate_config",
]

