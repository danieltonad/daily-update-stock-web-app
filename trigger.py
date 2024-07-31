from pusher import Pusher, pusher
from settings import Settings



class Triggers(Settings):
    pusher_client = None
    
    def __init__(self) -> None:
        self.pusher_client = Pusher(
            app_id=self.PUSHER_APP_ID,
            key=self.PUSHER_KEY,
            secret=self.PUSHER_SECRET,
            cluster=self.PUSHER_CLUSTER,
            ssl=True
        )



    def notify(self, event: str, channel: str, message: str):
        self.pusher_client.trigger(channels=channel, event_name=event, data=message)