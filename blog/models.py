from .database import Base
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    body = Column(Text)
    
    creator_id = Column(Integer, nullable=True)
    
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    
    blogs = relationship("Blog", backref="creator")  # One-to-many relationship with Blog