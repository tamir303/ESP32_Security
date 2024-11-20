from datetime import datetime
from event_router.dto import user_dto
from event_router.utils.security_utils import hash_api_key, generate_api_key, verify_api_key
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String

# Database setup (use an actual DB in production)
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    username = Column(String, primary_key=True, index=True)
    hashed_api_key = Column(String)


Base.metadata.create_all(bind=engine)


def create_user(user_data: user_dto.UserCreateDTO) -> user_dto.UserResponseDTO:
    """Creates a new user and generates an API key."""
    db = SessionLocal()

    # Check if the user already exists
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise ValueError(f"User {user_data.username} already exists")

    # Generate new API key
    api_key = generate_api_key()
    hashed_key = hash_api_key(api_key)

    # Save the user in the DB
    new_user = User(username=user_data.username, hashed_api_key=hashed_key)
    db.add(new_user)
    db.commit()

    return user_dto.UserResponseDTO(username=user_data.username, api_key=api_key)


def authenticate_user(api_key: str) -> bool:
    """Authenticates a user using their API key."""
    db = SessionLocal()
    user = db.query(User).filter(User.hashed_api_key == hash_api_key(api_key)).first()

    if user:
        return True
    return False
