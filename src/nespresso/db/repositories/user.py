import logging
from typing import Any

from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.attributes import InstrumentedAttribute

from nespresso.db.base import Base
from nespresso.db.models.user import NesUser, TgUser


def CheckColumnBelongsToModel(
    column: InstrumentedAttribute[Any], model: type[Base]
) -> None:
    if column.property.parent.class_ is not model:
        raise ValueError(
            "Provided column does not belong to the {model.__name__} model."
        )


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def CreateNewTgUser(
        self, chat_id: int, username: str | None = None, full_name: str | None = None
    ) -> None:
        try:
            self.session.add(
                TgUser(chat_id=chat_id, username=username, full_name=full_name)
            )

            await self.session.commit()
            logging.info(
                f"TgUser(chat_id={chat_id}, username={username}, full_name={full_name}) created successfully."
            )

        except IntegrityError:
            await self.session.rollback()
            logging.error(
                f"TgUser(chat_id={chat_id}, username={username}, full_name={full_name}) already exists. Creation failed."
            )

    async def UpsertNesUsers(self, users: NesUser | list[NesUser]) -> None:
        if isinstance(users, NesUser):
            users = [users]

        for user in users:
            user_dict = {
                c.name: getattr(user, c.name) for c in NesUser.__table__.columns
            }

            await self.session.execute(
                insert(NesUser)
                .values(user_dict)
                .on_conflict_do_update(
                    index_elements=[NesUser.nes_id],
                    set_=user_dict,
                )
            )

            logging.info(f"NesUser(nes_id={user.nes_id}) upserted successfully.")

        await self.session.commit()

    async def GetIds(
        self,
        chat_id: int | None = None,
        nes_id: int | None = None,
    ) -> TgUser | None:
        if sum(arg is not None for arg in [chat_id, nes_id]) != 1:
            raise ValueError("Exactly one of uid, chat_id, or nes_id must be provided.")

        if chat_id is not None:
            condition = TgUser.chat_id == chat_id
        else:
            condition = TgUser.nes_id == nes_id

        result = await self.session.execute(
            select(TgUser.chat_id, TgUser.nes_id).where(condition)
        )

        return result.scalar_one_or_none()

    async def GetTgUserInfo(self, chat_id: int) -> TgUser | None:
        result = await self.session.execute(
            select(TgUser).where(TgUser.chat_id == chat_id)
        )

        return result.scalar_one_or_none()

    async def GetNesUserInfo(self, nes_id: int) -> NesUser | None:
        result = await self.session.execute(
            select(NesUser).where(NesUser.nes_id == nes_id)
        )

        return result.scalar_one_or_none()

    # can be used to check wether username exists
    async def CheckTgUserValueExists(
        self, column: InstrumentedAttribute[Any], value: Any
    ) -> bool:
        CheckColumnBelongsToModel(column, TgUser)

        result = await self.session.execute(select(column).where(column == value))

        return result.scalar_one_or_none() is not None

    async def UpdateTgUserColumn(
        self, chat_id: int, column: InstrumentedAttribute[Any], value: Any
    ) -> None:
        CheckColumnBelongsToModel(column, TgUser)

        try:
            result = await self.session.execute(
                update(column).where(TgUser.chat_id == chat_id).values({column: value})
            )

            if result.rowcount == 0:
                raise NoResultFound()

            await self.session.commit()
            logging.info(f"TgUser(chat_id={chat_id}) updated: {column}={value}.")

        except NoResultFound:
            logging.error(
                f"Failed to update: {column}={value}. No TgUser(chat_id={chat_id}) found."
            )
