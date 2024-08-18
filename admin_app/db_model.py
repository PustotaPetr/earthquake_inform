from datetime import datetime
from typing import Optional
from flask_security import RoleMixin, UserMixin
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa
import sqlalchemy.orm as so
# from flask_login import UserMixin,


db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.BigInteger, unique=True, nullable=False)
    chat_id = db.Column(db.BigInteger, unique=True, nullable=False)
    full_name = db.Column(db.String(20), unique=False, nullable=True)
    user_name = db.Column(db.String(20), unique=False, nullable=True)


class Role(RoleMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    description = db.Column(db.String(255))
    users: so.Mapped[list["Admin"]] = so.relationship(
        "Admin", secondary="roles_users", back_populates="roles"
    )


class Admin(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[Optional[str]] = so.mapped_column(
        sa.String(64), index=True, unique=True, nullable=True
    )
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    last_login_at: so.Mapped[Optional[datetime]] = so.mapped_column(sa.DateTime())
    current_login_at: so.Mapped[Optional[datetime]] = so.mapped_column(sa.DateTime())
    last_login_ip: so.Mapped[Optional[str]] = so.mapped_column(
        sa.String(100), nullable=True
    )
    current_login_ip: so.Mapped[str] = so.mapped_column(sa.String(100), nullable=True)
    login_count: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    active: so.Mapped[bool] = so.mapped_column(sa.Boolean, nullable=True)
    fs_uniquifier: so.Mapped[Optional[str]] = so.mapped_column(
        sa.String(64), unique=True, nullable=False
    )
    confirmed_at: so.Mapped[Optional[datetime]] = so.mapped_column(
        sa.DateTime(), nullable=True
    )
    roles: so.Mapped[list["Role"]] = so.relationship(
        "Role", secondary="roles_users", back_populates="users"
    )


class RolesUsers(db.Model):
    __tablename__ = "roles_users"
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Admin.id))
    role_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Role.id))


class EarthQuake(db.Model):
    __tablename__ = "earthquake"
    id: so.Mapped[str] = so.mapped_column(sa.String(20), primary_key=True)
    description: so.Mapped[str] = so.mapped_column(nullable=True)
    time: so.Mapped[datetime] = so.mapped_column(nullable=True)
    longitude: so.Mapped[float] = so.mapped_column(nullable=True)
    latitude: so.Mapped[float] = so.mapped_column(nullable=True)
    depth: so.Mapped[int] = so.mapped_column(nullable=True)
    magnitude: so.Mapped[float] = so.mapped_column(nullable=True)