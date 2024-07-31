from apscheduler.schedulers.background import BackgroundScheduler
from services.stocks import Stocks
from apscheduler.triggers.cron import CronTrigger


class CronJobs(Stocks):

    def execute(self):
        scheduler = BackgroundScheduler()
        
        scheduler.add_job(func=self.fetch_stocks_data, trigger=CronTrigger(minute=self.CRON_MINUTE))
        scheduler.start()
        
        for job in scheduler.get_jobs():
            print("Next Job: ", job.next_run_time)