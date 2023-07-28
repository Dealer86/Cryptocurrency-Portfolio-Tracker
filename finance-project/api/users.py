from fastapi import APIRouter
from api.users_models import UserSchema, UserAddSchema
from domain_logic.user_factory import UserFactory
from domain_logic.user_repo import UserRepo

users_router = APIRouter(prefix="/users")

user_repo = UserRepo()


@users_router.get("", response_model=list[UserSchema])
def get_all_users():
    return user_repo.get_all()


@users_router.post("", response_model=UserSchema)
def create_user(user: UserAddSchema):
    new_user = UserFactory.make(user.username)
    user_repo.add(new_user)
    return new_user


@users_router.get("/{user_id}", response_model=UserSchema)
def get_by_id(user_id: str):
    return user_repo.get_by_id(user_id)


@users_router.delete("/{user_id}")
def delete(user_id: str):
    try:
        user_repo.delete(user_id)
        return {"status": "ok"}
    except Exception as e:
        raise e


@users_router.put("/{user_id}", response_model=UserSchema)
def update(user_id: str, username: UserAddSchema):
    user_repo.update(user_id, username.username)
    return user_repo.get_by_id(user_id)

