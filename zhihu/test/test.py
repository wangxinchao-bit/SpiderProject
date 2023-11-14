import requests

def get_suggestions(query):
    base_url = "http://www.baidu.com/su"
    params = {
        'wd': query,
        'cb': 'callback',  # JSONP callback function name
    }

    response = requests.get(base_url, params=params)
    # suggestions = response.json()

    return response.text

query = "python tutorial"
suggestions = get_suggestions(query)

print(f"Suggestions for '{query}': {suggestions}")
