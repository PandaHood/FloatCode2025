from src.depth_sensor import *

if __name__ == "__main__":
    num_read = int(input("How many times to run: "))
    sensor = ms5837.MS5837()
    sensor.init()
    i = 0
    while i < num_read:
        x = read_depth(sensor)
        print("Depth: ", x[0],"\n","Pressure: ", x[1])
        i+=1