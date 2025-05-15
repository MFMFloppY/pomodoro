from fastapi import APIRouter
from dependecy import get_db_session


router = APIRouter(prefix="/tests", tags=["ping_db"])


@router.get("/")
def ping_db():

    if str(get_db_session()) is not None:
        return "Пашет"
    
    return "Не пашет"