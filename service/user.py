from dataclasses import dataclass
from models import UserLoginSchema
from repository import UserRepository
from service.auth import AuthService


@dataclass
class UserService:
    user_repository: UserRepository
    auth_service: AuthService

    async def create_user(self, username: str, password: str) -> UserLoginSchema:
        created_user = await self.user_repository.create_user(username, password)
        access_token = self.auth_service.generate_access_token(user_id = created_user.id)
        return UserLoginSchema(user_id=created_user.id, access_token=access_token)


