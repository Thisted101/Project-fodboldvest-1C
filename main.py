from machine import Pin, I2C
from machine import PWM
import umqtt_robust2 as mqtt
import ssd1306
from time import sleep
import ADC
import neopixel
import mpu6050
import gps_funktion


#Initialisering af I2C objekt
mpu_i2c = I2C(scl=Pin(22), sda=Pin(21))    
mpu = mpu6050.accel(mpu_i2c)

mpu = mpu6050.accel(mpu_i2c)
fald_status = False
Antal_Fald = 0
X = mpu.get_values()["GyZ"]



# OLED identification
i2c =I2C(-1,scl=Pin(26), sda=Pin(27)) # Pins of LED display goes here
oled = ssd1306.SSD1306_I2C(128, 64, i2c, 0x3c)

# # Neopixel identification
n = 8
p = 18
np = neopixel.NeoPixel(Pin(p), n)



while True:
    try: 
#		batteri adafruit
        mqtt.web_print(ADC.get_battery())
        # opret feed 'KasperBond213/feeds/IoT-Vest_Feed
#		SSD1306 OLED KODE		
        print("Step 1: OLED CODE INITIATE")
        oled.fill(0)
        bat = str(ADC.get_battery())+" %"
        oled.text(bat, 30,10,)
        oled.text('Battery left',15,30)
        oled.show()
        sleep(3)
    
#			GPS KODE			  
        print("Step 2: GPS CODE INITIATE")
        gps_data = gps_funktion.gps_to_adafruit
        print(f"\ngps_data er: {gps_data}")
        mqtt.web_print(gps_data, 'KasperBond213/feeds/IoT-Vest_Feed/csv')    
        sleep(3)

#			NEOPIXEL KODE			  
        print("Step 3: NEOPIXEL INITIATE")
        np[0] = (0, 50, 50,)
        np[1] = (50, 0, 50,)
        np[2] = (0, 50, 50,)
        np[3] = (50, 0, 50,)
        np[4] = (0, 50, 50,)
        np[5] = (50, 0, 50,)
        np[6] = (0, 50, 50,)
        np[7] = (250, 0, 0,)
        np.write()

    
#			IMU OG NEOPIXEL KODE			  
        print("Step 4: IMU AND NEOPIXEL INITIATE")
        print(mpu.get_values())
#     if fald_status == False and X >= 0:
#         fald_status = True
#         Antal_Fald = Antal_Fald + 1
#         for i in range(n):
# #             np[0,7]
# #             np.write()
#     if fald_status == True and X <= 0:
#         fald_status = False
        print("Step 5: END OF CODE")
        sleep(3)
        
        if len(mqtt.besked) != 0:
            mqtt.besked = ""            
        mqtt.sync_with_adafruitIO()          
        print(".", end = '')       
    except KeyboardInterrupt:
        print('Ctrl-C pressed...exiting')
        mqtt.c.disconnect()
        mqtt.sys.exit()