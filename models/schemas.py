from app import ma
from models.models import User


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    email = ma.auto_field()
    username = ma.auto_field()
    phone = ma.auto_field()
    avatar = ma.auto_field()
    created_at = ma.auto_field()
