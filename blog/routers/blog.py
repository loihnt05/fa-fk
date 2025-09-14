from typing import List
from .. import schemas, database, oauth2
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from ..repositories import blog as repository_blog

router = APIRouter(
    tags=["Blogs"],
    prefix="/blog"
)
@router.get("/all", response_model=List[schemas.ShowBlog])
def read_all(db: Session = Depends(database.get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return repository_blog.get_all_blogs(db)

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def read(id: int, db: Session = Depends(database.get_db)):
    return repository_blog.get_blog(id, db)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ShowBlog)
def create(blog: schemas.Blog, db: Session = Depends(database.get_db)):
    return repository_blog.create_blog(blog, db)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(database.get_db)):
    return repository_blog.delete_blog(id, db)

@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.Blog, db: Session = Depends(database.get_db)):
    return repository_blog.update_blog(id, request, db)