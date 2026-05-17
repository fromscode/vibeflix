from langchain.tools import tool

import requests
from dotenv import load_dotenv
import json
from os import getenv

load_dotenv()


@tool
def discover_movies(
    page: int = 1,
    include_adult: bool = False,
    primary_release_year: int = None,
    date_after: str = None,
    date_before: str = None,
    sort_by: str = "popularity.desc",
    with_cast: str = None,
    with_crew: str = None,
    with_genres: str = None,
    with_keywords: str = None,
    with_origin_country: str = None,
    with_original_language: str = None,
    with_runtime_gte: int = None,
    with_runtime_lte: int = None,
    without_genres: str = None,
    without_keywords: str = None,
):
    """
    Discover movies in TMDB

    Args:
        page (int, default=1): Which page to search, by default the first page will be searched

        include_adult (bool, default = False): Should the result include adult searches, (This option should be true if trying to discover movies in the adult industry)

        primary_release_year (int, default = None): Specify a release year

        date_after (str, default=None, format='yyyy-mm-dd'): Discover movies released after a particular date

        date_before (str, default=None, format='yyyy-mm-dd'): Discover movies released before a particular date

        sort_by (str, accepted values:[original_title.asc, original_title.desc ,popularity.asc, popularity.desc, revenue.asc, revenue.desc, primary_release_date.asc, title.asc, title.desc, primary_release_date.desc, vote_average.asc, vote_average.desc, vote_count.asc, vote_count.desc], default=popularity.desc): Chose how to filter discovered movies

        with_cast (str, default = None): Discover movies with particular cast (Use cast Ids. Separate multiple ids using comma (AND) or pipe (OR))

        with_crew (str, default = None): Discover movies with particular crew membders (Use Ids. Separate multiple ids using comma (AND) or pipe (OR))

        with_genres (str, default = None): Discover movies in particular genres (Use genre Ids. Separate multiple ids using comma (AND) or pipe (OR))

        with_keywords (str, default = None): Discover movies with particular keywords (Use keyword Ids. Separate multiple ids using comma (AND) or pipe (OR))

        with_origin_country (str, default = None): Discover movies originated from this country (User country code, i.e., IN for India, BR for Brazil, etc)

        with_original_language (str, default = None): Discover movies with this language (Use language codes, eg.: en, bn, aa etc)

        with_runtime_gte (int, default = None): Discover movies greater than this runtime (in minutes)

        with_runtime_lte (int, default = None): Discover movies shorter than this runtime (in minutes)

        without_genres (str, default = None): Exclude genres (Use genre Ids. Separate multiple ids using comma (AND) or pipe (OR))

        without_keywords (str, default = None): Exclude keywords (use keyword Ids. Separate multiple ids using comma (AND) or pipe (OR))

    Returns:

        The discovered movies

    """

    url = "https://api.themoviedb.org/3/discover/movie"

    params = {
        "language": "en-US",
        "include_video": "false",
        "page": page,
        "include_adult": str(include_adult).lower(),
        "sort_by": sort_by,
        "primary_release_year": primary_release_year,
        "primary_release_date.gte": date_after,
        "primary_release_date.lte": date_before,
        "with_cast": with_cast,
        "with_crew": with_crew,
        "with_genres": with_genres,
        "with_keywords": with_keywords,
        "with_origin_country": with_origin_country,
        "with_original_language": with_original_language,
        "with_runtime.gte": with_runtime_gte,
        "with_runtime.lte": with_runtime_lte,
        "without_genres": without_genres,
        "without_keywords": without_keywords,
    }

    clean_params = {k: v for k, v in params.items() if v is not None}

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {getenv('TMDB_ACCESS_TOKEN')}",
    }

    try:
        response = requests.get(url, headers=headers, params=clean_params)

        if response.status_code == 200:
            json_response = response.json()
            results = json_response.get("results", [])

            if results:
                return json.dumps(
                    {
                        "results": [
                            {
                                "genre_ids": result.get("genre_ids"),
                                "id": result.get("id"),
                                "title": result.get("title"),
                                "original_language": result.get("original_language"),
                                "overview": result.get("overview"),
                                "poster_path": result.get("poster_path"),
                                "release_date": result.get("release_date"),
                            }
                            for result in results
                        ],
                        "total_pages": json_response.get("total_pages"),
                        "total_results": json_response.get("total_results"),
                    }
                )
            else:
                return "No results found for these set of filters"

        else:
            return (
                f"Could not fetch results, TMDB API retured {response.status_code} code"
            )
    except Exception as e:
        return f"An error occured during sending the request: {str(e)}"


if __name__ == "__main__":
    print(discover_movies(with_original_language="bn", with_origin_country="IN"))
