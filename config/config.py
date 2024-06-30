import os
from dotenv import load_dotenv

from dataclasses import dataclass


@dataclass
class RabbitCfg:
    user: str
    password: str
    host: str
    port: int


@dataclass
class TgBotCfg:
    bot_api: str


@dataclass
class Logging:
    filename: str
    level: str


@dataclass
class Config:
    rabbit_cfg: RabbitCfg
    tbbot_cfg: TgBotCfg
    logging: Logging


def get_config() -> Config:
    load_dotenv(override=True)

    config = Config(
        RabbitCfg(
            user=os.getenv("RABBITMQ_USER"),
            password=os.getenv("RABBITMQ_PASSWORD"),
            host=os.getenv("RABBITMQ_HOST"),
            port=int(os.getenv("RABBITMQ_PORT")),
        ),
        TgBotCfg(bot_api=os.getenv("TELEGRAM_BOT_API")),
        Logging(filename=os.getenv("LOG_FILE_NAME"), level=os.getenv("LOG_LEVEL")),
    )
    return config
