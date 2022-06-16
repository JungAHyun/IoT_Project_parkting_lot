# 웹서버 프로그램 웹 브라우저에서 http://localhost:5000/로 접속하면 
# index.html을 실행하고 버튼을 이용하여 LED 작동시킴

import threading
from time import sleep
import time

from flask import Flask, request
from flask import render_template

import RPi.GPIO as GPIO

app = Flask(__name__)
# GPIO.setmode(GPIO.BOARD)                    #BOARD는 커넥터 pin번호 사용
# pin=8                                       # 7번 pin. 즉, GPIO4 사용
# GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW) 


#초음파 센서 세팅
GPIO.setmode(GPIO.BCM)                    #BOARD는 커넥터 pin번호 사용
trig_pin =14
echo_pin= 15
GPIO.setup(trig_pin, GPIO.OUT)
GPIO.setup(echo_pin, GPIO.IN)

GPIO.output(trig_pin, False)
print("Waiting for sensor to settle")
time.sleep(2)

@app.route("/")
def home():
    return render_template('parkting_lot_temp.html')


class Car():
    def __init__(self, carnum, carnum_distance):
        self.carnum = carnum
        self.carnum_distance = carnum_distance

    def get_car_num(self):
        return self.carnum

    def get_car_distance(self):
        return self.carnum_distance

    def change_distance(self, distance):
        self.carnum_distance = distance




def distance_senser_on(carnum_distance, carnum):
    global car

    car = Car(carnum, carnum_distance)

    try:
        while True: 			     
            GPIO.output(trig_pin, True)   # Triger 핀에  펄스신호를 만들기 위해 1 출력
            time.sleep(0.00001)       # 10µs 딜레이 
            GPIO.output(trig_pin, False)
            
            while GPIO.input(echo_pin)==0:
                start = time.time()	 # Echo 핀 상승 시간 
            while GPIO.input(echo_pin)==1:
                stop= time.time()	 # Echo 핀 하강 시간 
                
            check_time = stop - start
            distance = check_time * 34300 / 2
            print("Distance : %.1f cm" % distance)
            time.sleep(0.4)	# 0.4초 간격으로 센서 측정 

            
            carnum_distance = distance
            car.change_distance(int(distance))
            sleep(1)
            
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()



@app.route("/thread/start")  
def distance_thread_start():
    try:
        distanse_thread1 = threading.Thread(target=distance_senser_on, args = ("car1_distance", "car1") )     # Thread t1 생성
        distanse_thread1.start()    #스레드 시작
        return "thread start"
    except:
        return "thread fail"
    # distanse_thread2 = threading.Thread(target=distance_senser_on, arg = ("car2_distance", "car2"))     # Thread t1 생성
    # distanse_thread2.start()    #스레드 시작



@app.route("/distance/get")  
def get_distance():
    try:
        str_distance = str(car.get_car_distance())
        print(" get_Distance => ", str_distance)
        return str_distance
    except KeyboardInterrupt:
        # GPIO.cleanup()
        print("STOP")
        exit()

@app.route("/carnum/get")  
def get_carnum():
    try:
        str_carnum = str(car.get_car_num())
        print(" car num => ", str_carnum)
        return str_carnum
    except KeyboardInterrupt:
        # GPIO.cleanup()
        print("STOP")
        exit()





@app.route("/induction/on")                       # index.html에서 이 주소를 접속하여 해당 함수를 실행
def induction_on():
    try:
        global induction_state, induction_thread ,distance 
        distance = 50
        induction_state = 'on'
        # GPIO.output(led_pin,1)   # LED ON 
        print("인덕션 ON!")
        return "on complet"                    
    except :
        return "on fail"

induction_state = 'off'

@app.route("/induction/state_set")                       # index.html에서 이 주소를 접속하여 해당 함수를 실행
def induction_state_set():
    global induction_state
    try:
        if induction_state == 'on':
            print("on")
            return "induction is on"      # 함수가 'ok'문자열을 반환함
        else: 
            print("off")
            return "induction is off"  
    except :
        return "fail"


@app.route("/induction/off")                       # index.html에서 이 주소를 접속하여 해당 함수를 실행
def induction_off():
    try:
        global  induction_state
        # GPIO.output(led_pin,0)   # LED ON 
        print("인덕션 OFF!")
        induction_state = 'off'
        return "off complet"                        
    except :
        return "off fail"


if __name__ == "__main__":
    app.run(host="0.0.0.0")