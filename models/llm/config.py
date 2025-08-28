from typing import Optional
from pydantic import BaseModel, Field, HttpUrl

class LLMConfig(BaseModel):
    """
    Pydantic 模型，用于存储通用 API 的配置信息。
    """
    id: int | None = Field(None, description="数据库内部的唯一标识符，自增")
    base_url: Optional[HttpUrl] = Field(
        default=None,
        description="API 的基地址。例如：https://api.example.com/v1"
    )
    model: str = Field(
        ...,
        description="要使用的模型名称，例如：gpt-4o、claude-3-opus-20240229 等。"
    )
    api_key: str = Field(
        ...,
        description="用于 API 请求的密钥。"
    )

class LLMConfigUpdate(BaseModel):
    """
    Pydantic 模型，用于更新通用 API 配置，所有字段都是可选的。
    """
    base_url: Optional[HttpUrl] = Field(
        default=None,
        description="API 的基地址。例如：https://api.example.com/v1"
    )
    model: Optional[str] = Field(
        default=None,
        description="要使用的模型名称，例如：gpt-4o、claude-3-opus-20240229 等。"
    )
    api_key: Optional[str] = Field(
        default=None,
        description="用于 API 请求的密钥。"
    )