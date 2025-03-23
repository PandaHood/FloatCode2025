from src.depth_sensor import *

if __name__ == "__main__":
    num_read = int(input("How many times to run"))

    i = 0
    while i < num_read:
        x = read_depth()
        print("Depth: ", x[0],"\n","Pressure: ", x[1])
        i+=1