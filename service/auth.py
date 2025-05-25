from dataclasses import dataclass
from repository import UserRepository
from models import UserLoginSchema
from exeption import UserNotFoundException, UserNotCorrectPasswordException, TokenExpiredError, TokenNotCorrectException
from db_models import UserProfile
from jose import jwt
import datetime as dt
from settings import Settings
from datetime import timedelta
from jose.exceptions import JWTError
from client import GoogleClient
from models import UserCreateSchema




@dataclass
class AuthService:
    user_repository: UserRepository
    settings: Settings
    google_client: GoogleClient

    def google_auth(self, code: str):
        user_data = self.google_client.get_user_info(code)
        if user := self.user_repository.get_user_by_email(email=user_data.email):
            access_token = self.generate_access_token(user_id = user.id)
            print("user login")
            return UserLoginSchema(user_id=user.id, access_token=access_token)
        
        create_user_data = UserCreateSchema(google_access_token=user_data.access_token,
                                            email=user_data.email,
                                            name=user_data.name
                                            )
        created_user = self.user_repository.create_user(create_user_data)
        access_token = self.generate_access_token(user_id = created_user.id)
        print("user created")
        return UserLoginSchema(user_id=created_user.id, access_token=access_token)


    def get_google_redirect_url(self) -> str:

        return self.settings.google_redirect_url


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
        expires_date_unix = (dt.datetime.utcnow() + timedelta(days=7)).timestamp()
        token = jwt.encode({"user_id" : user_id, "expire" : expires_date_unix}, self.settings.JWT_SECRET_KEY, algorithm=self.settings.JWT_ENCODE_ALGORHYTM)
        
        return token
    

    def get_user_id_from_access_token(self, access_token: str) -> int:

        try:
            payload = jwt.decode(access_token, self.settings.JWT_SECRET_KEY, algorithms=[self.settings.JWT_ENCODE_ALGORHYTM])
        except JWTError: 
            raise TokenNotCorrectException
        
        if payload["expire"] < dt.datetime.utcnow().timestamp():
           raise TokenExpiredError
        
        return payload["user_id"]
