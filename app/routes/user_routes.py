from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
from app.models.user import User
from app.models.library import LibraryDB
from app.schemas.user_schema import UserCreateSchema, UserResponseSchema, TokenSchema
from app.utils.auth import create_access_token, get_current_user, hash_password, verify_password
from app.database.db import users_collection

router = APIRouter()
library = LibraryDB()

import os

ADMIN_SECRET = os.getenv("ADMIN_SECRET", "supersecretadminkey")

@router.post("/signup", response_model=UserResponseSchema)
async def signup(user: UserCreateSchema):
    existing_user = await library.get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(user.password)

    # check if admin
    role = "admin" if user.admin_secret == ADMIN_SECRET else "user"

    new_user = User(
        name=user.name,
        email=user.email,
        password=hashed_pw,
        role=role
    )
    await library.add_user(new_user)
    return new_user.to_dict()



@router.post("/login", response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await library.get_user_by_email(form_data.username)
    if not user or not verify_password(form_data.password, user.password):  # <-- verify hash
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.id})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/", response_model=List[UserResponseSchema])
async def list_users(current_user: User = Depends(get_current_user)):
    # ✅ Check if current user is admin
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can view all users")

    cursor = users_collection.find()
    users = []
    async for u in cursor:
        u.pop("_id", None)  # remove MongoDB's _id
        users.append(User(**u))
    return users


@router.put("/promote/{user_id}")
async def promote_user(user_id: str, current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can promote users")
    if current_user.role == "admin":
        raise HTTPException(status_code=400, detail="Cannot promote an admin to admin again")
    
    await users_collection.update_one({"id": user_id}, {"$set": {"role": "admin"}})
    return {"message": "User promoted to admin"}
