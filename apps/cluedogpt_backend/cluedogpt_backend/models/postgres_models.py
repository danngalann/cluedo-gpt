"""
Sample PostgreSQL models using Tortoise ORM.
Only included when PostgreSQL is selected during project generation.
"""

from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class User(models.Model):
    """Sample User model for PostgreSQL"""

    id = fields.UUIDField(pk=True)
    name = fields.CharField(max_length=255)
    email = fields.CharField(max_length=255, unique=True)
    hashed_password = fields.CharField(max_length=255)
    is_active = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "users"

    def __str__(self):
        return f"{self.name} <{self.email}>"


class Item(models.Model):
    """Sample Item model for PostgreSQL"""

    id = fields.UUIDField(pk=True)
    title = fields.CharField(max_length=255)
    description = fields.TextField(null=True)
    owner = fields.ForeignKeyField("models.User", related_name="items")
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "items"

    def __str__(self):
        return self.title


# Create Pydantic models for serialization/deserialization
UserPydantic = pydantic_model_creator(User, name="User")
UserInPydantic = pydantic_model_creator(User, name="UserIn", exclude_readonly=True)

ItemPydantic = pydantic_model_creator(Item, name="Item")
ItemInPydantic = pydantic_model_creator(Item, name="ItemIn", exclude_readonly=True)
