"""Tenant models."""
from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    DateTime,
    LargeBinary,
)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method

from app.models.base import BaseModel


class Tenant(BaseModel):
    """A customer/workspace in the system."""

    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128))
    slug = Column(String(128), unique=True)  # Slug of the name for the URL.

    stripe_customer_id = Column(String(128), unique=True, nullable=True)
    stripe_subscription_id = Column(String(128), unique=True, nullable=True)
