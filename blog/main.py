from fastapi import FastAPI, Depends, HTTPException, status
from . import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import List
from hashing import Hash

app = FastAPI()
models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/blog", tags=["Blogs"], status_code=status.HTTP_201_CREATED, response_model=schemas.ShowBlog)
def create(blog: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=blog.title, body=blog.body)    
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Blogs"])
def destroy(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} is not available")
    blog.delete(synchronize_session=False)
    db.commit()
    return {"detail": "Blog deleted"}

@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED, tags=["Blogs"])
def update(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} is not available")
    blog.update({'title': request.title, 'body': request.body})
    db.commit()
    return 'updated'

@app.get("/blogs", response_model=List[schemas.ShowBlog], tags=["Blogs"])
def read_all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get("/blog/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog, tags=["Blogs"])
def read(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} is not available")
    return blog



@app.post('/user', response_model=schemas.ShowUser, tags=["Users"])
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(name=request.name, email=request.email, password=Hash.bcrypt_hash(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
@app.get('/user/{id}', response_model=schemas.ShowUser, tags=["Users"])
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with the id {id} is not available")
    return user
@app.get('/users', response_model=List[schemas.ShowUser], tags=["Users"])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@app.delete('/user/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=["Users"])
def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with the id {id} is not available")
    user.delete(synchronize_session=False)
    db.commit()
    return {"detail": "User deleted"}
@app.put('/user/{id}', status_code=status.HTTP_202_ACCEPTED, tags=["Users"])
def update_user(id: int, request: schemas.User, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with the id {id} is not available")
    user.update({'name': request.name, 'email': request.email, 'password': Hash.bcrypt_hash(request.password)})
    db.commit()
    return 'updated'

