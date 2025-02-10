from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import boto3
from boto3.dynamodb.conditions import Attr
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

app = FastAPI()


# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React app's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# get the service resource
dynamodb = boto3.resource('dynamodb')

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
        raise HTTPException(status_code=500, details=str(e))

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