import logging
from datetime import datetime
from zoneinfo import ZoneInfo

from apscheduler.schedulers.asyncio import (  # type: ignore[import-untyped]
    AsyncIOScheduler,
)
from apscheduler.triggers.cron import CronTrigger  # type: ignore[import-untyped]

from nespresso.recsys.matching.assign import MatchingPipeline

_JOB_ID = "weekly_matching"
_TIMEZONE = "Europe/Moscow"


def _CreateMatchingScheduler() -> AsyncIOScheduler:
    async def MatchingEverySecondWeek() -> None:
        current_week = datetime.now(ZoneInfo(_TIMEZONE)).isocalendar()[1]
        if current_week % 2 == 0:  # even week
            logging.info("Skipping matching this week.")
            return

        await MatchingPipeline()

    scheduler = AsyncIOScheduler(timezone=_TIMEZONE)

    scheduler.add_job(
        func=MatchingEverySecondWeek,
        trigger=CronTrigger(
            day_of_week="mon",
            hour=12,
            minute=0,
            timezone=_TIMEZONE,
        ),
        id=_JOB_ID,
        replace_existing=True,
    )

    return scheduler


_matching_scheduler = _CreateMatchingScheduler()


def StartMatching() -> None:
    _matching_scheduler.start()


def ShutdownMatching() -> None:
    _matching_scheduler.shutdown()


def GetNextMatchingTime() -> datetime | None:
    job = _matching_scheduler.get_job(_JOB_ID)
    assert job is not None

    next_run_time: datetime = job.next_run_time
    return next_run_time


def PauseMatching() -> None:
    _matching_scheduler.pause_job(_JOB_ID)


def ResumeMatching() -> None:
    _matching_scheduler.resume_job(_JOB_ID)
