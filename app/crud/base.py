from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType", bound=Any)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Базовый класс для CRUD (Create, Read, Update, Delete) операций с использованием SQLAlchemy и Pydantic.

    Args:
        ModelType (Type): Тип SQLAlchemy модели.
        CreateSchemaType (Type): Тип Pydantic схемы для создания экземпляров модели.
        UpdateSchemaType (Type): Тип Pydantic схемы для обновления экземпляров модели.

    Attributes:
        model (Type[ModelType]): Ссылка на класс SQLAlchemy модели.

    Methods:
        get(db: Session, id: Any) -> Optional[ModelType]:
            Получает экземпляр модели из базы данных по уникальному идентификатору.

        create(db: Session, obj_in: CreateSchemaType) -> ModelType:
            Создает новый экземпляр модели в базе данных, используя предоставленную Pydantic схему.

        update(db: Session, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> ModelType:
            Обновляет существующий экземпляр модели в базе данных на основе предоставленной Pydantic схемы или словаря данных обновления.

        remove(db: Session, id: int) -> ModelType:
            Удаляет экземпляр модели из базы данных по его уникальному идентификатору.
    """

    def __init__(self, model: Type[ModelType]):

        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def create(
        self, db: Session, *, obj_in: CreateSchemaType, user_id: Optional[int] = None
    ) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        if user_id:
            obj_in_data["user_id"] = user_id
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj
