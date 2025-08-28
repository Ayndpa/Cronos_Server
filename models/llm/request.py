# 定义请求体模型
from typing import Dict, List

from pydantic import BaseModel


class ChatRequest(BaseModel):
    model: str
    messages: List[Dict[str, str]]