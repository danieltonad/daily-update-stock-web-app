from settings import Settings
from datetime import datetime


class Utils(Settings):
    
    def split_list(self, data: list, size: int):
        return [data[i:i + size] for i in range(0, len(data), size)]
    
    def next_job_time(self):
        date_time = datetime.now().strftime(f"%d:%m:%Y %H:{self.CRON_MINUTE}:%S")
        return date_time