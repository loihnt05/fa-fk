from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from .. import schemas
from ..database import get_db
from ..repositories import user as user_repo

router = APIRouter(
    tags=["Users"], 
    prefix="/user"
)

@router.post('/', response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return user_repo.create_user(request, db)
    
@router.get('/{id}', response_model=schemas.ShowUser)
def get_user(id: int, db: Session = Depends(get_db)):
    return user_repo.get_user(id, db)

@router.get('/all', response_model=List[schemas.ShowUser])
def get_all_users(db: Session = Depends(get_db)):
    return user_repo.get_all_users(db)

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):
    return user_repo.delete_user(id, db)
        
@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_user(id: int, request: schemas.User, db: Session = Depends(get_db)):
    return user_repo.update_user(id, request, db)
   