from pusher import Pusher
from settings import settings


pusher_client = Pusher(
    app_id=settings.PUSHER_APP_ID,
    key=settings.PUSHER_KEY,
    secret=settings.PUSHER_SECRET,
    cluster=settings.PUSHER_CLUSTER,
    ssl=True
)


def trigger_pusher(event: str, channel: str, message: str):
    pusher_client.trigger(channels=channel, event_name=event, data=message)