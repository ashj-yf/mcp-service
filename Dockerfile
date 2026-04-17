FROM python:3.13-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# 复制项目源码与依赖定义
COPY . .

RUN pip install --upgrade pip && \
    pip install .

# 统一入口：与 pip 安装后的 CLI 一致
ENTRYPOINT ["mcp-service"]

