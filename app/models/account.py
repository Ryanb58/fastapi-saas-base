"""Account based models."""
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
from passlib.context import CryptContext

from app.models.base import BaseModel


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Account(BaseModel):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)

    first_name = Column(String(100))
    last_name = Column(String(100))

    is_system_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)

    def __repr__(self):
        return "<Account {} - {} {}>".format(self.id, self.first_name, self.last_name)

    @property
    def email(self):
        return self.email_addresses.filter_by(primary=True).first().email

    @property
    def primary_email_address(self):
        return self.email_addresses.filter_by(primary=True).first()

    @property
    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name)


class EmailAddress(BaseModel):
    __tablename__ = "email_addresses"

    id = Column(Integer, primary_key=True)
    # uuid = Column(
    #     UUID(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4
    # )

    account_id = Column(
        Integer, ForeignKey("accounts.id", ondelete="CASCADE"), nullable=True
    )
    account = relationship(
        "Account",
        backref=backref("email_addresses", passive_deletes=True, lazy="dynamic"),
    )

    email = Column(String(256), unique=True, nullable=False)
    primary = Column(Boolean(), nullable=True)
    verified = Column(Boolean(), nullable=True)
    verified_on = Column(DateTime, nullable=True)

    def __repr__(self):
        return "<EmailAddress {}>".format(self.email)


class Password(BaseModel):
    __tablename__ = "passwords"

    id = Column(Integer, primary_key=True)

    account_id = Column(
        Integer, ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False
    )
    account = relationship(
        "Account", backref=backref("passwords", passive_deletes=True), lazy=True
    )

    # _password = Column(LargeBinary(256), nullable=False)
    _password = Column(String(256), nullable=False)

    def __repr__(self):
        return "<Password %r>".format(self.account_id)

    def validate_password(self, plaintext_password):
        """If invalid raise ValidationError, else return True"""

        if len(plaintext_password) < 8:
            raise Exception("Password must be at 8 or more characters long.")

        return True

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, plain_password):
        self.validate_password(plain_password)
        self._password = pwd_context.hash(plain_password)

    @hybrid_method
    def is_correct_password(self, plain_password):
        return pwd_context.verify(plain_password, self.password)


# class PasswordReset(BaseModel):
#     id = Column(Integer, primary_key=True)

#     account_id = Column(
#         Integer, ForeignKey("account.id", ondelete="CASCADE"), nullable=False
#     )
#     account = relationship(
#         "Account",
#         backref=backref("password_resets", passive_deletes=True),
#         lazy=True,
#     )

#     token = Column(String(1024), nullable=False)

#     def __repr__(self):
#         return "<Password %r>".format(self.account_id)

#     @hybrid_method
#     def is_valid(self):
#         from flask_jwt_extended import decode_token

#         try:
#             decode_token(self.token)
#             return True
#         except (jwt.DecodeError, jwt.ExpiredSignatureError):
#             return False
