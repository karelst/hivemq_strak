from flask import Flask, render_template, request
# from weather import get_current_weather
from waitress import serve
import strmqtt_bg
import time

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    print(f'---RUN server/index() RUN----')    
    # return ('BlackBox0 TEXT')
    return render_template('index.html')


"""
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
 """

# @app.route('/button_click', methods=['POST'])
# # @app.route('/button_click')
# def button_click():
#     print(f' ButtonClick SUBMIT---***')  
#     return #"Button Clicked!"

@app.route('/myaction')
def maction():
    psw = request.args.get('psw')
    print(f'{psw} SUBMIT---***')
    return action('psw', psw )


@app.route('/button_update')
def update_action():
    #psw = request.args.get('psw')
    print(f'***UPDATE*************************************')
    return action('update', 1 )

app.route('/button_beep?')
def update_action():
    #psw = request.args.get('psw')
    print(f'***BEEP***BEEP***BEEP***BEEP***BEEP***')
    return action('beep', 1 )

app.route('/button_stop')
def update_action():
    #psw = request.args.get('psw')
    print(f'***STOP***STOP***STOP***STOP***STOP***')
    return action('stop', 1 )

# app.route('/button_HeatOn')
# def update_action():
#     #psw = request.args.get('psw')
#     print(f'***HEAT_ON***HEAT_ON***HEAT_ON***HEAT_ON***HEAT_ON***')
#     return action('TeplarnaOnOff', 'On' )


# app.route('/button_HeatOff')
# def update_action():
#     #psw = request.args.get('psw')
#     print(f'***HEAT_OFF***HEAT_OFF***HEAT_OFF***HEAT_OFF***HEAT_OFF***')
#     return action('TeplarnaOnOff', 'Off' )


def action(subject ,data):
    print(f'{subject} :: {data}***')
    # 
    
    strmqtt_bg.connect_broker()
    
    #time.sleep(6)
    # strmqtt_bg.disconnect_broker(client)
    # 
    if subject == 'update':
        strmqtt_bg.publish('InfoUpdate',1)
        #strmqtt_bg.publish('InfoUpdate','1')
    elif subject == 'beep':
        strmqtt_bg.publish('STRAKbeep',1)
        # strmqtt_bg.publish('STRAKbeep','1')
    # elif subject == 'TeplarnaOnOff':
    #     msg ='On' if data == 'On' else 'Off'
    #     strmqtt_bg.publish('TeplarnaOnOff',msg)
    elif subject == 'stop':
        strmqtt_bg.disconnect_broker()
       
    
    topic_values = strmqtt_bg.get_topic_values()

    # print(f'{psw} strmqtt_bg  {strmqtt_bg.topic_values["isalive"]}')
    # print(f'*****{topic_values["teploty"]}  strmqtt_bg:  {strmqtt_bg.topic_values["teploty"]}************')
    print(f'--- new data: {topic_values}')
    
    # strmqtt_bg.disconnect_broker(client)
    
       
    # time.sleep(2)
    
    print(f'---RENDER server/myaction()----')
    return render_template('myaction.html',
                           title=data,
                           isalive=topic_values["isalive"],                          
                           WillTopic=topic_values["WillTopic"],
                           teploty=topic_values["teploty"],
                           pir=topic_values["pir"],
                           TeplarnaStav = topic_values["TeplarnaStav"],
                           InfoUpdate = topic_values["InfoUpdate"],
                           TeplarnaOnOff = topic_values["TeplarnaOnOff"],
                           STRAKbeep = topic_values["STRAKbeep"]
                           
                           )






if __name__ == "__main__":
    # app.run( host="0.0.0.0", port=8000)
    serve(app, host="0.0.0.0", port=8000) #waitress module
    
