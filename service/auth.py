from dataclasses import dataclass
from repository import UserRepository
from models import UserLoginSchema
from exeption import UserNotFoundException, UserNotCorrectPasswordException
from db_models import UserProfile


@dataclass
class AuthService:
    user_repository: UserRepository

    def login(self, usename: str, password: str) -> UserLoginSchema:
        user = self.user_repository.get_user_by_username(usename)
        self.validate_auth_user(user, password)
        
        return UserLoginSchema(user_id=user.id, access_token=user.access_token)
    
    @staticmethod
    def validate_auth_user(user: UserProfile, password: str):
        if not user:
            raise UserNotFoundException
        if user.password != password:
            raise UserNotCorrectPasswordException