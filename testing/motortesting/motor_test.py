from src.motor_code import *

if __name__ == "__main__":
    # Example usage (pin numbers will vary)
    # Step, Dir, Enable, Min-switch, Max-switch
    motor = StepperMotor(step_pin=17, dir_pin=27, enable_pin=22, 
                         min_switch_pin=5, max_switch_pin=6)

    # Calibrate the motor (find min/max/neutral)
    motor.calibrate()
    
    # Move to different positions
    motor.move_motor_min_position()
    time.sleep(1)
    motor.move_motor_max_position()
    time.sleep(1)
    motor.move_motor_neutral()