from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from models import UserCreateSchema, UserLoginSchema
from service import AuthService
from dependecy import get_auth_service
from exeption import UserNotCorrectPasswordException, UserNotFoundException
from fastapi.responses import RedirectResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=UserLoginSchema)
async def login(body:UserCreateSchema, auth_service: Annotated[AuthService, Depends(get_auth_service)]):
    
    try:
        return auth_service.login(body.username, body.password)
         
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.detail)
    
    except UserNotCorrectPasswordException as e:
        raise HTTPException(status_code=401, detail=e.detail)
    

@router.get("/login/google", response_class=RedirectResponse)
async def google_login(auth_service: Annotated[AuthService, Depends(get_auth_service)]):
    
    redir_url = auth_service.get_google_redirect_url()
    print(redir_url)
    return RedirectResponse(redir_url)


@router.get("/google")
async def google_auth(auth_service: Annotated[AuthService, Depends(get_auth_service)],
                      code: str
                      ):
    return auth_service.google_auth(code=code)
