import time
import datetime
import ms5837

import src.util as util 
import src.depth_sensor as depth_sensor
import src.motor_code as motor_code

## Main loop



def main():
    sensor = ms5837.MS5837()
    sensor.init()
    motor_obj = motor_code.Motor(14,15)
    team_number = input("Team Number: ")
    profile_num = input("Profile Number (1 or 2): ")
    # check what else we need to print out
    print(f"Team_number: {team_number}, Team_name: NUWave, Time: {datetime.datetime.now()}")
    
    # wait perhaps
    
    
    # move syringe to take in water 
    motor_obj.move_motor_max_position()

    # while true
    while True:
        # when depth reaches ~2 meters 
        # add time out
        if depth_sensor.read_depth(sensor)[0] >= 2: # check if this is in meters 
            motor_obj.move_position(motor_obj.neutral)
            break
    
    start = time.time()
    end = time.time()
    while True:
        if end - start >= 46: # check if it is in seconds
            break
        util.output_txt(profile_num,end-start,depth_sensor.read_depth(sensor)[0], depth_sensor.read_depth(sensor)[1])
        end = time.time()
        time.sleep(1)


    motor_obj.move_motor_min_position()
    print("End")
        



if __name__ == "__main__":
    main()