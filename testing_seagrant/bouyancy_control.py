# Imports
from datetime import datetime, timezone
import RPi.GPIO as GPIO     
import time

# Our modules
import depth_sensor
from stepper import TicI2C


class BouyancyFloatController:
    def __init__(self):
        # Class imports
        self.stepper = TicI2C()
        self.depth_sensor = depth_sensor.init()

        # Initial Variable Assignments
        self.extend_limit_pin = 2 # Input pin for hitting the max extension (positively bouyant)
        self.retract_limit_pin = 3 # Input pin for hitting the max retraction (negatively bouyant)
        self.explorer_team = "EX06"
        self.filename = "profile.txt"
        self.start_time = time.time()
        self.times_logged = 0
        self.times_logged_at_depth = 0
        self.total_steps = 0 # Assign to an expected value at some point
        self.current_position = 0 # Current position of the motor. 0 is fully extended, total_steps is retracted
        self.waiting_for_input = False
        self.depth_list = []

        # Tunable Parameters
        self.log_frequency = 1 # the number of seconds 
        self.bang_bang_radius = 0.05 # meters of buffer where we let our bouyancy be
        self.target_radius = 0.2 # meters of allowed buffer around our targer
        self.target_depth = 1.0 # targer depth in meters
        self.depth_hold_time = 20
        self.midpoint_ratio = 0.5 # midpoint of the bouyancy engine
        self.max_depth_hold_time = 60 # maximum number of seconds to attempt to depth hold before ascending
        self.descent_distance = 0.05
        self.ascension_breakpoint = 0.43
        self.max_anything_time = 240

        self.max_pos = 98
        self.mid_pos = 97
        self.min_pos = 95
        self.descent_pos = None
        self.neutral_pos = None
        self.ascent_pos = None


    def run_mission(self):
        # start by going to maximum positive bouyancy
        self.max_positive_bouyancy()

        # ensure logging is working
        while self.times_logged < 5:
            self.add_log_entry()

        self.start_descending()
        time.sleep(1)
        self.start_ascending()
        self.max_positive_bouyancy()
        self.neutral_pos = (self.descent_pos + self.ascent_pos) / 2
        print("Neutral Pos:", self.neutral_pos)
        print("Descent pos:", self.descent_pos)

        self.max_positive_bouyancy()
        self.descend_to_depth()
        self.hold_depth()
        self.ascend_to_surface()
        self.wait_for_transfer()


    def run_trash_mission(self):
        # start by going to maximum positive bouyancy
        self.max_positive_bouyancy()

        # ensure logging is working
        while self.times_logged < 5:
            self.add_log_entry()

        # go to max negative bouyancy and count how many steps that takes
        # self.max_negative_bouyancy()
        # print(self.read_depth_clean()[0], self.target_depth)
        # while self.read_depth_clean()[0] < self.target_depth:
        #     print(self.get_velocity_from_depth())
        # self.max_positive_bouyancy()
        # while self.read_depth_clean()[0] > self.ascension_breakpoint:
        #     print(self.get_velocity_from_depth())

        self.start_descending()
        self.max_negative_bouyancy()
        time.sleep(1)
        self.start_ascending()
        self.max_positive_bouyancy()
        self.neutral_pos = (self.descent_pos + self.ascent_pos) / 2
        print("Neutral Pos:", self.neutral_pos)
        print("Descent pos:", self.descent_pos)

        time.sleep(5)
        self.descend_to_depth()
        self.hold_depth()
        self.ascend_to_surface()
        self.wait_for_transfer()
        self.descend_to_depth()
        self.hold_depth()
        self.ascend_to_surface()
        self.wait_for_transfer()


    # Mission Methods
    def max_positive_bouyancy(self):
        self.stepper.set_target_position(self.max_pos)
        

    def max_negative_bouyancy(self):
        self.stepper.set_target_position(self.min_pos)
        
    def start_descending(self):
        print("Descending")
        if self.descent_pos is None:
            self.max_positive_bouyancy()
            time.sleep(3)
            curr_depth = self.read_depth_clean()
            print("Curr:", curr_depth)
            pos = self.max_pos
            new_depth = self.read_depth_clean()[0]
            start_time = time.time()
            while (new_depth < curr_depth[0] + self.descent_distance and 
                   self.get_velocity_from_depth() < 0.025 and 
                   time.time() < start_time + self.max_anything_time):
                new_depth = self.read_depth_clean()[0]
                self.add_log_entry()
                pos -= 0.1
                self.stepper.set_target_position(pos)
                time.sleep(1)
            self.descent_pos = pos - 0.15
            print("Descent Pos", pos)
            self.stepper.set_target_position(self.descent_pos + 0.25)
            time.sleep(1.5)
            self.stepper.set_target_position(self.descent_pos)
        else:
            self.stepper.set_target_position(self.descent_pos)
    
    def start_ascending(self):
        print("Ascend")
        start_time = time.time()
        if self.ascent_pos is None:
            curr_depth = self.read_depth_clean()
            print("Curr:", curr_depth)
            pos = self.min_pos
            while (self.get_velocity_from_depth() > -0.02 and 
                   time.time() < start_time + self.max_anything_time):
                self.add_log_entry()
                pos += 0.1
                self.stepper.set_target_position(pos)
                time.sleep(1)
            self.ascent_pos = pos
            print("Ascent_pos", pos)
            self.stepper.set_target_position(self.ascent_pos + 0.25)
            time.sleep(1.5)
            self.stepper.set_target_position(self.ascent_pos)
        else:
            self.stepper.set_target_position(self.ascent_pos)
             

    def descend_to_depth(self):
        self.waiting_for_input = False
        # TOself.stepper.set_target_position(self.descent_pos)ASK: should we get closer in before we start slowing down?
        print(self.read_depth_clean()[0], self.target_depth, self.target_radius, )
        while self.read_depth_clean()[0] < self.target_depth - self.target_radius:
            print("descending")
            self.add_log_entry()
            self.stepper.set_target_position(self.descent_pos)

        self.stepper.set_target_position(self.neutral_pos)

    def hold_depth(self):
        depth_hold_start_time = time.time()
        self.times_logged_at_depth = 0

        # We make sure we have logged 1 more time that the needed number in the zone
        while (self.times_logged_at_depth * self.log_frequency + 1 <= self.depth_hold_time and 
               time.time() - depth_hold_start_time < self.max_depth_hold_time):
            self.add_log_entry()
            self.step_to_position()
        print(self.times_logged_at_depth * self.log_frequency + 1 <= self.depth_hold_time, '<- logged: time ->', time.time() - depth_hold_start_time < self.max_depth_hold_time)
            

    def ascend_to_surface(self):
        self.add_log_entry()
        self.max_positive_bouyancy()
    
    def wait_for_transfer(self):
        # this method might hold on input and create a logging buildup
        self.waiting_for_input = True
        user_input = input("Please input command to continue: ")
        while True:
            self.add_log_entry()
            if user_input == "transfer" or user_input == "t":
                self.transfer_file()
            if user_input == "continue" or user_input == "c":
                return
            user_input = input("Please input command to continue:")
            

    # need a better method name
    def step_to_position(self):
        current_depth = self.depth_sensor.depth()
        ratio = (self.target_depth - current_depth) / self.target_radius
        if ratio > 1:
            self.max_negative_bouyancy()
        elif ratio < -1:
            self.max_positive_bouyancy()
        elif current_depth > self.target_depth + self.bang_bang_radius:
            target_pos = self.neutral_pos - (self.neutral_pos - self.descent_pos) * ratio
            self.stepper.set_target_position(target_pos)
        elif current_depth < self.target_depth - self.bang_bang_radius:
            target_pos = self.neutral_pos + (self.neutral_pos - self.ascent_pos) * ratio
            self.stepper.set_target_position(target_pos)
        else: # we are in the bang bang region
            self.stepper.set_target_position(self.neutral_pos)
    
    def transfer_file(self):
        f = open(self.filename)
        lines = f.readlines()
        for line in lines:
            print(line)

    def get_velocity_from_depth(self):
        depth = self.read_depth_clean()[0]
        if depth is None:
            return 0.0
        if len(self.depth_list) < 2:
            return 0.0
        old_depth, old_time = self.depth_list[-2]
        # None checking
        if old_depth is None:
            old_depth, old_time = self.depth_list[-3]
            if old_depth is None:
                return 0.0
        curr_depth, curr_time = self.depth_list[-1]
        dx = old_depth - curr_depth
        dt = old_time - curr_time
        velocity = dx/dt
        return velocity

    def read_depth_clean(self):
        try: 
            depth, pressure = depth_sensor.read_depth(self.depth_sensor)
            self.depth_list.append((depth, time.time()))
            return depth, pressure
        except KeyboardInterrupt:
            raise(Exception("inter"))
        except:
            print("failed to read depth")
            return None, None


    def add_log_entry(self):
        # This need to be put into all hot loops
        utc_time = datetime.now(timezone.utc)
        depth, pressure = self.read_depth_clean()
        # Try to read depth twice, if it fails both times, return
        if depth is None:
            depth, pressure = self.read_depth_clean()
            if depth is None:
                return
        if time.time() - self.start_time > self.log_frequency * self.times_logged:
            with open(self.filename, "a") as file:
                file.write(f"{self.explorer_team}, {utc_time}, {pressure}, {depth}\n")
            self.times_logged += 1
            if self.target_depth - self.target_radius > depth and depth > self.target_depth + self.target_radius:
                self.times_logged_at_depth +=1
            print(f"Data Point {self.times_logged}: {self.explorer_team}, {utc_time}, {depth}, {pressure}")
            if self.waiting_for_input:
                print("Please input command to continue:")
