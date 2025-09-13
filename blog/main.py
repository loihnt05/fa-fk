from fastapi import FastAPI, Depends, HTTPException, status
from . import schemas
from . import models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import List
from passlib import CryptContext

app = FastAPI()
models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/blog")
def create(blog: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=blog.title, body=blog.body)    
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} is not available")
    blog.delete(synchronize_session=False)
    db.commit()
    return {"detail": "Blog deleted"}

@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} is not available")
    blog.update({'title': request.title, 'body': request.body})
    db.commit()
    return 'updated'

@app.get("/blogs", response_model=List[schemas.ShowBlog])
def read_all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get("/blog/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def read(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} is not available")
    return blog


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.post('/user')
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(request.password)
    new_user = models.User(name=request.name, email=request.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user