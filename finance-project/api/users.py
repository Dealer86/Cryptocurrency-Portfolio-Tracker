from fastapi import APIRouter, Depends, HTTPException

from api.models.crypto_models import CryptoSchema, CryptoAdd
from api.models.users_models import UserSchema, UserAddSchema
from configuration.config import set_user_persistence_type, set_crypto_persistence_type
from domain_logic.crypto.crypto_factory import CryptoFactory
from domain_logic.crypto.crypto_repo import CryptoRepo
from exceptions.exceptions import (
    UserFileError,
    InvalidUsername,
    UsernameAlreadyExistsException,
    UserNotFound,
    InvalidCoinId,
)
from domain_logic.user.user_factory import UserFactory
from domain_logic.user.repo import UserRepo

users_router = APIRouter(prefix="/users")


def get_user_repo():
    user_persistence_type = set_user_persistence_type("configuration/config.json")
    user_repo = UserRepo(user_persistence_type)
    return user_repo


def get_crypto_repo():
    crypto_persistence_type = set_crypto_persistence_type("configuration/config.json")
    crypto_repo = CryptoRepo(crypto_persistence_type)
    return crypto_repo


@users_router.get("", response_model=list[UserSchema])
def get_all_users(user_repo=Depends(get_user_repo)):
    try:
        return user_repo.get_all()
    except UserFileError as e:
        raise HTTPException(status_code=422, detail=str(e))


@users_router.post("", response_model=UserSchema)
def create_user(user: UserAddSchema, user_repo=Depends(get_user_repo)):
    try:
        new_user = UserFactory.make(user.username)
        user_repo.add(new_user)
        return new_user
    except InvalidUsername as e:
        raise HTTPException(status_code=400, detail=str(e))
    except UsernameAlreadyExistsException as e:
        raise HTTPException(status_code=409, detail=str(e))


@users_router.get("/{user_id}", response_model=UserSchema)
def get_by_id(user_id: str, user_repo=Depends(get_user_repo)):
    try:
        return user_repo.get_by_id(user_id)
    except UserNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@users_router.delete("/{user_id}")
def delete(user_id: str, user_repo=Depends(get_user_repo)):
    try:
        user_repo.delete(user_id)
        return {"status": f"Successfully deleted user with id {user_id}"}
    except UserNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@users_router.put("/{user_id}", response_model=UserSchema)
def update(user_id: str, username: UserAddSchema, user_repo=Depends(get_user_repo)):
    try:
        user_repo.update(user_id, username.username)
        return user_repo.get_by_id(user_id)
    except UserNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@users_router.post("/{user_id}/crypto")
def add_crypto(user_id: str, crypto: CryptoAdd, crypto_repo=Depends(get_crypto_repo)):
    try:
        new_crypto = CryptoFactory.make(crypto.name)
        crypto_repo.add_crypto_to_user(user_id, new_crypto)
    except InvalidCoinId as e:
        raise HTTPException(status_code=400, detail=str(e))
    except UserNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@users_router.get("/{user_id}/crypto", response_model=list[CryptoSchema])
def get_crypto_for_user(user_id: str, crypto_repo=Depends(get_crypto_repo)):
    try:
        return crypto_repo.get_crypto_for_user(user_id)
    except UserNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@users_router.get("{user_id}/total")
def get_crypto_total_value_for_user(user_id: str, crypto_repo=Depends(get_crypto_repo)):
    try:
        return crypto_repo.calculate_total_crypto_value(user_id)
    except UserNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
