import asyncio

from apscheduler.schedulers.asyncio import (  # type: ignore[import-untyped]
    AsyncIOScheduler,
)
from apscheduler.triggers.cron import CronTrigger  # type: ignore[import-untyped]

from nespresso.recsys.matching.assign import MatchingPipeline

_JOB_ID = "weekly_matching"


def _CreateMatchingScheduler() -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler(timezone="Russia/Moscow")

    scheduler.add_job(
        func=lambda: asyncio.create_task(MatchingPipeline()),
        trigger=CronTrigger(day_of_week="mon", hour=12, minute=0),  # AM
        id=_JOB_ID,  # unique identifier
        replace_existing=True,
    )


_matching_scheduler = _CreateMatchingScheduler()


def StartMatchingSchedulling() -> None:
    _matching_scheduler.start()


def PauseMatchingSchedulling() -> None:
    _matching_scheduler.pause_job(_JOB_ID)


def ResumeMatchingSchedulling() -> None:
    _matching_scheduler.resume_job(_JOB_ID)


def ShutdownMatchingSchedulling() -> None:
    _matching_scheduler.shutdown()
