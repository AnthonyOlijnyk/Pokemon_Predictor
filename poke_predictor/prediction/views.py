from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from joblib import dump, load

# Create your views here.
def index(request):
    return render(request, 'index.html')

def calculate(request):

    pokemon_info = []

    hp = request.GET['hp']
    attack = request.GET['attack']
    defense = request.GET['defense']
    sp_attack = request.GET['sp_attack']
    sp_defense = request.GET['sp_defense']
    speed = request.GET['speed']
    capture_rate = request.GET['capture_rate']
    height = request.GET['height']

    data = pd.read_csv('prediction/pokemon.csv')
    data = data[:721]
    data['height_m'].fillna(data.height_m.mean() - 0.3, inplace=True)

    lookup_pokemon_name = dict(zip(data.pokedex_number.unique(), data.name.unique()))

    knn = load('prediction/pokemon_classifier.joblib')
    pokemon_name = lookup_pokemon_name.get(knn.predict([[
        hp,
        attack,
        defense,
        sp_attack,
        sp_defense,
        speed,
        capture_rate,
        height
    ]])[0])
    pokemon_number = str(knn.predict([[
        hp,
        attack,
        defense,
        sp_attack,
        sp_defense,
        speed,
        capture_rate,
        height
    ]])[0])

    pokemon_info.append(pokemon_name)
    pokemon_info.append(pokemon_number)

    return render(request, 'result.html', 
        {'pokemon_info': pokemon_info}
    )