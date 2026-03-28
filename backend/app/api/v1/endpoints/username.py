from fastapi import APIRouter
from pydantic import BaseModel

from app.services.username_service import check_and_suggest

router = APIRouter(prefix="/username", tags=["Username"])


class UsernameResponse(BaseModel):
    available: bool
    username: str
    suggestions: list[str]


@router.get("/check/{username}", response_model=UsernameResponse)
def check_username(username: str):
    return check_and_suggest(username)

