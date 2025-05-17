from handlers.tasks import router as task_router
from handlers.tests import router as test_router
from handlers.user import router as user_router
from handlers.auth import router as auth_router

routers = [task_router, test_router, user_router, auth_router]
