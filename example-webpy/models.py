from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(200))
    password: Mapped[str] = mapped_column(String(200), default="")
    name: Mapped[str | None] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(200))
    active: Mapped[bool] = mapped_column(default=True)

    def is_active(self):
        return self.active

    def is_authenticated(self):
        return True
