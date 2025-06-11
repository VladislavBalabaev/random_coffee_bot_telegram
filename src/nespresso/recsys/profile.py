from __future__ import annotations

from dataclasses import dataclass

from nespresso.bot.lib.chat.username import GetTgUsername
from nespresso.db.services.user_context import GetUserContextService


@dataclass
class Profile:
    nes_id: int
    name: str
    username: str
    phone_number: str
    email: str
    about: str

    @classmethod
    async def FromNesId(cls, nes_id: int) -> Profile:
        ctx = await GetUserContextService()

        chat_id = await ctx.GetTgChatIdBy(nes_id)

        name = "-/-"
        username = "[doesn't use bot]"
        phone_number = "-/-"
        email = "-/-"
        about = "[no self description]"

        if chat_id:
            if tg := await GetTgUsername(chat_id):
                username = tg

            if tg_user := await ctx.GetTgUser(chat_id=chat_id):
                phone_number = tg_user.phone_number
                about = tg_user.about

        if nes_user := await ctx.GetNesUser(nes_id=nes_id):
            name = nes_user.name or "-/-"
            email = nes_user.email_primary or "-/-"

        # TODO: add programm'year and format. For that need to see the data.

        return cls(
            nes_id=nes_id,
            name=name,
            username=username,
            phone_number=phone_number,
            email=email,
            about=about,
        )

    def DescribeProfile(self) -> str:
        text = ""
        text += f"{self.name}\n"
        text += f"tg: {self.username}\n"
        text += f"phone: {self.phone_number}\n"
        text += f"email: {self.email}\n\n"
        text += f"{self.about}"

        return text
