# routes/llms.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
import sqlite3

from models.llm.config import LLMConfig, LLMConfigUpdate
from services.database import get_db
from services.llm.config import create_llm_config_service, delete_llm_config_service, get_all_llm_config_service, get_llm_config_service, update_llm_config_service

router = APIRouter(
    prefix="/llm",
    tags=["LLMs"],
)

@router.post(
    "/llm_config",
    response_model=LLMConfig,
    status_code=status.HTTP_201_CREATED,
    summary="创建一个新的 OpenAI API 配置"
)
def create_llm_config(config: LLMConfig, db: sqlite3.Connection = Depends(get_db)):
    """
    创建一个新的 OpenAI API 配置。
    """
    return create_llm_config_service(db, config)

@router.get(
    "/llm_config/{config_id}",
    response_model=LLMConfig,
    summary="根据 ID 获取一个 OpenAI API 配置"
)
def get_llm_config(config_id: int, db: sqlite3.Connection = Depends(get_db)):
    """
    根据 ID 获取一个特定的 OpenAI API 配置。
    """
    config = get_llm_config_service(db, config_id)
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="OpenAI 配置未找到"
        )
    return config

@router.get(
    "/llm_config",
    response_model=List[LLMConfig],
    summary="获取所有 OpenAI API 配置"
)
def get_all_llm_config(db: sqlite3.Connection = Depends(get_db)):
    """
    获取数据库中的所有 OpenAI API 配置。
    """
    return get_all_llm_config_service(db)

@router.patch(
    "/llm_config/{config_id}",
    response_model=LLMConfig,
    summary="更新一个 OpenAI API 配置"
)
def update_llm_config(config_id: int, config_update: LLMConfigUpdate, db: sqlite3.Connection = Depends(get_db)):
    """
    更新一个现有的 OpenAI API 配置。
    """
    updated_config = update_llm_config_service(db, config_id, config_update)
    if not updated_config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="OpenAI 配置未找到"
        )
    return updated_config

@router.delete(
    "/llm_config/{config_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="删除一个 OpenAI API 配置"
)
def delete_llm_config(config_id: int, db: sqlite3.Connection = Depends(get_db)):
    """
    删除一个特定的 OpenAI API 配置。
    """
    is_deleted = delete_llm_config_service(db, config_id)
    if not is_deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="OpenAI 配置未找到"
        )
    return