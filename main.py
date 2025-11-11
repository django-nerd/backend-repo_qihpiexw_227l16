import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from database import db, create_document, get_documents
from schemas import Product, Category, Order, ContactMessage

app = FastAPI(title="E-Commerce API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "E-Commerce Backend Running"}

@app.get("/api/hello")
def hello():
    return {"message": "Hello from the backend API!"}

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
            
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    
    import os
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    
    return response

# API Endpoints

@app.get("/api/products", response_model=List[Product])
def list_products(category: Optional[str] = None):
    query = {"category": category} if category else {}
    try:
        docs = get_documents("product", query, limit=50)
        # Convert ObjectId and remove internal fields if present
        for d in docs:
            d.pop("_id", None)
        return docs  # Pydantic will validate/serialize
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/categories", response_model=List[Category])
def list_categories():
    try:
        docs = get_documents("category", {}, limit=50)
        for d in docs:
            d.pop("_id", None)
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class CreateContact(BaseModel):
    name: str
    email: str
    subject: str
    message: str

@app.post("/api/contact")
def submit_contact(payload: CreateContact):
    try:
        create_document("contactmessage", payload.dict())
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class CreateOrder(BaseModel):
    items: list
    total: float
    currency: str = "USD"
    customer_email: Optional[str] = None

@app.post("/api/checkout")
def checkout(payload: CreateOrder):
    try:
        # For demo, just store order; payment provider integration could be added later
        order = Order(
            items=payload.items,
            total=payload.total,
            currency=payload.currency,
            status="paid",
            customer_email=payload.customer_email
        )
        create_document("order", order)
        return {"success": True, "status": "paid"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
