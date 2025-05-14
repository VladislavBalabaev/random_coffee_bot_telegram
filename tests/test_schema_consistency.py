from typing import Any

from pydantic import BaseModel
from pydantic.fields import FieldInfo
from sqlalchemy.sql.elements import KeyedColumnElement

from nespresso.db.base import Base
from nespresso.db.models.nes_user import NesUser
from nespresso.schemas.nes_user import NesUserIn

ALLOWED_EXTRA_FIELDS = {"created_at", "updated_at"}


def ExtractSQLAlchemyFields(model: type[Base]) -> dict[str, KeyedColumnElement[Any]]:
    return {col.name: col for col in model.__table__.columns}


def ExtractPydanticFields(model: type[BaseModel]) -> dict[str, FieldInfo]:
    return model.model_fields


def test_nes_user_schema_matches_sqlalchemy() -> None:
    sa_fields = ExtractSQLAlchemyFields(NesUser)
    pyd_fields = ExtractPydanticFields(NesUserIn)

    sa_field_names = set(sa_fields.keys())
    pyd_field_names = set(pyd_fields.keys())

    missing_in_sa = pyd_field_names - sa_field_names
    assert not missing_in_sa, f"Pydantic fields missing in SQLAlchemy: {missing_in_sa}"

    extra_in_sa = sa_field_names - pyd_field_names - ALLOWED_EXTRA_FIELDS
    assert not extra_in_sa, f"SQLAlchemy fields missing in Pydantic: {extra_in_sa}"

    for name in pyd_field_names:
        pyd_field = pyd_fields[name]
        sa_col = sa_fields[name]

        if sa_col.nullable:
            assert (
                not pyd_field.is_required()
            ), f"Field `{name}` is nullable in SQLAlchemy but required in Pydantic"
        else:
            assert (
                pyd_field.is_required()
            ), f"Field `{name}` is NOT nullable in SQLAlchemy but optional in Pydantic"
