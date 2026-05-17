from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI

from dotenv import load_dotenv

from tools.discover_movies import discover_movies
from tools.get_movie_credits import get_movie_credits
from tools.get_movie_details import get_movie_details
from tools.get_similar_movies import get_similar_movies
from tools.get_trending_movies import get_trending_movies
from tools.search_movie_by_title import search_movie_by_title
from tools.search_person import search_person

from sys import argv

from schema import AgentResponse

load_dotenv()


def main(query: str):
    llm = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite")

    tools = [
        discover_movies,
        get_movie_credits,
        get_movie_details,
        get_similar_movies,
        get_trending_movies,
        search_movie_by_title,
        search_person,
    ]

    system_prompt = """
        You are a film bro who loves cinema.

        Based on the user's prompt, use the tools provided to you.

        CRITICAL INSTRUCTIONS:
        1. If a user asks about a specific movie, ALWAYS use `search_movie_by_title` first to get its exact ID.
        2. If a user asks for movies starring or directed by a specific person, you MUST FIRST use `search_person` to get their TMDB ID, and then you MUST use `discover_movies` to find their actual films.
        3. NEVER hallucinate or guess a movie ID or person ID.
        4. NEVER recommend movies purely from your internal knowledge. Always fetch live data using your tools before answering.
        5. Providing responses that don't satisfy all the criterias of the expected output (like poster, title, overview, genres etc) is strictly forbidden, you are given all the tools to figure out this information, you should use the tools and not return N/A or None for any ouput fields
        
        If the user enquires about something outside the domain of movies and tv-shows. Simply reply how you cannot entertain that request.
    # """

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt,
        response_format=AgentResponse,
    )

    result = agent.invoke({"messages": [query]})

    agent_response = result["structured_response"]
    return {"response": agent_response.response, "movies": agent_response.movies}


if __name__ == "__main__":
    print(main(" ".join(argv[1:])))
