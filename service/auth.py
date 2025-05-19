from dataclasses import dataclass
from repository import UserRepository
from models import UserLoginSchema
from exeption import UserNotFoundException, UserNotCorrectPasswordException
from db_models import UserProfile
from jose import jwt
import datetime as dt
from settings import Settings




@dataclass
class AuthService:
    user_repository: UserRepository
    settings: Settings

    def login(self, username: str, password: str) -> UserLoginSchema:
        user = self.user_repository.get_user_by_username(username)
        self.validate_auth_user(user, password)
        access_token = self.generate_access_token(user_id = user.id)
        return UserLoginSchema(user_id=user.id, access_token=access_token)
    
    @staticmethod
    def validate_auth_user(user: UserProfile, password: str):
        if not user:
            raise UserNotFoundException
        if user.password != password:
            raise UserNotCorrectPasswordException
        
    
    def generate_access_token(self, user_id: int) -> str:
        expires_date_unix = (dt.datetime.utcnow() + dt.timedelta(days=7)).timestamp()
        token = jwt.encode({"user_id" : user_id, "expire" : expires_date_unix}, self.settings.JWT_SECRET_KEY, algorithm=self.settings.JWT_ENCODE_ALGORHYTM)
        
        return token
    

    def get_user_id_from_access_token(self, access_token: str) -> int:
        payload = jwt.decode(access_token, self.settings.JWT_SECRET_KEY, algorithms=[self.settings.JWT_ENCODE_ALGORHYTM])
        print(payload)
        return payload["user_id"]