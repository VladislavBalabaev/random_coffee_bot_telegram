import pytest

from nespresso.db.models.nes_user import NesUser
from nespresso.db.models.tg_user import TgUser
from nespresso.db.repositories.checking import (
    CheckColumnBelongsToModel,
    CheckOnlyOneArgProvided,
)


def test_check_column_belongs_to_model_accepts_correct_pair() -> None:
    # Should not raise when column matches the model
    CheckColumnBelongsToModel(TgUser.chat_id, TgUser)


def test_check_column_belongs_to_model_rejects_mismatched_pair() -> None:
    with pytest.raises(ValueError):
        CheckColumnBelongsToModel(TgUser.chat_id, NesUser)


def test_check_only_one_arg_provided_with_single_argument() -> None:
    # Should not raise when exactly one argument is provided
    CheckOnlyOneArgProvided(a=1, b=None)


def test_check_only_one_arg_provided_with_no_arguments() -> None:
    with pytest.raises(ValueError):
        CheckOnlyOneArgProvided(a=None, b=None)


def test_check_only_one_arg_provided_with_multiple_arguments() -> None:
    with pytest.raises(ValueError):
        CheckOnlyOneArgProvided(a=1, b=2)
