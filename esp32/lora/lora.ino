#include <SPI.h>
#include <RH_RF95.h>
#include <OneWire.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <DallasTemperature.h>

#define RFM95_CS 15
#define RFM95_RST 4
#define RFM95_INT 26

#define RF95_FREQ 434.0

#define GREAN_LED 25
#define RED_LED 33

#define ONE_WIRE_BUS 27

RH_RF95 rf95(RFM95_CS, RFM95_INT);

LiquidCrystal_I2C lcd(0x3F, 16, 2);

OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);


void setup()
{
  Serial.begin(9600);

  pinMode(GREAN_LED, OUTPUT);
  digitalWrite(GREAN_LED, LOW);
   
  lcd.begin();
  lcd.backlight();
  lcd.clear();
  lcd.print("Booting...");
  
  pinMode(RFM95_RST, OUTPUT);
  digitalWrite(RFM95_RST, LOW);
  delay(10);
  digitalWrite(RFM95_RST, HIGH);
  delay(10);

  sensors.begin();

  while (!rf95.init()) {
    Serial.println("LoRa radio init failed");
    lcd.print("LoRa radio init failed");
    while (1);
  }
  if (!rf95.setFrequency(RF95_FREQ)) {
    Serial.println("setFrequency failed");
    lcd.print("setFrequency failed");
    while (1);
  }
  rf95.setTxPower(18);
}
void loop()
{
  digitalWrite(GREAN_LED, LOW);
  sensors.requestTemperatures();
  float tempC = sensors.getTempCByIndex(0);
  
    if(tempC == DEVICE_DISCONNECTED_C) 
  {
    lcd.clear();
    Serial.println("Error: Could not read temperature data");
    lcd.print("Error:Could not \n read tmp data");
    delay(1000);
    return;
  }
  String results = ""; 
  results.concat(tempC);
  
  lcd.clear();
  String res="TMP:"+results+" C";
  lcd.print(res);
  
  uint8_t dataArray[res.length()];
  for(int i=0;i++;i<=sizeof(dataArray)){
    dataArray[i]=0;
  }
  
  results.getBytes(dataArray, sizeof(dataArray));
//  uint8_t data[4] = { highByte(results), lowByte(results)};

  rf95.send(dataArray, sizeof(dataArray));
  rf95.waitPacketSent();
  digitalWrite(GREAN_LED, HIGH);
  delay(50);
}
