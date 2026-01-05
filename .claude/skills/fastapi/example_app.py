"""
Example FastAPI application demonstrating common patterns and best practices.
"""

from typing import List, Optional
from fastapi import FastAPI, HTTPException, status, Depends, BackgroundTasks
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings
import random
import time


# Settings configuration
class Settings(BaseSettings):
    app_name: str = "FastAPI Example App"
    version: str = "1.0.0"
    debug: bool = False

    class Config:
        env_file = ".env"


# Pydantic models for request/response validation
class ItemBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="The item name")
    description: Optional[str] = Field(None, max_length=500, description="Optional description")


class ItemCreate(ItemBase):
    price: float = Field(..., gt=0, description="Price of the item")


class ItemUpdate(ItemBase):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    price: Optional[float] = Field(None, gt=0)
    description: Optional[str] = Field(None, max_length=500)


class Item(ItemBase):
    id: int
    price: float

    class Config:
        from_attributes = True


class ItemResponse(BaseModel):
    message: str
    item: Item


class ItemListResponse(BaseModel):
    items: List[Item]
    total: int


# Initialize FastAPI app
app = FastAPI(
    title="FastAPI Example API",
    description="An example API demonstrating FastAPI features and best practices",
    version="1.0.0",
    contact={
        "name": "API Support",
        "email": "support@example.com",
    },
)


# In-memory storage for demonstration (use a database in production)
items_db = []
next_id = 1


def get_next_id():
    global next_id
    current_id = next_id
    next_id += 1
    return current_id


def send_notification_email(email: str, message: str):
    """Simulate sending a notification email as a background task."""
    print(f"Sending email to {email}: {message}")
    time.sleep(1)  # Simulate network delay
    print(f"Email sent to {email}")


# Dependency for getting current user (simplified)
def get_current_user():
    # In a real application, this would validate tokens, etc.
    return {"username": "john_doe", "id": 1}


# CRUD operations
@app.post("/items/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(
    item: ItemCreate, 
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user)
):
    """
    Create a new item.
    """
    global items_db
    
    new_item = Item(
        id=get_next_id(),
        name=item.name,
        description=item.description,
        price=item.price
    )
    
    items_db.append(new_item)
    
    # Add a background task to send notification
    background_tasks.add_task(
        send_notification_email, 
        "admin@example.com", 
        f"New item created: {new_item.name}"
    )
    
    return ItemResponse(message="Item created successfully", item=new_item)


@app.get("/items/", response_model=ItemListResponse)
async def get_items(skip: int = 0, limit: int = 100):
    """
    Get a list of items with optional pagination.
    """
    paginated_items = items_db[skip:skip + limit]
    return ItemListResponse(items=paginated_items, total=len(items_db))


@app.get("/items/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int):
    """
    Get a specific item by ID.
    """
    for item in items_db:
        if item.id == item_id:
            return ItemResponse(message="Item retrieved successfully", item=item)
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Item with ID {item_id} not found"
    )


@app.put("/items/{item_id}", response_model=ItemResponse)
async def update_item(item_id: int, item_update: ItemUpdate):
    """
    Update a specific item by ID.
    """
    for i, item in enumerate(items_db):
        if item.id == item_id:
            # Create updated item with new values or existing values
            updated_item = Item(
                id=item.id,
                name=item_update.name or item.name,
                description=item_update.description or item.description,
                price=item_update.price or item.price
            )
            items_db[i] = updated_item
            return ItemResponse(message="Item updated successfully", item=updated_item)
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Item with ID {item_id} not found"
    )


@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int):
    """
    Delete a specific item by ID.
    """
    global items_db
    initial_length = len(items_db)
    
    items_db = [item for item in items_db if item.id != item_id]
    
    if len(items_db) == initial_length:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found"
        )
    
    return


@app.get("/random/{max_value}")
async def get_random_number(max_value: int):
    """
    Get a random number between 1 and max_value.
    Demonstrates path parameters with type validation.
    """
    if max_value < 1:
        raise HTTPException(
            status_code=status.HTTP_422,
            detail="max_value must be greater than 0"
        )
    
    return {
        "max": max_value,
        "random_number": random.randint(1, max_value)
    }


@app.get("/")
async def home():
    """
    Home endpoint for the API.
    """
    return {
        "message": "Welcome to the FastAPI Example API",
        "version": "1.0.0",
        "items_count": len(items_db)
    }


# Include this example in the documentation
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)