from langchain.tools import tool

import requests
from dotenv import load_dotenv
import json
from os import getenv

load_dotenv()


@tool
def get_movie_credits(id: int):
    """
    Fetch the credits of a particular movie id from the TMDB

    Args:
        id (int): The id of the movie

    Returns:
        str: A JSON string containing movie credits or an error message.
    """

    url = f"https://api.themoviedb.org/3/movie/{id}/credits"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {getenv('TMDB_ACCESS_TOKEN')}",
    }

    print(f"get_movie_credits called with params {id}")

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            json_response = response.json()
            cast = json_response.get("cast")
            crew = json_response.get("crew")

            return json.dumps(
                {
                    "cast": [
                        {
                            "gender": member.get("gender"),
                            "id": member.get("id"),
                            "name": member.get("name"),
                            "original_name": member.get("original_name"),
                            "character": member.get("character"),
                        }
                        for member in cast
                        if member.get("popularity") > 1
                    ],
                    "crew": [
                        {
                            "gender": member.get("gender"),
                            "id": member.get("id"),
                            "name": member.get("name"),
                            "original_name": member.get("original_name"),
                            "job": member.get("job"),
                        }
                        for member in crew
                        if member.get("popularity") > 1
                    ],
                }
            )
        else:
            return f"Could not fetch results, TMDB API returned {response.status_code} code"
    except Exception as e:
        return f"Some error occurred: {str(e)}"


if __name__ == "__main__":
    print(get_movie_credits.invoke({"id": 550}))
