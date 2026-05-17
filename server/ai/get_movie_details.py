from langchain.tools import tool

import requests
from dotenv import load_dotenv
import json
from os import getenv

load_dotenv()


@tool
def get_movie_details(id: int):
    """
    Fetch the details of a particular movie id from the TMDB

    Args:
        id (int): The id of the movie

    Returns:
        str: A JSON string containing movie details or an error message.
    """

    url = f"https://api.themoviedb.org/3/movie/{id}"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {getenv('TMDB_ACCESS_TOKEN')}",
    }

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            json_response = response.json()

            return json.dumps(
                {
                    k: v
                    for k, v in json_response.items()
                    if k
                    not in [
                        "backdrop_path",
                        "homepage",
                        "popularity",
                        "softcore",
                        "tagline",
                        "video",
                        "vote_average",
                        "vote_count",
                    ]
                }
            )
        else:
            return f"Could not fetch results, TMDB API returned {response.status_code} code"
    except Exception as e:
        return f"Some error occurred: {str(e)}"


if __name__ == "__main__":
    print(get_movie_details.invoke({"id": 872585}))
