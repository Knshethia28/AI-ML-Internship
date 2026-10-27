
from urllib.parse import quote_plus
import webbrowser


def web_search(query, open_browser=False):
    """Prepare a web search and optionally open it in a browser."""

    if not isinstance(query, str) or not query.strip():
        return {"success": False, "error": "Search query cannot be empty."}

    query = query.strip()
    url = "https://www.google.com/search?q=" + quote_plus(query)

    if open_browser:
        try:
            opened = webbrowser.open(url)
            if not opened:
                return {
                    "success": False,
                    "error": "Browser could not be opened.",
                    "query": query,
                    "url": url
                }
        except Exception as error:
            return {"success": False, "error": str(error), "url": url}

    return {"success": True, "query": query, "url": url}


def display_result(result):
    print("\n" + "=" * 45)
    print("              WEB SEARCH")
    print("=" * 45)

    if result["success"]:
        print(f"  Query : {result['query']}")
        print(f"  URL   : {result['url']}")
        print("  Status: Search link prepared.")
    else:
        print(f"  Error : {result['error']}")

    print("=" * 45)


if __name__ == "__main__":
    result = web_search("Python function calling")
    display_result(result)
