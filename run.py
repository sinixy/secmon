import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from config import SERVER_PORT


async def run():
    from server import Server
    server = Server(SERVER_PORT)

    from sec.utils import update_cik_to_ticker
    # see sec.utils for the explanation
    await update_cik_to_ticker()
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        update_cik_to_ticker,
        trigger=CronTrigger(hour=0, minute=1, day_of_week='mon-fri')
    )
    scheduler.start()

    from sec import monitor_filings
    asyncio.create_task(monitor_filings(server))

    await server.start()


if __name__ == "__main__":
    asyncio.run(run())