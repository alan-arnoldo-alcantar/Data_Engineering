from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI()
app.title = "Mi aplicacion con FastAPI"
app.version = "0.0.1"

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

@app.get('/movies', tags=['movies'], response_model=List[Movie])
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