"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

# Example schemas (kept for reference):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: EmailStr = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")
    image: Optional[str] = Field(None, description="Product image URL")

# E-commerce specific schemas

class Category(BaseModel):
    """Categories collection schema"""
    name: str = Field(..., description="Category name")
    slug: str = Field(..., description="URL-friendly identifier")
    description: Optional[str] = Field(None, description="Category description")

class OrderItem(BaseModel):
    product_id: str
    title: str
    quantity: int = Field(..., ge=1)
    price: float = Field(..., ge=0)

class Order(BaseModel):
    """Orders collection schema"""
    items: List[OrderItem]
    total: float = Field(..., ge=0)
    currency: str = Field("USD")
    status: str = Field("paid", description="paid, pending, failed")
    customer_email: Optional[EmailStr] = None

class ContactMessage(BaseModel):
    """Contact messages collection schema"""
    name: str
    email: EmailStr
    subject: str
    message: str
