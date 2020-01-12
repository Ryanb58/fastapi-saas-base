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

    billing_email = Column(String(256), unique=True, nullable=True)
    stripe_customer_id = Column(String(128), unique=True, nullable=True)
    stripe_subscription_id = Column(String(128), unique=True, nullable=True)

    def __repr__(self):
        return "<Tenant {} - {}>".format(self.id, self.name)


class TenantAccount(BaseModel):
    """
    Through table for M2M relationship between a Tenant and Accounts.
    """

    __tablename__ = "tenant_account"
    id = Column(Integer, primary_key=True, index=True)

    tenant_id = Column(
        Integer, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False
    )
    tenant = relationship(
        "Tenant",
        backref=backref("accounts", passive_deletes=True, lazy="dynamic"),
        lazy=True,
    )

    account_id = Column(
        Integer, ForeignKey("accounts.id", ondelete="CASCADE"), nullable=True
    )
    account = relationship(
        "Account",
        backref=backref("tenants", passive_deletes=True, lazy="dynamic"),
        lazy=True,
    )

    # Use this field in case the user doesn't have an account yet.
    email_address = Column(String, nullable=True)

    def __repr__(self):
        return "<TenantAccount {} - Tenant ID: {} - Account ID: {}>".format(
            self.id, self.tenant_id, self.account_id
        )
