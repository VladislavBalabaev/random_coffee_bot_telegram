import logging

from aiogram import F, Router, types
from aiogram.filters.command import Command
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

from nespresso.bot.handlers.client.email.verification import CreateCode
from nespresso.bot.lib.message.checks import CheckVerified
from nespresso.bot.lib.message.io import ContextIO, SendDocument, SendMessage
from nespresso.core.configs.paths import PATH_TERMS_OF_USE
from nespresso.db.models.tg_user import TgUser
from nespresso.db.services.user_context import GetUserContextService

router = Router()

# TODO: add bot's: picture, about, description, description picture


class StartStates(StatesGroup):
    GetPhoneNumber = State()
    EmailGet = State()
    EmailConfirm = State()
    Terms = State()


@router.message(StateFilter(None), Command("start"))
async def CommandStart(message: types.Message, state: FSMContext) -> None:
    if await CheckVerified(chat_id=message.chat.id):
        await SendMessage(
            chat_id=message.chat.id,
            text="You've already registered!",
        )
        return

    button = KeyboardButton(text="📱 Share my contact", request_contact=True)
    keyboard = ReplyKeyboardMarkup(keyboard=[[button]], resize_keyboard=True)

    await SendMessage(
        chat_id=message.chat.id,
        text="Please share your contact with us\n\n"
        "If the button menu is hidden, click the 🎛 icon in the lower right corner",
        reply_markup=keyboard,
    )

    await state.set_state(StartStates.GetPhoneNumber)


@router.message(StateFilter(StartStates.GetPhoneNumber))
async def CommandStartGetPhoneNumber(message: types.Message, state: FSMContext) -> None:
    if message.contact is None:
        await SendMessage(
            chat_id=message.chat.id,
            text="❌ Please share your phone number using the button below.\n\n"
            "If the button menu is hidden, click the 🎛 icon in the lower right corner",
            context=ContextIO.UserFailed,
        )
        return

    if message.contact.user_id is None or message.from_user is None:
        await SendMessage(
            chat_id=message.chat.id,
            text="❌ Could not retrieve your phone number since you're not a telegram user.\n"
            "Please try again from your user profile",
            context=ContextIO.UserFailed,
        )
        return

    if message.contact.user_id != message.from_user.id:
        await SendMessage(
            chat_id=message.chat.id,
            text="❌ You sent someone else's phone number.\n"
            "Please share your own number.\n\n"
            "If the button menu is hidden, click the 🎛 icon in the lower right corner",
            context=ContextIO.UserFailed,
        )
        return

    ctx = await GetUserContextService()
    await ctx.UpdateTgUser(
        chat_id=message.chat.id,
        column=TgUser.phone_number,
        value=message.contact.phone_number,
    )

    await SendMessage(
        chat_id=message.chat.id,
        text="✅ Thank you!",
        reply_markup=ReplyKeyboardRemove(),
    )

    await SendMessage(
        chat_id=message.chat.id,
        text="Please enter your NES alumni e-mail to continue",
    )

    await state.set_state(StartStates.EmailGet)


@router.message(StateFilter(StartStates.EmailGet), F.content_type == "text")
async def CommandStartEmailGet(message: types.Message, state: FSMContext) -> None:
    assert message.text is not None

    email = message.text.replace(" ", "")

    if "@nes.ru" not in email:
        await SendMessage(
            chat_id=message.chat.id,
            text="An email should have '@nes.ru' in it",
            context=ContextIO.UserFailed,
        )
        return

    ctx = await GetUserContextService()
    await ctx.UpdateTgUser(
        chat_id=message.chat.id,
        column=TgUser.nes_email,
        value=email,
    )

    await SendMessage(
        chat_id=message.chat.id,
        text="Sending a code.\nPlease wait",
    )

    code = CreateCode()
    logging.info(f"Sending code '{code}' to '{email}'")
    # TODO: uncomment
    # await SendCode(email=email, code=code)

    await SendMessage(
        chat_id=message.chat.id,
        text="We've sent you a code.\nPlease provide it here",
    )

    await state.set_data({"code": code})
    await state.set_state(StartStates.EmailConfirm)


@router.message(StateFilter(StartStates.EmailConfirm), F.content_type == "text")
async def CommandStartEmailConfirm(message: types.Message, state: FSMContext) -> None:
    assert message.text is not None

    data = await state.get_data()
    code_actual = str(data["code"])
    code_provided = message.text.replace(" ", "")

    if code_actual != code_provided:
        await SendMessage(
            chat_id=message.chat.id,
            text="The code is incorrect.\nPlease try again",
            context=ContextIO.UserFailed,
        )
        return

    ctx = await GetUserContextService()
    await ctx.UpdateTgUser(
        chat_id=message.chat.id,
        column=TgUser.verified,
        value=True,
    )

    await SendMessage(
        chat_id=message.chat.id,
        text="✅ Thank you!",
    )

    button = KeyboardButton(text="📄 Yes, I accept")
    keyboard = ReplyKeyboardMarkup(keyboard=[[button]], resize_keyboard=True)

    # TODO: create actual service of service
    await SendDocument(
        chat_id=message.chat.id,
        document=types.FSInputFile(PATH_TERMS_OF_USE),
        caption="Read the terms of the User Agreement and confirm your consent to the processing of personal information in the Terms of Service by clicking `📄 Yes, I accept`\n\n"
        "If the button menu is hidden, click the 🎛 icon in the lower right corner",
        reply_markup=keyboard,
    )

    await state.set_state(StartStates.Terms)
    await state.set_data({"button_text": button.text})


@router.message(StateFilter(StartStates.EmailConfirm), F.content_type == "text")
async def CommandStartTerms(message: types.Message, state: FSMContext) -> None:
    assert message.text is not None

    data = await state.get_data()
    button_text = data["button_text"]

    if message.text != button_text:
        await SendMessage(
            chat_id=message.chat.id,
            text="❌ Please confirm the Terms of Service by clicking `📄 Yes, I accept`\n"
            "Without it you are not allowed to use the service.\n\n"
            "If the button menu is hidden, click the 🎛 icon in the lower right corner",
            context=ContextIO.UserFailed,
        )
        return

    await SendMessage(
        chat_id=message.chat.id,
        text="🎉 You've become a verified user with full access to bot's functionality!",
    )

    await SendMessage(
        chat_id=message.chat.id,
        # TODO: tell more
        text="Let me tell you more about the bot\n...",
    )

    await state.clear()
