from fastapi import APIRouter, HTTPException, Depends
from event_router.service.user_service import create_user, authenticate_user
from event_router.dto.user_dto import UserCreateDTO, UserResponseDTO
from fastapi.security import HTTPBearer, HTTPBasicCredentials

router = APIRouter(prefix="/users")
security = HTTPBearer()


@router.post("/register", response_model=UserResponseDTO)
def register_user(user_data: UserCreateDTO):
    """Register a new user and generate an API key."""
    try:
        return create_user(user_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/authenticate")
def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    """Authenticate the user with the provided API key."""
    api_key = credentials.credentials
    if authenticate_user(api_key):
        return {"message": "Authentication successful"}
    raise HTTPException(status_code=401, detail="Invalid API key")
