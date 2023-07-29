from fastapi import APIRouter

from api.crypto_models import CryptoSchema, CryptoAdd
from api.users_models import UserSchema, UserAddSchema
from domain_logic.crypto.crypto_factory import CryptoFactory
from domain_logic.crypto.crypto_repo import CryptoRepo
from domain_logic.user.user_factory import UserFactory
from domain_logic.user.user_repo import UserRepo
from persistence.UserPersistenceSqlite import UserPersistenceSqlite

users_router = APIRouter(prefix="/users")

user_repo = UserRepo(UserPersistenceSqlite("main_users.db"))
crypto_repo = CryptoRepo()


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


@users_router.post("/{user_id}/crypto")
def add_crypto(user_id: str, crypto: CryptoAdd):
    new_crypto = CryptoFactory.make(crypto.name)
    crypto_repo.add_crypto_to_user(user_id, new_crypto)


@users_router.get("/{user_id}/crypto", response_model=list[CryptoSchema])
def get_crypto_for_user(user_id: str):
    return crypto_repo.get_crypto_for_user(user_id)


@users_router.get("{user_id}/total")
def get_crypto_total_value_for_user(user_id: str):
    return crypto_repo.calculate_total_crypto_value(user_id)
