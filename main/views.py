import requests
from django.shortcuts import render
from main.models import City
from main.forms import CityForm

def index_page(request):
    appid = 'adef32d66669f8b5bbb100a83e95b9bf'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + appid

    error_message = None
    all_cities = []

    if(request.method == 'POST'):
        form = CityForm(request.POST)
        if form.is_valid():
            form.save()


            city_name = form.cleaned_data['name']
            try:
                res = requests.get(url.format(city_name)).json()

                if res.get("cod") != 200:

                    city_info = {
                        'city': city_name,
                        'temp': res["main"]["temp"],
                        'icon': res["weather"][0]["icon"]
                    }
                    all_cities.append(city_info)
                    if not any(city_info['city'] == c['city'] for c in all_cities):
                        all_cities.append(city_info)
                else:
                    pass

            except Exception as e:
                error_message = "City not found"

    form = CityForm()

    cities = City.objects.order_by('-date')

    for city in cities:
        try:
            res = requests.get(url.format(city.name)).json()

            if res.get("cod") == 200:
                city_info = {
                    'city': city.name,
                    'temp': res["main"]["temp"],
                    'icon': res["weather"][0]["icon"]
                }
                all_cities.append(city_info)
            else:
                continue

        except Exception as e:
            error_message = "City not found "

    context = {
        'all_info': all_cities,
        'form': form,
        'error_message': error_message
    }

    return render(request, 'main/index.html', context)
