from machine import Pin, PWM
import time
import xbee

DUTY_CYCLE_MAX = 1023
DUTY_CYCLE_MIN = 0
DUTY_CYCLE_STEP = 200
current_duty_cycle = DUTY_CYCLE_MIN

max_speed = 300
max_direction = DUTY_CYCLE_MAX

stby = Pin("D4", Pin.OUT)

# Motor A layout
ain1 = Pin("D11", Pin.OUT)
ain2 = Pin("D1", Pin.OUT)
apwm = PWM(Pin(Pin.board.P0, Pin.OUT, value=0))

# Motor B layout
bin1 = Pin("P2", Pin.OUT)
bin2 = Pin("D3", Pin.OUT)
bpwm = PWM(Pin(Pin.board.P1, Pin.OUT, value=0)) # PWM Pin1 muss in XCTU konfiguriert werden!

# initialize states
ain1.value(0)
ain2.value(0)

bin1.value(0)
bin2.value(0)

stby.value(0)

run = True
car_on = False


def controlSpeed(speed):
    if -0.04 <= speed <= 0.04:  # car hold
        ain1.value(0)
        ain2.value(0)
        apwm.duty(0)
    elif speed > 0:  # car drive forward
        ain1.value(1)
        ain2.value(0)
        apwm.duty(speed)
    elif speed < 0:  # car drive backward
        ain1.value(0)
        ain2.value(1)
        apwm.duty(-speed)


def controlDirection(direction):
    if -0.04 <= direction <= 0.04:  # car direction straight
        bin1.value(0)
        bin2.value(0)
        bpwm.duty(0)
    elif direction > 0:  # car direction right
        bin1.value(1)
        bin2.value(0)
        bpwm.duty(direction)
    elif direction < 0:  # car direction left
        bin1.value(0)
        bin2.value(1)
        bpwm.duty(-direction)


print(" +----------------------------------------+")
print(" | XBee MicroPython Remote Car |")
print(" +----------------------------------------+\n")
print("Waiting for data...\n")

while run:
    received_msg = xbee.receive()
    if received_msg:
        # sender = received_msg['sender_eui64']
        payload = received_msg['payload']
        payload = payload.decode("utf8")
        print(payload)

        data = payload.split(",")
        if data[0] == "W":
            if data[1] == "1":
                controlSpeed(max_speed)
            else:
                controlSpeed(0)

        elif data[0] == "A":
            if data[1] == "1":
                controlDirection(max_direction)
            else:
                controlDirection(0)

        elif data[0] == "S":
            if data[1] == "1":
                controlSpeed(-max_speed)
            else:
                controlSpeed(0)

        elif data[0] == "D":
            if data[1] == "1":
                controlDirection(-max_direction)
            else:
                controlDirection(0)

        elif data[0] == "T" and data[1] == "1":
            print("Fahre fuer 1 Meter")

        elif data[0] == "Q" and data[1] == "1":
            if not car_on:
                print("Motor wurde eingeschaltet!")
                car_on = True
                stby.value(1)
            elif car_on:
                print("Motor wurde ausgeschaltet!")
                car_on = False
                stby.value(0)

        elif data[0] == "P" and data[1] == "1":
            print("Auto wurde geparkt!")
            run = False

# while current_duty_cycle < DUTY_CYCLE_MAX:
#     current_duty_cycle = current_duty_cycle + DUTY_CYCLE_STEP
#     if current_duty_cycle > DUTY_CYCLE_MAX:
#         current_duty_cycle = DUTY_CYCLE_MAX
#     apwm.duty(current_duty_cycle)
#     time.sleep(wait)
#
#     # Keep at maximum 2 seconds.
# time.sleep(wait)
#
# # Decrease the duty cycle to the minimum value.
# while current_duty_cycle > DUTY_CYCLE_MIN:
#     current_duty_cycle = current_duty_cycle - DUTY_CYCLE_STEP
#     if current_duty_cycle < DUTY_CYCLE_MIN:
#         current_duty_cycle = DUTY_CYCLE_MIN
#     apwm.duty(current_duty_cycle)
#     time.sleep(wait)
#
#     # Keep at maximum 2 seconds.
#     time.sleep(wait)
#
#
#
#     # Keep at maximum 2 seconds.
# time.sleep(wait)
