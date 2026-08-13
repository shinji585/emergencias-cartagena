from typing import Generic, TypeVar, Type, Any, Sequence
from sqlalchemy.orm import Session
from app.db.config import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], db: Session):
        self.model = model
        self.db = db

    def get_by_id(self, id_val: Any) -> ModelType | None:
        return self.db.query(self.model).filter(self.model.id == id_val).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> Sequence[ModelType]:
        return self.db.query(self.model).offset(skip).limit(limit).all()

    def create(self, obj_data: dict[str, Any]) -> ModelType:
        db_obj = self.model(**obj_data)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def update(self, db_obj: ModelType, update_data: dict[str, Any]) -> ModelType:
        for field, value in update_data.items():
            if value is not None and hasattr(db_obj, field):
                setattr(db_obj, field, value)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def delete(self, id_val: Any) -> bool:
        db_obj = self.get_by_id(id_val)
        if db_obj:
            self.db.delete(db_obj)
            self.db.commit()
            return True
        return False
