import logging
from typing import Any, overload

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.sql.elements import ColumnElement

from nespresso.db.models.nes_user import NesUser
from nespresso.db.repositories.checking import (
    CheckColumnBelongsToModel,
)


class NesUserRepository:
    def __init__(self, session: async_sessionmaker[AsyncSession]):
        self.session = session

    # ----- Create -----

    async def UpsertNesUsers(self, users: NesUser | list[NesUser]) -> None:
        if isinstance(users, NesUser):
            users = [users]

        async with self.session() as session:
            for user in users:
                full = {
                    c.name: getattr(user, c.name) for c in NesUser.__table__.columns
                }
                # only keep client-supplied (non-None) fields
                insert_dict = {k: v for k, v in full.items() if v is not None}
                update_dict = {k: v for k, v in insert_dict.items() if k != "nes_id"}

                await session.execute(
                    insert(NesUser)
                    .values(insert_dict)
                    .on_conflict_do_update(
                        index_elements=[NesUser.nes_id],
                        set_=update_dict,
                    )
                )

                logging.info(f"NesUser(nes_id={user.nes_id}) upserted successfully.")

            await session.commit()

    # ----- Read -----

    @overload
    async def GetNesUsersOnCondition(
        self,
        condition: ColumnElement[bool] | InstrumentedAttribute[bool],
        column: None = None,
    ) -> list[NesUser] | None: ...

    @overload
    async def GetNesUsersOnCondition(
        self,
        condition: ColumnElement[bool] | InstrumentedAttribute[bool],
        column: InstrumentedAttribute[Any],
    ) -> list[Any] | None: ...

    async def GetNesUsersOnCondition(
        self,
        condition: ColumnElement[bool] | InstrumentedAttribute[bool],
        column: InstrumentedAttribute[Any] | None = None,
    ) -> list[NesUser] | list[Any] | None:
        selection = NesUser
        if column is not None:
            CheckColumnBelongsToModel(column, NesUser)
            selection = getattr(NesUser, column.key)

        async with self.session() as session:
            result = await session.execute(select(selection).where(condition))

            return list(result.scalars().all())

    @overload
    async def GetNesUser(
        self,
        nes_id: int,
        column: None = None,
    ) -> NesUser | None: ...

    @overload
    async def GetNesUser(
        self,
        nes_id: int,
        column: InstrumentedAttribute[Any],
    ) -> Any | None: ...

    async def GetNesUser(
        self,
        nes_id: int,
        column: InstrumentedAttribute[Any] | None = None,
    ) -> NesUser | Any | None:
        result = await self.GetNesUsersOnCondition(
            condition=NesUser.nes_id == nes_id,
            column=column,
        )
        return result[0] if result else None

    # ----- Update -----

    # ----- Delete -----
