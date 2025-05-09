import logging
from typing import Any

from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
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


def CheckOnlyOneArgProvided(**kwargs: Any) -> None:
    provided = [key for key, value in kwargs.items() if value is not None]

    if len(provided) != 1:
        raise ValueError(f"More than one argument is provided: {', '.join(provided)}.")


class UserRepository:
    def __init__(self, session: async_sessionmaker[AsyncSession]):
        self.session = session

    # ----- Create -----

    async def CreateTgUser(
        self, chat_id: int, username: str | None = None, full_name: str | None = None
    ) -> None:
        async with self.session() as session:
            try:
                session.add(
                    TgUser(chat_id=chat_id, username=username, full_name=full_name)
                )

                await session.commit()
                logging.info(
                    f"TgUser(chat_id={chat_id}, username={username}, full_name={full_name}) created successfully."
                )

            except IntegrityError:
                await session.rollback()
                logging.error(
                    f"TgUser(chat_id={chat_id}, username={username}, full_name={full_name}) already exists. Creation failed."
                )

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

    async def GetTgUser(self, chat_id: int) -> TgUser | None:
        async with self.session() as session:
            result = await session.execute(
                select(TgUser).where(TgUser.chat_id == chat_id)
            )

            return result.scalar_one_or_none()

    async def GetTgUserColumn(
        self, chat_id: int, column: InstrumentedAttribute[Any]
    ) -> Any | None:
        CheckColumnBelongsToModel(column, TgUser)

        async with self.session() as session:
            result = await session.execute(
                select(getattr(TgUser, column.key)).where(TgUser.chat_id == chat_id)
            )

            return result.scalar_one_or_none()

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

    async def GetChatIdBy(
        self,
        tg_username: str | None = None,
        nes_id: int | None = None,
        nes_email: str | None = None,
    ) -> int | None:
        CheckOnlyOneArgProvided(
            tg_username=tg_username, nes_id=nes_id, nes_email=nes_email
        )

        if tg_username is not None:
            condition = TgUser.username == tg_username
        elif nes_id is not None:
            condition = TgUser.nes_id == nes_id
        elif nes_email is not None:
            condition = TgUser.nes_email == nes_email

        async with self.session() as session:
            result = await session.execute(select(TgUser.chat_id).where(condition))

            return result.scalar_one_or_none()

    # ----- Update -----

    async def UpdateTgUser(
        self, chat_id: int, column: InstrumentedAttribute[Any], value: Any
    ) -> None:
        CheckColumnBelongsToModel(column, TgUser)

        async with self.session() as session:
            try:
                result = await session.execute(
                    update(column)
                    .where(TgUser.chat_id == chat_id)
                    .values({column: value})
                )

                if result.rowcount == 0:
                    raise NoResultFound()

                await session.commit()
                logging.info(f"TgUser(chat_id={chat_id}) updated: {column}={value}.")

            except NoResultFound:
                logging.error(
                    f"Failed to update: {column}={value}. No TgUser(chat_id={chat_id}) found."
                )

    # ----- Delete -----
