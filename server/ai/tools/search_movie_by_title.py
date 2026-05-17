from langchain.tools import tool

import requests
from dotenv import load_dotenv
import json
from os import getenv

load_dotenv()


@tool
def search_movie_by_title(
    title: str, include_adult: bool = False, primary_release_year: int = None
):
    """
    Search the IMDB database for a particular title

    Args:
        title (string): The title to search
        include_adult (bool, default=False): True if trying to search movies in the adult industry
        primary_release_year (int, default=None): Specify a release year

    Returns:
        str: A JSON string containing search movie results or an error message.
    """

    url = "https://api.themoviedb.org/3/search/movie"

    params = {
        "query": title,
        "include_adult": str(include_adult).lower(),
        "primary_release_year": primary_release_year,
    }

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {getenv('TMDB_ACCESS_TOKEN')}",
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            params={k: v for k, v in params.items() if v is not None},
        )

        if response.status_code == 200:
            json_response = response.json()
            results = json_response.get("results", [])

            if results:
                return json.dumps(
                    {
                        "page": json_response.get("page", None),
                        "results": [
                            {
                                "id": work.get("id", None),
                                "genre_ids": work.get("genre_ids", None),
                                "title": work.get("title", None),
                                "overview": work.get("overview", None),
                                "original_language": work.get(
                                    "original_language", None
                                ),
                                "release_date": work.get("release_date", None),
                            }
                            for work in results
                        ],
                        "total_pages": json_response.get("total_pages", None),
                        "total_results": json_response.get("total_results", None),
                    }
                )
            else:
                return "No results found for this name"

        else:
            return f"Could not fetch results, TMDB API returned {response.status_code} code"
    except Exception as e:
        return f"Some error occurred: {str(e)}"


if __name__ == "__main__":
    print(search_movie_by_title.invoke({"title": "Oppenheimer"}))
