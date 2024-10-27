import json
import random
import numpy as np
import nltk
import pickle
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import Adam
from nltk.stem import WordNetLemmatizer
import requests
from googlesearch import search
import webbrowser
import time
from pycricbuzz import Cricbuzz
import billboard
from pygame import mixer
import COVID19Py

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

# Load intents data
data_file = open('intents.json').read()
intents = json.loads(data_file)

# Prepare words and classes
words = []
classes = []
documents = []
ignore = ['?', '!', ',', "'s"]

for intent in intents['intents']:
    for pattern in intent['patterns']:
        w = nltk.word_tokenize(pattern)
        words.extend(w)
        documents.append((w, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

words = [lemmatizer.lemmatize(word.lower()) for word in words if word not in ignore]
words = sorted(list(set(words)))
classes = sorted(list(set(classes)))

# Save words and classes
pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))

# Prepare training data
training = []
output_empty = [0] * len(classes)

for doc in documents:
    bag = []
    pattern = doc[0]
    pattern = [lemmatizer.lemmatize(word.lower()) for word in pattern]
    
    for word in words:
        bag.append(1 if word in pattern else 0)
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1
    
    training.append([bag, output_row])

random.shuffle(training)
training = np.array(training)  
X_train = list(training[:, 0])
y_train = list(training[:, 1])  

# Create the model
model = Sequential()
model.add(Dense(128, activation='relu', input_shape=(len(X_train[0]),)))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(y_train[0]), activation='softmax'))

# Compile the model
adam = Adam(0.001)
model.compile(optimizer=adam, loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(np.array(X_train), np.array(y_train), epochs=200, batch_size=10, verbose=1)

# Save the model
model.save('mymodel.h5')

# Load the model and data
from keras.models import load_model
model = load_model('mymodel.h5')
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))

# Helper functions
def clean_up(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def create_bow(sentence, words):
    sentence_words = clean_up(sentence)
    bag = np.zeros(len(words), dtype=int)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
    return bag.reshape(1, -1)  # Ensure bag is 2D

def predict_class(sentence, model):
    p = create_bow(sentence, words)
    res = model.predict(p)[0]  # p is already 2D
    threshold = 0.8
    results = [[i, r] for i, r in enumerate(res) if r > threshold]
    results.sort(key=lambda x: x[1], reverse=True)

    return_list = []
    for result in results:
        return_list.append({'intent': classes[result[0]], 'prob': str(result[1])})
    return return_list

def get_response(return_list, intents_json):
    if len(return_list) == 0:
        tag = 'noanswer'
    else:    
        tag = return_list[0]['intent']
    
    if tag == 'datetime':        
        return time.strftime("%A") + ", " + time.strftime("%d %B %Y") + ", " + time.strftime("%H:%M:%S")

    if tag == 'google':
        query = input('Enter query: ')
        for url in search(query, tld="co.in", num=1, stop=1, pause=2):
            webbrowser.open("https://google.com/search?q=%s" % query)
        return "Google search completed."

    if tag == 'weather':
        api_key = '832f4cd2d19db9710943b270621a53c9'  # Add your OpenWeatherMap API key here
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        city_name = input("Enter city name: ")
        complete_url = base_url + "appid=" + api_key + "&q=" + city_name
        response = requests.get(complete_url)
        x = response.json()
        return f'Present temp: {round(x["main"]["temp"] - 273, 2)} Celsius, Feels Like: {round(x["main"]["feels_like"] - 273, 2)} Celsius, Weather: {x["weather"][0]["main"]}'

    if tag == 'news':
        main_url = "http://newsapi.org/v2/top-headlines?country=in&apiKey=635b394344b844dd90a8f75defeeb78f"  # Add your NewsAPI key here
        open_news_page = requests.get(main_url).json()
        article = open_news_page["articles"]
        results = []
        for ar in article: 
            results.append([ar["title"], ar["url"]]) 
        return "\n".join(f"{i + 1}: {results[i][0]} - {results[i][1]}" for i in range(min(10, len(results))))

    if tag == 'cricket':
        c = Cricbuzz()
        matches = c.matches()
        return "\n".join(f"{match['srs']} {match['mnum']} {match['status']}" for match in matches)

    if tag == 'song':
        chart = billboard.ChartData('hot-100')
        return "\n".join(f"{song.title} - {song.artist}" for song in chart[:10])

    if tag == 'timer':        
        mixer.init()
        x = input('Minutes to timer: ')
        time.sleep(float(x) * 60)
        mixer.music.load('Handbell-ringing-sound-effect.mp3')
        mixer.music.play()
        return "Timer ended!"

    if tag == 'covid19':
        covid19 = COVID19Py.COVID19(data_source='jhu')
        country = input('Enter Location: ')
        
        if country.lower() == 'world':
            latest_world = covid19.getLatest()
            return f'Confirmed: {latest_world["confirmed"]}, Deaths: {latest_world["deaths"]}'
        
        else:
            latest = covid19.getLocations()
            latest_conf = []
            latest_deaths = []
            for location in latest:
                if location['country'].lower() == country.lower():
                    latest_conf.append(location['latest']['confirmed'])
                    latest_deaths.append(location['latest']['deaths'])
            return f'Confirmed: {np.sum(latest_conf)}, Deaths: {np.sum(latest_deaths)}'

    # Get a random response from the intent's responses
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if tag == i['tag']:
            return random.choice(i['responses'])
    
    return "Sorry, I didn't understand that."

def response(text):
    return_list = predict_class(text, model)
    response = get_response(return_list, intents)
    return response

# Start the chatbot
while True:
    x = input()
    print(response(x))
    if x.lower() in ['bye', 'goodbye', 'get lost', 'see you']:  
        break

# Self-learning feature
print('Help me Learn?')
tag = input('Please enter the general category of your question: ')
flag = -1
for i in range(len(intents['intents'])):
    if tag.lower() in intents['intents'][i]['tag']:
        intents['intents'][i]['patterns'].append(input('Enter your message: '))
        intents['intents'][i]['responses'].append(input('Enter expected reply: '))
        flag = 1

if flag == -1:
    intents['intents'].append(
        {'tag': tag,
         'patterns': [input('Please enter your message: ')],
         'responses': [input('Enter expected reply: ')]}
    )

# Save updated intents
with open('intents.json', 'w') as outfile:
    outfile.write(json.dumps(intents, indent=4))