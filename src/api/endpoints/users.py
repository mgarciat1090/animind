from fastapi import APIRouter, HTTPException
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from ...models.user import UserModel
import json

router = APIRouter()

# Initialize a DynamoDB client
dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('animind_Users')


@router.post("/users/")
async def create_user(user: dict):
  try:
    user = UserModel(**user)
    user.save()
    return {"status": "User created", "user": json.dumps(user, default=str, indent=4)}
  except (NoCredentialsError, PartialCredentialsError) as e:
    print(e)
    return None

@router.get("/users/")
async def get_all_users():
  try:
    response = table.scan()
  except (NoCredentialsError, PartialCredentialsError) as e:
    print(e)
    return None
  return response['Items']

@router.get("/users/{id}")
async def get_user(id: str):
  try:
    user = UserModel.get(id)
    return {"email": user.email, "name": user.name, "age": user.age}

  except UserModel.DoesNotExist as e:
    raise HTTPException(status_code=404, detail="User not found")

@router.delete("/users/{user_id}")
async def delete_user(user_id: str):
  try:
    response = table.delete_item(
      Key={
          'user_id': user_id
      }
    )
  except (NoCredentialsError, PartialCredentialsError) as e:
    print(e)
    return None
  return {"status": "User deleted", "user_id": user_id}

@router.put("/users/{user_id}")
async def update_user(user_id: str, name: str, email: str):
  try:
    response = table.update_item(
      Key={
          'user_id': user_id
      },
      UpdateExpression='SET name = :name, email = :email',
      ExpressionAttributeValues={
          ':name': name,
          ':email': email
      }
    )
  except (NoCredentialsError, PartialCredentialsError) as e:
    print(e)
    return None
  return {"status": "User updated", "user_id": user_id}