"""配置"""

APP_NAME = "flyflower"
# 数据量配置
TORTOISE_ORM = {
    "connections": {"default": "sqlite://flyflower.sqlite3"},
    "apps": {
        APP_NAME: {
            "models": ["flyflower.models", "aerich.models"],
            "default_connection": "default",
        },
    },
    "timezone": "Asia/Shanghai",
}
