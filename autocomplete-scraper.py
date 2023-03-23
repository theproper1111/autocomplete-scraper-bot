import requests
import json
from fake_useragent import UserAgent
import random
import time


# Set the keyword, language, language, country, number of results, and time delay between requests
seed_keyword = "how does CBD"
language = "en"
country = "us"
num_results = 100  # Number of results to collect
time_delay = 2 # I've had good success keeping this at 2. 0 will fail after about 300 requests 

# Collect suggestions from multiple requests
suggestions = []
unrelated_suggestions = []
current_keyword = seed_keyword

while len(suggestions) < num_results:
    # Format the keyword for the URL
    formatted_keyword = current_keyword.replace(" ", "+")
    
    # Set the URL with the keyword, language, country, and start index
    url = f"http://suggestqueries.google.com/complete/search?output=firefox&q={formatted_keyword}&hl={language}&gl={country}"
    
    print(f"Sending request to URL: {url}")
    
    # Make the request and parse the response
    ua = UserAgent()
    headers = {"user-agent": ua.chrome}
    response = requests.get(url, headers=headers, verify=False)
    if response.status_code == 200:
        try:
            suggestions_batch = json.loads(response.text)[1]
            new_suggestions = [word for word in suggestions_batch if word not in suggestions]
            suggestions += new_suggestions

            # Find unrelated keywords to add to the unrelated_suggestions list
            for word in new_suggestions:
                words = word.split()
                for w in words:
                    if w.lower() != seed_keyword.lower() and w.lower() not in unrelated_suggestions:
                        unrelated_suggestions.append(w.lower())
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON response: {e}")
            print(f"Response text: {response.text}")
            break
    else:
        print(f"Request failed with status code {response.status_code}")
        print(f"Response text: {response.text}")
        break

    # Select a random unrelated suggestion and combine it with the seed keyword for the next query
    if unrelated_suggestions:
        next_keyword = random.choice(unrelated_suggestions)
        current_keyword = f"{seed_keyword} {next_keyword}"

    # Add a two-second delay before the next request
    time.sleep(time_delay)

# Print or write the suggestions to a file
for word in suggestions:
    try:
        print(word)
    except UnicodeEncodeError:
        safe_word = word.encode('utf-8', errors='replace').decode('utf-8', errors='replace')
        print(safe_word)
