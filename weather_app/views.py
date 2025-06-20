from django.shortcuts import render, redirect
import requests

def index(request):
    weather_data = {}
    favorites = request.session.get('favorites', [])

    if request.method == 'POST':
        fav = request.POST.get('favorite_city')
        city = request.POST.get('city')
        remove = request.POST.get('remove_city')
        language = request.POST.get('language', 'en')

        # ⭐ Handle saving favorite
        if fav:
            if fav not in favorites:
                favorites.append(fav)
                request.session['favorites'] = favorites
            # Don't return here; maybe city is also posted
         # ❌ Remove favorite city
        if remove:
            if remove in favorites:
                favorites.remove(remove)
                request.session['favorites'] = favorites
            return redirect('index')
        # 🌤️ Handle fetching weather for city
        if city:
            API_KEY = '50411742cf9597bde19ec36cced3e832'
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang={language}"
            response = requests.get(url)
            data = response.json()
            if data.get("cod") == 200:
                weather_data = {
                    'city': data['name'],
                    'temperature': data['main']['temp'],
                    'description': data['weather'][0]['description'],
                    'humidity': data['main']['humidity'],
                    'wind': data['wind']['speed'],
                    'condition': data['weather'][0]['main'].lower(),
                }
            else:
                weather_data['error'] = "City not found"

    return render(request, 'weather_app/one.html', {
        'weather': weather_data,
        'favorites': favorites
    })
