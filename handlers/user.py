from fastapi import APIRouter, Depends, HTTPException
from models import UserLoginSchema, UserCreateSchema
from typing import Annotated
from dependecy import get_user_service, get_auth_service
from service import UserService, AuthService
from exeption import UserNotCorrectPasswordException, UserNotFoundException

router = APIRouter(prefix="/user", tags=["Autorization by Username/Password"])


@router.post("/login", response_model=UserLoginSchema)
async def login(body:UserCreateSchema, auth_service: Annotated[AuthService, Depends(get_auth_service)]):
    
    try:
        return await auth_service.login(body.username, body.password)
         
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.detail)
    
    except UserNotCorrectPasswordException as e:
        raise HTTPException(status_code=401, detail=e.detail)


@router.post("", response_model=UserLoginSchema)
async def create_user(body: UserCreateSchema, user_service: Annotated[UserService, Depends(get_user_service)]):

    return await user_service.create_user(body.username, body.password)
