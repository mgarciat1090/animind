from typing import Union
from fastapi import FastAPI
import boto3
from boto3.dynamodb.conditions import Key
from src.api.endpoints import users


app = FastAPI()
  

# Initialize a DynamoDB client
dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('UsersTable')

@app.get("/")
def read_root():
    return {"Hello": "World"}
  
app.include_router(users.router, prefix="/api/v1", tags=["items"])
  
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
  return {"item_id": item_id, "q": q}