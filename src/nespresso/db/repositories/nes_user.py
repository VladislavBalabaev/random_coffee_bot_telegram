import logging
from typing import Any

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.orm.attributes import InstrumentedAttribute

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
                user_dict = {
                    c.name: getattr(user, c.name) for c in NesUser.__table__.columns
                }

                await session.execute(
                    insert(NesUser)
                    .values(user_dict)
                    .on_conflict_do_update(
                        index_elements=[NesUser.nes_id],
                        set_=user_dict,
                    )
                )

                logging.info(f"NesUser(nes_id={user.nes_id}) upserted successfully.")

            await session.commit()

    # ----- Read -----

    async def GetNesUser(self, nes_id: int) -> NesUser | None:
        async with self.session() as session:
            result = await session.execute(
                select(NesUser).where(NesUser.nes_id == nes_id)
            )

            return result.scalar_one_or_none()

    async def GetNesUserColumn(
        self, nes_id: int, column: InstrumentedAttribute[Any]
    ) -> Any | None:
        CheckColumnBelongsToModel(column, NesUser)

        async with self.session() as session:
            result = await session.execute(
                select(getattr(NesUser, column.key)).where(NesUser.nes_id == nes_id)
            )

            return result.scalar_one_or_none()

    # ----- Update -----

    # ----- Delete -----
