from apscheduler.schedulers.background import BackgroundScheduler
from services.stocks import fetch_stocks_data
from apscheduler.triggers.cron import CronTrigger



class CronJobs:

    def execute():
        scheduler = BackgroundScheduler()
        
        scheduler.add_job(func=fetch_stocks_data, trigger=CronTrigger(minute=2))
        scheduler.start()
        
        for job in scheduler.get_jobs():
            print("Next Job: ",job.next_run_time)