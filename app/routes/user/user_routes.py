from fastapi import APIRouter, HTTPException, Depends
from app.models.user_model import UserCreate, UserOut, UserLogin
from app.services.user.user_service import UserService
from app.core.database import get_db

router = APIRouter(prefix="/user", tags=["User"])

@router.post("/", summary="Registrar nuevo usuario")
async def create_user(user: UserCreate, db=Depends(get_db)):
    try:
        return await UserService.create_user(user, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", summary="Login de usuario")
async def login(credentials: UserLogin, db=Depends(get_db)):
    user = await UserService.authenticate_user(credentials.username, credentials.password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user

@router.get("/all", response_model=list[UserOut], summary="Listar usuarios")
async def list_users(db=Depends(get_db)):
    return await UserService.get_all_users(db)
