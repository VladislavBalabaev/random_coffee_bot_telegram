import logging
from typing import Any, overload

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.sql.elements import ColumnElement

from nespresso.db.models.tg_user import TgUser
from nespresso.db.repositories.checking import (
    CheckColumnBelongsToModel,
    CheckOnlyOneArgProvided,
)


class TgUserRepository:
    def __init__(self, session: async_sessionmaker[AsyncSession]):
        self.session = session

    # ----- Create -----

    async def CreateTgUser(
        self,
        chat_id: int,
        username: str | None = None,
        full_name: str | None = None,
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

    # ----- Read -----

    @overload
    async def GetTgUsersOnCondition(
        self,
        condition: ColumnElement[bool] | InstrumentedAttribute[bool],
        column: None = None,
    ) -> list[TgUser] | None: ...

    @overload
    async def GetTgUsersOnCondition(
        self,
        condition: ColumnElement[bool] | InstrumentedAttribute[bool],
        column: InstrumentedAttribute[Any],
    ) -> list[Any] | None: ...

    async def GetTgUsersOnCondition(
        self,
        condition: ColumnElement[bool] | InstrumentedAttribute[bool],
        column: InstrumentedAttribute[Any] | None = None,
    ) -> list[TgUser] | list[Any] | None:
        selection = TgUser
        if column is not None:
            selection = getattr(TgUser, column.key)

        async with self.session() as session:
            result = await session.execute(select(selection).where(condition))

            return list(result.scalars().all())

    @overload
    async def GetTgUser(
        self,
        chat_id: int,
        column: None = None,
    ) -> TgUser | None: ...

    @overload
    async def GetTgUser(
        self,
        chat_id: int,
        column: InstrumentedAttribute[Any],
    ) -> Any | None: ...

    async def GetTgUser(
        self,
        chat_id: int,
        column: InstrumentedAttribute[Any] | None = None,
    ) -> TgUser | Any | None:
        result = await self.GetTgUsersOnCondition(
            condition=TgUser.chat_id == chat_id,
            column=column,
        )
        return result[0] if result else None

    async def GetChatIdBy(
        self,
        chat_id: int | None = None,
        tg_username: str | None = None,
        nes_id: int | None = None,
        nes_email: str | None = None,
    ) -> int | None:
        CheckOnlyOneArgProvided(
            chat_id=chat_id,
            tg_username=tg_username,
            nes_id=nes_id,
            nes_email=nes_email,
        )

        if chat_id is not None:
            condition = TgUser.chat_id == chat_id
        elif tg_username is not None:
            condition = TgUser.username == tg_username
        elif nes_id is not None:
            condition = TgUser.nes_id == nes_id
        elif nes_email is not None:
            condition = TgUser.nes_email == nes_email

        result = await self.GetTgUsersOnCondition(
            condition=condition,
            column=TgUser.chat_id,
        )
        return int(result[0]) if result else None

    # ----- Update -----

    async def UpdateTgUser(
        self,
        chat_id: int,
        column: InstrumentedAttribute[Any],
        value: Any,
    ) -> None:
        CheckColumnBelongsToModel(column, TgUser)

        async with self.session() as session:
            try:
                result = await session.execute(
                    update(TgUser)
                    .where(TgUser.chat_id == chat_id)
                    .values({column.key: value})
                )

                if result.rowcount == 0:
                    raise NoResultFound()

                await session.commit()
                logging.info(
                    f"TgUser(chat_id={chat_id}) updated: '{column}={value}' successfully."
                )

            except NoResultFound:
                logging.error(
                    f"Failed to update: '{column}={value}'. No TgUser(chat_id={chat_id}) found."
                )
                raise

    # ----- Delete -----
