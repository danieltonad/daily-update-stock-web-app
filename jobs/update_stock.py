from apscheduler.schedulers.background import BackgroundScheduler
from services.stocks import Stocks
from apscheduler.triggers.cron import CronTrigger


class CronJobs(Stocks):

    def execute(self):
        scheduler = BackgroundScheduler()
        
        scheduler.add_job(func=self.fetch_stocks_data, trigger=CronTrigger(minute=self.CRON_MINUTE))
        scheduler.start()
        print("Next Job: ", self.next_job_time())