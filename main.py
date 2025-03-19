import time
import datetime
import src.util as util 

## Main loop

def main():
    team_number = input("Team Number: ")
    # check what else we need to print out
    print(f"Team_number: {team_number}, Team_name: NUWave, Time: {datetime.datetime.now()}")

    #test output function
    start = time.time()
    util.output_txt(time.time() - start,5,5)
    time.sleep(1)
    util.output_txt(time.time() - start,5,5)
    time.sleep(1)
    util.output_txt(time.time() - start,5,5)
    time.sleep(1)
    util.output_txt(time.time() - start,5,5)
    time.sleep(1)
    util.output_txt(time.time() - start,5,5)



if __name__ == "__main__":
    main()