from fastapi import APIRouter,Depends,HTTPException
from db import create_user,get_user_by_email
from auth import hash_password,verify_password,create_token,get_current_user
from schemas import UserCreate,UserLogin

router=APIRouter(prefix="/auth",tags=["Authentication"])

@router.post("/register",status_code=201)
def register(user:UserCreate):
    existing_user=get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400,detail="Email aleady exists!")
    print(user.password)
    print(type(user.password))
    hashed_password=hash_password(user.password)
    created_user=create_user(user.email,hashed_password)

    return{
        "id":created_user["id"],
        "email":created_user["email"]
    }

@router.post("/login")
def login(user:UserLogin):

    db_user=get_user_by_email(user.email)
    if not db_user:
        raise HTTPException(status_code=401,detail="Invalid credentials!")
    if not verify_password(user.password,db_user["hashed_password"]):
        raise HTTPException(status_code=401,detail="Invalid credentails!")
    
    token=create_token(db_user["email"])
    
    return{
        "token":token
    }

@router.get("/me")
def me(current_user=Depends(get_current_user)):
    user=get_user_by_email(current_user)
    return{
        "id":user["id"],
        "email":user["email"]
    }
