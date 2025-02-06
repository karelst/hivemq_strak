from flask import Flask, render_template, request
from weather import get_current_weather
from waitress import serve

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    print(f'---RUN server/index() RUN----')    
    # return ('BlackBox0 TEXT')
    return render_template('index.html')


@app.route('/weather')
def get_weather():
    print(f'---RUN server/get_weather() RUN----')
    # http://localhost:8000/weather?city=oslo
    city= request.args.get('city')
    print(f'{city} SUBMIT*******************')
    
    # Check for empty strings or string with only spaces
    if not bool(city.strip()):
        # You could render "City Not Found" instead like we do below
        city = "Praha"

    weather_data = get_current_weather(city)

    # City is not found by API
    if not weather_data['cod'] == 200:
        return render_template('city-not-found.html')

    return render_template(
        "weather.html",
        title=weather_data["name"],
        status=weather_data["weather"][0]["description"].capitalize(),
        temp=f"{weather_data['main']['temp']:.1f}",
        feels_like=f"{weather_data['main']['feels_like']:.1f}"
    )


@app.route('/myaction')
def maction():
    print(f'---RUN server/myaction() RUN----')
    return render_template('myaction.html')


if __name__ == "__main__":
    # app.run( host="0.0.0.0", port=8000)
    serve(app, host="0.0.0.0", port=8000) #waitress module
    
