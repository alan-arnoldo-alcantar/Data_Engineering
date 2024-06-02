from fastapi import FastAPI, Body, Path, Query, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security.http import HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import Coroutine, Optional, List
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer
from config.database import session, engine, base
from models.movie import Movie

app = FastAPI()
app.title = "Mi aplicacion con FastAPI"
app.version = "0.0.1"

base.metadata.create_all(bind=engine) # Crea la base de datos

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != "admin@gmail.com":
            raise HTTPException(status_code=403, detail="Credenciales invalidas")

class User(BaseModel):
    email:str
    password:str

class Movie(BaseModel):
    id:Optional[int] = None
    title:str=Field(max_length=15, min_length=2)
    overview:str=Field(max_length=50, min_length=15)
    year:int=Field(le=2024)
    rating:float=Field(ge=0,le=10)
    category:str=Field(max_length=15, min_length=2)

    model_config = {
        "json_schema_extra": {
            "examples": [
               {
                'id': 1,
                'title' : 'Crepusculo',
                'overview' : 'The twilight is almost better than sunday',
                'year' : '2022',
                'rating' : 9.5,
                'category' : 'Phantasy'
            }
            ]
        }
    }

movies = [
    {
        "id": 1,
        "title": "Avatar",
        "overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que...",
        "year": "2009",
        "rating": 7.8,
        "category": "Acción"
    },
    {
        "id": 2,
        "title": "Avatar",
        "overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que...",
        "year": "2009",
        "rating": 7.8,
        "category": "Drama"
    }
]

@app.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1>Hello world!!</h1>')

@app.post('/login', tags=['auth'])
def login(user:User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token:str = create_token(user.model_dump())
        return JSONResponse(content=token, status_code=200)

@app.get('/movies', tags=['movies'], response_model=List[Movie], dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    return JSONResponse(status_code=200,content=movies)

@app.get('/movie/{id}', tags=['movies'], response_model=Movie)
def get_movie(id:int=Path(ge=1,le=2000)) -> Movie:
    for item in  movies:
        if item['id'] == id:
            return JSONResponse(content=item)
    return JSONResponse(status_code=200,content=[])

@app.get('/movies/', tags=['movies'], response_model=List[Movie])
def get_movies_by_category(category:str=Query(min_length=2,max_length=15)) -> List[Movie]:
    data = [item for item in movies if item['category']==category]        
    return JSONResponse(content=data)

@app.post('/movies', tags=['movies'], response_model=dict)
def create_movie(movie: Movie) -> dict:
    movies.append(movie)
    return JSONResponse(status_code=201,content={"message":"Se ha registrado la pelicula"})

@app.put('/movies/{id}', tags=['movies'], response_model=dict)
def update_movie(id:int,movie:Movie) -> dict:
    for item in movies:
        if item['id']==id:
            item['title']=movie.title
            item['overview']=movie.overview
            item['year']=movie.year
            item['rating']=movie.rating
            item['category']=movie.category
    return JSONResponse(status_code=200,content={"message":"Se ha actualizado la pelicula"})

@app.delete('/movies/{id}', tags=['movies'], response_model=dict)
def delete_movie(id:int) -> dict:
    for item in movies:
        if item['id']==id:
            movies.remove(item)
            return JSONResponse(status_code=200,content={"message":"Se ha eliminado la pelicula"})