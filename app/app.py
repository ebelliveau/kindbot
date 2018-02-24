import os
import serial
from flask import Flask
from flask import render_template, Response, request
from flask_ask import Ask, statement, session

app=Flask(__name__)
ask = Ask(app, '/')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    with open('/home/pi/kindbot/app/logs/kindbot.log', 'rb') as fl:
        last_rd = fl.read()
    read_dict = eval(last_rd)
    return render_template('dashboard.html', temp=read_dict['Temperature'], hum=read_dict['Humidity'],
    lux=read_dict['Lumens'])

@app.route('/camera')
def camera():
    pic_lst = ['../static/images/' + str(x) for x in os.listdir("static/images")]
    pic_lst.sort()
    pic_lst = pic_lst[::-1]
    return render_template('camera.html', pic_lst=pic_lst)

@app.route('/automate', methods=['POST', 'GET'])
def automate():
#    if request.form['button'] == "on":
#        print 'yass'
#    elif request.form['button'] == "off":
#        print 'poo'
    return render_template('automate.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')


############### Alexa Intents #################

@ask.intent('stats')
def stats():
    """ Returns last reading """
    with open('/home/pi/kindbot/app/logs/kindbot.log', 'rb') as fl:
        last_rd = fl.read()
    read_dict = eval(last_rd)
    speech_text = 'Last reading was taken at %s. The temperature is %s degrees Fahrenheit and humidity is at %s percent. The lux levels are %s.' % (read_dict['Time'], read_dict['Temperature'],read_dict['Humidity'], read_dict['Lumens'])
    return statement(speech_text)


@ask.intent('dripon')
def dripon():
    """ Turn switch on """
    arduinoSerialData = serial.Serial('/dev/ttyACM0',9600)
    arduinoSerialData.write('1')
    speech_text = 'Switch is on now'
    return statement(speech_text)

@ask.intent('dripoff')
def dripoff():
    """ Turn switch off """
    arduinoSerialData = serial.Serial('/dev/ttyACM0',9600)
    arduinoSerialData.write('0')
    speech_text = 'I have turned off the switch'
    return statement(speech_text)


@ask.intent('photo')
def photo():
    """ Show image of grow """
    pic_lst = ['/static/images/' + str(x) for x in os.listdir("static/images")]
    pic_lst.sort()
    last_pic = pic_lst[-1]
    pic_url = <your URL string> + last_pic
    speech_text = 'Here is your grow!'
    return statement(speech_text).display_render(template='BodyTemplate7', title='kindbot', backButton='HIDDEN', token=None, background_image_url=pic_url, text=None, hintText=None)


@ask.intent('schedule')
def schedule(date,time):
    with open('/home/pi/kindbot/app/logs/schedule.logs', 'a') as fl:
        ln = str(date) + ',' + str(time) + '\n'
        fl.write(ln)
    return statement("Ok. I've got it scheduled for {} at {}".format(date, time))


if __name__ == "__main__":
    app.run()
