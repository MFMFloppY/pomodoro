class UserNotFoundException(Exception):
    detail = "User not found"

class UserNotCorrectPasswordException(Exception):
    detail = "Incorrect password!"

class TokenExpiredError(Exception):
    detail = "Your token expired!"

class TokenNotCorrectException(Exception):
    detail = "Token is not correct!"

class TaskNotFound(Exception):
    detail = "Task not found"
