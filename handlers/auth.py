from fastapi import APIRouter, Depends
from typing import Annotated
from service import AuthService
from dependecy import get_auth_service
from fastapi.responses import RedirectResponse


router = APIRouter(prefix="/auth", tags=["OAuth2 authorization"])


@router.get("/login/google", response_class=RedirectResponse)
async def google_login(auth_service: Annotated[AuthService, Depends(get_auth_service)]):
    
    redir_url = auth_service.get_google_redirect_url()
    print(redir_url)
    return RedirectResponse(redir_url)


@router.get("/google")
async def google_auth(auth_service: Annotated[AuthService, Depends(get_auth_service)],
                      code: str
                      ):
    return await auth_service.google_auth(code=code)


@router.get("/login/yandex", response_class=RedirectResponse)
async def yandex_login(auth_service: Annotated[AuthService, Depends(get_auth_service)]):
    redir_url = auth_service.get_yandex_redirect_url()
    print(redir_url)
    return RedirectResponse(redir_url)


@router.get("/yandex")
async def yandex_auth(auth_service: Annotated[AuthService, Depends(get_auth_service)], code: str):
    return await auth_service.get_yandex_auth(code=code)



