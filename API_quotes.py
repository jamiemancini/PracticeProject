import requests
import random
import config

api_key = config.API_KEY



categories = ['age', 'alone', 'amazing', 'anger', 'architecture', 'art', 'attitude', 'beauty', 'best', 'birthday', 'business', 'cartouch', 'change', 'communications', 'computers', 'cool', 'courage', 'dad', 'dating', 'death', 'design', 'dreams', 'education', 'environmental', 'equality', 'experience', 'failure', 'faith', 'family', 'famous', 'fear', 'fitness', 'food', 'forgiveness', 'freedom', 'friendship', 'funny', 'future', 'god', 'good', 'government', 'graduation', 'great', 'happiness', 'health', 'history', 'home', 'hope', 'humor', 'imagination', 'inspirational', 'intelligence', 'jealousy', 'knowledge', 'leadership', 'learning', 'legal', 'life', 'love', 'marriage', 'medical', 'men', 'mom', 'money', 'morning', 'movies', 'success']


random_category = categories[random.randint(0,len(categories)-1)]

print(random_category)


api_url = 'https://api.api-ninjas.com/v1/quotes?category={}'.format(random_category)
response = requests.get(api_url, headers={'X-Api-Key': api_key})
if response.status_code == requests.codes.ok:

    print(response.json()[0]['quote'])
else:
    print("Error:", response.status_code, response.text)