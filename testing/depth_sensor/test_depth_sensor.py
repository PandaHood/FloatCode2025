import sys, os
# Append the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src/depth_sensor')))
from depth_sensor import *

if __name__ == "__main__":
    num_read = input("How many times to run")

    i = 0
    while i < num_read:
        x = read_depth()
        print("Depth: ", x[0],"\n","Pressure: ", x[1])
        i+=1