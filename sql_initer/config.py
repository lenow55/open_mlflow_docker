from typing import Annotated, final, override

from pydantic import BaseModel, BeforeValidator, SecretStr
from pydantic.fields import Field
from pydantic_settings import (
    BaseSettings,
    JsonConfigSettingsSource,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)
from typing_extensions import Any


def convert_str2int(v: Any):
    if isinstance(v, str):
        v = int(v)
    return v


def convert_str2float(v: Any):
    if isinstance(v, str):
        v = float(v)
    return v


FloatMapStr = Annotated[float, BeforeValidator(convert_str2float)]
IntMapStr = Annotated[int, BeforeValidator(convert_str2int)]


class ConnectConfig(BaseSettings):
    db_host: str = Field(default="postgres")
    db_port: IntMapStr = Field(default=5432)
    db_user: str = Field(default="user")
    db_password: SecretStr = SecretStr(secret_value="password")
    db_name: str = Field("db")
    dialect: str = Field(default="psycopg2")
    sql_command_echo: bool = Field(default=False)

    @property
    def db_connect_url(self) -> str:
        """
        полный url для подключения к postgresql
        """
        return f"postgresql+{self.dialect}://{self.db_user}:{self.db_password.get_secret_value()}@{self.db_host}:{self.db_port}/{self.db_name}"


class DBProjectConfig(BaseSettings):
    username: str = Field()
    password: SecretStr
    database_name: str = Field()


class Config(BaseSettings):
    connect_config: ConnectConfig = Field()
    db_projects_configs: list[DBProjectConfig] = Field()

    model_config = SettingsConfigDict(
        json_file=(
            "config.json",
            "debug_bases_config.json",
        ),
    )

    @classmethod
    @override
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            env_settings,
            JsonConfigSettingsSource(settings_cls),
            dotenv_settings,
            file_secret_settings,
        )
