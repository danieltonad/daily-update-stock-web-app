from apscheduler.schedulers.background import BackgroundScheduler
from settings import settings
# from services.stocks import 


def test_me():
    print("test me" + settings.YF_SYMBOLS_URL)


def cron_execute():
    print("in")
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=test_me, trigger="interval", minutes=32)
    scheduler.start()