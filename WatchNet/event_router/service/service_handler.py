from event_router.service.impl.notification_service import NotificationService
from datetime import datetime


class MicroserviceHandler:
    def __init__(self):
        self.services = {
            # Notification-Service
            "notification": NotificationService.get_instance(
                topic="notification",
                group_id="notification-group"
            ),
        }

    async def send(self, device_id: str, interrupt_type: str, payload: str, timestamp: datetime) -> dict:
        await self.services["notification"].send({device_id, interrupt_type, payload, timestamp})
        return {"message": "Notification sent!"}
