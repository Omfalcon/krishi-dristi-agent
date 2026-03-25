import requests
from typing import List


SEARXNG_URL = "http://localhost:8080/search"


def search_web(query: str, max_results: int = 3) -> str:
    """
    Search the web using a local SearXNG instance and return a clean text-only answer.
    """
    params = {
        "q": query,
        "format": "json",
        "language": "en",
    }

    try:
        response = requests.get(SEARXNG_URL, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()

        results = data.get("results", [])
        if not results:
            return f"No useful answer found for: {query}"

        answer_parts: List[str] = []

        for item in results[:max_results]:
            snippet = item.get("content", "").strip()
            title = item.get("title", "").strip()

            if snippet:
                answer_parts.append(snippet)
            elif title:
                answer_parts.append(title)

        if not answer_parts:
            return f"No useful answer found for: {query}"

        return " ".join(answer_parts)

    except requests.exceptions.ConnectionError:
        return "Could not connect to the local SearXNG server."
    except requests.exceptions.Timeout:
        return "The search request timed out."
    except requests.exceptions.RequestException as e:
        return f"Search request failed: {str(e)}"
    except Exception as e:
        return f"Unexpected error during search: {str(e)}"


if __name__ == "__main__":
    print("🌐 Local SearXNG Web Search Test")

    while True:
        query = input("Enter search query (or 'exit' to quit): ").strip()
        if query.lower() in ["exit", "quit"]:
            print("Goodbye! 👋")
            break

        result = search_web(query)
        print(f"\nSearch result:\n{result}\n")