from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.config import Config
from app.schemas.config import ConfigCreate, ConfigOut, ConfigUpdate

router = APIRouter()


@router.get("/", response_model=list[ConfigOut])
def get_all_configs(db: Session = Depends(get_db)):
    return db.query(Config).all()


@router.delete("/{config_id}")
def delete_config(config_id: int, db: Session = Depends(get_db)):
    db_config = db.query(Config).filter(Config.config_id == config_id).first()
    if not db_config:
        raise HTTPException(status_code=404, detail="Config not found")
    db.delete(db_config)
    db.commit()
    return {"detail": "Config deleted"}


@router.post("/", response_model=ConfigOut)
def create_config(config: ConfigCreate, db: Session = Depends(get_db)):
    db_config = db.query(Config).filter(Config.path == config.path).first()
    if db_config:
        raise HTTPException(status_code=400, detail="Config path already exists")
    new_config = Config(path=config.path, value=config.value)
    db.add(new_config)
    db.commit()
    db.refresh(new_config)
    return new_config


@router.put("/{config_id}", response_model=ConfigOut)
def update_config(config_id: int, config: ConfigUpdate, db: Session = Depends(get_db)):
    db_config = db.query(Config).filter(Config.config_id == config_id).first()
    if not db_config:
        raise HTTPException(status_code=404, detail="Config not found")
    db_config.value = config.value
    db.commit()
    db.refresh(db_config)
    return db_config
