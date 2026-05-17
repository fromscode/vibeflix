from langchain.tools import tool

import requests
from dotenv import dotenv_values
from json import JSONEncoder

@tool
def search_person(name: str, include_adult: bool = False):
    """
    Search the IMDB database for this particular person
    
    Args:
        name (string): The name of the person to search for
        include_adult (bool, default = False): Should the result include adult searches, (This option should be true if searching for people involved with the adult industry)
        
    Returns:

    """
    
    url = f"https://api.themoviedb.org/3/search/person?query={'%20'.join(name.split())}&include_adult={ 'true' if include_adult else 'false'}&language=en-US&page=1"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {dotenv_values()['TMDB_ACCESS_TOKEN']}"
    }

    response = requests.get(url, headers=headers)

    if (response.status_code == 200):
        results = response.json()['results']
        
        if (len(results)):
            return JSONEncoder().encode({
                "id": results[0]["id"],
                "name": results[0]["name"],
                "known_for_department": results[0]["known_for_department"],
                "known_for": [
                    {
                        'id': work.get('id'),
                        'title': work.get('title') or work.get('name'),
                        'overview': work.get('overview'),
                        'type': work.get('media_type'),
                        'language': work.get('original_language'),
                        'genre_ids': work.get('genre_ids'),
                        'release_date': work.get('release_date')
                    }
                    for work in results[0]['known_for']
                ]
            })
            
        else:
            return "No results found for this name"
    
    else:
        return "Could not fetch results, server error"
        
    
    
if __name__ == "__main__":
    print(search_person("Cillian Murphy"))