from time import sleep
from SX127x.LoRa import *
import RPi.GPIO as GPIO
from SX127x.board_config import BOARD
from subprocess import Popen, PIPE
import http.client
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd
device_name="sen1"
server_ip="127.0.0.1"
server_port=81
def find_interface():
    find_device = "ip addr show"
    interface_parse = run_cmd(find_device)
    for line in interface_parse.splitlines():
        if "state UP" in line:
            dev_name = line.split(':')[1]
    return dev_name
def parse_ip():
    find_ip = "ip addr show %s" % interface
    find_ip = "ip addr show %s" % interface
    ip_parse = run_cmd(find_ip)
    for line in ip_parse.splitlines():
        if "inet " in line:
            ip = line.split(' ')[5]
            ip = ip.split('/')[0]
    return ip
def run_cmd(cmd):
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output.decode('ascii')

sleep(2)
led_grean=16
led_blue=12
lcd_columns = 16
lcd_rows = 2
lcd_rs = digitalio.DigitalInOut(board.D21)
lcd_en = digitalio.DigitalInOut(board.D20)
lcd_d4 = digitalio.DigitalInOut(board.D26)
lcd_d5 = digitalio.DigitalInOut(board.D19)
lcd_d6 = digitalio.DigitalInOut(board.D13)
lcd_d7 = digitalio.DigitalInOut(board.D6)
lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6,lcd_d7, lcd_columns, lcd_rows)
lcd.clear()

GPIO.setwarnings(False)
GPIO.setup(led_grean, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(led_blue, GPIO.OUT, initial=GPIO.LOW)

GPIO.output(led_grean, GPIO.HIGH)

interface = find_interface()
ip_address = parse_ip()

BOARD.setup()

def lcdWriter(lcd_line_1):
    
    lcd_line_2 = "" + ip_address
    lcd.message = "T:"+lcd_line_1+"C R:"+str(lora.get_rssi_value())+"\n" + lcd_line_2 

class LoRaRcvCont(LoRa):

    def __init__(self, verbose=False):

        super(LoRaRcvCont, self).__init__(verbose)

        self.set_mode(MODE.SLEEP)

        self.set_dio_mapping([0] * 6)


    def start(self):

        self.reset_ptr_rx()

        self.set_mode(MODE.RXCONT)

        while True:

            sleep(.5)

            rssi_value = self.get_rssi_value()
            
            status = self.get_modem_status()
            # print("status: ",status)
            sys.stdout.flush()

            


    def on_rx_done(self):
        GPIO.output(led_blue, GPIO.HIGH)
        print("\nReceived: ")

        self.clear_irq_flags(RxDone=1)

        payload = self.read_payload(nocheck=True)
        stringData=bytes(payload).decode("utf-8",'ignore')
        print(payload)
        tmp=stringData[:-4][2:]
        print(tmp+" C")
        lcdWriter(tmp)
        self.set_mode(MODE.SLEEP)

        self.reset_ptr_rx()
        
        self.set_mode(MODE.RXCONT) 

        GPIO.output(led_blue, GPIO.LOW)
        conn = http.client.HTTPConnection(server_ip, server_port)
        payload = ''
        headers = {}
        conn.request("GET", "/setdata?name="+device_name+"&tmp="+tmp, payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))



lora = LoRaRcvCont(verbose=False)

lora.set_mode(MODE.STDBY)

lora.set_pa_config(pa_select=1)


try:

    lora.start()

except KeyboardInterrupt:

    sys.stdout.flush()

    print("")

    sys.stderr.write("KeyboardInterrupt\n")

finally:

    sys.stdout.flush()

    print("")

    lora.set_mode(MODE.SLEEP)

    BOARD.teardown()

