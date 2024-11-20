from fastapi import APIRouter, Depends
from event_router.dto.interrupt_dto import InterruptRequest
from event_router.etc.logger import Logger
from event_router.service.service_handler import MicroserviceHandler

router = APIRouter(prefix="/interrupt")
logger = Logger(__name__).get_logger()


@router.post("/")
async def receive_interrupt(request: InterruptRequest, handler: MicroserviceHandler = Depends(MicroserviceHandler)):
    result: dict = await handler.send(request.device_id, request.interrupt_type, request.payload, request.timestamp)
    logger.info(f"Received interrupt: {request.json}")
    logger.info(f"Result: {result}")
    return result
