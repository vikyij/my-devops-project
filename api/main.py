from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import boto3
import boto3.session
from boto3.dynamodb.conditions import Attr
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
AWS_ACCESS_KEY_ID=os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY=os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION=os.getenv('AWS_REGION')

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React app's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# get the service resource, use session so that I can pass the region name and aws credentials needed to run the api container
session = boto3.session.Session(region_name=AWS_REGION, aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
dynamodb = session.resource('dynamodb')

# get table
table = dynamodb.Table('Movie-data')

@app.get("/")
async def root():
    return {"message": "Welcome to the TV Shows API!"}

@app.get("/api/movies")

async def get_movies():
    try:
        response = table.scan()
        items = response['Items']
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error quering dynamodb: {str(e)}")

@app.get("/api/seasons")

async def get_seasons(movie_id: str):
    try:
        response = table.scan(
            FilterExpression=Attr('movieId').eq(movie_id)
        )
        movie = response['Items']
        return movie
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error quering dynamodb: {str(e)}")