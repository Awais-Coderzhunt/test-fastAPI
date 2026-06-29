from fastapi import APIRouter, Depends, HTTPException, status, UploadFile
from sqlalchemy.orm import Session

from ..database import get_db
from ..oauth2 import get_current_user

from ..models.userModels import User
from ..schemas.userSchemas import UserCreate, UserResponse, Token
from ..core.security import hash_password, verify_password

from PIL import UnidentifiedImageError
from starlette.concurrency import run_in_threadpool

from image_utils import delete_profile_image, process_profile_image

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/user", response_model = UserResponse , status_code = status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    hashPassword = hash_password(user.password)
    new_user = User(email = user.email , password = hashPassword)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/me", response_model=UserResponse)
def get_me(
    current_user: User = Depends(get_current_user)
):
    return current_user
