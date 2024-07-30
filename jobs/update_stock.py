from apscheduler.schedulers.background import BackgroundScheduler
from settings import settings
from services.stocks import fetch_stocks_data
from apscheduler.triggers.cron import CronTrigger


def test_me():
    print("\n test me \n" + settings.YF_SYMBOLS_URL)


def cron_execute():
    scheduler = BackgroundScheduler()
    
    scheduler.add_job(func=fetch_stocks_data, trigger=CronTrigger(minute=35))
    scheduler.start()
    
    for job in scheduler.get_jobs():
        print(job.next_run_time)