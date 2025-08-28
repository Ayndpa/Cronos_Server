from fastapi import APIRouter, Depends, HTTPException
from sqlite3 import Connection
from typing import List
from services.database import get_db
from models.config import Config

from services.config import (
    create_config,
    get_config,
    update_config,
    delete_config,
    list_configs,
)

router = APIRouter(
    prefix="/config",
)

@router.get("/", response_model=List[Config])
def list_configs_route(db: Connection = Depends(get_db)):
    """
    List all config entries.
    """
    return list_configs(db)

@router.post("/", response_model=List[Config])
def update_configs_route(configs: dict, db: Connection = Depends(get_db)):
    """
    Batch update config entries from a JSON object.
    """
    updated_configs = []
    for key, value in configs.items():
        try:
            updated_config = update_config(db, key=key, value=value)
            updated_configs.append(updated_config)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"Error updating key '{key}': {str(e)}")
    return updated_configs


@router.get("/{key}", response_model=Config)
def get_config_route(key: str, db: Connection = Depends(get_db)):
    """
    Retrieve a config entry by key.
    """
    config = get_config(db, key=key)
    if not config:
        raise HTTPException(status_code=404, detail="Config not found")
    return config


@router.put("/{key}", response_model=Config)
def update_config_route(key: str, config: Config, db: Connection = Depends(get_db)):
    """
    Update an existing config entry.
    """
    try:
        return update_config(db, key=key, value=config.value)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{key}")
def delete_config_route(key: str, db: Connection = Depends(get_db)):
    """
    Delete a config entry by key.
    """
    try:
        delete_config(db, key=key)
        return {"detail": "Config deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))