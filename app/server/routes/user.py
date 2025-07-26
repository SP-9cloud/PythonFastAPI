
from fastapi import APIRouter, Body, Depends
from fastapi.encoders import jsonable_encoder

from app.server.auth.auth_handler import (
    sign_jwt,
    get_password_hash,
    verify_password,
    JWTBearer
)

from app.server.database.user import (
    add_user,
    retrieve_user,
    retrieve_users,
    login_user,
)

from app.server.schemas.user import (
    ErrorResponseModel,
    ResponseModel,
    UserSchema,
    UserLoginSchema
)

router = APIRouter()

@router.post("/signup",response_description="User data added into the database")
def create_user(user: UserSchema = Body(...)):
    userdata = retrieve_user(user.email)
    if userdata:
        return ErrorResponseModel("An error occurred.", 404, "User already exists.")
    else:
        user.password=get_password_hash(user.password)
        user = jsonable_encoder(user)
        new_user = add_user(user)
        return ResponseModel(sign_jwt(new_user['id']), "User Created successfully.")

@router.post("/login",response_description="User Login successfully")
def login_user(user: UserLoginSchema = Body(...)):
    userdata = retrieve_user(user.email)
    try:
        if userdata and verify_password(user.password,userdata['password']):
            return ResponseModel(sign_jwt(userdata['id']), "User Login successfully.")
        else:
            return ErrorResponseModel("An error occurred.", 404, "Invalid user details.")
    except:
        return ErrorResponseModel("An error occurred.", 404, "Invalid user details.")

@router.get("/", dependencies=[Depends(JWTBearer())],response_description="Users retrieved")
def get_users():
    users = retrieve_users()
    if users:
        return ResponseModel(users, "Uses data retrieved successfully")
    return ResponseModel(users, "Empty list returned")
