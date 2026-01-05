from flask import Flask, render_template, request
# from weather import get_current_weather
from waitress import serve
from strmqtt_Class import MqttApp
import time


app = Flask(__name__)
Mq = MqttApp()

@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index():
    print(f'---RUN server/index() RUN----')    
    # return ('BlackBox0 TEXT')
    return render_template('index.html')


@app.route('/myaction')
def maction():
    psw = request.args.get('psw').lower()
    print(f'--reload myaction.html--psw: {psw} SUBMIT---***')
    if psw != "strak" :
        return render_template('index.html')
    return action('psw', psw )
    
def action(subject ,data):
    #print(f'- - action ( subject={subject} :: data={data} ) ***')
    if not Mq.connection_ok:
        Mq.connect_broker()  
    # if  Mq.connection_ok:
    #     Mq.publish('InfoUpdate','1')
    
    topic_values = Mq.get_topic_values()
    #print(f'--- new data: {topic_values}')
    #print(f'action->RENDER myaction.html : subject={subject} :: data={data}***')
    return render_template('myaction.html',
                           title=data,
                           isalive=topic_values["isalive"],                          
                           WillTopic=topic_values["WillTopic"],
                           teploty=topic_values["teploty"],
                           pir=topic_values["pir"],
                           TeplarnaStav = topic_values["TeplarnaStav"],
                           InfoUpdate = topic_values["InfoUpdate"],
                           TeplarnaOnOff = topic_values["TeplarnaOnOffSubs"],
                           STRAKbeep = topic_values["STRAKbeep"]
                           )

    
@app.route('/action_password')
def action_password():
    print(f'---RUN action_password() RUN----')    
    # return ('BlackBox0 TEXT')
    return render_template('action_password.html')
 

@app.route('/button_stop')
def stop_action():
    #psw = request.args.get('psw')
    print(f'***STOP***STOP***STOP***STOP***STOP***')
    #return action('stop', 1)
    Mq.disconnect_broker()
    print(f'- -  *** DISCONNECT mqtt broker!')
    return render_template('index.html')   


@app.route('/action_confirm')
def action_confirm():
    #action_confirm?cmd=other&psw=alfa
    cmd = request.args.get('cmd')
    psw = request.args.get('psw')
    psw = psw.lower()
    print(f'*** RUNNING: action_confirm()---{cmd} / {psw}---***')

    if psw != "strak":
      #return action('psw', psw )
      return render_template('index.html')
    
    if cmd == 'update':
        Mq.publish('InfoUpdate','1')
    elif cmd == 'beep_On':
        Mq.publish('STRAKbeep','1')
    elif cmd == 'TeplarnaOnOff_Off':
        Mq.publish('TeplarnaOnOff','Off') 
    ##	mqttClient20.Publish(&S"TeplarnaOnOff",&S"Off",1)
    #   Mq.publish('TeplarnaONOff','Off') 
        print(f'*** publish( --{cmd}***')
    elif cmd == 'TeplarnaOnOff_On':
        Mq.publish('TeplarnaOnOff','On')
    ##	mqttClient20.Publish(&S"TeplarnaOnOff",&S"On",1)
     #   Mq.publish('TeplarnaOnOff','On') 
        print(f'*** publish( --{cmd}***')
    elif cmd == 'other':
    #    Mq.publish('STRAKbeep',1)
        #print(f'***OTHER--{cmd}***')
        print(f'*** cmd OTHER(: --{cmd}***')
    else:
        print(f'*** ELSE : --{cmd}***')
    return render_template('action_confirm.html',  cmd=cmd, psw=psw)


@app.route('/myaction_confirm')
def maction_confirm():
    return action('psw', 'strak' )
    
    # return render_template('action_password.html')
    # return render_template('index.html')



# @app.route('/button_HeatOn')
# def heaton_action():
#     #psw = request.args.get('psw')
#     print(f'***HEAT_ON***HEAT_ON***HEAT_ON***HEAT_ON***HEAT_ON***')
#     return action('TeplarnaOnOff', 'On' )
#
# app.route('/button_HeatOff')
# def update_action():
#     #psw = request.args.get('psw')
#     print(f'***HEAT_OFF***HEAT_OFF***HEAT_OFF***HEAT_OFF***HEAT_OFF***')
#     return action('TeplarnaOnOff', 'Off' )



@app.route('/xxxxxxx', methods=["GET", "POST"])
def home():
    print(f'BEEP-BEEP-BEEP-BEEP-BEEP-')
    if request.method == "POST":
        if "my_bep" in request.form:
                # name = request.args.get('name')
                print(f'***BEEP***BEEP***BEEP***BEEP***BEEP***')
                Mq.publish('STRAKbeep',1)
    
    topic_values = Mq.get_topic_values()
    #print(f'--- new data: {topic_values}')
    
    print(f'---RENDER server/myaction()----')
    # return action('none', 0)
    return render_template('myaction.html')




if __name__ == "__main__":
    # app.run( host="0.0.0.0", port=8000)
    serve(app, host="0.0.0.0", port=8000) #waitress module
    

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

"""OLD 
@app.route('/button_beep', methods=['POST'])
def beep_action():
    #psw = request.args.get('psw')
    print(f'***BEEP***BEEP***BEEP***BEEP***BEEP***')
    #return action('beep', 1 )
    Mq.publish('STRAKbeep',1)
    # Mq.publish('STRAKbeep','1')
 """
    
    
    # # return render_template("index.html", message=message)
  
    #psw = request.args.get('psw')
    # Mq.publish('STRAKbeep','1')


""" EXAMPLE
@app.route("/", methods=["GET", "POST"])
def home():
    message = ""
    if request.method == "POST":
        if "my_button" in request.form:
            message = "Button clicked!"
    return render_template("index.html", message=message)
 """
