
# IoT Temperature Read with ESP32 & RaspberryPI NodeJS(ExpressJS) & Python & NextJS


[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/DJFRS/Lora-Esp32-Nodejs-RPI)

## Parts

- 1 x ESP32 Dev modules
- 1 x RaspberryPI 2 B
- 1 x Char LCD 2*16 with i2c ic
- 1 x Char LCD 2*16
- 2 x LORA-RA02(Sx1278)
- 2 x 2.4GHZ Antena 3dbi with converter cable
- 3 x push button with 10k resistor pull down
- 4 x led 2 on esp32 2 on pi (on esp32 for send signal and else)(on pi for app running and receive)
- 1 x wifi adapter usb
- 1 x DS18B20 with 4.7k resistor

The PINOUT file for ESP32 and PI is available in each directory
## Installation ESP32
First, add ESP32 to your list of boards in Arduino

Then install the following libraries

```bash
  DallasTemperature
  LiquidCrystal_I2C
  RH_RF95
```
Then compile the code and transfer it to the board.


## Installation PI

First, we clone all the codes in Raspberry Pi

```bash
  git clone https://github.com/DJFRS/Lora-Esp32-Nodejs-RPI.git
```
Then we have to ensure the installation of Python 3.9 and NodeJS 16, if the version is not available, update it.

```bash
  python3 -V
  python3 -m pip -v
  node -v
  npm -V
```
Then we need to install yarn

```bash
  npm install --global yarn
```
Then enter the Python directory and install the modules
```bash
  cd Lora-Esp32-Nodejs-RPI
  cd pi
  cd Python
  python3 -m pip install -r requirements.txt
```
Then we need to install the NodeJS and NextJS packages
```bash
  cd ..
  cd nodejs
  cd nextjs-iot-core
  yarn install
  cd .. 
  cd nodejs-iot-core
  yarn install

```
You need to enter nodejs server ip in nextjs and python

in python 
```bash
  Lora-Esp32-Nodejs-RPI
    └── pi
        └── python
            └── main.py
```
Set the server line and port according to nodejs
```python
device_name="sen1"
server_ip="127.0.0.1"
server_port=81
```

in Nextjs 
```bash
  Lora-Esp32-Nodejs-RPI
    └── pi
        └── nodejs
            └── nextjs-iot-core
                └── next.config.js
```
Set the server line and port according to nodejs
```js
env: {
    serverUrl: "127.0.0.1:81",
  },
```

You can run nodejs and nextjs server on different servers

But you can't Python. It must be launched on Raspberry Pi

Now it's time to start the server

You have to run each section separately in different terminals and simultaneously

First NodeJS
```bash
cd Lora-Esp32-Nodejs-RPI
cd pi
cd nodejs
cd nodejs-iot-core
yarn start
```
Start nextjs
```bash
cd Lora-Esp32-Nodejs-RPI
cd pi
cd nodejs
cd nextjs-iot-core
yarn build
yarn start
```
Start python
```bash
cd Lora-Esp32-Nodejs-RPI
cd pi
cd python
python3 main.py
```

You should also turn on the transmitter board.

## 🔗 Links
[![portfolio](https://img.shields.io/badge/my_portfolio-000?style=for-the-badge&logo=ko-fi&logoColor=white)](https://github.com/DJFRS)
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/farbod-rostamsolat-453161151/)
[![twitter](https://img.shields.io/badge/twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://twitter.com/FRS_DJ)



