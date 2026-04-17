## 概览

多开放平台 MCP 服务（当前示例集成高德 Web 服务 API），支持作为 pip 包或 Docker 容器运行。

## 已支持的高德工具（MCP）

- `gaode_ip_geolocation(ip: str)`：IP 定位，返回指定 IP 的位置信息。
- `gaode_geocode(address: str, city: str | None = None)`：地理编码，将地址转换为经纬度。
- `gaode_regeocode(lng: float, lat: float, radius: int | None = None)`：逆地理编码，将经纬度转换为结构化地址。
- `gaode_route_driving(origin_lng: float, origin_lat: float, dest_lng: float, dest_lat: float)`：驾车路径规划。
- `gaode_route_walking(origin_lng: float, origin_lat: float, dest_lng: float, dest_lat: float)`：步行路径规划。
- `gaode_traffic_rectangle(rectangle: str)`：矩形区域交通态势查询，`rectangle` 格式为 `lng1,lat1;lng2,lat2`。
- `gaode_weather(city: str, forecast: bool = False)`：天气查询，`forecast=True` 时返回预报天气。
- `gaode_flowlevel()`：返回高德 Web 服务 API 流量限制说明文档链接及控制台查看路径等信息。

所有高德工具都依赖配置中的 `gaode.app_key` 或环境变量 `GAODE_API_KEY`，缺失时会返回清晰的错误提示。

