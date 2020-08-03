from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd

# Create your views here.
def index(request):
    return render(request, 'index.html')

def calculate(request):
    compatible_pokemon = []
    stats = []

    stats.append(request.GET['hp'])
    stats.append(request.GET['attack'])
    stats.append(request.GET['defense'])
    stats.append(request.GET['sp_attack'])
    stats.append(request.GET['sp_defense'])
    stats.append(request.GET['speed'])
    stats.append(request.GET['capture_rate'])
    stats.append(request.GET['weight'])
    stats.append(request.GET['height'])

    data = pd.read_csv('prediction/pokemon.csv')
    data['weight_kg'].fillna(data.weight_kg.mean() - 40, inplace=True)
    data['height_m'].fillna(data.height_m.mean() - 0.3, inplace=True)

    pokemon_error_dict = dict()
    for i in range(len(data.index)):
        error = abs(
            abs((int(data.hp[i]) - int(stats[0]))) +
            abs((int(data.attack[i]) - int(stats[1]))) +
            (abs((int(data.defense[i]) - int(stats[2]))) / 8) +
            abs((int(data.sp_attack[i]) - int(stats[3]))) +
            (abs((int(data.sp_defense[i]) - int(stats[4]))) / 8) +
            abs((int(data.speed[i]) - int(stats[5]))) +
            (abs((int(data.capture_rate[i]) - int(stats[6]))) / 5) +
            (abs((float(data.weight_kg[i]) - float(stats[7]))) / 5) +
            (abs((float(data.height_m[i]) - float(stats[8]))) * 10)
        )
        pokemon_error_dict[data.name[i]] = error
    pokemon_compatibility = sorted(pokemon_error_dict.items(), key = lambda x: x[1])
    for pokemon in pokemon_compatibility[:6]:
        compatible_pokemon.append(pokemon[0])
    for pokemon in pokemon_compatibility[-1:-7:-1]:
        compatible_pokemon.append(pokemon[0])
    return render(request, 'result.html', 
        {'compatible_pokemon': compatible_pokemon},
    )