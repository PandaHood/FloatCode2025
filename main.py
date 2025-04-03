import time
import datetime
import ms5837

import src.util as util 
import src.depth_sensor as depth_sensor
import src.dc_motor as motor

## Main loop



def main():
    """
    sensor = ms5837.MS5837()
    sensor.init()
    #motor_obj = motor_code.Motor(14,15)
    # wait perhaps

    for i in range(100):
        util.output_txt(i,depth_sensor.read_depth(sensor)[0], depth_sensor.read_depth(sensor)[1])
        time.sleep(1)
    
    
    # move syringe to take in water 

    # while true
    while True:
        # when depth reaches ~2 meters 
        # add time out
        if depth_sensor.read_depth(sensor)[0] >= 2: # check if this is in meters
            break
    
    start = time.time()
    end = time.time()
    while True:
        if end - start >= 46: # check if it is in seconds
            break
        util.output_txt(profile_num,end-start,depth_sensor.read_depth(sensor)[0], depth_sensor.read_depth(sensor)[1])
        end = time.time()
        time.sleep(1)

    print("End")
    """
    dcmotor = motor.DC(4,27)


    start = time.time()
    end = time.time()
    while True:
        if end - start >= 120: # check if it is in seconds
            break
        dcmotor.write_direction("on", "1")
        time.sleep(10)
        dcmotor.write_direction("off", "1")
        time.sleep(10)
        dcmotor.write_direction("on", "2")
        time.sleep(10)
        dcmotor.write_direction("off", "2")
        time.sleep(10)

        
        end = time.time()
        time.sleep(1)




if __name__ == "__main__":
    main()