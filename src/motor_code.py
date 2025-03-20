#import gpiozero

class Motor():
    def __init__(self):
        self.position = None
        self.max_position = None
        self.min_position = None 
        self.neutral = None

    #move motor to position
    def move_position(self,position):
        pass 

    #find max and min position
    def calibrate(self):
        pass

    # 
    def move_motor_max_position(self):
        self.move_position(self.max_position)

    def move_motor_min_position(self):
        self.move_position(self.min_position)