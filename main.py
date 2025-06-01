import time
import datetime
import ms5837

import src.util as util 
import src.depth_sensor as depth_sensor
import src.dc_motor as motor

## Main loop
def main():
   
    sensor = depth_sensor.init()
    dcmotor = motor.DC(4,27)


    start = time.time()
    end = time.time()
    while True:
        print("Before")
        if end - start >= 120: # check if it is in seconds
            break
        dcmotor.write_direction("1", "on")
        time.sleep(5)
        dcmotor.write_direction("1", "off")
        time.sleep(5)
        dcmotor.write_direction("2", "on")
        time.sleep(5)
        dcmotor.write_direction("2", "off")
        time.sleep(5)

        print(depth_sensor.read_depth(sensor))


        end = time.time()
        time.sleep(1)




if __name__ == "__main__":
    main()