from datetime import datetime
from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel

class Plan(SQLModel, table=True):
    __tablename__ = "plans"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    price: float = Field(default=0.0)
    monthly_request_limit: int = Field(default=1000)
    is_active: bool = Field(default=True)

    # Relationship back to subscriptions using this plan
    subscriptions: List["Subscription"] = Relationship(back_populates="plan")


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    hashed_password: str
    api_key: str = Field(index=True, unique=True)  #for clients to authenticate API requests
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    subscriptions: List["Subscription"] = Relationship(back_populates="user")
    usage_logs: List["UsageLog"] = Relationship(back_populates="user")


class Subscription(SQLModel, table=True):
    __tablename__ = "subscriptions"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    plan_id: int = Field(foreign_key="plans.id")
    status: str = Field(default="active")  # active, canceled, unpaid
    start_date: datetime = Field(default_factory=datetime.utcnow)
    end_date: datetime  # When the current billing cycle ends

    # Relationships to access linked objects easily
    user: User = Relationship(back_populates="subscriptions")
    plan: Plan = Relationship(back_populates="subscriptions")


class UsageLog(SQLModel, table=True):
    __tablename__ = "usage_logs"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    endpoint: str  # The specific API path being  called such as "/api/v1/data"
    status_code: int   #forexample 200, 429, 500
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    user: User = Relationship(back_populates="usage_logs")
