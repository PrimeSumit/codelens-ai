from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.db import Base
class Repository(Base):
    __tablename__="repository"
    id:Mapped[int]=mapped_column(primary_key=True)
    name:Mapped[str]=mapped_column(String(255))
    github_url:Mapped[str]=mapped_column(String(500))