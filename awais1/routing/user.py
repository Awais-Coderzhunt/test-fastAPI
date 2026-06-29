from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session
from starlette.concurrency import run_in_threadpool
from PIL import UnidentifiedImageError

from ..database import get_db
from ..models import User
from ..schemas import UserCreate, UserResponse, UserUpdate
from ..security import hash_password
from ..oauth2 import get_current_user
from ..image_utils import (
    ALLOWED_CONTENT_TYPES,
    MAX_IMAGE_BYTES,
    delete_profile_image,
    process_profile_image,
)

router = APIRouter(prefix="/api/users", tags=["users"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")

    user_data = user.model_dump()
    user_data["password"] = hash_password(user_data["password"])
    new_user = User(**user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/me/profile-image", response_model=UserResponse)
async def upload_profile_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 1. Validate the declared content type.
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Unsupported file type. Allowed: {', '.join(sorted(ALLOWED_CONTENT_TYPES))}",
        )

    # 2. Read bytes and enforce a size limit.
    content = await file.read()
    if len(content) > MAX_IMAGE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large. Max size is {MAX_IMAGE_BYTES // (1024 * 1024)} MB",
        )

    # 3. Process + store (CPU-bound, run off the event loop).
    try:
        filename = await run_in_threadpool(process_profile_image, content)
    except UnidentifiedImageError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is not a valid image",
        )

    # 4. Remove the previous image, then save the new filename.
    old_image = current_user.profile_image
    current_user.profile_image = filename
    db.commit()
    db.refresh(current_user)

    delete_profile_image(old_image)

    return current_user


@router.delete("/me/profile-image", response_model=UserResponse)
def remove_profile_image(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    old_image = current_user.profile_image
    current_user.profile_image = None
    db.commit()
    db.refresh(current_user)

    delete_profile_image(old_image)

    return current_user


@router.put("/{user_id}", response_model=UserResponse)
def user_update(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")

    if user_data.userName is not None:
        user.userName = user_data.userName
    if user_data.email is not None:
        user.email = user_data.email
    if user_data.age is not None:
        user.age = user_data.age

    db.commit()
    db.refresh(user)
    return user


@router.patch("/{user_id}", response_model=UserResponse)
def user_partial_update(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")

    for field, value in user_data.model_dump(exclude_unset=True).items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")

    db.delete(user)
    db.commit()


@router.get("/", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(User).order_by(User.id.desc()).all()
