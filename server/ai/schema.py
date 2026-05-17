from pydantic import BaseModel, Field
from typing import List, Optional


class Movie(BaseModel):
    title: str = Field(description="The title of the movie, Should NOT be empty")
    tmdb_id: int = Field(description="The TMDB ID of the movie, Should NOT be empty")
    poster: str = Field(description="The url of the image poster, Should NOT be empty")
    release_year: str = Field(
        description="Year of release of the movie, Should NOT be empty"
    )
    overview: str = Field(
        description="A short summary of the movie, no more than two line long, Should NOT be empty"
    )
    genres: List[str] = Field(
        description="The genres of the movie, Should NOT be empty"
    )


class AgentResponse(BaseModel):
    response: str = Field(
        description="A film-bro esque response that fits the user's response with a touch of filmy humor"
    )
    movies: Optional[List[Movie]] = Field(
        description="A list of movies that fit the user's criteria"
    )
