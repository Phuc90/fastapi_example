
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schema, utils

router = APIRouter(
    prefix="/users",
    tags = ['Users']
)


@router.post("/",status_code=status.HTTP_201_CREATED, response_model= schema.UserOut)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    hass_pwd = utils.pwd_context.hash(user.password)
    user.password = hass_pwd
    new_user =  models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


@router.get("/{id}",response_model= schema.UserOut)
def get_users(id:int,  db: Session = Depends(get_db),):
    user = db.query(models.Users).filter(models.Users.id == id).first()

    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail ='User with id {id} doesnt exist')

    return user